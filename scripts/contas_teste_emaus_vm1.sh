#!/usr/bin/env bash
# Confere e troca a senha das contas de teste @emaus.local NA PRODUÇÃO (VM1) — achado 🔴 de
# 2026-10-07: a senha de teste está escrita no código (repositório público) e, se essas contas
# existirem na produção com ela, qualquer um entra pelo login normal (master inclusive).
#
# 1) Testa o login de cada conta pela API pública com a senha de teste (lida do próprio repo,
#    não fica neste arquivo).
# 2) Só as que ENTRARAM recebem senha nova aleatória, gerada DENTRO da VM1. Nada é apagado.
#    A senha nova e o hash antigo ficam num arquivo só do dono na VM1 (não aparecem na tela).
# 3) Testa de novo: todas devem recusar a senha de teste (401).
#
# Quem roda é o Atila, da raiz do repo:  bash scripts/contas_teste_emaus_vm1.sh
# Só conferir, sem trocar nada:          bash scripts/contas_teste_emaus_vm1.sh --so-conferir
#
# Ver as senhas novas (na VM1):  cat ~/senhas_contas_teste_emaus_2026-10-07.tsv
# Voltar atrás: o arquivo acima tem o hash antigo de cada conta (3ª coluna).
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@163.176.70.148
API=https://nia-api.duckdns.org
ARQ='~/senhas_contas_teste_emaus_2026-10-07.tsv'

CONTAS="master admin1 admin2 admin3 professor1 professor2 professor3 professor4 professor5 aluno"

# Senha de teste: a mesma do login rápido de dev (fica só no repo, não neste script)
SENHA_TESTE=$(sed -n 's/^const SENHA_TESTE = "\(.*\)";/\1/p' emaus-web/app/api/sessao/dev/route.ts)
[ -n "$SENHA_TESTE" ] || { echo "Não achei a senha de teste no route.ts — parei."; exit 1; }

conferir() {
  ABERTAS=""
  for c in $CONTAS; do
    email="$c@emaus.local"
    cod=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API/auth/login" \
      -H "Content-Type: application/json" \
      -d "{\"email\":\"$email\",\"password\":\"$SENHA_TESTE\"}")
    case $cod in
      200) echo "  🔴 $email  ENTROU com a senha de teste"; ABERTAS="$ABERTAS $email" ;;
      401) echo "  ✅ $email  recusou (401)" ;;
      400) echo "  ✅ $email  não existe na produção (400)" ;;
      *)   echo "  ⚠️  $email  resposta $cod (conferir à mão)" ;;
    esac
  done
}

echo "== 1/3 Conferindo as contas na produção"
conferir

if [ "${1:-}" = "--so-conferir" ]; then echo "Só conferência — nada foi trocado."; exit 0; fi
if [ -z "$ABERTAS" ]; then echo "Nenhuma conta aberta — nada a trocar."; exit 0; fi

echo "== 2/3 Trocando a senha de:$ABERTAS"
ssh -i $K $H "set -e
  cd ~/NIA
  umask 077
  docker compose -f docker-compose.backend.yml exec -T backend python - $ABERTAS <<'PY' >> $ARQ
import secrets, sys
from app.database import SessionLocal
from app.models.models import User
from app.core.security import hash_password

db = SessionLocal()
try:
    for email in sys.argv[1:]:
        u = db.query(User).filter(User.email == email).first()
        if not u:
            continue
        nova = secrets.token_urlsafe(18)
        antigo = u.password_hash
        u.password_hash = hash_password(nova)
        db.commit()
        # email, senha nova, hash antigo (pra voltar atrás) — vai pro arquivo, não pra tela
        print(f'{email}\t{nova}\t{antigo}')
finally:
    db.close()
PY
  chmod 600 $ARQ
  echo \"trocadas: \$(cut -f1 $ARQ | tr '\n' ' ')\""

echo "== 3/3 Conferindo de novo (todas devem recusar)"
conferir
[ -z "$ABERTAS" ] && echo "Pronto. Senhas novas na VM1 em $ARQ (só o dono lê)." \
                  || { echo "🔴 Ainda abertas:$ABERTAS"; exit 1; }
