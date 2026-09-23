"""Progresso por avaliação (prova final do tópico) — FASE 2 do front Emaús.

Espelho de topico_progress.py trocando Topico/TopicoProgress por
Avaliacao/AvaliacaoProgress e topico_id por avaliacao_id.

Gating: a prova só pode ser acessada se o TÓPICO vinculado
(avaliacao.topico_id) tiver TopicoProgress.status == 'concluido' PRA AQUELE user_id.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.models import Avaliacao, AvaliacaoProgress, Topico, TopicoProgress, User
from app.core.auth import get_current_user, get_avaliacao_resposta_user_id
from app.schemas.topico_progress import ResultadoAvaliacaoOut
from app.schemas.avaliacao_progress import (
    AvaliacaoProgressOut,
    AvaliacaoProgressSlideOut,
    AvaliacaoProgressSlideUpsert,
    AvaliacaoProgressUpsert,
)

router = APIRouter(prefix="/avaliacao-progress", tags=["Avaliacao Progress"])


def _verificar_gating_avaliacao(db: Session, user_id: int, avaliacao_id: int) -> None:
    """Verifica se o usuário concluiu o conteúdo do tópico vinculado à avaliação.
    Lança HTTPException(403) se não tiver concluído."""
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


@router.get("/", response_model=list[AvaliacaoProgressOut])
def list_avaliacao_progress(
    user_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Achado de segurança 2026-09-23: ficava aberto, qualquer um lia resultado de
    # prova de qualquer aluno só trocando o user_id na URL.
    if current_user.id != user_id and current_user.role not in ("master", "admin", "professor"):
        raise HTTPException(403, "Sem permissão pra ver o progresso deste usuário.")
    return (
        db.query(AvaliacaoProgress)
        .filter(AvaliacaoProgress.user_id == user_id)
        .order_by(AvaliacaoProgress.avaliacao_id)
        .all()
    )


@router.put("/{avaliacao_id}", response_model=AvaliacaoProgressOut)
def upsert_avaliacao_progress(
    avaliacao_id: int,
    data: AvaliacaoProgressUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Checa identidade ANTES do gating — senão dá pra usar o 403 de gating
    # (repassando user_id de outra pessoa no corpo) pra descobrir se um
    # usuário arbitrário já concluiu um tópico específico.
    if data.user_id != current_user.id:
        raise HTTPException(403, "Só é possível marcar progresso da própria conta.")
    if not db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first():
        raise HTTPException(404, "Avaliação not found")
    _verificar_gating_avaliacao(db, data.user_id, avaliacao_id)

    def _buscar_registro():
        return (
            db.query(AvaliacaoProgress)
            .filter(
                AvaliacaoProgress.user_id == data.user_id,
                AvaliacaoProgress.avaliacao_id == avaliacao_id,
            )
            .first()
        )

    def _aplicar_status(registro: AvaliacaoProgress):
        registro.status = data.status
        if data.status == "em_andamento" and registro.iniciado_em is None:
            registro.iniciado_em = func.now()
        if data.status == "concluido":
            if registro.iniciado_em is None:
                registro.iniciado_em = func.now()
            registro.concluido_em = func.now()

    registro = _buscar_registro()
    if not registro:
        registro = AvaliacaoProgress(
            user_id=data.user_id, avaliacao_id=avaliacao_id, status="nao_iniciado"
        )
        db.add(registro)
        _aplicar_status(registro)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            registro = _buscar_registro()
            if not registro:
                raise
            _aplicar_status(registro)
            db.commit()
    else:
        _aplicar_status(registro)
        db.commit()

    db.refresh(registro)
    return registro


@router.get("/{avaliacao_id}/slide", response_model=AvaliacaoProgressSlideOut)
def obter_slide_atual(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_avaliacao_resposta_user_id),
):
    """Pro <iframe> restaurar o slide exato onde o aluno parou —
    reaproveita o MESMO token de escopo curto das respostas de exercício."""
    _verificar_gating_avaliacao(db, user_id, avaliacao_id)

    registro = (
        db.query(AvaliacaoProgress)
        .filter(
            AvaliacaoProgress.user_id == user_id,
            AvaliacaoProgress.avaliacao_id == avaliacao_id,
        )
        .first()
    )
    return AvaliacaoProgressSlideOut(ultimo_slide=registro.ultimo_slide if registro else None)


@router.get("/{avaliacao_id}/resultado", response_model=ResultadoAvaliacaoOut)
def obter_resultado(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_avaliacao_resposta_user_id),
):
    """Revisão personalizada da prova, pro <iframe> remontar o slide
    "Resultado" ao reabrir (mesmo token de escopo curto das respostas)."""
    registro = (
        db.query(AvaliacaoProgress)
        .filter(AvaliacaoProgress.user_id == user_id, AvaliacaoProgress.avaliacao_id == avaliacao_id)
        .first()
    )
    if not registro:
        return ResultadoAvaliacaoOut(status="nao_iniciado")
    return ResultadoAvaliacaoOut(
        status=registro.status, analise=(registro.tutor_analise or {}).get("ultima_avaliacao")
    )


@router.put("/{avaliacao_id}/slide", response_model=AvaliacaoProgressSlideOut)
def salvar_slide_atual(
    avaliacao_id: int,
    data: AvaliacaoProgressSlideUpsert,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_avaliacao_resposta_user_id),
):
    _verificar_gating_avaliacao(db, user_id, avaliacao_id)

    if not db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first():
        raise HTTPException(404, "Avaliação not found")

    def _buscar():
        return (
            db.query(AvaliacaoProgress)
            .filter(
                AvaliacaoProgress.user_id == user_id,
                AvaliacaoProgress.avaliacao_id == avaliacao_id,
            )
            .first()
        )

    registro = _buscar()
    if not registro:
        registro = AvaliacaoProgress(
            user_id=user_id, avaliacao_id=avaliacao_id, status="nao_iniciado"
        )
        db.add(registro)
        registro.ultimo_slide = data.indice
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            registro = _buscar()
            if not registro:
                raise
            registro.ultimo_slide = data.indice
            db.commit()
    else:
        registro.ultimo_slide = data.indice
        db.commit()

    db.refresh(registro)
    return AvaliacaoProgressSlideOut(ultimo_slide=registro.ultimo_slide)


@router.post("/{avaliacao_id}/reiniciar", response_model=AvaliacaoProgressOut)
def reiniciar_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Recomeçar avaliação — o aluno testou/espiou os exercícios e quer
    refazer valendo de verdade. NÃO apaga nada: só incrementa `rodada_atual`,
    o que faz GET/PUT /avaliacao-respostas passarem a ignorar as respostas
    antigas (ficam no banco, soft, só saem de vista)."""
    _verificar_gating_avaliacao(db, current_user.id, avaliacao_id)

    if not db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first():
        raise HTTPException(404, "Avaliação not found")

    registro = (
        db.query(AvaliacaoProgress)
        .filter(
            AvaliacaoProgress.user_id == current_user.id,
            AvaliacaoProgress.avaliacao_id == avaliacao_id,
        )
        .first()
    )
    if not registro:
        registro = AvaliacaoProgress(
            user_id=current_user.id,
            avaliacao_id=avaliacao_id,
            status="em_andamento",
            iniciado_em=func.now(),
            rodada_atual=1,
        )
        db.add(registro)
    else:
        registro.rodada_atual = (registro.rodada_atual or 1) + 1
        registro.status = "em_andamento"
        registro.ultimo_slide = None
    db.commit()
    db.refresh(registro)
    return registro