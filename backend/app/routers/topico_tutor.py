"""Tutor ao vivo por tópico (2026-09-19).

Corrige na hora quando o aluno erra um exercício (correção personalizada +
pergunta de reforço, mesmo conceito) e responde dúvidas que o aluno tira
durante o estudo — separado de anotação (TopicoAnotacao). Autenticado com o
MESMO token de escopo curto de /topico-respostas (já valida user+topico).

Ver memória do projeto [[nia-correcao-ia-avaliacoes]] pro desenho completo.
Deliberadamente por pergunta/dúvida — nunca o tópico inteiro numa chamada
(teto de tokens/minuto do Groq + achado de que ele "esquece" item quando
pede muitos objetos numa resposta só).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_topico_resposta_user_id
from app.database import get_db
from app.models.models import Topico, TopicoDuvida, TopicoReforco
from app.schemas.topico_tutor import (
    CorrigirRequest,
    CorrigirResponse,
    DuvidaRequest,
    DuvidaResponse,
    ResponderReforcoRequest,
)
from app.agents.tutor_agent import TutorAgent
from app.agents.perfis import resolver_perfil
from app.routers.pipeline import _perfil_do_curso, _service

router = APIRouter(prefix="/topico-tutor", tags=["Topico Tutor"])


def _buscar_pergunta(topico: Topico, question_id: str) -> dict | None:
    """Acha o objeto Pergunta original dentro do content do tópico, pelo id."""
    import json as _json

    content = topico.content if isinstance(topico.content, dict) else _json.loads(topico.content)
    for slide in content.get("slides", []):
        if slide.get("tipo") == "checkpoint":
            for p in slide.get("perguntas", []):
                if p.get("id") == question_id:
                    return p
        elif slide.get("tipo") == "avaliacao_pergunta":
            p = slide.get("pergunta") or {}
            if p.get("id") == question_id:
                return p
    return None


@router.post("/{topico_id}/corrigir", response_model=CorrigirResponse)
async def corrigir_exercicio(
    topico_id: int,
    data: CorrigirRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")

    pergunta = _buscar_pergunta(topico, data.question_id)
    if not pergunta:
        raise HTTPException(404, "Pergunta não encontrada neste tópico")

    perfil_id = _perfil_do_curso(db, topico)
    resultado = await TutorAgent(_service("groq")).corrigir_exercicio(
        pergunta,
        data.resposta_dada,
        contexto_topico=topico.titulo,
        perfil=resolver_perfil(perfil_id),
    )

    reforco = TopicoReforco(
        user_id=user_id,
        topico_id=topico_id,
        question_id_origem=data.question_id,
        correcao_personalizada=resultado.get("correcao_personalizada", ""),
        pergunta_gerada=resultado.get("pergunta_reforco"),
    )
    db.add(reforco)
    db.commit()
    db.refresh(reforco)

    return CorrigirResponse(
        correta=False,
        correcao_personalizada=reforco.correcao_personalizada,
        pergunta_reforco=reforco.pergunta_gerada,
        reforco_id=reforco.id,
    )


@router.put("/{topico_id}/reforco/{reforco_id}", response_model=CorrigirResponse)
def responder_reforco(
    topico_id: int,
    reforco_id: int,
    data: ResponderReforcoRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    """Salva a resposta do aluno pra pergunta de reforço gerada (sem chamar
    IA de novo — a correção objetiva usa o gabarito que já veio no JSON de
    pergunta_gerada, do mesmo jeito que o JS do render já faz pra pergunta
    normal)."""
    from sqlalchemy import func as _func

    reforco = (
        db.query(TopicoReforco)
        .filter(TopicoReforco.id == reforco_id, TopicoReforco.user_id == user_id, TopicoReforco.topico_id == topico_id)
        .first()
    )
    if not reforco:
        raise HTTPException(404, "Reforço não encontrado")

    reforco.resposta_dada = data.resposta_dada
    reforco.correta = data.correta
    reforco.respondido_em = _func.now()
    db.commit()
    db.refresh(reforco)

    return CorrigirResponse(
        correta=bool(reforco.correta),
        correcao_personalizada=reforco.correcao_personalizada,
        pergunta_reforco=reforco.pergunta_gerada,
        reforco_id=reforco.id,
    )


@router.post("/{topico_id}/duvida", response_model=DuvidaResponse)
async def tirar_duvida(
    topico_id: int,
    data: DuvidaRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")

    import json as _json
    content = topico.content if isinstance(topico.content, dict) else _json.loads(topico.content)
    slides = content.get("slides", [])
    contexto_slide = ""
    if 0 <= data.slide_index < len(slides):
        slide = slides[data.slide_index]
        contexto_slide = _json.dumps(
            {"secao": slide.get("secao"), "titulo_secao": slide.get("titulo_secao"), "blocos": slide.get("blocos")},
            ensure_ascii=False,
        )[:2000]  # corta — não precisa do slide inteiro pra responder uma dúvida pontual

    perfil_id = _perfil_do_curso(db, topico)
    resposta_texto = await TutorAgent(_service("groq")).responder_duvida(
        data.pergunta_aluno,
        contexto_slide=contexto_slide,
        contexto_topico=topico.titulo,
        perfil=resolver_perfil(perfil_id),
    )

    duvida = TopicoDuvida(
        user_id=user_id,
        topico_id=topico_id,
        slide_index=data.slide_index,
        question_id=data.question_id,
        pergunta_aluno=data.pergunta_aluno,
        resposta_ia=resposta_texto,
    )
    db.add(duvida)
    db.commit()
    db.refresh(duvida)

    return duvida
