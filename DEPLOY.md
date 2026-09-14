# Deploy — NIA + Emaús na Oracle Cloud (Always Free)

Duas topologias possíveis, mesmo código:

**A) Duas VMs pequenas (`E2.1.Micro`, 1GB cada)** — o que estamos usando agora,
porque o `A1.Flex` (maior) está sem capacidade disponível em São Paulo:

```
VM 1 (backend)                          VM 2 (Emaús)
Internet ─▶ Caddy (80/443)              Internet ─▶ Caddy (80/443)
              └─ api.SEU-DOMINIO ─▶ backend           └─ emaus.SEU-DOMINIO ─▶ emaus
            backend ─▶ db (Postgres)                emaus ─▶ backend (IP PRIVADO da VCN)
```
Arquivos: `docker-compose.backend.yml` + `Caddyfile.backend` + `.env.backend.example`
(VM 1) e `docker-compose.emaus.yml` + `Caddyfile.emaus` + `.env.emaus.example` (VM 2).

**B) Uma VM só (`A1.Flex`, 2 OCPU/12GB+)** — quando a capacidade liberar, dá pra
consolidar tudo numa VM só, mais simples de manter:

```
Internet ─▶ Caddy (80/443, HTTPS automático)
              ├─ api.SEU-DOMINIO   ─▶ backend  (FastAPI)
              ├─ emaus.SEU-DOMINIO ─▶ emaus    (Next 16)
              └─ nia.SEU-DOMINIO   ─▶ frontend (Next, front "tech" — opcional)
            backend ─▶ db (Postgres, volume persistente)
```
Arquivos: `docker-compose.prod.yml` + `Caddyfile` + `.env.prod.example`.

Em ambas: `*/Dockerfile.prod` fazem o build de cada serviço. O `.env` real fica
**só na VM**, nunca no git. Este guia documenta a topologia **A** (2 VMs) — pra
topologia B é o mesmo passo a passo trocando os nomes dos arquivos e usando só
uma VM.

---

## 0. Antes de começar (na sua máquina)

```bash
git push                      # manda os commits pendentes pro GitHub
```

Se o repo `AtilaMoura/NIA` for **privado**, você vai precisar de um jeito da VM
clonar — ver "Repo privado" no fim.

---

## 1. Criar as VMs no console da Oracle (ou via `oci` CLI)

Console ▸ menu ▸ **Compute ▸ Instances ▸ Create instance** — repita pras 2 VMs.

| Campo | VM 1 (backend) | VM 2 (Emaús) |
|---|---|---|
| Name | `nia-backend` | `nia-emaus` |
| Compartment | `atilagmoura (root)` | idem |
| Image | Canonical Ubuntu 24.04 (Minimal) | idem |
| Shape | `VM.Standard.E2.1.Micro` (grátis, sempre disponível) — ou `A1.Flex` se tiver capacidade | idem |
| SSH keys | **Generate a key pair** e **baixe a chave privada** (pode ser a mesma nas 2 VMs) | idem |
| Networking | mesma VCN/subnet nas duas (pra falarem por IP privado) | idem |

**Create.** Anota o **IP público e o IP privado** de cada uma quando ficarem `Running`.

> **Valores desta implantação (2026-09):** VM 1 `163.176.70.148` (privado `10.0.0.28`),
> VM 2 `137.131.152.20` (privado `10.0.0.5`), subnet `10.0.0.0/24`.

> **"Out of capacity"** no `A1.Flex` em São Paulo é comum e pode levar dias pra
> liberar — **não é bloqueio pra subir o sistema**: as `E2.1.Micro` sustentam
> a carga atual (ver análise em `DEPLOY_STATUS.md`). Automatizamos um retry
> (`~/retry_a1.sh` + cron na própria VM 2) que fica tentando sozinho; quando
> conseguir, dá pra migrar/consolidar depois.

---

## 2. Abrir as portas — 80/443 (as 2 VMs) e 8000 privada (só a VM 1)

São **dois** firewalls: o da rede (Oracle) e o da VM (Ubuntu). Faça nas duas VMs.

### 2a. Security List da VCN (console) — uma vez só, vale pra subnet inteira
Networking ▸ Virtual Cloud Networks ▸ sua VCN ▸ Subnet ▸ **Default Security List**
▸ **Add Ingress Rules**:

| Source CIDR | IP Protocol | Destination Port | Pra quê |
|---|---|---|---|
| `0.0.0.0/0` | TCP | `80` | HTTP (challenge do Let's Encrypt + redirect) |
| `0.0.0.0/0` | TCP | `443` | HTTPS |
| `10.0.0.0/24` | TCP | `8000` | Emaús (VM 2) chamar a API do backend (VM 1) **por dentro da rede** — não abre pra internet |

(A porta 22 já vem liberada.)

### 2b. Firewall de cada VM (via SSH, depois de entrar — passo 3)
As imagens Ubuntu da Oracle bloqueiam tudo menos SSH no `iptables`:

```bash
# nas 2 VMs
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80  -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

```bash
# só na VM 1 (backend) — libera a 8000 só pra rede privada da subnet
sudo iptables -I INPUT 6 -s 10.0.0.0/24 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo netfilter-persistent save
```

---

## 3. Entrar em cada VM e instalar o Docker

Repita nas **2 VMs**:

```bash
# na sua máquina — ajuste o caminho da chave e o IP
ssh -i ~/caminho/ssh-key-nia.key ubuntu@SEU_IP_PUBLICO
```

Dentro da VM:

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
newgrp docker            # ativa o grupo sem deslogar
docker compose version   # confirma que o plugin veio junto
```

(faça agora o passo **2b** do firewall)

---

## 4. Domínio grátis com DuckDNS

Sem domínio o Caddy não consegue certificado. O **DuckDNS** resolve isso de graça:

1. https://www.duckdns.org ▸ entra com Google/GitHub
2. Cria 2 domínios (ex.): `atila-api`, `atila-emaus` (+ `atila-nia` se for usar o front tech)
3. Em cada um, põe o **IP público da VM correspondente** no campo `current ip` ▸ **update ip**
   — `atila-api` aponta pro IP da **VM 1**, `atila-emaus` pro IP da **VM 2**.

Ficam: `atila-api.duckdns.org` (VM 1), `atila-emaus.duckdns.org` (VM 2).

> Quando quiser um domínio de verdade (`.com.br` ~R$40/ano), é só trocar os valores
> no `.env` e `up -d --build`.

---

## 5. Clonar o repo e preencher o `.env` (em cada VM)

### VM 1 (backend)

```bash
cd ~
git clone https://github.com/AtilaMoura/NIA.git
cd NIA

cp .env.backend.example .env
nano .env
```

Preencha:

```ini
POSTGRES_PASSWORD=<openssl rand -base64 24>
SECRET_KEY=<openssl rand -hex 32>
CORS_ORIGINS=https://atila-emaus.duckdns.org
GEMINI_API_KEY=<sua chave, ou vazio>
GROQ_API_KEY=<sua chave, ou vazio>
OPENAI_API_KEY=<sua chave, ou vazio>
SITE_API=atila-api.duckdns.org
SITE_NIA=
ACME_EMAIL=atilagmoura@gmail.com
```

Gere os segredos direto na VM:

```bash
echo "POSTGRES_PASSWORD=$(openssl rand -base64 24)"
echo "SECRET_KEY=$(openssl rand -hex 32)"
```

> **Vai usar o front "tech" nesta VM também?** Descomente o serviço `frontend`
> no `docker-compose.backend.yml`, preencha `SITE_NIA` e `NEXT_PUBLIC_API_URL`
> no `.env`, e acrescente o domínio do front tech no `CORS_ORIGINS`.

### VM 2 (Emaús)

```bash
cd ~
git clone https://github.com/AtilaMoura/NIA.git
cd NIA

cp .env.emaus.example .env
nano .env
```

Preencha (troque `10.0.0.28` pelo **IP privado real da VM 1**, se for diferente):

```ini
NEXT_PUBLIC_API_URL=https://atila-api.duckdns.org
API_URL_INTERNAL=http://10.0.0.28:8000
SITE_EMAUS=atila-emaus.duckdns.org
ACME_EMAIL=atilagmoura@gmail.com
```

---

## 6. Subir

### VM 1 (backend)

```bash
docker compose -f docker-compose.backend.yml up -d --build
docker compose -f docker-compose.backend.yml ps
docker compose -f docker-compose.backend.yml logs -f caddy      # veja o cert sair
docker compose -f docker-compose.backend.yml logs -f backend
```

Teste:

```bash
curl -I https://atila-api.duckdns.org/          # 200, JSON {"status":"online"}
curl -I http://10.0.0.28:8000/                  # de dentro da VM 2, testa o caminho privado
```

### Copiar as imagens/áudios (`backend/static/`) pra VM 1

Esses arquivos **não estão no git** (o repo fica enxuto de propósito — ver
`DEPLOY_STATUS.md`). Copie direto da sua máquina pra VM 1 depois do primeiro
`up -d --build` (a pasta `static/` é montada de dentro do container, então
o comando de baixo já resolve; refaça sempre que adicionar mídia nova):

```bash
# na sua máquina
scp -i ssh-key-2026-09-07now.key -r backend/static/* ubuntu@163.176.70.148:~/NIA/backend/static/
# na VM 1, aplica sem rebuildar a imagem inteira
ssh -i ssh-key-2026-09-07now.key ubuntu@163.176.70.148 \
  "cd ~/NIA && docker compose -f docker-compose.backend.yml restart backend"
```

### VM 2 (Emaús)

```bash
docker compose -f docker-compose.emaus.yml up -d --build
docker compose -f docker-compose.emaus.yml ps
docker compose -f docker-compose.emaus.yml logs -f caddy
docker compose -f docker-compose.emaus.yml logs -f emaus
```

Abra `https://atila-emaus.duckdns.org` no navegador.

---

## 7. Popular usuários e publicar cursos

Roda **na VM 1** (é lá que fica o backend/banco):

```bash
# perfis do Emaús (master / admin1-3 / professor1-5, senha emaus2026)
docker compose -f docker-compose.backend.yml exec backend python _seed_emaus_users.py
```

Publicar os cursos (o gate de publicação bloqueia o aluno até `status=published`).
Logue como master e use a tela de governança (`/revisao/curso/{id}`), **ou** via API:

```bash
# pega o token do master
TOKEN=$(curl -s -X POST https://atila-api.duckdns.org/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"master@emaus.local","password":"emaus2026"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

# publica os cursos que existem (ajuste os ids)
for id in 8 9; do
  curl -s -X POST https://atila-api.duckdns.org/cursos/$id/publicar \
    -H "Authorization: Bearer $TOKEN"
done
```

> O conteúdo dos cursos **não** é gerado no servidor — ele já está no banco/repo.
> A geração de curso e de imagem continua rodando na sua máquina.

---

## 8. Atualizações (deploy novo)

Em cada VM (troque o nome do compose conforme a VM):

```bash
cd ~/NIA
git pull
docker compose -f docker-compose.backend.yml up -d --build   # VM 1
# ou: docker compose -f docker-compose.emaus.yml up -d --build   # VM 2
docker image prune -f
```

Mudou `NEXT_PUBLIC_API_URL` ou qualquer coisa de front? O `--build` já rebuilda
— e precisa rebuildar **as duas VMs** se a URL da API mudou (está embutida no
bundle de cada front em build time).

---

## 9. Backup do banco

Roda **na VM 1** (é lá que fica o Postgres). Manual:

```bash
docker compose -f docker-compose.backend.yml exec -T db \
  pg_dump -U niauser niadb | gzip > ~/backup-niadb-$(date +%F).sql.gz
```

Diário via cron (`crontab -e`):

```
0 3 * * * cd ~/NIA && docker compose -f docker-compose.backend.yml exec -T db pg_dump -U niauser niadb | gzip > ~/backups/niadb-$(date +\%F).sql.gz && find ~/backups -name 'niadb-*' -mtime +14 -delete
```

Restaurar:

```bash
gunzip -c ~/backups/niadb-2026-09-06.sql.gz | \
  docker compose -f docker-compose.backend.yml exec -T db psql -U niauser -d niadb
```

---

## Problemas comuns

| Sintoma | Causa / solução |
|---|---|
| `curl` externo trava, SSH funciona | Falta o passo **2** (Security List **e** `iptables` da VM). |
| Caddy fica tentando cert e falha | O subdomínio DuckDNS não aponta pro IP certo, ou a porta 80 não está aberta pro mundo. `dig atila-api.duckdns.org`. |
| `Ampere ... out of capacity` na criação | Repetir; tentar outro AD; tentar em horário diferente. |
| Front carrega mas API dá erro de CORS | `CORS_ORIGINS` no `.env` precisa bater **exatamente** com o domínio do front (com `https://`, sem barra final). Depois `up -d`. |
| Login não persiste | Cookie do Emaús é `Secure` — só funciona em HTTPS. Confirme que abriu por `https://`. |
| Build do Next fica sem memória | Raro com 12 GB. Se acontecer, buildar um serviço por vez: `up -d --build backend`, depois `emaus`, depois `frontend`. |

### Repo privado

Na VM, gere uma chave só-leitura e cadastre como **Deploy Key** no GitHub:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/nia_deploy -N ""
cat ~/.ssh/nia_deploy.pub
# GitHub ▸ repo NIA ▸ Settings ▸ Deploy keys ▸ Add ▸ cola a pública (sem write)
cat >> ~/.ssh/config <<'EOF'
Host github-nia
  HostName github.com
  User git
  IdentityFile ~/.ssh/nia_deploy
EOF
git clone git@github-nia:AtilaMoura/NIA.git
```
