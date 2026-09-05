"""
Seed dos perfis do front Emaús (FASE 1 — auth). Idempotente: só cria quem não existe
(procura por e-mail). Roda de dentro de backend/ (ou dentro do container, que já
tem cwd em /app):  python _seed_emaus_users.py

Senha de teste igual pra todos, propositalmente simples (é ambiente local/dev, sem
dado sensível de verdade) — dá pro botão de "login rápido" do /entrar logar sem o
usuário digitar nada.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models.models import User
from app.core.security import hash_password

SENHA_TESTE = "emaus2026"

PERFIS = [
    {"email": "master@emaus.local", "name": "Master (Atila)", "role": "master"},
    {"email": "admin1@emaus.local", "name": "Admin 1", "role": "admin"},
    {"email": "admin2@emaus.local", "name": "Admin 2", "role": "admin"},
    {"email": "admin3@emaus.local", "name": "Admin 3", "role": "admin"},
    {"email": "professor1@emaus.local", "name": "Professor 1", "role": "professor"},
    {"email": "professor2@emaus.local", "name": "Professor 2", "role": "professor"},
    {"email": "professor3@emaus.local", "name": "Professor 3", "role": "professor"},
    {"email": "professor4@emaus.local", "name": "Professor 4", "role": "professor"},
    {"email": "professor5@emaus.local", "name": "Professor 5", "role": "professor"},
]


def main():
    db = SessionLocal()
    try:
        criados, existentes = [], []
        for p in PERFIS:
            existe = db.query(User).filter(User.email == p["email"]).first()
            if existe:
                existentes.append(p["email"])
                continue
            db.add(User(
                name=p["name"],
                email=p["email"],
                password_hash=hash_password(SENHA_TESTE),
                role=p["role"],
            ))
            criados.append(p["email"])
        db.commit()
        print(f"Criados ({len(criados)}): {criados}")
        print(f"Já existiam ({len(existentes)}): {existentes}")
        print(f"Senha de teste (todos): {SENHA_TESTE}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
