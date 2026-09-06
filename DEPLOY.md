# Deploy — NIA + Emaús numa VM (Oracle Cloud Always Free)

Sobe tudo numa VM só com Docker Compose:

```
Internet ─▶ Caddy (80/443, HTTPS automático)
              ├─ api.SEU-DOMINIO   ─▶ backend  (FastAPI)
              ├─ emaus.SEU-DOMINIO ─▶ emaus    (Next 16)
              └─ nia.SEU-DOMINIO   ─▶ frontend (Next, front "tech" — opcional)
            backend ─▶ db (Postgres, volume persistente)
```

Arquivos deste deploy: `docker-compose.prod.yml`, `Caddyfile`, `*/Dockerfile.prod`,
`.env.prod.example`. O `.env` real fica **só na VM**, nunca no git.

---

## 0. Antes de começar (na sua máquina)

```bash
git push                      # manda os commits pendentes pro GitHub
```

Se o repo `AtilaMoura/NIA` for **privado**, você vai precisar de um jeito da VM
clonar — ver "Repo privado" no fim.

---

## 1. Criar a VM no console da Oracle

Console ▸ menu ▸ **Compute ▸ Instances ▸ Create instance**

| Campo | Valor |
|---|---|
| Name | `nia-prod` |
| Compartment | `atilagmoura (root)` |
| Image | **Canonical Ubuntu 24.04** (ou 22.04) |
| Shape | **Ampere** ▸ `VM.Standard.A1.Flex` ▸ **2 OCPUs / 12 GB** |
| Boot volume | 50–100 GB (o Always Free dá 200 GB de block storage no total) |
| SSH keys | **Generate a key pair** e **baixe a chave privada** (ou cole a sua pública) |
| Networking | deixa criar uma VCN nova (`Create new virtual cloud network`), com "Assign a public IPv4 address" |

**Create.** Anota o **IP público** quando a instância ficar `Running`.

> **"Out of capacity"** no Ampere em São Paulo é comum. Se der, espere alguns
> minutos e tente de novo, ou tente outro Availability Domain. Vale insistir —
> costuma sair.

---

## 2. Abrir as portas 80 e 443

São **dois** firewalls: o da rede (Oracle) e o da VM (Ubuntu).

### 2a. Security List da VCN (console)
Networking ▸ Virtual Cloud Networks ▸ sua VCN ▸ Subnet ▸ **Default Security List**
▸ **Add Ingress Rules**, uma pra cada:

| Source CIDR | IP Protocol | Destination Port |
|---|---|---|
| `0.0.0.0/0` | TCP | `80` |
| `0.0.0.0/0` | TCP | `443` |

(A porta 22 já vem liberada.)

### 2b. Firewall da VM (via SSH, depois de entrar — passo 3)
As imagens Ubuntu da Oracle bloqueiam tudo menos SSH no `iptables`:

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80  -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
```

---

## 3. Entrar na VM e instalar o Docker

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

Sem domínio o Caddy não consegue certificado e você não roda 3 apps numa porta só.
O **DuckDNS** resolve isso de graça:

1. https://www.duckdns.org ▸ entra com Google/GitHub
2. Cria 3 domínios (ex.): `atila-api`, `atila-nia`, `atila-emaus`
3. Em cada um, põe o **IP público da VM** no campo `current ip` ▸ **update ip**

Ficam: `atila-api.duckdns.org`, `atila-emaus.duckdns.org`, `atila-nia.duckdns.org`.

> Quando quiser um domínio de verdade (`.com.br` ~R$40/ano), é só trocar os valores
> no `.env` e `up -d --build`.

---

## 5. Clonar o repo e preencher o `.env`

```bash
cd ~
git clone https://github.com/AtilaMoura/NIA.git
cd NIA

cp .env.prod.example .env
nano .env
```

Preencha:

```ini
POSTGRES_PASSWORD=<openssl rand -base64 24>
SECRET_KEY=<openssl rand -hex 32>
CORS_ORIGINS=https://atila-emaus.duckdns.org,https://atila-nia.duckdns.org
GEMINI_API_KEY=<sua chave, ou vazio>
GROQ_API_KEY=<sua chave, ou vazio>
OPENAI_API_KEY=<sua chave, ou vazio>
NEXT_PUBLIC_API_URL=https://atila-api.duckdns.org
SITE_API=atila-api.duckdns.org
SITE_NIA=atila-nia.duckdns.org
SITE_EMAUS=atila-emaus.duckdns.org
ACME_EMAIL=atilagmoura@gmail.com
```

Gere os segredos direto na VM:

```bash
echo "POSTGRES_PASSWORD=$(openssl rand -base64 24)"
echo "SECRET_KEY=$(openssl rand -hex 32)"
```

> **Não vai usar o front "tech" agora?** Comente o serviço `frontend` no
> `docker-compose.prod.yml`, o bloco `{$SITE_NIA}` no `Caddyfile`, e tire
> `atila-nia...` do `CORS_ORIGINS`.

---

## 6. Subir

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

O primeiro build leva alguns minutos (compila os dois Next na VM). Acompanhe:

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f caddy      # veja o cert sair
docker compose -f docker-compose.prod.yml logs -f backend
```

Teste:

```bash
curl -I https://atila-api.duckdns.org/          # 200, JSON {"status":"online"}
```

Abra `https://atila-emaus.duckdns.org` no navegador.

---

## 7. Popular usuários e publicar cursos

```bash
# perfis do Emaús (master / admin1-3 / professor1-5, senha emaus2026)
docker compose -f docker-compose.prod.yml exec backend python _seed_emaus_users.py
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

```bash
cd ~/NIA
git pull
docker compose -f docker-compose.prod.yml up -d --build
docker image prune -f
```

Mudou `NEXT_PUBLIC_API_URL` ou qualquer coisa de front? O `--build` já rebuilda.

---

## 9. Backup do banco

Manual:

```bash
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U niauser niadb | gzip > ~/backup-niadb-$(date +%F).sql.gz
```

Diário via cron (`crontab -e`):

```
0 3 * * * cd ~/NIA && docker compose -f docker-compose.prod.yml exec -T db pg_dump -U niauser niadb | gzip > ~/backups/niadb-$(date +\%F).sql.gz && find ~/backups -name 'niadb-*' -mtime +14 -delete
```

Restaurar:

```bash
gunzip -c ~/backups/niadb-2026-09-06.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T db psql -U niauser -d niadb
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
