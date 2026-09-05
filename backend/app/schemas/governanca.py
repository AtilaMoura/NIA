# Schemas de governança/publicação de curso (FASE 5b do front Emaús).

from datetime import datetime

from pydantic import BaseModel


class ConfigCursoUpdate(BaseModel):
    aprovacao_master_basta: bool
    aprovacao_exige_todos_tutores: bool
    tutor_ids: list[int]


class AprovacaoCursoUpsert(BaseModel):
    aprovado: bool
    observacao: str | None = None


class PessoaOut(BaseModel):
    id: int
    name: str | None
    email: str


class AprovacaoOut(BaseModel):
    user_id: int
    name: str | None
    papel_no_momento: str
    aprovado: bool
    observacao: str | None
    updated_at: datetime | None


class GovernancaCursoOut(BaseModel):
    course_id: int
    status: str
    publicado: bool
    published_at: datetime | None
    aprovacao_master_basta: bool
    aprovacao_exige_todos_tutores: bool
    tutores: list[PessoaOut]
    professores_disponiveis: list[PessoaOut]
    aprovacoes: list[AprovacaoOut]
    pode_publicar: bool
    sou_tutor: bool
