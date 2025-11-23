from fastapi import FastAPI
from app.database import engine
from app.models import models
from app.routers import users, courses, modules, progress

def create_app():
    app = FastAPI(
        title="NIA API",
        description="Backend da plataforma NIA",
        version="1.0.0",
    )

    # Importante para o SQLAlchemy registrar models
    models.Base.metadata.create_all(bind=engine)

    # Registrar rotas
    app.include_router(users.router)
    app.include_router(courses.router)
    app.include_router(modules.router)
    app.include_router(progress.router)

    @app.get("/")
    def root():
        return {"status": "online", "message": "NIA API funcionando!"}

    return app

app = create_app()
