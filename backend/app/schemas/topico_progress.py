# Schemas do progresso por tópico (FASE 2 do front Emaús).

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

StatusTopico = Literal["nao_iniciado", "em_andamento", "concluido"]


class TopicoProgressUpsert(BaseModel):
    user_id: int
    status: StatusTopico


class AvaliarTopicoRequest(BaseModel):
    """Aluno cola o '=== RESUMO ===' que o render monta no fim do tópico; o Tutor
    avalia (dominado / reforço) — FASE 4 do front Emaús."""

    user_id: int
    resumo_texto: str
    modelo: str = "groq"


class TopicoProgressOut(BaseModel):
    id: int
    user_id: int
    topico_id: int
    status: str
    iniciado_em: datetime | None = None
    concluido_em: datetime | None = None
    tutor_veredito: str | None = None
    tutor_analise: dict | None = None
    avaliado_em: datetime | None = None

    class Config:
        from_attributes = True
