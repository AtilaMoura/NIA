# backend/app/schemas/courses.py

from pydantic import BaseModel
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