"""NIA-T-031 — regras de correção das respostas ABERTAS e perfil de IA guardado no curso.

Achado real (T304, curso 16): "git cat-fale -p HEAD" virou "errada" (sem tolerância a
digitação) e a IA disse que o aluno "confundiu" algo que o próprio material afirma.
"""
import asyncio

import pytest
from pydantic import ValidationError

from app.agents.perfis import PERFIS, resolver_perfil
from app.agents.tutor_agent import TutorAgent
from app.routers.pipeline import _perfil_do_curso
from app.schemas.courses import CourseUpdate


def _capturar_prompt_corrigir_abertas(perfil=None):
    """Roda corrigir_abertas com a chamada de IA falsa e devolve o prompt montado."""
    capturado = {}

    class Falso(TutorAgent):
        def __init__(self):  # sem serviço de IA de verdade
            pass

        async def run_json_com_retry(self, prompt, tentativas=3, max_tokens=None):
            capturado["prompt"] = prompt
            return {"itens": []}

    abertas = [{"id": "q1", "enunciado": "Qual comando?", "resposta": "git cat-fale -p HEAD", "esperado": "git cat-file -p HEAD"}]
    kwargs = {"perfil": perfil} if perfil else {}
    asyncio.run(Falso().corrigir_abertas(abertas, "[Slide 1] material", **kwargs))
    return " ".join(capturado["prompt"].split())  # espaços normalizados (quebras de linha)


def test_prompt_abertas_tolera_grafia():
    p = _capturar_prompt_corrigir_abertas()
    assert "Atenção à grafia" in p
    # a regra de grafia vale para ABERTA (não só FRASE), inclusive comando/termo técnico
    assert "nome de comando" in p


def test_prompt_abertas_parcial_nunca_errada_quando_acertou_parte():
    p = _capturar_prompt_corrigir_abertas()
    assert "NUNCA \"errada\"" in p or 'nunca "errada"' in p


def test_prompt_abertas_confere_material_antes_de_dizer_que_errou():
    p = _capturar_prompt_corrigir_abertas()
    assert "além da resposta esperada" in p
    assert "confira no MATERIAL" in p


def test_pipeline_usa_perfil_ia_do_curso(cenario):
    cenario.curso.perfil_ia = "eng_ia"
    cenario.db.flush()
    perfil = _perfil_do_curso(cenario.db, cenario.topico)
    assert perfil.id == "eng_ia"


def test_sem_perfil_ia_devolve_perfil_geral_sem_garden_center(cenario):
    cenario.curso.perfil_ia = None
    cenario.db.flush()
    perfil = _perfil_do_curso(cenario.db, cenario.topico)
    assert cenario.curso.title in perfil.contexto_curso
    texto = perfil.contexto_curso + perfil.fio_condutor + perfil.exemplo_calibracao
    assert "Garden Center" not in texto


def test_perfil_ia_invalido_no_banco_cai_no_geral(cenario):
    cenario.curso.perfil_ia = "inexistente"
    cenario.db.flush()
    perfil = _perfil_do_curso(cenario.db, cenario.topico)
    assert cenario.curso.title in perfil.contexto_curso


def test_schema_rejeita_perfil_invalido():
    with pytest.raises(ValidationError):
        CourseUpdate(perfil_ia="nao_existe")
    assert CourseUpdate(perfil_ia="obreiro_acp").perfil_ia == "obreiro_acp"
    assert CourseUpdate(perfil_ia="").perfil_ia is None
    assert CourseUpdate().perfil_ia is None


def test_api_curso_perfil_invalido_422_e_valido_grava(api, cenario):
    r = api.put(f"/courses/{cenario.curso.id}", json={"perfil_ia": "xyz"}, headers=_h(cenario.master))
    assert r.status_code == 422
    r = api.put(f"/courses/{cenario.curso.id}", json={"perfil_ia": "eng_ia"}, headers=_h(cenario.master))
    assert r.status_code == 200
    assert r.json()["perfil_ia"] == "eng_ia"


def _h(user):
    from tests.conftest import como
    return como(user)


def test_obreiro_acp_sem_neutralidade_e_com_acf():
    p = resolver_perfil("obreiro_acp")
    assert p.id == "obreiro_acp"
    texto = " ".join((p.fio_condutor + p.contexto_curso).lower().split())
    assert "sem viés denominacional" not in texto
    assert "neutralidade" not in texto.replace("não use nota de neutralidade", "").replace("nunca use nota de neutralidade", "")
    assert "acf" in texto


def test_perfis_existentes_continuam_e_novos_registrados():
    for pid in ("tech", "teologia", "obreiro", "ingles", "redes", "obreiro_acp", "eng_ia"):
        assert pid in PERFIS
