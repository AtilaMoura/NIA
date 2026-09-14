# Schemas das anotações pessoais do aluno por tópico/slide (2026-09-10).

from datetime import datetime

from pydantic import BaseModel


class TopicoAnotacaoUpsert(BaseModel):
    texto: str


class TopicoAnotacaoOut(BaseModel):
    id: int
    user_id: int
    topico_id: int
    slide_index: int
    texto: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
