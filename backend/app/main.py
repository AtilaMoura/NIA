from fastapi import FastAPI
from app.database import Base, engine
from app.models.models import Course, Module, Progress

app = FastAPI(
    title="NIA API",
    description="Backend da plataforma NIA",
    version="1.0.0"
)

# Criar tabelas automaticamente
@app.on_event("startup")
def startup_event():
    print("🔄 Criando tabelas no banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

@app.get("/")
def root():
    return {"status": "online", "message": "NIA API funcionando!"}
