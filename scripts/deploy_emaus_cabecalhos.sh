#!/usr/bin/env bash
# Deploy dos cabeçalhos de segurança + logs que não se perdem — Emaús (VM2), 2026-10-07.
# Só Caddyfile.emaus e docker-compose.emaus.yml. NÃO envia imagem nova (usa a que já está na VM).
# Recria os 2 containers (caddy e emaus): alguns segundos de site fora.
# Quem roda é o Atila, da raiz do repo:  bash scripts/deploy_emaus_cabecalhos.sh
#
# Voltar atrás (na VM2):
#   cp ~/Caddyfile.emaus.antes_cabecalhos_2026-10-07 ~/NIA/Caddyfile.emaus
#   cp ~/docker-compose.emaus.yml.antes_cabecalhos_2026-10-07 ~/NIA/docker-compose.emaus.yml
#   cd ~/NIA && docker compose -f docker-compose.emaus.yml up -d --no-build
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@137.131.152.20
SITE=https://caminho-emaus.duckdns.org

echo "== 1/5 Memória da VM2 e backup dos 2 arquivos"
ssh -i $K $H 'free -h | head -2
  cp ~/NIA/Caddyfile.emaus ~/Caddyfile.emaus.antes_cabecalhos_2026-10-07
  cp ~/NIA/docker-compose.emaus.yml ~/docker-compose.emaus.yml.antes_cabecalhos_2026-10-07'

echo "== 2/5 Validar o Caddyfile novo no Caddy que está rodando (se falhar, para aqui e nada muda)"
scp -q -i $K Caddyfile.emaus $H:/tmp/Caddyfile.novo
scp -q -i $K docker-compose.emaus.yml $H:/tmp/compose.novo
ssh -i $K $H 'set -e
  docker cp /tmp/Caddyfile.novo nia-emaus-caddy-1:/tmp/Caddyfile.novo
  docker exec nia-emaus-caddy-1 caddy validate --config /tmp/Caddyfile.novo --adapter caddyfile 2>&1 | tail -1'

echo "== 3/5 Aplicar: arquivos novos + recriar os containers (sem build)"
ssh -i $K $H 'set -e
  mkdir -p ~/NIA/logs/caddy
  cat /tmp/Caddyfile.novo > ~/NIA/Caddyfile.emaus
  cat /tmp/compose.novo > ~/NIA/docker-compose.emaus.yml
  cd ~/NIA && docker compose -f docker-compose.emaus.yml up -d --no-build'

echo "== 4/5 Conferência do site (o 1º 502 é o Next subindo)"
sleep 20
echo -n "site:            "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/
echo -n "entrar:          "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/entrar
echo -n "Next-Action (403 esperado): "; curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Next-Action: x" $SITE/
echo "cabeçalhos (esperado: 7 linhas e nenhum x-powered-by):"
curl -sI $SITE/ | grep -iE "^(strict-transport|x-content-type|referrer-policy|permissions-policy|cross-origin-opener|content-security-policy|x-powered-by)" | cut -c1-90

echo "== 5/5 Logs fora do container"
ssh -i $K $H 'sudo ls -la ~/NIA/logs/caddy/
  echo "últimas linhas do Next no journald:"
  sudo journalctl CONTAINER_TAG=emaus -n 3 --no-pager
  docker ps --format "{{.Names}}  {{.Status}}"'
echo "Pronto."
