#!/usr/bin/env bash
# Deploy da imagem do Emaús (VM2) a partir do último commit — 2026-10-07.
# Leva: proxy.ts no lugar do middleware.ts, /entrar sem a chamada à rota de dev (f2d83b7),
# repasse do 429 do login (c8bb9e5) e o que mais estiver commitado em emaus-web/.
# Builda no PC (a VM2 trava se buildar lá) de uma cópia LIMPA do commit — o que está sem
# commit na pasta não entra. Recria só o container do Emaús (segundos de 502).
# Rodar DEPOIS do deploy do backend (a mensagem de "muitas tentativas" vem de lá).
# Quem roda é o Atila, da raiz do repo:
#   bash scripts/deploy_emaus_imagem.sh              -> só mostra o que iria (não muda nada)
#   bash scripts/deploy_emaus_imagem.sh --confirmar  -> builda, envia (~230 MB) e sobe
#
# Voltar atrás (na VM2): a imagem anterior fica guardada com a etiqueta "anterior":
#   docker tag nia-emaus-emaus:anterior nia-emaus-emaus:latest
#   cd ~/NIA && docker compose -f docker-compose.emaus.yml up -d --no-build emaus
set -euo pipefail

K=ssh-key-2026-09-07now.key
H=ubuntu@137.131.152.20
SITE=https://caminho-emaus.duckdns.org
API_PUBLICA=https://nia-api.duckdns.org

echo "== Commit que vai virar imagem: $(git log --oneline -1)"
echo "== Mudanças em emaus-web/ SEM commit (não entram):"
git status --short emaus-web | head -20

if [ "${1:-}" != "--confirmar" ]; then
  echo
  echo "Só conferência. Pra seguir, rode de novo com --confirmar"
  echo "(e marque antes a linha 🚦 do PENDENCIAS.md: VM2 — item 8 — HH:MM)."
  exit 0
fi

echo "== 1/4 Build no PC, de uma cópia limpa do commit (alguns minutos)"
T=$(mktemp -d)
git archive HEAD emaus-web | tar -x -C "$T"
( cd "$T/emaus-web" && docker build --platform linux/amd64 -f Dockerfile.prod \
    --build-arg NEXT_PUBLIC_API_URL=$API_PUBLICA -t nia-emaus-emaus:latest . 2>&1 | tail -6 )
rm -rf "$T"

echo "== 2/4 VM2: memória e guardar a imagem atual como 'anterior'"
ssh -i $K $H 'free -h | head -2; docker tag nia-emaus-emaus:latest nia-emaus-emaus:anterior'

echo "== 3/4 Enviar a imagem e recriar só o Emaús"
docker save nia-emaus-emaus:latest | gzip -1 | ssh -i $K $H \
  'gunzip | docker load && cd ~/NIA && docker compose -f docker-compose.emaus.yml up -d --no-build emaus'

echo "== 4/4 Conferência (o 1º 502 é o Next subindo)"
sleep 20
echo -n "site:    "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/
echo -n "entrar:  "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/entrar
echo -n "página protegida sem login (307 esperado): "; curl -s -o /dev/null -w "%{http_code}\n" $SITE/inicio
echo -n "Next-Action (403 esperado): "; curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Next-Action: x" $SITE/
echo -n "cabeçalhos de segurança (7 esperado): "
curl -sI $SITE/ | grep -ciE "^(strict-transport|x-content-type|referrer-policy|permissions-policy|cross-origin-opener|content-security-policy)"
ssh -i $K $H 'docker exec nia-emaus-emaus-1 node -e "console.log(\"next\", require(\"next/package.json\").version)"
  docker ps --format "{{.Names}}  {{.Status}}"'
echo "Pronto. Teste: entrar com a sua conta, abrir um tópico e uma prova. Depois, 🚦 livre."
