# backend/app/database.py
"""
Configuração da conexão com o banco de dados PostgreSQL
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ============================================
# 1. CARREGAR VARIÁVEIS DO .ENV
# ============================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrada no .env!")

print(f"🔌 Conectando ao banco: {DATABASE_URL.split('@')[1]}")

# ============================================
# 2. ENGINE
# ============================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  
    echo=False,
    pool_size=10,
    max_overflow=20
)

print("✅ Engine criado com sucesso!")

# ============================================
# 3. SESSIONMAKER
# ============================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================
# 4. BASE
# ============================================
Base = declarative_base()

# ============================================
# 5. DEPENDENCY FASTAPI
# ============================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# 6. CRIAR TABELAS (somente MVP)
# ============================================
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

# ============================================
# 7. TESTE DE CONEXÃO
# ============================================
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Conexão com banco OK!")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
