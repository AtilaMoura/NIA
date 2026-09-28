# Schemas da página Pessoas do Master no Emaús (2026-09-28): quem está
# estudando, desde quando e quanto — alunos, admins e professores juntos.

from datetime import datetime

from pydantic import BaseModel


class PessoaResumo(BaseModel):
    id: int
    name: str | None = None
    email: str
    role: str
    cadastro_em: datetime | None = None
    ultimo_login: datetime | None = None
    # Maior data entre as marcas de progresso (tópico e prova) — existe mesmo
    # pra quem entrou antes de o login começar a ser gravado.
    ultima_atividade: datetime | None = None
    topicos_iniciados: int = 0
    topicos_concluidos: int = 0
    provas_feitas: int = 0
    tempo_s: int = 0


class TopicoDaPessoa(BaseModel):
    topico_id: int
    titulo: str
    course_id: int
    curso: str
    status: str
    iniciado_em: datetime | None = None
    concluido_em: datetime | None = None
    ultimo_slide: int | None = None
    tempo_s: int = 0
    tutor_veredito: str | None = None
    prova_status: str | None = None   # status do AvaliacaoProgress do tópico, se houver
    prova_veredito: str | None = None


class PessoaDetalhe(PessoaResumo):
    topicos: list[TopicoDaPessoa] = []
