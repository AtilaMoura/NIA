# Schemas do progresso por tópico (FASE 2 do front Emaús).

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

StatusTopico = Literal["nao_iniciado", "em_andamento", "concluido"]


class TopicoProgressUpsert(BaseModel):
    user_id: int
    status: StatusTopico


class TopicoProgressOut(BaseModel):
    id: int
    user_id: int
    topico_id: int
    status: str
    iniciado_em: datetime | None = None
    concluido_em: datetime | None = None

    class Config:
        from_attributes = True
