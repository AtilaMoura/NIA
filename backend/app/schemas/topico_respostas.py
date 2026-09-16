# Schemas das respostas de exercício por tópico (2026-09-09).

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel

TipoPergunta = Literal["mc", "tf", "classify", "associar", "lacuna", "open", "ditado"]


class TopicoRespostaUpsert(BaseModel):
    gate_id: str
    tipo: TipoPergunta
    resposta_dada: Any
    correta: bool | None = None


class TopicoRespostaOut(BaseModel):
    id: int
    user_id: int
    topico_id: int
    gate_id: str
    question_id: str
    tipo: str
    resposta_dada: Any
    correta: bool | None = None
    tentativas: int
    rodada: int
    respondido_em: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
