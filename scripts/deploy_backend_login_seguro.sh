#!/usr/bin/env bash
# Deploy do backend (VM1) com o login seguro — commit c8bb9e5 (2026-10-07).
# Sem mudança de banco. Faz build na própria VM1 e recria só o container do backend
# (o site fica uns segundos devolvendo 502 enquanto ele sobe).
# ATENÇÃO: leva TUDO que estiver commitado no master, inclusive de outros terminais.
# Quem roda é o Atila, da raiz do repo:
#   bash scripts/deploy_backend_login_seguro.sh              -> só mostra o que iria (não muda nada)
#   bash scripts/deploy_backend_login_seguro.sh --confirmar  -> envia e faz o deploy
#
# Voltar atrás (na VM1), trocando <commit> pelo "antes" que o passo 2 mostra:
#   cd ~/NIA && git checkout <commit> && docker compose -f docker-compose.backend.yml up -d --build backend
#   (depois de resolver, voltar pro master:  git checkout master)
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@163.176.70.148
API=https://nia-api.duckdns.org

echo "== Commits que ainda não estão no GitHub (vão no push):"
git fetch -q originNIA
git log --oneline originNIA/master..master
echo "== Mudanças locais sem commit em backend/ (NÃO vão no deploy):"
git status --short backend docker-compose.backend.yml | head -20

if [ "${1:-}" != "--confirmar" ]; then
  echo
  echo "Só conferência. Se todos os commits acima estão prontos, rode de novo com --confirmar"
  echo "(e marque antes a linha 🚦 do PENDENCIAS.md: VM1 — item 8 — HH:MM)."
  exit 0
fi

echo "== 1/4 Enviar pro GitHub"
git push originNIA master

echo "== 2/4 VM1: memória, commit de antes e git pull"
ssh -i $K $H 'set -e
  free -h | head -2
  cd ~/NIA
  echo "antes: $(git rev-parse --short HEAD)"
  git pull --ff-only
  echo "depois: $(git rev-parse --short HEAD)"'

echo "== 3/4 VM1: build e recriar só o backend"
ssh -i $K $H 'cd ~/NIA && docker compose -f docker-compose.backend.yml up -d --build backend 2>&1 | tail -8'

echo "== 4/4 Conferência (o 1º 502 é o backend subindo)"
sleep 25
echo -n "API /docs (200 esperado):                  "; curl -s -o /dev/null -w "%{http_code}\n" $API/docs
echo -n "/auth/me sem token (401 esperado):         "; curl -s -o /dev/null -w "%{http_code}\n" $API/auth/me
echo -n "login com e-mail que não existe (esperado 401 E-mail ou senha incorretos.): "
curl -s -w " [%{http_code}]\n" -X POST $API/auth/login -H "Content-Type: application/json" \
  -d '{"email":"conferencia-deploy@naoexiste.local","password":"x"}'
ssh -i $K $H 'docker ps --format "{{.Names}}  {{.Status}}"'
echo "Pronto. Teste: entrar no Emaús com a sua conta e abrir um tópico. Depois, 🚦 livre."
