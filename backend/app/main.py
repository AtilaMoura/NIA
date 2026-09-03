from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app.models import models
from app.routers import users, courses, modules, progress, lessons, pipeline, topicos
from app.routers import auth
from app.routers import topico_progress
from app.routers import test_ai

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

def create_app():
    app = FastAPI(
        title="NIA API",
        description="Backend da plataforma NIA",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:4000",
            "http://localhost:4200",  # dev server do emaus-web (front de formação bíblica)
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Importante para o SQLAlchemy registrar models
    models.Base.metadata.create_all(bind=engine)

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
    app.include_router(pipeline.router)
    app.include_router(test_ai.router)

    @app.get("/")
    def root():
        return {"status": "online", "message": "NIA API funcionando!"}

    return app

app = create_app()
