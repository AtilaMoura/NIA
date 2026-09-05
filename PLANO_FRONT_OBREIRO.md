# Plano — Emaús (front da plataforma de formação bíblica)

**Emaús** = plataforma de cursos de Bíblia / teologia / vida cristã, sem viés denominacional,
focada em a pessoa comum *entender* de verdade (nome de Lc 24 — Jesus "abrindo as Escrituras"
até o coração arder). Primeiro curso: "Formação Geral do Novo Obreiro Cristão" (`Course.id 8`).

**Arquitetura (decidido 2026-09-01 — opção C): projeto Next SEPARADO.**
- Pasta `emaus-web/` (irmã de `backend/` e `frontend/` no mesmo repo). `package.json` próprio,
  build/deploy próprio. **Zero código compartilhado** com `frontend/`.
- Cliente puro da API do NIA (`http://localhost:8100`) — o NIA é o control plane (dados,
  geração, aprovação); o Emaús só consome e envia (progresso).
- `frontend/` (com `/aluno`) fica **intocado** como a frente de tecnologia.
- Identidade visual fixa (pergaminho / trigo-maduro), tokens `--tm-*`.
- **Sem login por ora:** usuário fixo (`ALUNO_USER_ID` em `_lib/config.ts`) identifica o
  progresso no NIA. Auth entra numa fase futura sem refazer o resto.

**Divisão de trabalho (decidido 2026-09-01 — opção B):**
- **Claude implementa direto.** Para cada feature: escreve a spec em `docs/front-obreiro/FASE-<n>-<slug>.md`
  (contrato + registro pro usuário conferir), implementa, roda os testes (`tsc --noEmit`, `curl`,
  checagem visual quando a extensão do Chrome conectar), e mostra pro usuário validar **antes** de
  seguir pra próxima. Mantém este documento.
- OpenCode ficou fora do fluxo (o classificador do Claude Code bloqueia disparar agente autônomo
  daqui, e o opencode local só tem Groq configurado).

---

## Decisões travadas (não reabrir sem motivo)

| Tema | Decisão |
|---|---|
| Rota | ~~`/formacao/*` (segmento no app existente)~~ → **SUPERADO 2026-09-01 (opção C):** projeto Next separado `emaus-web/`, rotas **sem** prefixo (`/inicio`, `/curso/[id]`, `/topico/[id]`, …). |
| Auth (revisado 2026-09-03) | **Sem login por ora** (segue o cabeçalho, opção C): usuário fixo `ALUNO_USER_ID = 1` em `_lib/config.ts`. Auth real entra numa fase futura sem refazer o resto. (A linha "login real desde a Fase 1" abaixo ficou obsoleta.) |
| Identidade visual | Fixa: pergaminho âmbar, Fraunces (títulos) + Source Sans 3 (corpo), tokens `--tm-*` — mesmos valores dos `curso de obreiro/topico*-completo.html`. Sem sistema de "humor". |
| Modo claro/escuro | Sim, preferência real do usuário (`users/{id}`). Sem "humor". |
| Responsivo | Mobile-first de verdade, 360px → ultrawide. Toda feature entrega o responsivo, não fica pra "polish". |
| Unidade de conteúdo | **`Topico`** (Aula = `Lesson`, Tópico = `Topico`). O front é topico-aware. |
| Escopo de catálogo | Hardcoded `TEOLOGIA_COURSE_IDS = [8]` num módulo de config, até a tabela `Tenant` existir. |
| Auth | Login real (e-mail/senha, `POST /auth/login`) desde a Fase 1. Sem `MOCK_USER_ID` neste front. |
| Gamificação | **Sem** pontos/selos/streak arcade. Só progresso limpo (% e "X de Y tópicos concluídos") + vereditos do tutor. |
| Geração de conteúdo (admin) | **Fora** deste front. Continua manual (Claude + scripts). |
| Imagens do front | Geradas por uma **cópia** do script (`scripts/gerar_imagem_front.py`), assets em `frontend/public/formacao/`. `scripts/gerar_imagem_gemini.py` fica intocado pra geração dos cursos. |
| Revisão (professor) | Área própria em `/formacao/revisao/*`, Fase 5. Exige tabela `TopicoComment` nova (pequena). |

---

## Lacunas de backend (o que precisa ser criado, e em qual fase)

| Lacuna | Fase | O que fazer |
|---|---|---|
| Sem progresso por tópico (`Progress` é por módulo) | Fase 2 | Tabela `TopicoProgress` (`user_id`, `topico_id`, `status`, `concluido_em`, `time_spent_s`) + router `GET /topico-progress/?user_id=` e `PUT /topico-progress/{topico_id}` |
| `role` não tem `professor` garantido | Fase 1 | Conferir CHECK do `role`, incluir `professor`; seed de 1 aluno demo + 1 professor |
| Sem avaliação por tópico | Fase 3 | Decidir: a avaliação final já vem embutida no `render` dos slides — o front só captura "concluído" (via botão ou `postMessage` do iframe). Sem endpoint novo se der. |
| Sem tabela de comentário de revisão | Fase 5 | `TopicoComment` (`topico_id`, `user_id`, `secao_ref` opcional, `texto`, `resolvido` bool, timestamps) + CRUD |
| `modules` filtro por curso | Fase 2 | Conferir se `GET /modules/?course_id=` existe; se não, filtrar no front |
| Sem `Tenant` | — | Hardcoded por ora (ver decisões) |

---

## Sequência de implementação (fases)

Cada fase quebrada em features. OpenCode faz uma feature, Claude valida, próxima.

### FASE 0 — Fundação do segmento `/formacao`
- **F0.1 — Config + cliente de API.** `frontend/app/formacao/_lib/config.ts` (`TEOLOGIA_COURSE_IDS`, `API_URL`, `THEME_TOPICO = "trigo-maduro"`). `frontend/app/formacao/_lib/api.ts` — fetch tipado: `login`, `register`, `me`, `listCourses`, `getCourse`, `listModules`, `listLessons`, `listTopicos(lessonId?)`, `getTopico`, `topicoRenderUrl`, `getUser`, `updateUser`, `listProgress`. Tipos `Topico`, `Course`, `Module`, `Lesson`, `UserMe`.
- **F0.2 — Tema + layout do segmento.** `frontend/app/formacao/formacao.css` com os tokens `--tm-*` (claro + escuro via `[data-tm-theme]`), importado só no `frontend/app/formacao/layout.tsx`. Layout carrega Fraunces + Source Sans 3, aplica `data-tm-theme` do lado servidor (cookie ou default claro), sem flash.
- **F0.3 — Kit de componentes `_ui/`.** `frontend/app/formacao/_ui/`: `Botao`, `Card`, `Chip`, `BarraProgresso`, `Selo` (status), `Avatar`, `CabecalhoApp` (marca + navegação + avatar, responsivo), `Rodape`. Só tokens `--tm-*`, zero cor hardcoded. Mobile-first.
- **F0.4 — Página de verificação.** `frontend/app/formacao/_dev/page.tsx` (sem link no menu) — todos os componentes nos 2 modos.
- **Aceite:** `node node_modules/typescript/bin/tsc --noEmit` limpo; `/formacao/_dev` renderiza 200; trocar `data-tm-theme` muda tudo sem reload.

### FASE 1 — Autenticação real
- **F1.1 — Backend: papéis + seed.** Conferir/ajustar CHECK de `User.role` pra aceitar `professor`. Script de seed `backend/_seed_formacao_users.py`: 1 aluno (`aluno-demo@formacao.local`) + 1 professor (`professor@formacao.local`), senha simples de teste, idempotente.
- **F1.2 — Telas de entrada.** `/formacao/entrar` e `/formacao/criar-conta` — formulários (client), `POST /auth/login` / `/auth/register`, token gravado em cookie httpOnly via Route Handler (`app/formacao/_lib/session.ts` + `app/api/formacao/session/route.ts`).
- **F1.3 — Guarda de sessão.** `middleware.ts` (ou checagem no layout server) — `/formacao/*` exige token, exceto `/formacao`, `/entrar`, `/criar-conta`. `/formacao/revisao/*` exige `role` ∈ {professor, admin}. Redireciona pra `/formacao/entrar?next=...`.
- **Aceite:** logar com usuário do banco, sessão persiste entre navegações, aluno abrindo `/formacao/revisao` é barrado, `/auth/me` alimenta o avatar.

### FASE 2 — Índice do curso + navegação por tópico
- **F2.1 — Backend: `TopicoProgress`.** Modelo + `ALTER TABLE` + router (`GET /topico-progress/?user_id=`, `PUT /topico-progress/{topico_id}` com body `{user_id, status}`). Status: `nao_iniciado` | `em_andamento` | `concluido`.
- **F2.2 — Helper de árvore.** `frontend/app/formacao/_lib/arvore.ts` — monta `{ modulo → aulas → topicos }` de um curso a partir de `modules`+`lessons`+`topicos`, anexa estado de cada tópico (`concluido` / `atual` / `disponivel` / `em_preparacao` = sem `content`).
- **F2.3 — `/formacao/curso/[courseId]`.** Árvore navegável: módulos (accordion), aulas, tópicos com `Selo` de estado. Tópico disponível → link pra `/formacao/topico/[id]`. "Em preparação" desabilitado com tooltip.
- **F2.4 — `/formacao/inicio`.** Hero "continue de onde parou" (primeiro tópico não `concluido` da sequência) + `BarraProgresso` do curso + atalho pra árvore.
- **Aceite:** árvore bate com o banco (Módulo 26 → Aula 57 → T1..T5); T1/T2 abríveis, T3-T5 "em preparação"; hero aponta pro T3 quando T1/T2 concluídos.

### FASE 3 — Estudo do tópico
- **F3.1 — `/formacao/topico/[topicoId]`.** Moldura mínima (voltar ao curso, título da aula, progresso da aula) + `<iframe>` de `topicoRenderUrl(id, { theme: "trigo-maduro", userId })` ocupando o resto da tela. Ao montar: `PUT /topico-progress` → `em_andamento`.
- **F3.2 — Conclusão + avanço.** Botão "Marcar como concluído" (ou captura de `postMessage` do render quando a avaliação final é enviada — investigar o render primeiro). Ao concluir: `PUT` → `concluido`, mostra CTA "Próximo tópico" / "Voltar ao curso".
- **Aceite:** abrir T1, estudar, concluir, `/formacao/inicio` e a árvore refletem; "próximo" leva ao T2.

### FASE 4 — Progresso, Perfil, Preferências
- **F4.1 — `/formacao/progresso`.** Linha do tempo por aula/tópico: estado + veredito do tutor (`Progress.tutor_analysis.historico`) + diagnóstico + link pra rever.
- **F4.2 — `/formacao/perfil`.** Nome, e-mail, progresso geral ("X de Y tópicos", cursos em andamento). Sem pontos/selos.
- **F4.3 — `/formacao/preferencias`.** Modo claro/escuro + tamanho de fonte (`pequeno`/`médio`/`grande`), persiste em `users/{id}` (`preferred_panel_mode` reaproveitado pro claro/escuro; tamanho de fonte = coluna nova ou campo em prefs — decidir na spec).
- **Aceite:** valores batem com o banco; mudar preferência e recarregar mantém.

### FASE 5 — Área de revisão (professor)
- **F5.1 — Backend: `TopicoComment`.** Modelo + `ALTER TABLE` + CRUD (`GET /topico-comments/?topico_id=`, `POST`, `PUT /{id}` p/ editar/resolver, `DELETE`). Campo `secao_ref` (string livre, ex. "03" ou "verse-ef-4-11") opcional.
- **F5.2 — `/formacao/revisao`.** Fila: todos os tópicos dos cursos de teologia por status (`rascunho` = sem content / `em revisão` = content sem `is_approved` / `aprovado`), contador de comentários abertos, quem revisou (`reviewed_by`).
- **F5.3 — `/formacao/revisao/topico/[id]`.** Versão de leitura do tópico (render `?modo=leitura` se existir, senão o `-completo.html` equivalente / o próprio render) + painel lateral de comentários por seção, marcar resolvido, botão "Aprovar" (`PUT /topicos/{id}` `is_approved=true`, `reviewed_by`).
- **F5.4 — `/formacao/revisao/topico/[id]/comparar`.** Groq × Gemini lado a lado, lendo `curso de obreiro/conteudo_{groq,gemini}_topicoN.json` (endpoint novo `GET /topicos/{id}/geracoes` ou servir os arquivos).
- **Aceite:** professor comenta numa seção, resolve, aprova; aluno só vê tópico aprovado.

### FASE 6 — Capa pública + imagens + polish
- **F6.1 — `/formacao`.** Landing: apresentação da formação, card do(s) curso(s), CTA "Entrar" / "Criar conta". Se logado, "Continuar".
- **F6.2 — Imagens do front.** `scripts/gerar_imagem_front.py` (cópia do `gerar_imagem_gemini.py`, salva em `frontend/public/formacao/`). Hero da landing + og-image. `scripts/gerar_imagem_gemini.py` **não é tocado**.
- **F6.3 — Polish responsivo + erros + a11y.** 360px → ultrawide sem corte; estados de erro amigáveis (API fora, rate limit Groq, tópico reprovado); foco visível; `prefers-reduced-motion`; ARIA nos controles.
- **F6.4 — Metadados.** `metadata` por rota, favicon, título, `og:*`.
- **Aceite:** fluxo completo (capa → login → início → curso → tópico → concluir → progresso) no celular sem corte; a11y sem erro crítico.

---

## Processo por feature

1. Claude escreve `docs/front-obreiro/FASE-<n>-<slug>.md` (spec exata: arquivos, contratos, tokens, aceite).
2. Claude implementa a feature.
3. Claude roda `node node_modules/typescript/bin/tsc --noEmit`, sobe o dev / `curl`, confere.
4. Claude mostra pro usuário (o que mudou + como testar) e **espera validação** antes da próxima feature.
5. Marca a feature como `[OK]` aqui, com os comandos de teste usados.

## Estado

- [~] **FASE 0 — Fundação** — implementada 2026-09-01 no projeto separado `emaus-web/`
  (opção C), aguardando validação visual.
  - Arquivos: `emaus-web/app/_lib/{config,api,theme}.ts`, `emaus-web/app/globals.css`,
    `emaus-web/app/layout.tsx`, `emaus-web/app/_ui/{Botao,Card,Chip,BarraProgresso,Selo,Avatar,CabecalhoApp,Rodape}.tsx`,
    `emaus-web/app/dev/page.tsx`.
  - **Pendente: conferência visual nos 2 modos** (extensão do Chrome não conectou).
- [x] **FASE 1 — Auth** — retomada e implementada 2026-09-04. Spec/estado completo em
  `docs/front-obreiro/FASE-1-autenticacao.md`. Reaproveitou `/auth/*` que já existia no
  backend; `role` ganhou `master`/`professor`; 9 usuários seedados
  (`backend/_seed_emaus_users.py`, senha `emaus2026`); sessão via cookie httpOnly +
  `middleware.ts`; todas as páginas trocaram `ALUNO_USER_ID` fixo pela sessão real. Testado
  via curl (login/logout/gate de papel/registro/login rápido de dev), `tsc` 0 erros.
  **Pendente: conferência visual.**
- [~] **FASE 2 — Índice do curso + navegação por tópico** — implementada 2026-09-03.
  Spec: `docs/front-obreiro/FASE-2-arvore.md`.
  - Backend: model `TopicoProgress` + schema + router `GET/PUT /topico-progress/`
    (`backend/app/{models/models.py, schemas/topico_progress.py, routers/topico_progress.py, main.py}`);
    CORS liberou `localhost:4200`.
  - Front (`emaus-web/`): `_lib/api.ts` (+`listTopicoProgress`/`setTopicoProgress`), `_lib/arvore.ts`
    (`montarArvore`), `app/curso/[courseId]/{page,arvore-ui}.tsx`, `app/inicio/page.tsx`,
    `app/page.tsx` (redirect → `/inicio`).
  - Testes: `tsc --noEmit` 0 erros; `PUT/GET /topico-progress/` OK via curl; dev server em `:4200`;
    `/inicio` 200 (hero → T1), `/curso/8` 200 (Módulo 26 → Aula 57 → T1–T3 abríveis, T4–T5 "em preparação"),
    `/curso/6` → 404 (fora de `TEOLOGIA_COURSE_IDS`), `/` → 307 → `/inicio`. Marcar T1–T3
    concluídos via curl → `/inicio` vira "Você está em dia" (60%). Nada em `frontend/` tocado.
  - **Pendente: conferência visual.**
- [~] **FASE 3 — Estudo do tópico** — implementada junto com a FASE 2 (2026-09-03).
  Spec: `docs/front-obreiro/FASE-3-estudo-topico.md`.
  - `emaus-web/app/topico/[topicoId]/{page,topico-ui}.tsx`: moldura mínima + `<iframe>` do
    render (`trigo-maduro`), `PUT em_andamento` ao abrir, botão "Marcar como concluído" +
    CTA "Próximo tópico".
  - Testes: `/topico/1` 200 (iframe `…/topicos/1/render?user_id=1&theme=trigo-maduro`);
    `/topico/4` → tela "em preparação" (sem iframe). **Pendente: conferência visual + testar o
    botão de concluir no navegador.**
- [~] **Extra (2026-09-03) — Catálogo público + landing** (adiantado da FASE 6, a pedido do usuário).
  Spec: `docs/front-obreiro/FASE-2b-catalogo.md`.
  - `emaus-web/app/_lib/catalogo.ts` — 12 cursos **hardcoded** (1 real = `courseId 8`, 11 "em breve"
    com cadeado). Decisão: não criar rows fake na tabela `courses` do NIA (compartilhada).
  - `_lib/capas.ts` (checa `/public/capas/{slug}.jpg`), `_ui/CapaCurso.tsx` (degradê por tom
    enquanto não há imagem), `app/page.tsx` reescrito como landing (hero + grade de cards).
    `/` deixou de redirecionar; `/inicio` continua sendo o painel.
  - Toggle de tema (☾/☀) adicionado ao `CabecalhoApp` (`_ui/AlternarTema.tsx`) — provisório
    até `/preferencias` (FASE 4).
  - **Imagens de capa: pendente.** Prompts prontos em `scripts/capas_emaus.json` (estilo
    aquarela+tinta / pergaminho). Gerar com `python scripts/gerar_imagem_gemini.py
    scripts/capas_emaus.json` → saem em `imagem/capas/emaus/v1/*.png` → copiar pra
    `emaus-web/public/capas/{slug}.jpg`.
  - Bug corrigido: botão "Tela cheia" (`⛶`) do render não funcionava dentro do `<iframe>` —
    faltava `allow="fullscreen"` em `app/topico/[topicoId]/page.tsx`.
- [~] **FASE 4 — Progresso / Perfil / Preferências (+ Tutor por tópico)** — implementada 2026-09-04.
  Spec: `docs/front-obreiro/FASE-4-progresso-perfil-preferencias.md`. Auth (FASE 1) segue adiada
  (usuário avisa quando fazer).
  - Backend: `TopicoProgress` += `tutor_veredito`/`tutor_analise`/`avaliado_em`; `User` +=
    `preferred_font_size` (CHECK sm/md/lg). `main.py` ganhou `_ensure_colunas_extras()` (ALTER
    TABLE ADD COLUMN IF NOT EXISTS no startup — `create_all` não altera tabela existente).
    Novo endpoint `POST /pipeline/topicos/{id}/avaliar` (Tutor por tópico, perfil via
    `_PERFIL_POR_CURSO={8:"obreiro"}`, grava em `TopicoProgress`, **sem** gamificação, sem tocar
    `Progress`; 503 amigável em rate-limit). `topico.html.j2`: `postMessage({tipo:"emaus:resumo"})`
    no fim de `buildSummary()`.
  - Front (`emaus-web/`): `_lib/api.ts` (tipos `AvaliacaoTutor`/`Progress`/`FontSize`,
    `avaliarTopico`, `listProgress` tipado), `_lib/arvore.ts` (datas + `tutor_veredito` por tópico,
    `linhaDoTempo`, `resumo.tempoTotalMin`). Páginas novas: `app/progresso/page.tsx`,
    `app/perfil/{page,perfil-ui}.tsx`, `app/preferencias/{page,preferencias-ui}.tsx`.
    `app/topico/[topicoId]/topico-ui.tsx` reescrito (painel do Tutor + fallback textarea).
    `_ui/MenuUsuario.tsx` novo (menu no avatar: Perfil/Progresso/Preferências), `CabecalhoApp` e
    `Avatar` (tamanho `lg`) ajustados.
  - Testes (2026-09-04, backend no ar): `tsc --noEmit` 0 erros; migration verificada
    (`\d topico_progress`, `users.preferred_font_size` + constraint); `POST
    /pipeline/topicos/{2,3}/avaliar` OK (reforço mantém `em_andamento`; dominado → `concluido`
    + `concluido_em`, idempotente); `PUT /users/1` persiste font/mode; rotas `/`, `/inicio`,
    `/curso/8`, `/progresso`, `/perfil`, `/preferencias`, `/topico/1` → 200 sem erro no log.
    Dados de teste do tutor resetados. **Pendente só: conferência visual + clicar o fluxo do
    painel do Tutor no navegador.**
- [x] **FASE 5a — Revisão (professor), slide-a-slide + checklist** — implementada e testada
  2026-09-04. Spec: `docs/front-obreiro/FASE-5-revisao.md`. Backend: `TopicoComment`/
  `TopicoChecklist` novos + `routers/revisao.py` (exige login `master`/`admin`/`professor`,
  1 aprovação já libera `Topico.is_approved` nesta fase). `topico.html.j2` ganhou
  `postMessage` de slide. Front: `/revisao` (fila), `/revisao/topico/[id]` (painel de
  anotação por slide + checklist), `/revisao/alunos` + `/revisao/aluno/[userId]`
  (progresso, leitura). Testado ao vivo (guarda de papel, criar/resolver comentário,
  aprovar/reprovar mudando `is_approved` de verdade). `tsc` 0 erros.
  **Cortado desta rodada:** comparar Groq×Gemini (precisa de mudança no
  `docker-compose.yml`, baixo valor — registrado na spec).
- [x] **FASE 5b — Governança/publicação** — implementada e testada 2026-09-04. `Course` +=
  `aprovacao_master_basta`/`aprovacao_exige_todos_tutores`; tabelas novas `CourseTutor`/
  `CourseAprovacao`; `routers/governanca.py` (config, aprovar, publicar/despublicar com regra
  de quórum). Front: `/revisao/curso/[courseId]` (publicar + config de tutores/regras +
  aprovação individual). Testado ao vivo o cenário completo (quórum "todos os tutores",
  bloqueios de papel, master publica sozinho, despublicar só master). Usuário optou por manter
  os placeholders Admin/Professor por ora.
- [x] **Gate de publicação** (2026-09-05) — `Course.status` controla o acesso do aluno:
  `/curso/[id]`, `/topico/[id]`, `/inicio` só liberam se `published`; revisor sempre passa e
  vê "prévia". Landing mostra cadeado "Em revisão" nos cursos não publicados. Cursos 8 e 9
  publicados antes de ligar. Testado (despublicar/republicar).
- [ ] FASE 6 — Capa + imagens + polish (parte da capa/landing já adiantada acima)

Dev server do emaus-web: `cd emaus-web && npx next dev -p 4200`. Backend NIA: Docker `nia_backend` em `:8100`.
Nada commitado até o usuário pedir.

---

## Registro da sessão 2026-09-03

**Arquivos criados/alterados:**
- Backend: `backend/app/models/models.py` (+`TopicoProgress`, +import `UniqueConstraint`),
  `backend/app/main.py` (+router, +CORS `:4200`), `backend/app/schemas/topico_progress.py` (novo),
  `backend/app/routers/topico_progress.py` (novo).
- emaus-web (novos): `app/_lib/{arvore,catalogo,capas}.ts`, `app/_ui/{CapaCurso,AlternarTema}.tsx`,
  `app/curso/[courseId]/{page,arvore-ui}.tsx`, `app/inicio/page.tsx`,
  `app/topico/[topicoId]/{page,topico-ui}.tsx`.
- emaus-web (alterados): `app/_lib/api.ts` (+topico-progress), `app/_ui/CabecalhoApp.tsx` (+toggle),
  `app/page.tsx` (redirect → landing).
- Scripts/docs: `scripts/capas_emaus.json` (novo), `docs/front-obreiro/FASE-{2-arvore,3-estudo-topico,2b-catalogo}.md` (novos).

**Comandos de teste:**
- `cd emaus-web && node node_modules/typescript/bin/tsc --noEmit` → 0 erros.
- Backend (Docker `nia_backend`, `--reload`): `docker restart nia_backend`;
  `curl -X PUT localhost:8100/topico-progress/1 -d '{"user_id":1,"status":"concluido"}'` +
  `GET /topico-progress/?user_id=1`.
- `npx next dev -p 4200` + `curl` em `/`, `/inicio`, `/curso/8`, `/curso/6` (404), `/topico/1`, `/topico/4`, `/dev` → todos 200 (`/` = 307→landing… na verdade agora 200, landing).

**Decisões arquiteturais:**
- Progresso por tópico = tabela nova `TopicoProgress` (o `Progress` existente é por módulo).
  Só upsert, nunca deleta; `concluido_em` não é limpo ao voltar status (histórico).
- Login adiado — usuário fixo `ALUNO_USER_ID = 1` (segue o cabeçalho do plano / opção C).
- Catálogo hardcoded no emaus-web, não no banco NIA (evita vazar cursos fake pro front tech).
- Capas: script do Gemini web (não a API), estilo aquarela+tinta/pergaminho.
- Toggle de tema no cabeçalho é provisório (o definitivo é a tela `/preferencias`, FASE 4).

**Pendências abertas:** gerar as 12 capas (passo do usuário); conferência visual (extensão
Chrome não conecta); T4-T5 do curso 8 e as outras 20 aulas sem conteúdo.

### Rodada 2 (mesma sessão) — identidade + polish + imagens "fechar o visual"

Detalhes em `docs/front-obreiro/FASE-2b-catalogo.md` (seções "Rodada 2" / "Marca" / "Capas").
- Logo `_ui/Logo.tsx` (livro + brasa). Marca **B** gerada pelo script + fundo recortado por
  saturação (`scripts/preparar_imagens_emaus.py marca`) → `public/marca/emaus-simbolo.png`
  transparente; `MARCA_ILUSTRADA_PRONTA = true`. Favicon `app/icon.svg` (fica SVG).
- **12 capas** geradas (`scripts/capas_emaus.json`) + processadas (`preparar_imagens_emaus.py
  capas`) → `public/capas/*.jpg`. Estilo aquarela+tinta coerente com o logo.
- Landing reescrita (hero + 3 pilares + rodapé Lc 24.32), `globals.css` (`.grao`, selection,
  scrollbar), `app/{not-found,error,loading}.tsx`, metadata por rota (`generateMetadata`).
- Arquivos novos: `_ui/{Logo,CapaCurso,AlternarTema}.tsx`, `app/icon.svg`,
  `app/{not-found,error,loading}.tsx`, `scripts/{capas_emaus,marca_emaus,preparar_imagens_emaus}.{json,py}`.
  Originais das imagens em `imagem/{marca,capas}/emaus/v1/`.
- `tsc --noEmit` → 0 erros; todas as rotas 200, 12 capas servidas. Bug menor:
  `/curso/{fora do catálogo}` → "não encontrado" mas HTTP 200 (quirk `notFound()` dev Next 16).
- Dev server `:4200` caiu 1x (exit 139) durante a sessão — reiniciado, é flaky.
