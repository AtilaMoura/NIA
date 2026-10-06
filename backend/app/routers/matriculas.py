"""Liberação de estudos privados por pessoa (2026-10-06) — só o Master.
A regra de quem vê o quê fica em services/acesso_service.py; aqui só se
libera/pausa (services/matricula_service.py)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.matricula import LiberacaoEstudo, MudarLiberacao
from app.services.matricula_service import liberacoes_da_pessoa, mudar_liberacao

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


def _exigir_master(user: User):
    if user.role != "master":
        raise HTTPException(403, "Só o Master libera estudos.")


@router.get("/pessoa/{user_id}", response_model=list[LiberacaoEstudo])
def liberacoes(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_master(current_user)
    return liberacoes_da_pessoa(db, user_id)


@router.put("/pessoa/{user_id}/curso/{course_id}", response_model=LiberacaoEstudo)
def mudar(
    user_id: int,
    course_id: int,
    data: MudarLiberacao,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_master(current_user)
    return mudar_liberacao(db, current_user, user_id, course_id, data.status)
