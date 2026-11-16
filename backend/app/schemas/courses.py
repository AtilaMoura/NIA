# backend/app/schemas/courses.py

from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime

class Lesson(BaseModel):
    title: str
    content: str = ""

class ModuleStructure(BaseModel):
    """Módulo SEM conteúdo (só estrutura)"""
    index: int
    title: str
    description: str
    lessons: Optional[List[Lesson]] = []

class CourseGenerateRequest(BaseModel):
    """Request para gerar estrutura"""
    topic: str
    goal: str
    level: str = "beginner"

class CourseStructureResponse(BaseModel):
    """Response com estrutura criada"""
    id: int
    topic: str
    title: str
    description: str
    modules: List[ModuleStructure]
    total_modules: int
    created_at: datetime

class ModuleGenerateResponse(BaseModel):
    """Response do módulo gerado"""
    message: str
    module_id: int
    title: str

def _validar_perfil_ia(v):
    """Vazio vira None (= perfil geral do curso); id desconhecido vira erro 422."""
    from app.agents.perfis import PERFIS_VALIDOS
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    v = v.strip()
    if v not in PERFIS_VALIDOS:
        raise ValueError(f"perfil_ia inválido: '{v}'. Use um destes: {', '.join(PERFIS_VALIDOS)} (ou vazio = geral).")
    return v


class CourseUpdate(BaseModel):
    """Atualização/criação de curso: os campos antigos seguem livres (extra=allow, como
    era com dict); só perfil_ia é validado (NIA-T-031)."""
    model_config = ConfigDict(extra="allow")
    perfil_ia: Optional[str] = None

    @field_validator("perfil_ia")
    @classmethod
    def _perfil_valido(cls, v):
        return _validar_perfil_ia(v)


class CourseCreate(CourseUpdate):
    pass
