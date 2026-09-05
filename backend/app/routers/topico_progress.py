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
from app.core.auth import get_current_user
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
