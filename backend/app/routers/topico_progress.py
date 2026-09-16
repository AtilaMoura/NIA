"""Progresso por tópico — FASE 2 do front de formação bíblica (Emaús).

O model Progress existente é por MÓDULO; aqui a granularidade é por TÓPICO.
Só upsert de status, nunca deleta.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.models import Topico, TopicoProgress, User
from app.core.auth import get_current_user, get_topico_resposta_user_id
from app.schemas.topico_progress import (
    TopicoProgressOut,
    TopicoProgressSlideOut,
    TopicoProgressSlideUpsert,
    TopicoProgressUpsert,
)

router = APIRouter(prefix="/topico-progress", tags=["Topico Progress"])


@router.get("/", response_model=list[TopicoProgressOut])
def list_topico_progress(user_id: int = Query(...), db: Session = Depends(get_db)):
    return (
        db.query(TopicoProgress)
        .filter(TopicoProgress.user_id == user_id)
        .order_by(TopicoProgress.topico_id)
        .all()
    )


@router.put("/{topico_id}", response_model=TopicoProgressOut)
def upsert_topico_progress(
    topico_id: int,
    data: TopicoProgressUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ninguém grava progresso "como" outra pessoa, nem papel elevado — é sempre o
    # próprio usuário autenticado (achado de segurança 2026-09-04: user_id vinha só
    # do corpo da requisição, sem checar contra o token).
    if data.user_id != current_user.id:
        raise HTTPException(403, "Só é possível marcar progresso da própria conta.")
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    def _buscar_registro():
        return (
            db.query(TopicoProgress)
            .filter(
                TopicoProgress.user_id == data.user_id,
                TopicoProgress.topico_id == topico_id,
            )
            .first()
        )

    def _aplicar_status(registro: TopicoProgress):
        registro.status = data.status
        if data.status == "em_andamento" and registro.iniciado_em is None:
            registro.iniciado_em = func.now()
        if data.status == "concluido":
            if registro.iniciado_em is None:
                registro.iniciado_em = func.now()
            registro.concluido_em = func.now()
        # voltar pra em_andamento/nao_iniciado NÃO limpa concluido_em (mantém histórico)

    registro = _buscar_registro()
    if not registro:
        registro = TopicoProgress(
            user_id=data.user_id, topico_id=topico_id, status="nao_iniciado"
        )
        db.add(registro)
        _aplicar_status(registro)
        try:
            db.commit()
        except IntegrityError:
            # Corrida (achado real, 2026-09-04): duas requisições quase simultâneas
            # (ex: React em modo dev disparando o "marcar em_andamento" duas vezes ao
            # montar a página) podem passar pelo SELECT acima antes de qualquer uma
            # commitar o INSERT — a segunda esbarra na unique constraint
            # (user_id, topico_id). Trata como upsert de verdade: descarta a tentativa
            # de insert e aplica a mudança em cima do registro que a outra já criou.
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


@router.get("/{topico_id}/slide", response_model=TopicoProgressSlideOut)
def obter_slide_atual(
    topico_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    """Pro <iframe> restaurar o slide exato onde o aluno parou (2026-09-15) —
    reaproveita o MESMO token de escopo curto das respostas de exercício (é a
    mesma fronteira de confiança: só este usuário, só este tópico)."""
    registro = (
        db.query(TopicoProgress)
        .filter(TopicoProgress.user_id == user_id, TopicoProgress.topico_id == topico_id)
        .first()
    )
    return TopicoProgressSlideOut(ultimo_slide=registro.ultimo_slide if registro else None)


@router.put("/{topico_id}/slide", response_model=TopicoProgressSlideOut)
def salvar_slide_atual(
    topico_id: int,
    data: TopicoProgressSlideUpsert,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_resposta_user_id),
):
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    def _buscar():
        return (
            db.query(TopicoProgress)
            .filter(TopicoProgress.user_id == user_id, TopicoProgress.topico_id == topico_id)
            .first()
        )

    registro = _buscar()
    if not registro:
        registro = TopicoProgress(user_id=user_id, topico_id=topico_id, status="nao_iniciado")
        db.add(registro)
        registro.ultimo_slide = data.indice
        try:
            db.commit()
        except IntegrityError:
            # mesma corrida do upsert de status acima.
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
    return TopicoProgressSlideOut(ultimo_slide=registro.ultimo_slide)


@router.post("/{topico_id}/reiniciar", response_model=TopicoProgressOut)
def reiniciar_topico(
    topico_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Recomeçar tópico (2026-09-15) — o aluno testou/espiou os exercícios (ex:
    respondeu qualquer coisa só pra ver o conteúdo) e quer refazer valendo de
    verdade. NÃO apaga nada: só incrementa `rodada_atual`, o que faz
    GET/PUT /topico-respostas passarem a ignorar as respostas antigas (ficam no
    banco, soft, só saem de vista por não serem mais a rodada corrente — ver
    docstring de topico_respostas.py). `iniciado_em`/`concluido_em` não são
    limpos (mesmo princípio do upsert de status acima: nunca apaga histórico).
    """
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    registro = (
        db.query(TopicoProgress)
        .filter(TopicoProgress.user_id == current_user.id, TopicoProgress.topico_id == topico_id)
        .first()
    )
    if not registro:
        registro = TopicoProgress(
            user_id=current_user.id,
            topico_id=topico_id,
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
