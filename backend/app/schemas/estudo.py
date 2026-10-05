# Schemas da área de estudo do próprio usuário no Emaús (2026-10-04):
# página "Minhas anotações" e o painel da /estudos (protótipos 11 e 12).

from datetime import date, datetime

from pydantic import BaseModel


class AnotacaoMinha(BaseModel):
    topico_id: int
    topico_titulo: str
    course_id: int
    curso: str
    modulo_index: int
    modulo_titulo: str
    lesson_id: int
    aula_index: int
    aula_titulo: str
    slide_index: int
    slide_titulo: str | None = None
    texto: str
    atualizado_em: datetime | None = None


class UltimoTopico(BaseModel):
    topico_id: int
    titulo: str
    ultimo_slide: int | None = None
    total_slides: int | None = None
    atualizado_em: datetime | None = None


class ResumoCurso(BaseModel):
    course_id: int
    tempo_s: int = 0
    anotacoes: int = 0
    concluidos_semana: int = 0
    ultimo: UltimoTopico | None = None
    reforcar: list[str] = []  # títulos dos tópicos em que o tutor pediu reforço


class DiaEstudo(BaseModel):
    dia: date
    segundos: int = 0


class ResumoEstudo(BaseModel):
    cursos: list[ResumoCurso] = []
    dias: list[DiaEstudo] = []        # últimos 7 dias, do mais antigo pro de hoje
    tempo_semana_s: int = 0
    concluidos_semana: int = 0
    sequencia_dias: int = 0           # dias seguidos estudando, até hoje (ou ontem)
