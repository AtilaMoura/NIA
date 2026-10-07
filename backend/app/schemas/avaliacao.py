# Schemas da prova do tópico no padrão novo (banco de perguntas + sorteio por rodada).
# Regras: docs/processo-topico/PROVA.md. Os campos de cada pergunta seguem o schema
# "Pergunta" (docs/schema/schema-conteudo-topico.md) + "assunto"; a checagem fina é o
# validar_prova() (app/renderer/validate.py), que roda antes de gravar.

from pydantic import BaseModel, Field


class ProvaUpsert(BaseModel):
    intro: dict
    resultado: dict
    banco: list[dict] = Field(min_length=1)
    por_rodada: int = Field(ge=1)
    nota_minima: float = Field(gt=0, le=1)
    tipos_minimos: dict[str, int] = Field(default_factory=dict)
    aprovada: bool = True  # False = grava mas o aluno ainda não vê (render devolve 409)


class ProvaOut(BaseModel):
    id: int
    topico_id: int
    is_approved: bool
    conteudo: dict
