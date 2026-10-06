"""Área de estudo do próprio usuário no Emaús (2026-10-04): "Minhas anotações",
o resumo da /estudos e (2026-10-06) a lista de estudos privados liberados pra
ele. Sempre do usuário logado — nunca de outra pessoa."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.models.models import User
from app.schemas.estudo import AnotacaoMinha, ResumoEstudo
from app.schemas.matricula import EstudoMeu
from app.services import acesso_service
from app.services.matricula_service import meus_estudos
from app.services.estudo_service import minhas_anotacoes, resumo_estudo

router = APIRouter(prefix="/estudo", tags=["Estudo"])


@router.get("/anotacoes", response_model=list[AnotacaoMinha])
def anotacoes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Anotação de curso que a pessoa não abre mais (estudo pausado) fica guardada,
    # só não aparece
    visiveis = {c.id for c in acesso_service.cursos_visiveis(db, current_user)}
    return [a for a in minhas_anotacoes(db, current_user.id) if a.course_id in visiveis]


@router.get("/resumo", response_model=ResumoEstudo)
def resumo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return resumo_estudo(db, current_user.id)


@router.get("/meus-estudos", response_model=list[EstudoMeu])
def estudos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return meus_estudos(db, current_user)
