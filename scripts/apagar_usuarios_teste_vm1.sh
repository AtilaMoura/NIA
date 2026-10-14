#!/usr/bin/env bash
# APAGA DE VERDADE usuários de teste da produção (VM1) — pedido do Atila em 2026-10-07
# ("exclui todos esses usuários, deixa só os reais"), escolhendo apagar em vez de desativar.
#
# O banco apaga junto (ON DELETE CASCADE) tudo da pessoa: progresso, lições, provas, matrículas.
# Por isso:
#   - SEM --apagar: só MOSTRA quem seria apagado e quanto estudo cada um tem. Não muda nada.
#   - COM --apagar: primeiro faz backup do banco inteiro na VM1, depois apaga tudo numa transação
#     só (ou apaga todos, ou nenhum). Recusa se a lista deixar o sistema sem nenhum master.
#
# Quem roda é o Atila, da raiz do repo:
#   bash scripts/apagar_usuarios_teste_vm1.sh                       # só mostra (contas @emaus.local)
#   bash scripts/apagar_usuarios_teste_vm1.sh outro@x.com           # + outros e-mails
#   bash scripts/apagar_usuarios_teste_vm1.sh --apagar [outros...]  # apaga de verdade
#
# Voltar atrás (na VM1): restaurar ~/backups/antes_apagar_usuarios_2026-10-07.sql.gz
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@163.176.70.148
BACKUP='~/backups/antes_apagar_usuarios_2026-10-07.sql.gz'

APAGAR=0
EXTRAS=""
for a in "$@"; do
  if [ "$a" = "--apagar" ]; then APAGAR=1; else EXTRAS="$EXTRAS $a"; fi
done

# Contas do seed de teste (as que não existem na produção são ignoradas)
EMAILS="admin1@emaus.local admin2@emaus.local admin3@emaus.local professor1@emaus.local
professor2@emaus.local professor3@emaus.local professor4@emaus.local professor5@emaus.local
master@emaus.local aluno@emaus.local$EXTRAS"
EMAILS=$(echo $EMAILS)  # junta numa linha só

if [ $APAGAR = 1 ]; then
  echo "== 1/3 Backup do banco inteiro na VM1"
  ssh -i $K $H "set -e; mkdir -p ~/backups; cd ~/NIA
    docker compose -f docker-compose.backend.yml exec -T db sh -c 'pg_dump -U \"\$POSTGRES_USER\" \"\$POSTGRES_DB\"' | gzip > $BACKUP
    chmod 600 $BACKUP
    [ \$(stat -c %s $BACKUP) -gt 100000 ] || { echo 'backup pequeno demais — parei sem apagar'; exit 1; }
    ls -lh $BACKUP"
fi

[ $APAGAR = 1 ] && echo "== 2/3 Apagando" || echo "== Só mostrando (nada será apagado)"
ssh -i $K $H "cd ~/NIA && docker compose -f docker-compose.backend.yml exec -T backend python - $APAGAR $EMAILS" <<'PY'
import sys
from sqlalchemy import text
from app.database import SessionLocal

apagar = sys.argv[1] == "1"
emails = [e.lower() for e in sys.argv[2:]]
db = SessionLocal()
try:
    alvos = db.execute(text("""
        SELECT u.id, u.email, u.role,
               (SELECT count(*) FROM progress p WHERE p.user_id = u.id) AS progresso
        FROM users u WHERE lower(u.email) = ANY(:e) ORDER BY u.id
    """), {"e": emails}).fetchall()
    achados = {a.email.lower() for a in alvos}
    for a in alvos:
        print(f"  {a.id:>4}  {a.email:40} {a.role:10} progresso: {a.progresso}")
    nao = [e for e in emails if e not in achados]
    if nao:
        print(f"  (não existem, ignorados: {' '.join(nao)})")
    if not alvos:
        print("Ninguém a apagar.")
        sys.exit(0)

    masters_fora = db.execute(text(
        "SELECT count(*) FROM users WHERE role = 'master' AND NOT (lower(email) = ANY(:e))"
    ), {"e": emails}).scalar()
    if masters_fora == 0:
        print("RECUSADO: a lista apagaria todos os masters. Nada foi apagado.")
        sys.exit(1)

    if not apagar:
        print(f"{len(alvos)} usuário(s) seriam apagados. Rode de novo com --apagar pra apagar.")
        sys.exit(0)

    n = db.execute(text("DELETE FROM users WHERE id = ANY(:ids)"),
                   {"ids": [a.id for a in alvos]}).rowcount
    db.commit()
    print(f"Apagados: {n} usuário(s) (e o que era ligado a eles).")
except Exception:
    db.rollback()
    raise
finally:
    db.close()
PY

if [ $APAGAR = 1 ]; then
  echo "== 3/3 Conferência: lista atual"
  bash scripts/listar_usuarios_vm1.sh
fi
