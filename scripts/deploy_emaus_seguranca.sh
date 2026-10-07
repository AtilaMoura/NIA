#!/usr/bin/env bash
# Deploy de segurança do Emaús (VM2) — 2026-10-07, commit 9aef09f.
# 1) Escudo no Caddy (recusa Next-Action + log de acesso)  2) imagem nova (Next 16.3.8 / React 19.2.8)
# Pré-requisito: imagem nia-emaus-emaus:latest já buildada no PC (build do commit 9aef09f).
# Rodar da raiz do repo:  bash scripts/deploy_emaus_seguranca.sh
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@137.131.152.20
SITE=https://caminho-emaus.duckdns.org

echo "== 1/4 Backup do Caddyfile atual na VM2"
ssh -i $K $H 'cp ~/NIA/Caddyfile.emaus ~/Caddyfile.emaus.antes_escudo_2026-10-07'

echo "== 2/4 Caddy: validar o novo e recarregar (sem derrubar o site)"
scp -q -i $K Caddyfile.emaus $H:/tmp/Caddyfile.novo
ssh -i $K $H '
  docker cp /tmp/Caddyfile.novo nia-emaus-caddy-1:/tmp/Caddyfile.novo
  docker exec nia-emaus-caddy-1 caddy validate --config /tmp/Caddyfile.novo --adapter caddyfile
  cat /tmp/Caddyfile.novo > ~/NIA/Caddyfile.emaus
  docker exec nia-emaus-caddy-1 caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile
'

echo "== 3/4 Imagem nova do Emaús (Next 16.3.8) — envia ~230 MB"
docker save nia-emaus-emaus:latest | gzip -1 | ssh -i $K $H \
  'gunzip | docker load && cd ~/NIA && docker compose -f docker-compose.emaus.yml up -d --no-build emaus'

echo "== 4/4 Conferência"
sleep 15
echo -n "site:            "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/
echo -n "entrar:          "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/entrar
echo -n "Next-Action (403 esperado): "; curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Next-Action: x" $SITE/
ssh -i $K $H 'docker exec nia-emaus-emaus-1 node -e "console.log(\"next\", require(\"next/package.json\").version)"'
echo "Pronto."
