# Schemas do tutor ao vivo por tópico (2026-09-19).

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CorrigirRequest(BaseModel):
    question_id: str
    resposta_dada: Any


class CorrigirResponse(BaseModel):
    correta: bool
    correcao_personalizada: str | None = None
    pergunta_reforco: dict | None = None
    reforco_id: int | None = None


class ResponderReforcoRequest(BaseModel):
    resposta_dada: Any
    correta: bool | None = None


class DuvidaRequest(BaseModel):
    slide_index: int
    question_id: str | None = None
    pergunta_aluno: str


class DuvidaResponse(BaseModel):
    id: int
    resposta_ia: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
