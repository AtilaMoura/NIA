"""Caderno da aula (2026-10-05): organiza e corrige as anotações do aluno numa
aula, com a IA lendo também o conteúdo dos slides anotados (pra poder corrigir
contra o material, não contra a memória dela).

- A versão original são as TopicoAnotacao — nunca alteradas aqui.
- Cada "organizar" cria uma CadernoVersao nova (nada é apagado).
- A IA devolve blocos JSON validados por schemas/caderno.py; o front desenha.
- Limite de gerações por dia por pessoa (cota de IA é curta).
"""

import json
from datetime import datetime, timedelta

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import (
    CadernoVersao,
    Course,
    Lesson,
    Module,
    Topico,
    TopicoAnotacao,
    TopicoProgress,
)
from app.renderer.render import carregar_temas
from app.schemas.caderno import (
    AnotacaoDaAula,
    CadernoConteudo,
    CadernoEstado,
    CadernoVersaoOut,
    CoresTema,
    TopicoDaAula,
)
from app.services.modelos import servico
from app.services.tempo_estudo import FUSO_BRASILIA

GERACOES_POR_DIA = 6
TEMA_PADRAO = "trigo-maduro"

# Campos do slide que não são texto de estudo (ids, mídia, layout)
_CHAVES_IGNORADAS = {"id", "tipo", "imagem", "imagem_url", "url", "audio", "audios", "src", "layout", "icone", "cor"}
_LIMITE_SLIDE = 1500
_LIMITE_TOTAL = 16000


# ---------------------------------------------------------------- leitura

def _slides(conteudo: str | None) -> list:
    if not conteudo:
        return []
    try:
        return json.loads(conteudo).get("slides") or []
    except (ValueError, AttributeError):
        return []


def _texto_do_slide(slide) -> str:
    """Junta os textos do slide (qualquer estrutura de bloco), sem ids/mídia."""
    partes: list[str] = []

    def andar(v, chave=""):
        if chave in _CHAVES_IGNORADAS:
            return
        if isinstance(v, str):
            t = v.strip()
            if t and not t.startswith(("http://", "https://", "/static/")):
                partes.append(t)
        elif isinstance(v, list):
            for x in v:
                andar(x)
        elif isinstance(v, dict):
            for k, x in v.items():
                andar(x, k)

    andar(slide)
    return " · ".join(partes)[:_LIMITE_SLIDE]


def _aula(db: Session, lesson_id: int):
    linha = (
        db.query(Lesson, Module, Course)
        .join(Module, Lesson.module_id == Module.id)
        .join(Course, Module.course_id == Course.id)
        .filter(Lesson.id == lesson_id)
        .first()
    )
    if not linha:
        raise HTTPException(404, "Aula não encontrada.")
    return linha


def _topicos_da_aula(db: Session, lesson_id: int) -> list[Topico]:
    return db.query(Topico).filter(Topico.lesson_id == lesson_id).order_by(Topico.topico_index).all()


def _anotacoes(db: Session, user_id: int, topicos: list[Topico]) -> list[tuple[Topico, TopicoAnotacao]]:
    por_id = {t.id: t for t in topicos}
    if not por_id:
        return []
    notas = (
        db.query(TopicoAnotacao)
        .filter(TopicoAnotacao.user_id == user_id, TopicoAnotacao.topico_id.in_(por_id))
        .all()
    )
    # Texto vazio = anotação "apagada" na UI (a linha fica, padrão do projeto)
    notas = [n for n in notas if (n.texto or "").strip()]
    notas.sort(key=lambda n: (por_id[n.topico_id].topico_index, n.slide_index))
    return [(por_id[n.topico_id], n) for n in notas]


def _ultima_versao(db: Session, user_id: int, lesson_id: int) -> CadernoVersao | None:
    return (
        db.query(CadernoVersao)
        .filter(CadernoVersao.user_id == user_id, CadernoVersao.lesson_id == lesson_id)
        .order_by(CadernoVersao.versao.desc())
        .first()
    )


def _geracoes_hoje(db: Session, user_id: int) -> int:
    inicio_dia = datetime.now(FUSO_BRASILIA).replace(hour=0, minute=0, second=0, microsecond=0)
    return (
        db.query(func.count(CadernoVersao.id))
        .filter(CadernoVersao.user_id == user_id, CadernoVersao.created_at >= inicio_dia)
        .scalar()
        or 0
    )


def _azulado(hexcor: str) -> bool:
    try:
        r, g, b = (int(hexcor.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return False
    return b > r and b >= g * 0.9


def _cores(tema_id: str | None) -> CoresTema | None:
    """Tema do curso → variáveis do caderno. A 2ª cor de destaque é o azul do tema,
    ou o âmbar quando o próprio destaque já é azulado (ex.: azul-petróleo)."""
    temas = carregar_temas()
    tema = temas.get(tema_id or "") or temas.get(TEMA_PADRAO)
    if not tema:
        return None

    def mapa(c: dict) -> dict[str, str]:
        acento = c.get("accent", "#8a5a2b")
        segundo = c.get("amber") if _azulado(acento) else c.get("blue")
        return {
            "bg": c.get("bg", ""), "surface": c.get("surface", ""), "surface2": c.get("surface2", ""),
            "border": c.get("border", ""), "borderSoft": c.get("borderSoft", c.get("border", "")),
            "ink": c.get("text", ""), "dim": c.get("textMuted", ""), "faint": c.get("textDim", ""),
            "accent": acento, "accentSoft": c.get("accentSoft", ""),
            "accent2": segundo or acento, "fix": c.get("bad", "#a3402f"), "fixSoft": c.get("badSoft", ""),
        }

    return CoresTema(claro=mapa(tema.get("cores", {})), escuro=mapa(tema.get("coresDark") or tema.get("cores", {})))


def estado(db: Session, user_id: int, lesson_id: int, tema: str | None = None) -> CadernoEstado:
    aula, modulo, curso = _aula(db, lesson_id)
    topicos = _topicos_da_aula(db, lesson_id)
    pares = _anotacoes(db, user_id, topicos)

    concluidos = {
        r.topico_id
        for r in db.query(TopicoProgress).filter(
            TopicoProgress.user_id == user_id,
            TopicoProgress.topico_id.in_([t.id for t in topicos] or [0]),
            TopicoProgress.status == "concluido",
        )
    }

    anotacoes = []
    for t, n in pares:
        slides = _slides(t.content)
        s = slides[n.slide_index] if 0 <= n.slide_index < len(slides) else None
        anotacoes.append(AnotacaoDaAula(
            topico_id=t.id,
            topico_titulo=t.titulo,
            slide_index=n.slide_index,
            slide_titulo=s.get("titulo") if isinstance(s, dict) else None,
            texto=n.texto,
            atualizado_em=n.updated_at or n.created_at,
        ))

    ultima = _ultima_versao(db, user_id, lesson_id)
    caderno = None
    novas = 0
    if ultima:
        try:
            caderno = CadernoVersaoOut(
                versao=ultima.versao,
                conteudo=CadernoConteudo.model_validate(ultima.conteudo),
                anotacoes_usadas=ultima.anotacoes_usadas,
                criado_em=ultima.created_at,
            )
        except ValidationError:
            caderno = None
        novas = sum(
            1 for _, n in pares
            if ultima.created_at and (n.updated_at or n.created_at) and (n.updated_at or n.created_at) > ultima.created_at
        )

    return CadernoEstado(
        lesson_id=aula.id,
        aula=aula.title,
        aula_index=aula.lesson_index,
        modulo=modulo.title,
        modulo_index=modulo.module_index,
        course_id=curso.id,
        curso=curso.title,
        topicos=[TopicoDaAula(id=t.id, titulo=t.titulo, concluido=t.id in concluidos) for t in topicos],
        anotacoes=anotacoes,
        caderno=caderno,
        novas_desde_caderno=novas,
        geracoes_restantes_hoje=max(0, GERACOES_POR_DIA - _geracoes_hoje(db, user_id)),
        cores=_cores(tema),
    )


# ---------------------------------------------------------------- geração

def _prompt(curso: str, aula: str, topicos: list[Topico], pares: list[tuple[Topico, TopicoAnotacao]]) -> str:
    notas_txt = []
    material_txt = []
    vistos: set[tuple[int, int]] = set()
    total = 0
    for t, n in pares:
        notas_txt.append(f"[topico_id={t.id} slide={n.slide_index + 1}] {n.texto.strip()}")
        chave = (t.id, n.slide_index)
        if chave in vistos:
            continue
        vistos.add(chave)
        slides = _slides(t.content)
        if 0 <= n.slide_index < len(slides) and total < _LIMITE_TOTAL:
            trecho = _texto_do_slide(slides[n.slide_index])
            total += len(trecho)
            material_txt.append(f"[topico_id={t.id} slide={n.slide_index + 1}] {trecho}")

    lista_topicos = "\n".join(f"- topico_id={t.id}: {t.titulo}" for t in topicos)

    return f"""Você organiza o CADERNO DE ESTUDO de um aluno. Curso: "{curso}". Aula: "{aula}".

Tópicos da aula:
{lista_topicos}

ANOTAÇÕES DO ALUNO (como ele escreveu; o marcador diz de qual tópico/slide é):
{chr(10).join(notas_txt)}

MATERIAL DOS SLIDES ANOTADOS (fonte da verdade pra corrigir):
{chr(10).join(material_txt)}

Tarefa: reescreva as anotações como um caderno bem organizado, em português do Brasil, na
primeira pessoa do aluno ("eu"), agrupando POR ASSUNTO (não por slide). Regras:
1. Use SÓ o que está nas anotações e no material acima. Não invente fato, número, nome nem
   referência. Referência bíblica só se aparecer nas anotações ou no material, exatamente igual.
2. Corrija ortografia e deixe claro, mas mantenha as ideias do aluno.
3. Bloco "correcao" SOMENTE quando a anotação CONTRADIZ o material (erro de fato). Anotação
   incompleta não é erro. "era" = trecho curto do que o aluno escreveu; "agora" = o certo,
   segundo o material; preencha topico_id e slide com os do marcador da anotação.
4. Use "passos" pra sequências, "tabela" pra comparações (até 4 colunas), "lembrete" pra uma
   frase curta de margem, "nota" e "nota_alt" (alternando) pros conceitos, com "rotulo" curto.
5. "pratica": até 4 ações práticas que saem das anotações (pode ser vazio).
6. "veredito": resumo de 1-2 frases sobre as anotações e "pontos" = um por correção feita
   (título curto + por que vale reforçar). Sem correção → pontos vazio.
7. Destaque com **negrito** (no máximo 1-2 por bloco). Nada de HTML nem markdown além disso.

Responda com este JSON:
{{"subtitulo": "frase curta sobre a aula",
  "secoes": [{{"titulo": "assunto", "blocos": [
     {{"tipo": "nota", "rotulo": "...", "texto": "...", "referencia": "opcional"}},
     {{"tipo": "correcao", "era": "...", "agora": "...", "topico_id": 0, "slide": 0}},
     {{"tipo": "passos", "itens": [{{"titulo": "...", "detalhe": "..."}}]}},
     {{"tipo": "tabela", "colunas": ["..."], "linhas": [["..."]]}},
     {{"tipo": "lembrete", "texto": "..."}}
  ]}}],
  "pratica": ["..."],
  "veredito": {{"resumo": "...", "pontos": [{{"titulo": "...", "detalhe": "..."}}]}}}}"""


def _limpar_links(conteudo: CadernoConteudo, topicos: list[Topico]) -> CadernoConteudo:
    """Correção só aponta pra tópico/slide que existe nesta aula."""
    total_por_topico = {t.id: len(_slides(t.content)) for t in topicos}
    for secao in conteudo.secoes:
        for b in secao.blocos:
            if b.tipo != "correcao":
                continue
            total = total_por_topico.get(b.topico_id or -1)
            if not total or not b.slide or not (1 <= b.slide <= total):
                b.topico_id = None
                b.slide = None
    return conteudo


async def organizar(db: Session, user_id: int, lesson_id: int) -> CadernoVersao:
    aula, _modulo, curso = _aula(db, lesson_id)
    topicos = _topicos_da_aula(db, lesson_id)
    pares = _anotacoes(db, user_id, topicos)
    if not pares:
        raise HTTPException(400, "Nada anotado nesta aula ainda.")
    if _geracoes_hoje(db, user_id) >= GERACOES_POR_DIA:
        raise HTTPException(429, f"Limite de {GERACOES_POR_DIA} cadernos por dia. Tente amanhã.")

    ia = servico("caderno")
    prompt = _prompt(curso.title, aula.title, topicos, pares)

    conteudo: CadernoConteudo | None = None
    erro: Exception | None = None
    for _ in range(2):  # resposta fora do formato → mais uma tentativa
        try:
            bruto = await ia.generate_json(prompt, temperature=0.3, max_tokens=6000)
            conteudo = CadernoConteudo.model_validate(bruto)
            break
        except (ValidationError, ValueError) as e:
            erro = e
        except Exception as e:  # cadeia inteira falhou (cota/servidor)
            raise HTTPException(503, "A IA está indisponível agora. Tente de novo em alguns minutos.") from e
    if conteudo is None:
        print(f"[caderno] resposta inválida da IA: {str(erro)[:300]}")
        raise HTTPException(502, "A IA devolveu um caderno fora do formato. Tente de novo.")

    conteudo = _limpar_links(conteudo, topicos)
    ultima = _ultima_versao(db, user_id, lesson_id)
    versao = CadernoVersao(
        user_id=user_id,
        lesson_id=lesson_id,
        versao=(ultima.versao + 1) if ultima else 1,
        conteudo=conteudo.model_dump(),
        anotacoes_usadas=len(pares),
        modelo=ia.ultimo_modelo,
    )
    db.add(versao)
    db.commit()
    db.refresh(versao)
    return versao
