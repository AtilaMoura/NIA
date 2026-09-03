"""Progresso por tópico — FASE 2 do front de formação bíblica (Emaús).

O model Progress existente é por MÓDULO; aqui a granularidade é por TÓPICO.
Só upsert de status, nunca deleta.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.models import Topico, TopicoProgress
from app.schemas.topico_progress import TopicoProgressOut, TopicoProgressUpsert

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
    topico_id: int, data: TopicoProgressUpsert, db: Session = Depends(get_db)
):
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    registro = (
        db.query(TopicoProgress)
        .filter(
            TopicoProgress.user_id == data.user_id,
            TopicoProgress.topico_id == topico_id,
        )
        .first()
    )
    if not registro:
        registro = TopicoProgress(
            user_id=data.user_id, topico_id=topico_id, status="nao_iniciado"
        )
        db.add(registro)

    registro.status = data.status
    if data.status == "em_andamento" and registro.iniciado_em is None:
        registro.iniciado_em = func.now()
    if data.status == "concluido":
        if registro.iniciado_em is None:
            registro.iniciado_em = func.now()
        registro.concluido_em = func.now()
    # voltar pra em_andamento/nao_iniciado NÃO limpa concluido_em (mantém histórico)

    db.commit()
    db.refresh(registro)
    return registro
