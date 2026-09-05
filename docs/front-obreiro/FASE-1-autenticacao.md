# FASE 1 — Autenticação (implementada 2026-09-04, junto com a FASE 5 sendo desenhada)

O backend já tinha `/auth/register`, `/auth/login`, `/auth/me` prontos (JWT bearer,
`get_current_user`) — nunca tinham sido ligados no Emaús. Esta fase só liga isso.

## Backend
- `User.role` CHECK ganha `master` / `professor` (além de `aluno`/`admin`) — nada no código
  valida `role` hoje, extensão seguro. `main._ensure_colunas_extras()` faz
  `DROP CONSTRAINT`/`ADD CONSTRAINT` idempotente.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 60 → 60*24*30 (30 dias) — pra não exigir relogin toda hora
  em dev. Compartilhado com `frontend/` (pausado), risco baixo.
- `backend/_seed_emaus_users.py` — idempotente, roda com `docker exec nia_backend python
  _seed_emaus_users.py`. Cria 9 usuários (senha igual pra todos: `emaus2026`):
  - `master@emaus.local` — role `master` (id 2 no banco atual)
  - `admin{1,2,3}@emaus.local` — role `admin`
  - `professor{1..5}@emaus.local` — role `professor`

## Front (`emaus-web/`)
- `_lib/sessao.ts` — `getSessao()` (server-only) lê o cookie `emaus_token` httpOnly, chama
  `GET /auth/me` com Bearer, devolve `{id,name,email,role}` ou `null`.
- `app/api/sessao/route.ts` — `POST` (login: chama `/auth/login`+`/auth/me`, grava
  `emaus_token` + `emaus_role`, ambos httpOnly) e `DELETE` (logout, limpa os 2 cookies).
- `app/api/sessao/dev/route.ts` — login rápido só em dev (`NODE_ENV !== "production"` →
  404 em prod). Credenciais de teste ficam só no servidor, nunca no bundle do cliente.
- `app/api/registrar/route.ts` — `POST` cria conta (`/auth/register`) e já loga.
- `middleware.ts` (raiz do projeto) — exige `emaus_token` em tudo menos `/`, `/entrar`,
  `/criar-conta`; `/revisao/*` exige `emaus_role ∈ {master,admin,professor}` (lê o cookie
  puro, não decodifica o JWT — mais barato no Edge; a validação de verdade é o backend).
- `/entrar` + `/criar-conta` — formulários + botões de "login rápido (dev)".
- `MenuUsuario` ganhou "Sair".
- Todas as páginas que usavam `ALUNO_USER_ID` fixo (`/inicio`, `/curso/[id]`, `/topico/[id]`
  + `topico-ui.tsx`, `/progresso`, `/perfil` + `perfil-ui.tsx`, `/preferencias` +
  `preferencias-ui.tsx`) passaram a usar `getSessao().id` (redirect pra `/entrar?next=...`
  se não tiver sessão). `montarArvore(courseId, userId?)` ganhou o parâmetro, default
  `ALUNO_USER_ID` só como fallback (não é mais importado direto nas páginas).
- Landing (`/`) fica pública, mostra "Entrar" ou o menu do usuário conforme sessão.

## Testes (via curl com cookie jar, backend + dev server no ar)
- `/` 200 sem cookie; `/inicio` e `/revisao` → 307 pra `/entrar?next=...` sem cookie.
- Login (`master@emaus.local`) grava cookies httpOnly; `/inicio` 200 com cookie.
- Gate de papel: cookie `emaus_role=aluno` em `/revisao` → 307 pra `/inicio` (barrado).
- Logout limpa os cookies; `/inicio` volta a redirecionar.
- Login rápido de dev (`POST /api/sessao/dev {perfil:"professor1"}`) loga de verdade;
  `/perfil` reflete nome/e-mail do professor.
- `/curso/8`, `/topico/1`, `/progresso`, `/preferencias`, `/perfil`, `/criar-conta` → 200
  com sessão. `/topico/1` usa `user_id` da sessão real na URL do render (conferido: `user_id=6`
  pro professor1, não mais fixo em 1).
- Registro de conta nova (`POST /api/registrar`) cria usuário `role=aluno` e já loga.
- `tsc --noEmit` 0 erros. Nenhum erro no log do `next dev`.

## Correção de segurança (2026-09-04, mesma sessão — achado real, testado ao vivo)

O usuário perguntou "dá pra alguém mudar o nível de acesso mexendo na requisição?". Testei:
sim, dava. 3 problemas reais no backend (que nunca teve autorização — foi construído antes
do login existir):

1. **Escalação de privilégio sem token.** `PUT /users/{id}` aceitava qualquer campo,
   inclusive `role`, sem exigir login — qualquer requisição virava `master`. Confirmado ao
   vivo em `users/1` e revertido.
2. **Vazamento do hash de senha.** `GET /users/{id}` devolvia `password_hash` (bcrypt) sem
   login.
3. **Falsificação de identidade.** `PUT /topico-progress/{id}` e
   `POST /pipeline/topicos/{id}/avaliar` confiavam no `user_id` do **corpo** da requisição,
   não no token — dava pra agir "como" outra pessoa.

**Correção:**
- `routers/users.py`: `_sem_senha()` tira `password_hash` de toda resposta. `PUT`/`POST`/
  `DELETE` exigem `Depends(get_current_user)`; só o próprio dono ou `master`/`admin` editam;
  só `master` muda o campo `role` de alguém (nem admin se autopromove); `POST` rejeita
  `password_hash` cru.
- `routers/topico_progress.py` (`PUT`) e `routers/pipeline.py`
  (`POST /topicos/{id}/avaliar`): exigem login e verificam `data.user_id ==
  current_user.id` — 403 se não bater.
- **GET seguem abertos** (leitura de nome/e-mail/progresso sem login) — gap conhecido e
  documentado, não é o que foi perguntado (a questão era sobre alterar/escalar acesso).
  Fechar isso exige propagar o Bearer em toda leitura também (`_lib/api.ts` inteiro) — fica
  registrado como próximo passo, não bloqueia nada hoje.

**Front — os writes de Client Component agora passam por proxy autenticado** (o token é
`httpOnly`, um Client Component não tem como anexar `Authorization` sozinho):
- Novo: `app/api/{perfil,preferencias,topico-progress,tutor}/route.ts` — cada um lê o
  cookie no servidor, confirma a sessão via `/auth/me`, e só then chama o NIA com Bearer. O
  `user_id`/dono da ação **nunca** vem do corpo mandado pelo navegador — é sempre
  `getSessao()`. `/api/preferencias` tem allowlist estrita de campos (nunca repassa o body
  inteiro).
- `_lib/api.ts`: `updateUser`/`setTopicoProgress`/`avaliarTopico` (chamavam o NIA direto)
  saíram; entraram `salvarPerfil`, `salvarPreferencia`, `marcarProgresso`,
  `enviarAvaliacaoTutor` (chamam os proxies acima, sem precisar de `userId` como parâmetro).
- `perfil-ui.tsx`, `preferencias-ui.tsx`, `topico-ui.tsx` atualizados; `userId` como prop
  sumiu de `EditarNome`, `Preferencias` e `AcoesTopico` — não é mais necessário.

**Testado ao vivo (antes e depois da correção):** escalação sem token → 401; hash não vaza
mais; progresso "como outra pessoa" → 403; master edita o próprio nome → 200; professor
tenta virar master → 403; professor tenta editar outro perfil → 403; professor marca o
próprio progresso → 200; `user_id` mandado no corpo do proxy é ignorado (sempre usa o da
sessão, conferido no banco). Todas as 7 rotas do front → 200, `tsc` 0 erros.

## Estado
- [x] Implementada, testada (funcional + segurança) via curl. **Pendente: conferência
  visual no navegador** (extensão Claude-in-Chrome nunca conectou nesta máquina).
