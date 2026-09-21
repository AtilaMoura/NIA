# Schemas do progresso por avaliação (prova final do tópico).
# Espelho de topico_progress.py trocando topico_id por avaliacao_id.

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.schemas.topico_progress import AvaliarTopicoRequest

StatusAvaliacao = Literal["nao_iniciado", "em_andamento", "concluido"]


class AvaliacaoProgressUpsert(BaseModel):
    user_id: int
    status: StatusAvaliacao


class AvaliacaoProgressOut(BaseModel):
    id: int
    user_id: int
    avaliacao_id: int
    status: str
    iniciado_em: datetime | None = None
    concluido_em: datetime | None = None
    tutor_veredito: str | None = None
    tutor_analise: dict | None = None
    avaliado_em: datetime | None = None
    ultimo_slide: int | None = None
    rodada_atual: int

    class Config:
        from_attributes = True


class AvaliacaoProgressSlideUpsert(BaseModel):
    indice: int


class AvaliacaoProgressSlideOut(BaseModel):
    ultimo_slide: int | None = None