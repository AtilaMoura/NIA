# Schemas da liberação de estudos por pessoa (2026-10-06): o Master libera ou
# pausa um curso (estudo privado) pra alguém — ver services/matricula_service.py.

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class PessoaCurta(BaseModel):
    id: int
    name: str | None = None


class EstudoMeu(BaseModel):
    """Um estudo privado que o usuário logado pode abrir (/estudos)."""
    course_id: int
    titulo: str
    descricao: str | None = None
    cover_image_url: str | None = None
    # Só vem preenchido pro Master: quem mais tem esse estudo liberado
    liberado_para: list[PessoaCurta] = []


class LiberacaoEstudo(BaseModel):
    """Um estudo privado visto da página da pessoa (Pessoas → fulano)."""
    course_id: int
    titulo: str
    status: Literal["ativa", "pausada", "cancelada"] | None = None  # None = nunca liberado
    atualizada_em: datetime | None = None


class MudarLiberacao(BaseModel):
    status: Literal["ativa", "pausada"]
