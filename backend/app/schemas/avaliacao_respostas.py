# Schemas das respostas de exercício por avaliação (prova final do tópico).
# Espelho de topico_respostas.py trocando topico_id por avaliacao_id.

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel

TipoPergunta = Literal["mc", "tf", "classify", "associar", "lacuna", "open", "ditado"]


class AvaliacaoRespostaUpsert(BaseModel):
    gate_id: str
    tipo: TipoPergunta
    resposta_dada: Any
    correta: bool | None = None


class AvaliacaoRespostaOut(BaseModel):
    id: int
    user_id: int
    avaliacao_id: int
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