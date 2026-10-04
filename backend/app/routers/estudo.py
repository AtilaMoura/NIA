"""Área de estudo do próprio usuário no Emaús (2026-10-04): "Minhas anotações"
e o resumo da /estudos. Sempre do usuário logado — nunca de outra pessoa."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.estudo import AnotacaoMinha, ResumoEstudo
from app.services.estudo_service import minhas_anotacoes, resumo_estudo

router = APIRouter(prefix="/estudo", tags=["Estudo"])


@router.get("/anotacoes", response_model=list[AnotacaoMinha])
def anotacoes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return minhas_anotacoes(db, current_user.id)


@router.get("/resumo", response_model=ResumoEstudo)
def resumo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return resumo_estudo(db, current_user.id)
