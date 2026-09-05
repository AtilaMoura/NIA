# Schemas da área de revisão (FASE 5a do front Emaús) — anotação por slide +
# checklist de aprovação por tópico.

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Reacao = Literal["positivo", "negativo"]
ImagemSugerida = Literal["antes", "depois"]
Profundidade = Literal["raso", "adequado", "aprofundado"]
Clareza = Literal["confuso", "parcialmente_claro", "claro"]
QualidadeGeral = Literal["fraca", "regular", "boa", "excelente"]


class ComentarioCreate(BaseModel):
    topico_id: int
    slide_index: int | None = None
    reacao: Reacao | None = None
    imagem_sugerida: ImagemSugerida | None = None
    sobre_imagem: bool = False
    texto: str | None = None


class ComentarioUpdate(BaseModel):
    texto: str | None = None
    resolvido: bool | None = None


class ComentarioOut(BaseModel):
    id: int
    topico_id: int
    user_id: int
    slide_index: int | None
    reacao: Reacao | None
    imagem_sugerida: ImagemSugerida | None
    sobre_imagem: bool
    texto: str | None
    resolvido: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChecklistUpsert(BaseModel):
    profundidade: Profundidade
    clareza: Clareza
    qualidade_geral: QualidadeGeral
    observacao_final: str | None = None
    aprovado: bool


class ChecklistOut(BaseModel):
    id: int
    topico_id: int
    user_id: int
    profundidade: Profundidade
    clareza: Clareza
    qualidade_geral: QualidadeGeral
    observacao_final: str | None
    aprovado: bool
    updated_at: datetime | None

    class Config:
        from_attributes = True
