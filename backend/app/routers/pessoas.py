"""Página Pessoas do Master no Emaús (2026-09-28): todo mundo (alunos, admins,
professores) com último login, última atividade, tópicos, provas e tempo de
estudo. Só o Master — nem admin/professor veem (é acompanhamento da equipe
também)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.pessoas import PessoaDetalhe, PessoaResumo
from app.services.pessoas_service import detalhe_pessoa, listar_pessoas

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])


def _exigir_master(user: User):
    if user.role != "master":
        raise HTTPException(403, "Só o Master acessa a página de pessoas.")


@router.get("/", response_model=list[PessoaResumo])
def listar(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_master(current_user)
    return listar_pessoas(db)


@router.get("/{user_id}", response_model=PessoaDetalhe)
def detalhe(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_master(current_user)
    pessoa = detalhe_pessoa(db, user_id)
    if not pessoa:
        raise HTTPException(404, "Pessoa não encontrada.")
    return pessoa
