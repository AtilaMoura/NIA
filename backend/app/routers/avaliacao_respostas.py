"""Respostas de exercício por avaliação (prova final do tópico).

Espelho de topico_respostas.py trocando Topico/TopicoResposta por
Avaliacao/AvaliacaoResposta e topico_id por avaliacao_id.

Gating: a prova só pode ser acessada se o TÓPICO vinculado
(avaliacao.topico_id) tiver TopicoProgress.status == 'concluido' PRA AQUELE user_id.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_avaliacao_resposta_user_id
from app.database import get_db
from app.models.models import Avaliacao, AvaliacaoProgress, AvaliacaoResposta
from app.schemas.avaliacao_respostas import AvaliacaoRespostaOut, AvaliacaoRespostaUpsert

router = APIRouter(prefix="/avaliacao-respostas", tags=["Avaliacao Respostas"])


def _rodada_atual(db: Session, user_id: int, avaliacao_id: int) -> int:
    """A 'rodada' corrente de exercícios da avaliação pra este aluno.
    Sem AvaliacaoProgress ainda (avaliação nunca aberta), é sempre 1."""
    registro = (
        db.query(AvaliacaoProgress)
        .filter(
            AvaliacaoProgress.user_id == user_id,
            AvaliacaoProgress.avaliacao_id == avaliacao_id,
        )
        .first()
    )
    return registro.rodada_atual if registro else 1


def _verificar_gating_avaliacao(db: Session, user_id: int, avaliacao_id: int) -> None:
    """Verifica se o usuário concluiu o conteúdo do tópico vinculado à avaliação."""
    from app.models.models import Topico, TopicoProgress

    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(404, "Avaliação not found")

    topico_progress = (
        db.query(TopicoProgress)
        .filter(
            TopicoProgress.user_id == user_id,
            TopicoProgress.topico_id == avaliacao.topico_id,
            TopicoProgress.status == "concluido",
        )
        .first()
    )

    if not topico_progress:
        raise HTTPException(
            403, "Termine o conteúdo do tópico antes de fazer a prova."
        )


@router.get("/{avaliacao_id}", response_model=list[AvaliacaoRespostaOut])
def listar_respostas(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_avaliacao_resposta_user_id),
):
    """Pro render restaurar o estado (o que já foi respondido) ao reabrir a
    avaliação — só da RODADA corrente."""
    _verificar_gating_avaliacao(db, user_id, avaliacao_id)

    rodada = _rodada_atual(db, user_id, avaliacao_id)
    return (
        db.query(AvaliacaoResposta)
        .filter(
            AvaliacaoResposta.user_id == user_id,
            AvaliacaoResposta.avaliacao_id == avaliacao_id,
            AvaliacaoResposta.rodada == rodada,
        )
        .all()
    )


@router.put("/{avaliacao_id}/{question_id}", response_model=AvaliacaoRespostaOut)
def salvar_resposta(
    avaliacao_id: int,
    question_id: str,
    data: AvaliacaoRespostaUpsert,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_avaliacao_resposta_user_id),
):
    _verificar_gating_avaliacao(db, user_id, avaliacao_id)

    if not db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first():
        raise HTTPException(404, "Avaliação not found")

    rodada = _rodada_atual(db, user_id, avaliacao_id)

    def _buscar():
        return (
            db.query(AvaliacaoResposta)
            .filter(
                AvaliacaoResposta.user_id == user_id,
                AvaliacaoResposta.avaliacao_id == avaliacao_id,
                AvaliacaoResposta.question_id == question_id,
                AvaliacaoResposta.rodada == rodada,
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
        registro = AvaliacaoResposta(
            user_id=user_id,
            avaliacao_id=avaliacao_id,
            question_id=question_id,
            gate_id=data.gate_id,
            tipo=data.tipo,
            resposta_dada=data.resposta_dada,
            correta=data.correta,
            rodada=rodada,
        )
        db.add(registro)
        try:
            db.commit()
        except IntegrityError:
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