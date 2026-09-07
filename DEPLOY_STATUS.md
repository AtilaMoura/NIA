# Onde paramos — deploy NIA + Emaús na Oracle Cloud

_Atualizado: 2026-09-07 (sessão pausada — reinício de PC)_

## Resumo em 1 linha
Arquivos de produção prontos e commitados. VM na Oracle **não foi criada ainda** —
travou em **"Out of capacity"** do shape gratuito A1 em São Paulo. Falta: liberar
capacidade (ou upgrade) + `git push` + rodar o `DEPLOY.md` na VM.

---

## ✅ Feito

### Código (tudo commitado, **falta `git push`** — 19 commits locais à frente)
- `docker-compose.prod.yml` + `Caddyfile` + `backend/Dockerfile.prod` +
  `frontend/Dockerfile.prod` + `emaus-web/Dockerfile.prod` + `.dockerignore` de cada
- `.env.prod.example` (modelo das variáveis; o `.env` real fica só na VM)
- Patches de segurança: `SECRET_KEY` e `CORS_ORIGINS` do backend agora vêm de
  `os.getenv` (estavam hardcoded)
- `next.config.ts` dos 2 fronts: `output: "standalone"`
- Repo enxugado (commit `0124835`): conteúdo de curso / estudos pessoais / rascunhos
  saíram do git (continuam no disco)
- Builds validados local: `emaus-web` e `frontend` geram `.next/standalone/server.js`; backend compila
- Commit de referência do setup: **`7753eb9`**

### Oracle Cloud (console)
- Conta Free Tier, tenancy `atilagmoura`, região **Brasil Leste (São Paulo)** — **1 AD só (AD-1)**
- Passamos por TODO o wizard "Create instance". Config confirmada na tela de revisão:
  - **Shape:** `VM.Standard.A1.Flex` · **2 OCPU / 12 GB** · "Sempre elegível para gratuidade"
  - **Imagem:** Canonical Ubuntu 24.04 (build 2026.08.25-0, aarch64)
  - **Rede:** VCN nova `vcn-20260906-2208` + sub-rede **pública** nova (CIDR 10.0.0.0/24)
  - **SSH:** par de chaves gerado e baixado → `ssh-key-2026-09-07.key` (privada) +
    `.key.pub` (pública) **na raiz do projeto** — ⚠️ NÃO commitar (já está no `.gitignore`),
    mover pra um lugar seguro (ex. `~/.ssh/`)
- Clicou "Create" → **`Out of capacity for shape VM.Standard.A1.Flex in availability
  domain AD-1`**. A instância **não foi criada**. A VCN pode ter ficado criada (de graça,
  reutilizável).

---

## ❌ Bloqueio atual: capacidade do A1 em São Paulo

- São Paulo tem **só 1 AD**, então "tentar outro AD" não existe aqui.
- **Não dá pra trocar de região:** a região de casa é permanente no Free Tier e os
  recursos Always Free só funcionam nela. Outra região = pago.
- A capacidade do A1 libera de forma imprevisível (minutos a dias).

### Opções (decidir na volta)
- **A) Retry automático (grátis):** loop no Cloud Shell do console tentando criar a VM
  a cada ~1 min. Precisa: OCID da sub-rede, OCID da imagem Ubuntu 24.04 aarch64, e a
  chave SSH pública. (Claude monta o script.)
- **B) Upgrade "Pay As You Go":** adiciona cartão, o A1 grátis **continua grátis**
  (limites Always Free seguem), e ganha **prioridade de capacidade** → "out of capacity"
  praticamente some. Caminho mais rápido.
- **C) Começar pequeno:** subir backend + Postgres num `VM.Standard.E2.1.Micro` (1 GB,
  grátis, sempre disponível) e migrar pro A1 quando liberar. (Emaús não cabe em 1 GB.)

---

## ▶️ Próximos passos (na ordem)

1. Resolver a capacidade — opção A, B ou C acima
2. `git push` (os 19 commits locais)
3. Se repo for privado: criar Deploy Key na VM (ver seção "Repo privado" do `DEPLOY.md`)
4. Seguir o **`DEPLOY.md`** a partir do passo 2 (portas 80/443) — VM já vai existir
5. DuckDNS: 3 subdomínios (`*-api`, `*-nia`, `*-emaus`) apontando pro IP público
6. `.env` na VM → `docker compose -f docker-compose.prod.yml up -d --build`
7. `docker compose exec backend python _seed_emaus_users.py` + publicar cursos

## Pendências não relacionadas ao deploy (do FASE 6, também pausadas)
- Escolha do logo v3 (16 conceitos em `/dev/marca`) — usuário decide
- Spec da página inicial do Emaús — usuário vai passar
