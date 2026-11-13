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
    resposta_ia: str | None = None
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


# ---- Revisão no tópico (NIA-T-026) ----
StatusRevisao = Literal["pendente", "enviado_ia", "aprovado"]
AcaoRevisao = Literal["aprovar", "enviar_ia", "ia_revisou", "reabrir"]


class AprovarTopicoIn(BaseModel):
    observacao: str | None = None


class PontoTratado(BaseModel):
    comment_id: int
    resposta_ia: str


class AnotacaoTratada(BaseModel):
    anotacao_id: int
    resposta_ia: str


class IaRevisouIn(BaseModel):
    pontos: list[PontoTratado] = []
    anotacoes: list[AnotacaoTratada] = []


class PontoRevisaoOut(BaseModel):
    id: int
    user_id: int
    autor: str | None
    slide_index: int | None
    texto: str | None
    reacao: Reacao | None
    resolvido: bool
    resposta_ia: str | None
    created_at: datetime | None


class AnotacaoRevisaoOut(BaseModel):
    id: int
    user_id: int
    autor: str | None
    slide_index: int
    texto: str
    tratada: bool           # False = ainda conta como ponto aberto
    resposta_ia: str | None
    updated_at: datetime | None


class EventoRevisaoOut(BaseModel):
    id: int
    user_id: int
    autor: str | None
    acao: AcaoRevisao
    observacao: str | None
    created_at: datetime | None


class RevisaoTopicoOut(BaseModel):
    topico_id: int
    status: StatusRevisao
    pode_revisar: bool
    aprovado_por: str | None   # só quando status == 'aprovado'
    aprovado_em: datetime | None
    abertos: int               # pontos não resolvidos + anotações de revisor pendentes
    pontos: list[PontoRevisaoOut]
    anotacoes: list[AnotacaoRevisaoOut]
    eventos: list[EventoRevisaoOut]
