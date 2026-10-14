#!/usr/bin/env bash
# SÓ LEITURA: lista os usuários da produção (VM1) pra decidir quem é real e quem é teste.
# Mostra id, e-mail, papel, criação, último login e quanto estudo cada um tem (progresso,
# lições concluídas). Não mostra senha nem hash. Não muda nada no banco.
# Quem roda é o Atila, da raiz do repo:  bash scripts/listar_usuarios_vm1.sh
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@163.176.70.148

ssh -i $K $H 'cd ~/NIA && docker compose -f docker-compose.backend.yml exec -T backend python -' <<'PY'
from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()
try:
    linhas = db.execute(text("""
        SELECT u.id, u.email, u.role,
               to_char(u.created_at, 'YYYY-MM-DD') AS criado,
               coalesce(to_char(u.last_login, 'YYYY-MM-DD'), '-') AS ultimo_login,
               (SELECT count(*) FROM progress p WHERE p.user_id = u.id) AS progresso
        FROM users u ORDER BY u.id
    """)).fetchall()
    print(f"{'id':>4}  {'e-mail':40} {'papel':10} {'criado':10}  {'últ.login':10}  progresso")
    for l in linhas:
        print(f"{l.id:>4}  {l.email:40} {l.role:10} {l.criado:10}  {l.ultimo_login:10}  {l.progresso}")
    print(f"\nTotal: {len(linhas)} usuários")
finally:
    db.close()
PY
