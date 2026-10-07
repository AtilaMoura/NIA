#!/usr/bin/env bash
# Troca a SECRET_KEY do backend (VM1) por precaução depois da invasão do Emaús (2026-10-07).
# Efeito: TODOS os logins caem na hora (alunos entram de novo com a mesma senha) e quem estiver
# no meio de um tópico/prova perde o token de 2h daquela tela. Rodar em horário calmo.
# A chave nova é gerada DENTRO da VM e nunca aparece na tela nem sai de lá.
# Não mexe no banco nem faz build: só recria o container do backend.
# Quem roda é o Atila, da raiz do repo:  bash scripts/trocar_secret_key_vm1.sh
#
# Voltar atrás (na VM1):  cp ~/.env.antes_troca_chave_2026-10-07 ~/NIA/.env
#                         cd ~/NIA && docker compose -f docker-compose.backend.yml up -d backend
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@163.176.70.148
API=https://nia-api.duckdns.org

echo "== 1/3 Backup do .env (só o dono lê) e troca da chave"
ssh -i $K $H 'set -e
  cd ~/NIA
  grep -q "^SECRET_KEY=" .env || { echo "SECRET_KEY não está no .env — parei sem mudar nada"; exit 1; }
  cp .env ~/.env.antes_troca_chave_2026-10-07 && chmod 600 ~/.env.antes_troca_chave_2026-10-07
  antes=$(grep "^SECRET_KEY=" .env | sha256sum)
  sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$(openssl rand -hex 32)|" .env
  depois=$(grep "^SECRET_KEY=" .env | sha256sum)
  [ "$antes" != "$depois" ] && echo "chave trocada (valor não exibido)" || { echo "a chave NÃO mudou"; exit 1; }'

echo "== 2/3 Recriar só o backend (sem build)"
ssh -i $K $H 'cd ~/NIA && docker compose -f docker-compose.backend.yml up -d backend'

echo "== 3/3 Conferência (o 1º 502 é o backend subindo)"
sleep 20
echo -n "API /docs (200 esperado):          "; curl -s -o /dev/null -w "%{http_code}\n" $API/docs
echo -n "/auth/me sem token (401 esperado): "; curl -s -o /dev/null -w "%{http_code}\n" $API/auth/me
ssh -i $K $H 'docker ps --format "{{.Names}}  {{.Status}}"'
echo "Pronto. Teste: abra o Emaús — ele deve pedir login de novo; entre e confira um tópico."
