# Schemas do "Caderno da aula" (2026-10-05, protótipo 13-caderno.html).
#
# A IA devolve SÓ estes blocos (JSON) — o Emaús desenha cada um. Nunca HTML vindo
# da IA. Texto aceita **negrito** (o front transforma em <strong>, nada mais).

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ItemPasso(BaseModel):
    titulo: str = Field(max_length=200)
    detalhe: str | None = Field(None, max_length=400)


class Bloco(BaseModel):
    """Um bloco do caderno. Os campos usados dependem do `tipo`:
    - nota / nota_alt: rotulo?, texto, referencia?
    - correcao: era (o que o aluno escreveu), agora (o certo), topico_id?, slide? (1-based)
    - passos: itens[]
    - tabela: colunas[], linhas[][]
    - lembrete / paragrafo: texto
    """

    tipo: Literal["nota", "nota_alt", "correcao", "passos", "tabela", "lembrete", "paragrafo"]
    rotulo: str | None = Field(None, max_length=120)
    texto: str | None = Field(None, max_length=1500)
    referencia: str | None = Field(None, max_length=300)
    era: str | None = Field(None, max_length=600)
    agora: str | None = Field(None, max_length=1200)
    topico_id: int | None = None
    slide: int | None = None
    itens: list[ItemPasso] = Field(default_factory=list, max_length=12)
    colunas: list[str] = Field(default_factory=list, max_length=4)
    linhas: list[list[str]] = Field(default_factory=list, max_length=12)


class Secao(BaseModel):
    titulo: str = Field(max_length=120)
    blocos: list[Bloco] = Field(default_factory=list, max_length=12)


class PontoReforco(BaseModel):
    titulo: str = Field(max_length=120)
    detalhe: str = Field(max_length=400)


class Veredito(BaseModel):
    resumo: str = Field(max_length=800)
    pontos: list[PontoReforco] = Field(default_factory=list, max_length=6)


class CadernoConteudo(BaseModel):
    subtitulo: str = Field(max_length=240)
    secoes: list[Secao] = Field(min_length=1, max_length=10)
    pratica: list[str] = Field(default_factory=list, max_length=8)  # "o que vou praticar"
    veredito: Veredito


# ---- Respostas da API ----

class AnotacaoDaAula(BaseModel):
    topico_id: int
    topico_titulo: str
    slide_index: int
    slide_titulo: str | None = None
    texto: str
    atualizado_em: datetime | None = None


class TopicoDaAula(BaseModel):
    id: int
    titulo: str
    concluido: bool = False


class CadernoVersaoOut(BaseModel):
    versao: int
    conteudo: CadernoConteudo
    anotacoes_usadas: int
    criado_em: datetime | None = None


class CoresTema(BaseModel):
    """Cores do tema do curso (docs/schema/temas.json) já no formato do caderno."""

    claro: dict[str, str]
    escuro: dict[str, str]


class CadernoEstado(BaseModel):
    lesson_id: int
    aula: str
    aula_index: int
    modulo: str
    modulo_index: int
    course_id: int
    curso: str
    topicos: list[TopicoDaAula]
    anotacoes: list[AnotacaoDaAula]
    caderno: CadernoVersaoOut | None = None
    novas_desde_caderno: int = 0      # anotações criadas/alteradas depois da última versão
    geracoes_restantes_hoje: int = 0
    cores: CoresTema | None = None
