"""Tutor ao vivo por tópico (2026-09-19).

Corrige na hora quando o aluno erra um exercício (correção personalizada +
pergunta de reforço, mesmo conceito) e responde dúvidas que o aluno tira
durante o estudo — separado de anotação (TopicoAnotacao). Autenticado com o
MESMO token de escopo curto de /topico-respostas (já valida user+topico).

Ver memória do projeto [[nia-correcao-ia-avaliacoes]] pro desenho completo.
Deliberadamente por pergunta/dúvida — nunca pede vários objetos numa chamada
(achado de que o Groq "esquece" item quando pede muitos numa resposta só).
O chat de dúvidas (2026-09-23) manda o texto do tópico como referência, mas
cortado num teto fixo (ver agents/contexto_topico.py) por causa do limite de
tokens/minuto do Groq.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_topico_resposta_user_id
from app.database import get_db
from app.models.models import Topico, TopicoDuvida, TopicoReforco
from app.schemas.topico_tutor import (
    CorrigirRequest,
    CorrigirResponse,
    DuvidaItem,
    DuvidaRequest,
    DuvidaResponse,
    ResponderReforcoRequest,
)
from app.agents.tutor_agent import TutorAgent
from app.agents.perfis import resolver_perfil
from app.agents.contexto_topico import carregar_content, montar_contexto_duvida
from app.routers.pipeline import _perfil_do_curso, _rate_limited, _service

router = APIRouter(prefix="/topico-tutor", tags=["Topico Tutor"])

# Quantas trocas anteriores do chat de dúvidas entram no prompt (teto de token
# do Groq — o histórico completo continua no banco e aparece na tela).
HISTORICO_DUVIDAS_NO_PROMPT = 6


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

    # Chat (2026-09-23): tópico inteiro como referência + slide atual em foco
    # (ver contexto_topico.py pro teto de tamanho).
    material_topico, contexto_slide = montar_contexto_duvida(carregar_content(topico), data.slide_index)

    # Memória da conversa sempre vem do banco — nunca do front.
    anteriores = (
        db.query(TopicoDuvida)
        .filter(TopicoDuvida.user_id == user_id, TopicoDuvida.topico_id == topico_id)
        .order_by(TopicoDuvida.created_at.desc(), TopicoDuvida.id.desc())
        .limit(HISTORICO_DUVIDAS_NO_PROMPT)
        .all()
    )
    historico = [(d.pergunta_aluno, d.resposta_ia) for d in reversed(anteriores)]

    perfil_id = _perfil_do_curso(db, topico)
    try:
        resposta_texto = await TutorAgent(_service("groq")).responder_duvida(
            data.pergunta_aluno,
            contexto_slide=contexto_slide,
            contexto_topico=topico.titulo,
            perfil=resolver_perfil(perfil_id),
            material_topico=material_topico,
            numero_slide=data.slide_index + 1,
            historico=historico,
            tamanho=data.tamanho,
        )
    except Exception as e:
        if _rate_limited(e):
            raise HTTPException(503, "O tutor está sobrecarregado agora. Tente de novo em alguns minutos.")
        raise HTTPException(500, f"Erro ao responder dúvida: {str(e)}")

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


@router.get("/{topico_id}/duvidas", response_model=list[DuvidaItem])
def listar_duvidas(
    topico_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    """Conversa do chat de dúvidas deste aluno neste tópico, da mais antiga pra
    mais nova — o painel remonta a conversa ao reabrir o tópico."""
    return (
        db.query(TopicoDuvida)
        .filter(TopicoDuvida.user_id == user_id, TopicoDuvida.topico_id == topico_id)
        .order_by(TopicoDuvida.created_at.asc(), TopicoDuvida.id.asc())
        .all()
    )
