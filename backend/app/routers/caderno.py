"""Caderno da aula (2026-10-05): as anotações do aluno numa aula, organizadas
e corrigidas pela IA. Sempre do usuário logado — nunca de outra pessoa."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.caderno import CadernoEstado
from app.services.caderno_service import estado, organizar
from app.services import acesso_service

router = APIRouter(prefix="/caderno", tags=["Caderno"])


@router.get("/aula/{lesson_id}", response_model=CadernoEstado)
def ver_caderno(
    lesson_id: int,
    tema: str | None = Query(None, description="id do tema do curso (docs/schema/temas.json)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acesso_service.exigir_estudo_aula(db, current_user, lesson_id)
    return estado(db, current_user.id, lesson_id, tema)


@router.post("/aula/{lesson_id}/organizar", response_model=CadernoEstado)
async def organizar_caderno(
    lesson_id: int,
    tema: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acesso_service.exigir_estudo_aula(db, current_user, lesson_id)
    await organizar(db, current_user.id, lesson_id)
    return estado(db, current_user.id, lesson_id, tema)
