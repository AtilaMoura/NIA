"""Gera "resposta_modelo" pras perguntas ABERTAS das provas que não têm (2026-09-23).

Sem gabarito, a IA corrige resposta aberta pela opinião dela (achado real:
prova do Tópico 19). Aqui a resposta esperada é escrita a partir do MATERIAL
do tópico e gravada dentro de Avaliacao.conteudo — só ACRESCENTA a chave
"resposta_modelo" na pergunta, nunca apaga nem reescreve nada.

Antes de gravar, salva o conteúdo original de cada prova em
_backup_gabaritos_provas_<data>.json (reverter = gravar de volta).

Uso (dentro do container do backend, que já tem GROQ_API_KEY e o banco):
    python _gerar_gabaritos_provas.py --dry-run        # só mostra o que geraria
    python _gerar_gabaritos_provas.py --apply          # gera e grava
    python _gerar_gabaritos_provas.py --apply --ids 22 # só algumas provas
"""

import argparse
import asyncio
import copy
import json
import time
from datetime import datetime

from sqlalchemy.orm.attributes import flag_modified

from app.agents.contexto_topico import carregar_content, montar_contexto_duvida
from app.agents.perfis import resolver_perfil
from app.agents.tutor_agent import TutorAgent
from app.database import SessionLocal
from app.models.models import Avaliacao
from app.routers.pipeline import _perfil_do_curso, _service

TETO_MATERIAL = 6000
PAUSA_ENTRE_PROVAS_S = 20  # teto de ~8000 tokens/min do Groq é da conta inteira


def _prompt(titulo: str, material: str, perguntas: list[dict], perfil) -> str:
    lista = "\n\n".join(
        f'### id "{p["id"]}"\nPERGUNTA: {p["enunciado"]}' + (f'\nCENÁRIO: {p["cenario"]}' if p.get("cenario") else "")
        for p in perguntas
    )
    return f"""
Você escreve o GABARITO (resposta esperada) de perguntas abertas da prova do tópico
"{titulo}" do {perfil.contexto_curso}. Esse gabarito vai ser usado pra corrigir a resposta do
aluno, então tem que ser fiel ao MATERIAL abaixo — nada fora dele.

MATERIAL DO TÓPICO (numerado por slide):
{material}

PERGUNTAS:
{lista}

Pra cada pergunta, escreva a resposta esperada em 2 a 4 frases, direta, com o mecanismo/
motivo que o material explica. Se a pergunta pede um exemplo ou cenário "de sua
preferência", diga o que uma boa resposta PRECISA conter e dê um exemplo concreto do
material. Devolva APENAS um JSON válido (sem markdown):
{{"respostas": [{{"id": "...", "resposta_modelo": "..."}}]}}
"""


async def main(apply: bool, ids: list[int] | None):
    db = SessionLocal()
    q = db.query(Avaliacao).order_by(Avaliacao.id)
    if ids:
        q = q.filter(Avaliacao.id.in_(ids))
    provas = q.all()

    backup, resumo = {}, []
    nome_backup = f"_backup_gabaritos_provas_{datetime.now():%Y-%m-%d_%H%M}.json"
    agente = TutorAgent(_service("groq"))
    for i, av in enumerate(provas):
        perguntas = [p for p in (av.conteudo or {}).get("perguntas", [])
                     if p.get("tipo") == "open" and not p.get("resposta_modelo")]
        if not perguntas or not av.topico or not av.topico.content:
            continue
        if i and resumo:
            time.sleep(PAUSA_ENTRE_PROVAS_S)
        content = carregar_content(av.topico)
        material, _ = montar_contexto_duvida(content, len(content.get("slides", [])) // 2, teto_topico=TETO_MATERIAL)
        perfil = resolver_perfil(_perfil_do_curso(db, av.topico))
        try:
            r = await agente.run_json_com_retry(_prompt(av.topico.titulo, material, perguntas, perfil), max_tokens=2000)
        except Exception as e:
            print(f"❌ prova {av.id} (tópico {av.topico_id}): {e}")
            continue
        geradas = {str(x.get("id")): (x.get("resposta_modelo") or "").strip() for x in r.get("respostas") or []}

        novo = copy.deepcopy(av.conteudo)
        feitas = 0
        for p in novo.get("perguntas", []):
            texto = geradas.get(p.get("id"))
            if p.get("tipo") == "open" and not p.get("resposta_modelo") and texto:
                p["resposta_modelo"] = texto
                feitas += 1
                print(f"\n— prova {av.id} / {p['id']} — {p['enunciado'][:90]}\n  GABARITO: {texto}")
        faltou = len(perguntas) - feitas
        resumo.append((av.id, feitas, faltou))
        if apply and feitas:
            # Backup ANTES de gravar, a cada prova — se cair no meio, nada
            # fica gravado sem o original salvo.
            backup[str(av.id)] = av.conteudo
            with open(nome_backup, "w", encoding="utf-8") as f:
                json.dump(backup, f, ensure_ascii=False, indent=1)
            av.conteudo = novo
            flag_modified(av, "conteudo")
            db.commit()

    if apply and backup:
        print(f"\n💾 backup do conteúdo original: {nome_backup}")
    print("\nRESUMO (prova, gabaritos gerados, faltaram):", resumo)
    if not apply:
        print("(dry-run: nada gravado)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--dry-run", action="store_true")
    grupo.add_argument("--apply", action="store_true")
    ap.add_argument("--ids", type=int, nargs="*")
    a = ap.parse_args()
    asyncio.run(main(a.apply, a.ids))
