# Onde paramos — deploy NIA + Emaús na Oracle Cloud

_Atualizado: 2026-09-15 00:05 (🟢 NO AR — backend + Emaús em produção com HTTPS)_

## Resumo em 1 linha
**Está no ar.** `https://nia-api.duckdns.org` (backend) e `https://caminho-emaus.duckdns.org`
(Emaús) respondendo em produção, HTTPS automático, cursos 8 e 9 publicados, usuários do
Emaús criados. O `A1.Flex` (VM maior) segue em retry automático via cron na VM 2, mas
deixou de ser bloqueante — não precisa dele pra estar no ar.

## 🟢 URLs em produção
- **API:** https://nia-api.duckdns.org
- **Emaús:** https://caminho-emaus.duckdns.org (login: `master@emaus.local` / `emaus2026`,
  e `admin1-3@emaus.local` / `professor1-5@emaus.local`, mesma senha)

## ✅ VMs ativas agora

### VM 1 — backend + Postgres
- **Nome:** `instance-20260907-1748` (hostname `nia`) · **Always Free** · Running
- **Shape:** `VM.Standard.E2.1.Micro` — 1 OCPU / 1 GB RAM (x86_64) — não redimensionável
- **Imagem:** Ubuntu 24.04 Minimal
- **IP público:** `163.176.70.148` · **Username:** `ubuntu`
- **Chave SSH:** `ssh-key-2026-09-07now.key` (raiz do projeto, ⚠️ não commitar)

### VM 2 — Emaús (criada em 2026-09-14)
- **Nome:** `nia-emaus-e2` · **Always Free** · Running
- **Shape:** `VM.Standard.E2.1.Micro` — 1 OCPU / 1 GB RAM (x86_64)
- **Imagem:** Ubuntu 24.04 Minimal
- **IP público:** `137.131.152.20` · **Username:** `ubuntu`
- **Mesma chave SSH** (`ssh-key-2026-09-07now.key`) — `ssh -i ssh-key-2026-09-07now.key ubuntu@137.131.152.20`
- **É também onde roda o retry automático do A1.Flex** (ver seção abaixo)

Ambas na mesma VCN/subnet (`vcn-20260907-1838` / `subnet-20260907-1838`), então podem
se comunicar por **IP privado** dentro da rede — importante pro Emaús chamar a API do
backend sem expor a porta do backend pra internet.

### Capacidade: sustenta?
Medido nos containers locais + estimativa pra prod (Next.js `standalone`, bem mais leve
que o modo dev):
- Backend FastAPI: ~130 MB · Postgres: ~56 MB (idle) · Next.js standalone: ~80-150 MB cada
- VM 1 (954 MB úteis): backend + Postgres + Caddy ≈ 400-500 MB usado → **folga boa**
- VM 2 (954 MB úteis): só Emaús + Caddy ≈ 300-400 MB usado → **folga grande**

**Conclusão: o que temos hoje sustenta**, mesmo sem o A1. O A1 é só upgrade de conforto/margem.

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
- A capacidade libera de forma **imprevisível e sem fila** — é uma corrida: quando abre
  uma vaga, quem chamar a API primeiro consegue. Pode levar minutos ou semanas.
- Já tentamos dezenas de vezes (2 OCPU/12GB e 1 OCPU/6GB, ambos do pool A1) — sempre
  `Out of host capacity`. Reduzir pra 1 OCPU/6GB não muda a disputa, só aumenta um pouco
  a chance (pede menos hardware contíguo).
- `VM.Standard.A2.Flex` existe como shape maior (até 78 OCPU/946GB) mas **não é Always
  Free** — é pago, pool de capacidade separado, mais disponível.

### ✅ Opção A implementada: retry automático rodando na própria Oracle
Em vez de rodar o loop no PC local (que ficava sem memória e derrubava o processo), a
automação roda **dentro da VM `nia-emaus-e2`**, via cron, 24/7, independente do PC:
- Script: `~/retry_a1.sh` na VM · tenta criar `A1.Flex` 1 OCPU/6GB a cada **7 minutos**
- Log: `~/retry_a1.log` na VM
- Chave de API **dedicada** só pra essa automação (não reaproveita a chave principal),
  gerada na própria VM e cadastrada via API (fingerprint `f4:a8:88:99:17:33:15:58:1d:55:c6:cd:b0:2a:ad:6d`)
- Para sozinho quando tiver sucesso: cria `~/SUCESSO_A1` e remove o próprio cron job
- **Checar status quando quiser:**
  ```
  ssh -i ssh-key-2026-09-07now.key ubuntu@137.131.152.20 "tail -20 retry_a1.log"
  ```

### Outras opções (se quiser acelerar)
- **B) Upgrade "Pay As You Go":** adiciona cartão, o A1 grátis **continua grátis**
  (limites Always Free seguem), e ganha **prioridade de capacidade** → "out of capacity"
  praticamente some. Caminho mais rápido, mas exige cartão.
- Pagar pelo `A2.Flex` (maior, sem o gargalo de capacidade) — custo contínuo.

## 🔑 OCI CLI configurada (novo nesta sessão)
Agora dá pra rodar comandos `oci` direto (local e via automação), sem depender do
console web (que era muito instável por browser automation):
- **Local (Windows):** instalada em `C:\ocicli` (fora do OneDrive por causa de limite de
  path longo do Windows), no PATH do usuário. Config em `~/.oci/config`
  (fingerprint `dd:ab:e8:ac:8c:a2:94:16:9f:02:89:b5:38:c0:f7:bf`)
- **Na VM `nia-emaus-e2`:** instalada em `~/ocicli-venv` (venv Python), chave própria
  (ver acima)
- User OCID, Tenancy OCID e demais IDs (subnet, imagem Ubuntu 24.04 aarch64) já
  levantados e documentados nesta sessão — não precisa procurar de novo no console

---

## ✅ Deploy feito em 2026-09-14/15 — o que rolou

- **DuckDNS:** `nia-api` (VM1) e `caminho-emaus` (VM2) — IPs atualizados via API
  (token da conta salvo só na conversa, não no repo). `nia` sozinho já estava ocupado
  por outra conta.
- **Security List da VCN** (via `oci` CLI, sem console): liberado 80/443 pro mundo, e
  **8000 só pra rede privada `10.0.0.0/24`** (Emaús → backend, não exposto na internet).
- **Docker + repo clonado** nas 2 VMs, `.env` de cada uma preenchido com segredos gerados
  na hora (`openssl rand`).
- **3 fixes de dependência no `backend/requirements.txt`** — o `fastapi==0.104.1` antigo
  travava `anyio<4`, mas o `google-genai` novo exige mais recente. Corrigido em cadeia:
  `fastapi` → 0.115.6, `httpx` → 0.28.1, `pydantic` → 2.12.5. Código já usava sintaxe
  pydantic v2 atual, sem quebra.
- **Fix: `backend/static/` virou volume montado** (`./backend/static:/app/static`) em vez
  de só `COPY` no Dockerfile — sem isso, `scp` de mídia nova não tinha efeito sem rebuild
  completo da imagem.
- **VM 2 travou de verdade no primeiro build do Next.js** (1 OCPU/1GB sem swap — SSH
  parou de responder por ~20min, precisou `RESET` via `oci` CLI). Corrigido com **2GB de
  swap** (`/swapfile`) — build passou na segunda tentativa, mais lento mas estável.
- **Banco de dados migrado**: `pg_dump` do Postgres local → `scp` → `pg_restore --clean
  --if-exists` no Postgres da VM1 (sem apagar o banco, só recriando as tabelas — usuário
  preferiu essa opção a um `dropdb`).
- Usuários do Emaús semeados (`_seed_emaus_users.py`) e **cursos 8 e 9 publicados** via API.
- CORS testado e confirmado entre os dois domínios.

## ▶️ Próximos passos reais

1. Testar o fluxo completo no navegador (login, trilha, quiz) — só foi validado por `curl`
2. Backup automático do Postgres (cron + `pg_dump`, passo 9 do `DEPLOY.md`) — ainda não configurado na VM1
3. Se quiser mais margem, seguir esperando o retry do A1 (ou upgrade PAYG)
4. CI/CD: hoje não tem nada automatizado (sem `.github/workflows`, sem testes automatizados) — considerar depois

## Pendências não relacionadas ao deploy (do FASE 6, também pausadas)
- Escolha do logo v3 (16 conceitos em `/dev/marca`) — usuário decide
- Spec da página inicial do Emaús — usuário vai passar
