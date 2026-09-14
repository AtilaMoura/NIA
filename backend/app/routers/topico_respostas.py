"""Respostas de exercício por tópico (2026-09-09).

Cada resposta que o aluno dá dentro do render de um tópico (mc/tf/classify/
associar/lacuna/open/ditado) — hoje isso vivia só em JS na página e sumia ao
recarregar. 1 linha por (usuário, tópico, pergunta) — upsert, sem DELETE
(padrão do projeto). Autenticado com o token de ESCOPO CURTO emitido por
POST /auth/topico-token (ver app/core/auth.py:get_topico_resposta_user_id) —
não é o token de sessão real, que nunca sai do servidor Next.js.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_topico_resposta_user_id
from app.database import get_db
from app.models.models import Topico, TopicoResposta
from app.schemas.topico_respostas import TopicoRespostaOut, TopicoRespostaUpsert

router = APIRouter(prefix="/topico-respostas", tags=["Topico Respostas"])


@router.get("/{topico_id}", response_model=list[TopicoRespostaOut])
def listar_respostas(
    topico_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    """Pro render restaurar o estado (o que já foi respondido) ao reabrir o tópico."""
    return (
        db.query(TopicoResposta)
        .filter(TopicoResposta.user_id == user_id, TopicoResposta.topico_id == topico_id)
        .all()
    )


@router.put("/{topico_id}/{question_id}", response_model=TopicoRespostaOut)
def salvar_resposta(
    topico_id: int,
    question_id: str,
    data: TopicoRespostaUpsert,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    def _buscar():
        return (
            db.query(TopicoResposta)
            .filter(
                TopicoResposta.user_id == user_id,
                TopicoResposta.topico_id == topico_id,
                TopicoResposta.question_id == question_id,
            )
            .first()
        )

    registro = _buscar()
    if registro:
        registro.gate_id = data.gate_id
        registro.tipo = data.tipo
        registro.resposta_dada = data.resposta_dada
        registro.correta = data.correta
        registro.tentativas += 1
        db.commit()
    else:
        registro = TopicoResposta(
            user_id=user_id, topico_id=topico_id, question_id=question_id,
            gate_id=data.gate_id, tipo=data.tipo,
            resposta_dada=data.resposta_dada, correta=data.correta,
        )
        db.add(registro)
        try:
            db.commit()
        except IntegrityError:
            # mesma corrida do topico_progress (2 respostas quase simultâneas
            # pro mesmo item) — trata como upsert de verdade.
            db.rollback()
            registro = _buscar()
            if not registro:
                raise
            registro.gate_id = data.gate_id
            registro.tipo = data.tipo
            registro.resposta_dada = data.resposta_dada
            registro.correta = data.correta
            registro.tentativas += 1
            db.commit()

    db.refresh(registro)
    return registro
