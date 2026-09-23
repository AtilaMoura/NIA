# Schemas do tutor ao vivo por tópico (2026-09-19).

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


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
    # Limite de 500 caracteres (decisão do Atila, 2026-09-23) — também trava o
    # tamanho do prompt, que tem teto de token por requisição no Groq.
    pergunta_aluno: str = Field(min_length=1, max_length=500)
    # Tamanho da resposta escolhido no seletor do chat (2026-09-23). Sem o
    # campo vale "longa" — comportamento de antes do seletor existir.
    tamanho: Literal["resumida", "media", "longa"] = "longa"


class DuvidaResponse(BaseModel):
    id: int
    resposta_ia: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class DuvidaItem(BaseModel):
    """Uma troca do chat de dúvidas — usado pra remontar a conversa ao reabrir."""
    id: int
    slide_index: int
    pergunta_aluno: str
    resposta_ia: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
