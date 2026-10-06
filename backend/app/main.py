import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import models
from app.routers import users, courses, modules, progress, lessons, pipeline, topicos
from app.routers import auth
from app.routers import topico_progress
from app.routers import topico_respostas
from app.routers import avaliacao_progress
from app.routers import avaliacao_respostas
from app.routers import avaliacoes
from app.routers import topico_anotacoes
from app.routers import topico_tutor
from app.routers import revisao
from app.routers import governanca
from app.routers import pessoas
from app.routers import estudo
from app.routers import caderno
from app.routers import matriculas

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def _ensure_colunas_extras(bind):
    """`create_all` cria tabela nova mas não faz ALTER em tabela que já existe.
    Colunas da FASE 4 do front Emaús (Tutor por tópico + tamanho de fonte) —
    idempotente via ADD COLUMN IF NOT EXISTS (Postgres)."""
    stmts = [
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS tutor_veredito VARCHAR(10)",
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS tutor_analise JSONB",
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS avaliado_em TIMESTAMPTZ",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_font_size VARCHAR(4)",
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'valid_preferred_font_size') THEN "
        "ALTER TABLE users ADD CONSTRAINT valid_preferred_font_size "
        "CHECK (preferred_font_size IN ('sm', 'md', 'lg')); "
        "END IF; END $$;",
        # FASE 1 do front Emaús: role ganha 'master'/'professor' (além de 'aluno'/'admin').
        # A CHECK original só tinha 'aluno'/'admin' — precisa dropar e recriar.
        "ALTER TABLE users DROP CONSTRAINT IF EXISTS valid_role",
        "ALTER TABLE users ADD CONSTRAINT valid_role "
        "CHECK (role IN ('aluno', 'admin', 'master', 'professor'))",
        # FASE 5b: governança de publicação por curso.
        "ALTER TABLE courses ADD COLUMN IF NOT EXISTS aprovacao_master_basta BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE courses ADD COLUMN IF NOT EXISTS aprovacao_exige_todos_tutores BOOLEAN NOT NULL DEFAULT FALSE",
        # Identidade visual + capas geradas pelo ImagemAgent (2026-09-11).
        "ALTER TABLE courses ADD COLUMN IF NOT EXISTS identidade_visual JSONB",
        "ALTER TABLE courses ADD COLUMN IF NOT EXISTS cover_image_url VARCHAR(500)",
        "ALTER TABLE modules ADD COLUMN IF NOT EXISTS cover_image_url VARCHAR(500)",
        # Slide exato onde o aluno parou + "rodada" de exercícios pra separar
        # teste/preview de avaliação real (2026-09-15, ver POST
        # /topico-progress/{id}/reiniciar).
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS ultimo_slide INTEGER",
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS rodada_atual INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE topico_respostas ADD COLUMN IF NOT EXISTS rodada INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE topico_respostas DROP CONSTRAINT IF EXISTS uq_topico_resposta_user_topico_question",
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_topico_resposta_user_topico_question_rodada') THEN "
        "ALTER TABLE topico_respostas ADD CONSTRAINT uq_topico_resposta_user_topico_question_rodada "
        "UNIQUE (user_id, topico_id, question_id, rodada); "
        "END IF; END $$;",
        # Preferências do Emaús (2026-09-27): tema ganha 'auto' (segue o aparelho).
        # A CHECK original só tinha 'light'/'dark' — dropa e recria (idempotente).
        "ALTER TABLE users DROP CONSTRAINT IF EXISTS valid_preferred_panel_mode",
        "ALTER TABLE users ADD CONSTRAINT valid_preferred_panel_mode "
        "CHECK (preferred_panel_mode IN ('light', 'dark', 'auto'))",
        # Página Pessoas do Master (2026-09-28): tempo de estudo vem de um sinal do
        # slide a cada minuto; esta coluna guarda o último pra não somar repetido.
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS ultimo_sinal_em TIMESTAMPTZ",
        "ALTER TABLE avaliacao_progress ADD COLUMN IF NOT EXISTS ultimo_sinal_em TIMESTAMPTZ",
        # Estudos privados por pessoa (2026-10-06): visibilidade do curso. A tabela
        # `matriculas` é nova, o create_all cria.
        "ALTER TABLE courses ADD COLUMN IF NOT EXISTS visibilidade VARCHAR(20) NOT NULL DEFAULT 'publico'",
        "DO $$ BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'valid_visibilidade') THEN "
        "ALTER TABLE courses ADD CONSTRAINT valid_visibilidade "
        "CHECK (visibilidade IN ('publico', 'privado')); "
        "END IF; END $$;",
    ]
    with bind.begin() as conn:
        for s in stmts:
            conn.exec_driver_sql(s)


# Trava do Postgres pras "migrations" do start (2026-10-05). Em produção o uvicorn
# sobe 2 workers e os dois rodavam create_all juntos: com tabela NOVA, um deles
# morria com UniqueViolation (..._id_seq) e o backend ficava com 1 worker só
# (visto nos deploys de 2026-10-04 e 2026-10-05). Com a trava, o 2º worker espera
# o 1º terminar e depois só confere que está tudo criado (tudo é idempotente).
_TRAVA_MIGRACAO = 727_001


def _migrar_com_trava():
    with engine.connect() as trava:
        trava.exec_driver_sql(f"SELECT pg_advisory_lock({_TRAVA_MIGRACAO})")
        try:
            models.Base.metadata.create_all(bind=engine)
            _ensure_colunas_extras(engine)
        finally:
            trava.exec_driver_sql(f"SELECT pg_advisory_unlock({_TRAVA_MIGRACAO})")


def create_app():
    app = FastAPI(
        title="NIA API",
        description="Backend da plataforma NIA",
        version="1.0.0",
    )

    # Em produção, CORS_ORIGINS vem do ambiente (.env) — lista separada por vírgula
    # com os domínios reais dos fronts. Sem a variável, cai nos hosts de dev.
    _cors_origins = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "").split(",")
        if o.strip()
    ] or [
        "http://localhost:3000",
        "http://localhost:4000",
        "http://localhost:4200",  # dev server do emaus-web (front de formação bíblica)
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Importante para o SQLAlchemy registrar models
    _migrar_com_trava()

    # Imagens de capa das aulas (buscadas na internet, sem direito autoral — ver
    # sessão do curso de obreiro) e outros arquivos estáticos servidos direto pelo backend.
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Registrar rotas
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(courses.router)
    app.include_router(modules.router)
    app.include_router(progress.router)
    app.include_router(lessons.router)
    app.include_router(topicos.router)
    app.include_router(topico_progress.router)
    app.include_router(topico_respostas.router)
    app.include_router(avaliacao_progress.router)
    app.include_router(avaliacao_respostas.router)
    app.include_router(avaliacoes.router)
    app.include_router(topico_anotacoes.router)
    app.include_router(topico_tutor.router)
    app.include_router(revisao.router)
    app.include_router(governanca.router)
    app.include_router(pessoas.router)
    app.include_router(matriculas.router)
    app.include_router(estudo.router)
    app.include_router(caderno.router)
    app.include_router(pipeline.router)
    # test_ai.router NÃO é registrado em produção (achado de segurança 2026-09-23:
    # endpoints públicos sem autenticação, aceitando prompt livre — deixavam
    # qualquer um na internet gastar a cota paga de GROQ_API_KEY/GEMINI_API_KEY).
    # O arquivo continua em app/routers/test_ai.py pra reativar manualmente em
    # dev local se precisar testar os services de IA direto.

    @app.get("/")
    def root():
        return {"status": "online", "message": "NIA API funcionando!"}

    return app

app = create_app()
