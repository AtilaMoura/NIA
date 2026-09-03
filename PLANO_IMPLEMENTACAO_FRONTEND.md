# Plano de Implementação — Front-end do NIA

Objetivo: construir o front completo (aluno e admin) em cima do backend já pronto (`PLANO_IMPLEMENTACAO_ESTUDO_IA.md`, Fases 0-7 todas `[OK]`, commit `212f9c5`). Escopo fechado com o usuário em 2026-08-12: front completo dos dois lados mesmo com a venda acontecendo fora do NIA (plataforma externa tipo Hotmart/Kiwify — o NIA não processa pagamento, só organiza o conteúdo).

**Status geral: aguardando OK do usuário para começar a Fase 0.** Este documento fica pronto, nada será executado até o usuário confirmar.

Referências vivas: os dois protótipos de visual (Artifacts, interativos, aprovados nesta sessão):
- Aluno: https://claude.ai/code/artifact/69aaf62f-741b-4c88-96f9-3fd17f9547d4
- Admin: https://claude.ai/code/artifact/f4440186-2e06-4ae9-aa81-a8465c71da0d

Stack: Next.js 16 (App Router) + TypeScript + Tailwind v4, já scaffoldado em `frontend/` (só o `create-next-app` padrão até agora, nada construído).

---

## Decisões de visual já fechadas (não reabrir sem motivo)

**Sistema de "humor" de cor** — 5 paletas, cada uma pensada por família de assunto, com variante clara e escura: Musgo (Bem-estar & Natureza), Âmbar (Negócios & Carreira), Maré (Tecnologia & Dados), Framboesa (Criativo & Comunicação), Lavanda (Humanas & Idiomas). Tipografia: display geométrico humanista (`Century Gothic`/`Futura`/fallback `Segoe UI`), corpo (`Calibri`/`Segoe UI`), mono pra specs/hex (`Cascadia Code`/`Consolas`).

**Aluno**: humor + modo claro/escuro + layout do painel vira **preferência real, configurável** numa tela de preferências (não é só estética fixa). Padrão de fábrica: **Musgo, Claro, layout "Retomar"** (abre direto no curso em andamento). Os outros dois layouts prototipados (Biblioteca — sidebar + grade; Trilha — caminho vertical linear) ficam disponíveis como opção de troca.

**Admin**: padrão fixo, **não** é preferência configurável (só uma pessoa administra por enquanto). Padrão: **Maré, Claro**, tela inicial = **Fila** (lista de lições + parecer do Reviewer). A criação de curso usa o fluxo **Passo a passo** (assistente com revisão da estrutura antes de gerar conteúdo) como uma tela própria dentro do admin, não como alternativa à Fila — as duas coexistem. O layout **Mesa** (kanban) fica no backlog como visão alternativa, não bloqueia nenhuma fase.

Registrado em memória (`nia-visual-padroes`, `nia-curso-categoria-nicho`): a categorização de curso por nicho (Programação, Jardinagem etc.) é visão de longo prazo, ainda **não** entra nas fases abaixo — mas o schema não deve assumir que cada curso é uma ilha isolada, pra não precisar redesenhar depois.

---

## Fase 0 — Base do front
**Status: [ ]**

O que já existe: scaffold padrão do Next.js (`frontend/app/page.tsx` é o default do `create-next-app`), backend com `auth` (`/auth/register`, `/auth/login`) pronto.

**Construir:**
- Layout raiz (`app/layout.tsx`) com os tokens de cor/tipografia do design system (CSS vars, os 5 humores + claro/escuro).
- Cliente de API (fetch tipado contra o backend FastAPI).
- Autenticação: telas de login/registro, guarda de sessão (token), roteamento protegido por papel (`admin` vê `/admin/*`, `aluno` vê `/app/*` — nomes de rota a definir).

**Teste [OK quando]:** logar como usuário existente do banco (`user_id=1`, criado no teste real da Fase 7 do backend), sessão persistindo entre navegações, rota errada por papel redirecionando (ex: aluno tentando abrir `/admin` é barrado).

---

## Fase 1 — Design system componentizado
**Status: [~] construído em 2026-08-13 — pendente só a checagem visual final (ver abaixo)**

Depende da Fase 0 — mas a pedido explícito do usuário essa fase foi construída **antes** da Fase 0 (login fica pra depois; aqui não tem autenticação nenhuma, só o design system em si).

**Construído:**
- Tokens dos 5 humores × 2 modos direto do CSS-fonte dos dois protótipos aprovados (Artifacts), sem reinterpretar valores — em `frontend/app/globals.css` (bloco "Sistema de humor de cor do NIA"), variáveis `--nia-*` aplicadas via `[data-mood]`/`[data-theme]` na raiz.
- `ThemeProvider` em `frontend/app/components/theme/ThemeProvider.tsx` — contexto React (`mood`, `theme`, `setMood`, `setTheme`), padrão de fábrica Musgo/Claro, persiste em `localStorage` (`nia_mood`/`nia_theme` — é só local; guardar no backend fica pra Fase 4, não adiantado aqui). Já plugado no `app/layout.tsx`.
- 6 componentes em `frontend/app/components/ui/`: `Button.tsx` (variantes `accent`/`ghost`), `Badge.tsx` (`neutral`/`good`/`bad`/`info`/`new`), `ProgressBar.tsx`, `Card.tsx`, `Avatar.tsx`, `Chip.tsx`. Todos consomem só `var(--nia-*)`, nenhuma cor hardcoded.
- Página de verificação temporária em `frontend/app/dev/design-system/page.tsx` (sem link no menu) — mostra os 6 componentes com os chips de humor/modo do protótipo pra trocar ao vivo.

**Achado nessa sessão**: o `node_modules` do scaffold (`frontend/`) estava incompleto — faltavam `react`, `@types/*` e os binários (`.bin`). Corrigido com `npm install` (288 pacotes adicionados). Sem isso, `tsc` e `next dev` não rodavam.

**Comandos de teste usados:**
- `node node_modules/typescript/bin/tsc --noEmit` → 0 erros (rodar via `node .../bin/tsc` porque `npx tsc` não resolve certo nesse ambiente).
- `npm run dev` (Turbopack) → `GET /dev/design-system 200`, sem erro de compilação.

**Teste [OK quando]:** trocar `data-mood` e `data-theme` na raiz muda a cor de todos os componentes sem reload, nos 5 humores × 2 modos, sem quebrar contraste (checar visualmente os pares mais escuros). **Pendente**: a extensão Claude-in-Chrome não conectou nesta sessão, então só confirmei via `curl` que a página renderiza (200, conteúdo presente) — a checagem visual de contraste nas 10 combinações em `http://localhost:3000/dev/design-system` ainda não foi feita por ninguém. Fazer isso antes de considerar a Fase 1 de fato `[OK]`.

**Teste [OK quando]:** trocar `data-mood` e `data-theme` na raiz muda a cor de todos os componentes sem reload, nos 5 humores × 2 modos, sem quebrar contraste (checar visualmente os pares mais escuros).

---

## Fase 2 — Fluxo Admin
**Status: [ ]**

Depende das Fases 0-1. Endpoints já existentes: `POST /pipeline/cursos`, `POST /pipeline/licoes/{id}/gerar`, `GET`/`PUT` de `courses`/`modules`/`lessons`.

**Construir:**
- **Fila de aprovação** (tela inicial do admin) — lista de lições (todos os cursos, mais recentes primeiro) com status (aguardando revisão/aprovado/reprovado) e score; painel de detalhe mostrando o parecer completo do Reviewer (pontos fortes, problemas com gravidade bloqueante/leve, `Lesson.review_feedback`) e ações (aprovar manualmente, editar foco e gerar de novo).
- **Criar curso (Passo a passo)** — formulário assunto/nível/objetivo → `POST /pipeline/cursos` → tela de **revisão da estrutura/tópicos propostos** (isso cobre a pendência registrada na Fase 3 do backend, que hoje só gera e não tem tela de revisão humana) → confirmar e disparar geração lição por lição (`modo: comum|pro` escolhido por lição).

**Teste [OK quando]:** criar um curso novo pela UI, revisar a estrutura proposta, gerar pelo menos uma lição em cada modo (comum e pro), ver um caso de reprovação (estrutural ou semântica) renderizando o feedback do Reviewer corretamente na Fila, e aprovar manualmente.

---

## Fase 3 — Fluxo Aluno
**Status: [~] construído em 2026-08-13 — pendente checagem visual (mesma ressalva da Fase 1)**

Construída antes da Fase 2 e sem a Fase 0 (login), a pedido do usuário — usa `MOCK_USER_ID = 1` (usuário real de teste, `teste-fase7@nia.local`, com progresso real no curso 4) em vez de sessão.

**Construído:**
- `frontend/app/lib/api.ts` — cliente de API mínimo (só os endpoints desta fase: `courses`, `modules`, `lessons`, `progress`, `pipeline/licoes/{id}/avaliar`). Cliente completo continua sendo escopo da Fase 0.
- `frontend/app/lib/constants.ts` — `MOCK_USER_ID`.
- `frontend/app/components/shell/AppTopbar.tsx` — topbar reutilizável (marca + avatar).
- `frontend/app/aluno/page.tsx` — painel, layout "Retomar": hero "continue de onde parou" (calcula % com base em `Module.lessons_count`/`Progress.current_lesson_index`) + grade de cursos.
- `frontend/app/aluno/licoes/[lessonId]/page.tsx` + `AvaliacaoPanel.tsx` (client component) — página da lição com `<iframe>` pro `GET /lessons/{id}/render` (é HTML completo e independente, não dá pra injetar direto) e painel de avaliação (cola resumo → `POST /pipeline/licoes/{id}/avaliar` → mostra veredito).
- Estado "lição ainda não gerada" tratado (`lesson.is_approved && lesson.content`) — mostra badge "Em preparação" em vez de tentar renderizar. Testado de verdade: lição 10 (pronta) e lição 11 (não gerada, é o cenário real do curso 4 no banco) — os dois caminhos renderizam corretamente.

**Endpoint novo no backend** (fora do escopo original da fase, mas necessário — não existia nenhum jeito de listar lições): `GET /lessons/` em `backend/app/routers/lessons.py`, mesmo padrão sem filtro de `list_modules`/`list_progress`. Filtro por curso/módulo fica no lado do frontend.

**Bug real encontrado e corrigido**: `GET /lessons/{id}/render?user_id=` quebrava com 500 (`UndefinedColumn: users.role`) — o campo `role` estava em `models.py` (mudança não commitada de sessão anterior) mas nunca tinha rodado o `ALTER TABLE` no Postgres. Corrigido direto no banco local (Docker, `nia_db`):
```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'aluno';
ALTER TABLE users ADD CONSTRAINT valid_role CHECK (role IN ('aluno','admin'));
```

**Comandos de teste usados:**
- `node node_modules/typescript/bin/tsc --noEmit` → 0 erros.
- `npm run dev` (porta 3000) + backend/db já rodando via `docker compose` (containers `nia_backend`/`nia_db` já ativos, não precisou subir nada).
- `curl` em `/aluno` (200, hero + grade presentes), `/aluno/licoes/10` (200, iframe + avaliação), `/aluno/licoes/11` (200, estado "Em preparação"), e `/lessons/10/render?user_id=1` direto no backend (200 depois do fix do `role`).

**Teste [OK quando]:** aluno loga, vê o curso em andamento (`course_id=4`), abre a lição, o conteúdo renderiza dentro da moldura sem conflito visual entre os dois sistemas de tema, cola um resumo e recebe o veredito do Tutor. **Pendente**: checagem visual de verdade no navegador (fluxo completo: abrir `/aluno`, clicar continuar, ver o iframe renderizado, colar um resumo e ver o veredito) — extensão Claude-in-Chrome não conectou nesta sessão também, só validei via `curl`/HTML renderizado no servidor.

Depende das Fases 0-1.

**Construir:**
- **Painel do aluno** (layout "Retomar" como entrega inicial) — hero de "continuar de onde parou" + grade de cursos, usando `GET /lessons/temas/catalogo` e os dados de `Course`/`Progress` do usuário logado.
- **Página da lição** — embute o HTML de `GET /lessons/{id}/render?theme=...&user_id=...` dentro da moldura do app (topo, progresso, navegação com o humor do painel); o conteúdo do slide em si mantém os 4 temas já existentes (Vidro Fumê etc., sistema separado).
- **Avaliação** — tela de colar o resumo do fim da lição, `POST /pipeline/licoes/{id}/avaliar`, mostrar veredito do Tutor (dominado/reforço) e liberar avanço (`Progress.can_advance`).

**Teste [OK quando]:** aluno loga, vê o curso em andamento (`course_id=4`, já existe no banco), abre a lição, o conteúdo renderiza dentro da moldura sem conflito visual entre os dois sistemas de tema, cola um resumo e recebe o veredito do Tutor.

---

## Fase 4 — Preferências do aluno (tema como funcionalidade real)
**Status: [~] construído em 2026-08-13 — pendente checagem visual (mesma ressalva das Fases 1 e 3)**

Depende da Fase 3.

**Decisão tomada**: 3 colunas separadas em vez de JSON único (`preferred_mood`, `preferred_panel_mode`, `preferred_panel_layout`), cada uma com `CHECK` — consistente com o padrão já usado pra `role`/`Course.level`, mais simples de consultar que JSON.

**Construído:**
- `backend/app/models/models.py` — as 3 colunas + constraints; aplicado via `ALTER TABLE` manual no Postgres local (mesmo padrão da Fase 0/7). Sem endpoint novo — `GET/PUT /users/{id}` já eram genéricos.
- `frontend/app/components/theme/ThemeProvider.tsx` — trocou `localStorage` por `GET/PUT /users/{MOCK_USER_ID}` pra humor e modo (persistência real, critério de teste batido).
- `frontend/app/aluno/preferencias/page.tsx` — tela de preferências (humor/modo via `useTheme()`, layout via `PUT` direto).
- **3 layouts do painel** implementados de verdade (antes só existia Retomar): `frontend/app/aluno/_layouts/{RetomarLayout,BibliotecaLayout,TrilhaLayout}.tsx`, com a lógica de busca de dados centralizada em `frontend/app/aluno/page.tsx`, que escolhe o layout no server com base em `User.preferred_panel_layout` (sem flash de layout errado). `BibliotecaLayout` tem os links de sidebar "Explorar"/"Progresso"/"Perfil" desabilitados (cinza, `title="Em breve"`) — não existem telas atrás deles ainda (gap já registrado antes).

**Comandos de teste usados:** `tsc --noEmit` (0 erros); troquei `preferred_panel_layout` via `PUT /users/1` (curl) pros 3 valores e conferi via `curl /aluno` que cada um renderiza o markup certo (sidebar da Biblioteca, trilha vertical com estados done/current/bloqueado da Trilha); banco resetado pro padrão (Musgo/Claro/Retomar) no final do teste.

**Teste [OK quando]:** aluno muda a preferência, sai e loga de novo, o painel abre já na combinação escolhida (persistiu no banco, não só em memória local). **Pendente**: conferência visual de verdade (extensão Claude-in-Chrome não conectou nesta sessão) — só validado via `curl`/PUT direto.

**Bug real encontrado pelo usuário e corrigido**: os cards de curso não eram clicáveis em nenhum dos 3 layouts (só existia o link pequeno "Preferências" no topo) — quando a lição atual de um curso ainda não tinha sido gerada, a página ficava sem nenhuma navegação possível. Corrigido com `melhorLicaoParaAbrir()` em `frontend/app/aluno/page.tsx`: cada card linka pra lição atual se pronta, senão recua até a última lição aprovada (só fica sem link se o curso não tem nada gerado); hero ganhou um link secundário "Rever a última lição" quando a próxima está bloqueada; itens `done` da Trilha agora têm link "Rever →". Testado via `curl` nos 3 layouts.

---

## Fase 5 — Progresso
**Status: [~] construído em 2026-08-13 — pendente checagem visual (mesma ressalva das fases anteriores)**

Depende da Fase 3.

**Achado importante durante a implementação**: `Progress` é criado **por módulo**, não por curso (`backend/app/routers/pipeline.py`, `avaliar_resumo` busca por `user_id`+`module_id`) — um curso pode ter vários `Progress` conforme o aluno avança de módulo. O `/aluno/page.tsx` da Fase 3/4 assumia implicitamente 1 progress por curso; corrigido nessa fase com `progressoMaisAvancado()` (novo, em `frontend/app/aluno/_lib/progresso.ts`) que escolhe o mais avançado entre os vários. Os helpers de cálculo (`modulosDoCurso`, `percentDoCurso`, `melhorLicaoParaAbrir`, `trilhaDoCurso`) foram extraídos de `aluno/page.tsx` pra essa lib compartilhada, já que o dashboard de progresso precisa deles também.

**Construído:**
- `frontend/app/aluno/progresso/page.tsx` — agrupa por curso, junta o histórico (`tutor_analysis.historico`) de **todos** os `Progress` daquele curso, ordena por módulo/lição, mostra veredito (badge Dominado/Precisa reforçar) + diagnóstico do Tutor + link direto pra lição.
- Links "Progresso" adicionados nos topbars de Retomar/Trilha e habilitado na sidebar da Biblioteca (antes desabilitado, apontava pra lugar nenhum).

**Comandos de teste usados:** `tsc --noEmit` (0 erros); comparei direto `docker exec nia_db psql ... tutor_analysis->'historico'` com o HTML renderizado em `/aluno/progresso` — veredito e texto de diagnóstico batem exatamente.

**Teste [OK quando]:** o histórico de avaliações batendo com o que está salvo em `Progress.tutor_analysis` no banco — confirmado. **Pendente**: checagem visual (extensão Claude-in-Chrome não conectou nesta sessão).

---

## Fase 5.1 — Robustecendo o lado do aluno (pós-análise externa)
**Status: [~] construído em 2026-08-13 — pendente checagem visual (mesma ressalva das fases anteriores)**

Não estava numerada no plano original. Depois das Fases 1-5, o usuário achou o lado do aluno "cru" — usei um prompt (`PROMPT_UX_ALUNO.md`) pra levar o contexto completo do projeto pra 4 IAs externas (Gemini Pro, Gemini Flash, DeepSeek, ChatGPT) e pedir sugestão de mapa de páginas. As 4 convergiram em: falta Explorar, falta Perfil, gamificação (`total_points`/`level`/`badges`/`streak_days`) é UI que nunca foi construída. Análise completa registrada na conversa; duas decisões de arquitetura foram explicitamente confirmadas com o usuário antes de mexer:
- **Não** desmembrar os 3 layouts do painel (Retomar/Biblioteca/Trilha) em páginas separadas, apesar da crítica do ChatGPT nesse sentido — mantido como está.
- Explorar mostra **todos** os cursos do banco, sem controle de acesso (não existe conceito de matrícula hoje).

**Achado crítico que nenhuma das 4 IAs percebeu**: `User.total_points`, `level`, `streak_days` e `badges` são campos que existem no schema desde o início do projeto, mas **nenhum código em lugar nenhum escrevia neles** — gamificação nunca tinha lógica nenhuma, só coluna vazia.

**Construído:**
- `frontend/app/aluno/perfil/page.tsx` — nível/pontos/streak/badges/tópicos de interesse, tudo dado real.
- `frontend/app/aluno/explorar/page.tsx` — catálogo com todos os cursos, CTA "Começar"/"Continuar" reaproveitando `melhorLicaoParaAbrir`. Sem navegação por humor/categoria (`Course.category` não é populado por nenhum código do pipeline — ver Backlog de nicho).
- `frontend/app/aluno/progresso/page.tsx` evoluído — resumo geral (cursos em andamento, tópicos dominados) + seção "Pontos de atenção" (último veredito ≠ dominado por lição, deduplicado corretamente por ordem cronológica, não por posição).
- **Backend**: `_conceder_gamificacao()` em `backend/app/routers/pipeline.py`, chamada dentro de `POST /pipeline/licoes/{id}/avaliar` quando o veredito é "dominado" — soma 10 pontos, atualiza `streak_days` comparando `last_activity_date` (mesma data = mantém, +1 dia = incrementa, gap = reseta pra 1), recalcula `level` (`1 + total_points // 100`, capado em 100), e concede um catálogo mínimo de 4 badges objetivas (`primeira-licao-dominada`, `streak-3-dias`, `streak-7-dias`, `primeiro-curso-concluido` — este último via `_curso_ficou_completo()`, que checa se todos os módulos do curso têm `Progress` concluído, já que curso não tem status próprio).
- Navegação Explorar/Perfil ligada em todos os pontos (topbars dos 3 layouts + sidebar da Biblioteca, que antes apontava pra links desabilitados).

**Comandos de teste usados:** `tsc --noEmit` (0 erros); disparei uma avaliação real (`POST /pipeline/licoes/10/avaliar` via Groq, veredito voltou "dominado") e confirmei no Postgres que `total_points=10`, `level=1`, `streak_days=1`, `badges=["primeira-licao-dominada"]` foram gravados de verdade — não é mock. Conferido que `/aluno/perfil` e `/aluno/progresso` refletem esses valores.

**Pendente**: checagem visual (extensão Claude-in-Chrome não conectou nesta sessão). O resto das sugestões das 4 IAs (Conquistas como página própria, Revisão espaçada, Certificados, Notificações) ficou registrado como backlog — depende de catálogo de badges mais robusto ou de infraestrutura nova, não é UI simples.

**Atualização 2026-08-13 (mesma sessão)**: usuário achou o resultado "bonito mas limitado" e pediu um redesign do layout Retomar em formato fileiras (estilo streaming) — hero em destaque + linhas horizontais (Continuar/Já dominado/Todos os cursos). Processo novo adotado a partir daqui: **mockup em Artifact (HTML/CSS puro, dado mockado) primeiro, aprovação visual, só depois porta pro React** — mais rápido que iterar recompilando o Next a cada ajuste. Mockup: `https://claude.ai/code/artifact/cbcb72aa-2159-4e4c-a3e0-d76a6d2efcc6`.

**Decisões tomadas ao portar pro real:**
- Substitui o layout **Retomar** (não vira 4º layout, não substitui os 3 — Biblioteca/Trilha intactos).
- Pôster colorido por curso usa **hash determinístico do `course.id`** (`humorDoCurso()` em `_lib/progresso.ts`) — `Course.category` não existe populado no backend, então isso é provisório e comentado como tal no código. Trocar por categoria real quando o backlog de nicho for implementado.
- Nota do Reviewer (`Course.ai_quality_score`, campo real que nunca tinha virado tela) usada no chip do pôster; como os 2 cursos reais do banco têm o campo `null`, tem fallback "Revisado pela IA" sem número em vez de quebrar ou mostrar "null".

**Construído**: `globals.css` ganhou `.nia-mood-*` (tokens de humor por curso, independentes do `[data-mood]` do shell); `RetomarLayout.tsx` reescrito do zero (hero + 3 fileiras com scroll horizontal); `page.tsx` calcula `cursoDestaque` (curso "novo" com maior nota, fallback determinístico) e enriquece `HeroInfo` com módulo atual/total e último veredito do Tutor.

**Testado**: `tsc --noEmit` limpo; testei via `curl` com o curso 4 tendo passado por uma avaliação real (dominado) — o selo "Tópico anterior dominado" aparece corretamente na fileira de continuar; `cursoDestaque` escolheu certo o único curso "novo" (Agentes de IA). Pendente: conferência visual (mesma ressalva de sempre).

**Atualização 2026-08-13 (mesma sessão) — hero virou carrossel**: usuário aprovou a fileira mas pediu o destaque como carrossel (mockup atualizado no mesmo Artifact, com foto de fundo + setas + dots + autoplay). Ao portar: `cursoDestaque` (singular) virou `cursosDestaque[]` em `page.tsx` — todos os cursos "novos", ordenados por nota do Reviewer, capado em 5. Novo componente client `HeroCarousel.tsx` (`_layouts/`) se adapta ao tamanho real da lista: sem seção nenhuma se vazia, sem setas/dots se só tem 1 (é o caso hoje, só 1 curso "novo" no banco). Autoplay a cada 6s, pausa no hover, respeita `prefers-reduced-motion`.

**Decisão consciente ao portar**: o mockup usava fotos de banco de imagens (Wikimedia Commons) no hero; a versão real **não** tem foto de fundo — não existe fonte de imagem por curso no backend (nenhuma coluna, nenhum pipeline), e hotlinkar fotos de estoque pra cursos reais seria fabricar dado visual sem lastro, diferente do humor por hash (que já era assumidamente provisório e aprovado como tal). Fica só o gradiente do humor. Se quiser fotos de verdade em produção depois, precisa decidir a fonte (upload manual, geração por IA, banco de imagem) antes.

**Atualização 2026-08-13 (mesma sessão) — fotos entraram de verdade**: usuário pediu fotos sem direito autoral pra ficar mais bonito, revertendo a decisão acima. Resolvido com um **pool fixo de 5 fotos, uma por humor** (não por curso — mesma lógica provisória de `humorDoCurso()`), baixadas do Wikimedia Commons só com licença livre (domínio público / CC BY / CC BY-SA), salvas como assets estáticos reais em `frontend/public/course-images/{musgo,ambar,mare,framboesa,lavanda}.jpg` e servidas via `next/image`. Mapeamento em `IMAGEM_DO_HUMOR` (`_lib/progresso.ts`). Crédito das 5 imagens (autor + licença) no rodapé do `RetomarLayout` — CC BY/BY-SA exige atribuição. Deixado explícito no comentário do código: são fotos genéricas por humor, não fotos do conteúdo real de cada curso — se um dia existir capa de curso de verdade, troca esse mapeamento.

**Testado**: `tsc --noEmit` limpo; `curl` confirmou as 5 imagens servidas em `/course-images/*.jpg` (200) e referenciadas na página renderizada.

**Bug real encontrado pelo usuário (com print comparando mockup x real) e corrigido**: o hero real saiu com o texto quase ilegível em cima da foto — contraste bem mais fraco que o mockup. Causa: o mockup usa `--m-a2`, uma cor quase-preta *separada* por humor só pro degradê de legibilidade (ex. Musgo: `--m-a2:#1b2e1e`); ao portar, isso foi aproximado errado como `color-mix(in srgb, var(--m-a) 65%, black)` — como `--m-a` (a cor viva do humor) já é claro/saturado, escurecer ele na hora não chega nem perto do quase-preto do `--m-a2` original. Corrigido adicionando `--m-a2` de verdade nas 5 classes `.nia-mood-*` em `globals.css` (mesmos valores do mockup) e trocando os degradês em `HeroCarousel.tsx` e no pôster de `RetomarLayout.tsx` pra usar `var(--m-a2)` direto, igual ao mockup.

**Segundo bug real encontrado pelo usuário e corrigido — largura e mobile**: o container do painel tinha um teto fixo `max-w-[1180px] mx-auto`, deixando margem enorme vazia dos dois lados em tela grande ("espremido" no meio) — trocado por full-bleed com padding fluido (`max-w-[1800px]` + `px-[clamp(1rem,4vw,3rem)]`), mais parecido com o full-bleed real de streaming. `AppTopbar` não tinha nenhum tratamento pra mobile (nível/pontos/streak + 4 links + avatar todos numa linha só) — agora quebra em 2 linhas abaixo de `sm` (marca+avatar em cima, nav embaixo em largura cheia) e as estatísticas de nível/pontos/streak somem abaixo de `md` (já dá pra ver isso no Perfil). Hero também ganhou padding/fonte menores no mobile.

**Terceiro ajuste (mesmo dia) — hero desequilibrado em tela larga**: depois do fix de largura, o hero ficou achatado (`min-h-[300px]` fixo) numa seção agora bem mais larga, deixando o texto espremido numa coluna estreita à esquerda com muita foto vazia à direita. Corrigido com altura fluida (`min-h-[clamp(280px,38vw,480px)]`, cresce com a tela até um teto) e coluna de texto/fonte maiores em telas grandes (`max-w-[720px]`, título até `lg:text-[2.4rem]`). De brinde, corrigida a concordância "1 dias seguidos" → "1 dia seguido" no singular (`RetomarLayout.tsx`).

**Estado ao pausar (2026-08-13 fim de tarde)**: nada commitado ainda (git status mostra tudo modified/untracked desde o início da sessão — normal, commit só quando o usuário pedir). Servidor dev rodando em `http://localhost:3000` (deixei ligado de propósito pra retomar rápido). Pendência real em aberto: **checagem visual completa** de tudo isso — o usuário conferiu via prints pontuais (contraste do hero, largura), mas não confirmou o layout inteiro (Continuar/Já dominado/Todos os cursos, os 3 outros layouts do painel — Biblioteca/Trilha —, Explorar, Perfil, Progresso, Preferências, mobile de verdade) desde as mudanças de hoje. Próxima sessão: perguntar se quer revisar tudo com calma antes de seguir pra outra frente (Fase 2 Admin é o que falta maior).

**Atualização 2026-08-14 — processo mockup-primeiro estendido pras outras telas**: usuário confirmou que só o Painel passou pelo processo de mockup-antes-de-portar; decidiu repetir esse processo pra cada tela do aluno que falta antes de portar pro React. Ordem escolhida: **Explorar primeiro**, depois a decidir (candidatos: Perfil, Página da lição/moldura, Progresso, Preferências, Biblioteca, Trilha).

**Mockup do Explorar pronto, aguardando aprovação visual** — `https://claude.ai/code/artifact/c965f573-35bb-44f2-8322-49bcef342cf7`. Reaproveita a linguagem visual já aprovada no Painel (pôster com foto por humor, nota do Reviewer, mesmos tokens). Novidades: busca por título e filtro por humor (chips) funcionando de verdade em JS puro (só no mockup, ainda não portado); descrição do curso visível no card (2 linhas, `-webkit-line-clamp`); grade responsiva `auto-fill` em vez de fileira com scroll (faz mais sentido pra "ver tudo" numa tela de descoberta, diferente do painel que é sobre retomar/continuar). **Ainda não portado pro React** — só existe o Artifact. Script de geração: `scratchpad/build_explorar.py` (fora do repo do projeto, é arquivo de sessão).

**Estado ao pausar (2026-08-14)**: nada novo commitado (mesma pendência de sempre). Servidor dev deve seguir no ar em `localhost:3000` (mas já vazou 2x nessa sessão que o processo morre sozinho — se não responder, só pedir que eu subo de novo). Próxima sessão: mostrar o mockup do Explorar, colher feedback, portar pro React (mesmo padrão do Painel: extrair pra `_layouts/` ou ficar só na própria `page.tsx` já que Explorar não tem variantes de layout), e decidir a próxima tela da lista.

---

## Fase 6 — Polish
**Status: [ ]**

Depende de todas as anteriores.

**Construir:** responsividade desktop/mobile (usando o mesmo padrão de container query validado nos dois protótipos — sidebar/kanban se readaptam, não é reflow genérico), tratamento de erro amigável (IA fora do ar, rate limit da Groq, lição reprovada), acessibilidade (foco visível, `prefers-reduced-motion`, papéis ARIA nos controles interativos).

**Teste [OK quando]:** navegar o fluxo completo (login → painel → lição → avaliação, e criar curso → revisar → aprovar no admin) só no celular, sem nenhum elemento cortado ou sobreposto.

---

## Ordem recomendada

0 → 1 são pré-requisito de tudo. 2 e 3 podem andar em paralelo depois da 1 (admin e aluno não dependem um do outro). 4 e 5 dependem da 3. 6 é sempre por último.

---

## Nota de desatualização + decisão de produto (2026-08-26)

**Frontend pausado por decisão do usuário** — prioridade agora é deixar o backend de geração de
conteúdo (`PLANO_IMPLEMENTACAO_ESTUDO_IA.md`, Fase 2c) e o schema multi-tenant básico
(`PLANO_MULTITENANT_E_PILOTO_TEOLOGIA.md`, T0-T2) funcionando primeiro. Ver
`curso de obreiro/anotação para IA.md` pro registro completo da conversa.

**Retrofit necessário quando o frontend voltar a ser trabalhado**: as telas do aluno construídas
até aqui (`/aluno/explorar`, painel, etc.) mostram **todos os cursos pra todo mundo**, sem
isolamento — decisão que fazia sentido antes do multi-tenant existir, mas contradiz "isolamento
total de catálogo por tenant", já travado em `PLANO_MULTITENANT_E_PILOTO_TEOLOGIA.md` (mais
recente que este documento). Precisa de retrofit assim que a Fase T1 (roteamento por tenant)
acontecer — filtrar catálogo/painel pelo tenant resolvido, não listar tudo.

**Decisão de produto registrada pro frontend futuro**: cada frente (tenant) terá um front com
identidade visual própria pensada pra sua categoria de curso, não um shell único genérico —
substitui o sistema antigo de "humor" por hash de `course.id` (`humorDoCurso()`,
`nia-curso-categoria-nicho`) por algo ancorado na categoria real do tenant. A primeira frente a
receber isso é a de teologia (curso de obreiro e futuros cursos do mesmo tenant — "evangelho de
Jesus Cristo" como tema declarado pelo usuário), reaproveitando a pesquisa de identidade visual já
feita pro curso de obreiro (tema "trigo-maduro" do renderizador de lição — ver
`docs/schema/temas.json` — como ponto de partida, não necessariamente o resultado final do shell
inteiro do app).

## Backlog (fora do escopo atual — só registrado)

- **Categoria/Nicho de curso** ([[nia-curso-categoria-nicho]] na memória): taxonomia `Category` N:N com `Course`, catálogo filtrado por nicho, humor do tema amarrado à categoria em vez de escolha solta. Visão de longo prazo, não trava nada das fases acima, mas o schema de `Course` não deve assumir isolamento total.
- **Layout "Mesa" (kanban) do admin**: prototipado, não faz parte da entrega da Fase 2, pode entrar depois como visão alternativa.
- **Checkout/pagamento dentro do NIA**: decidido ficar fora por enquanto (venda em plataforma externa tipo Hotmart/Kiwify). Se algum dia entrar em escopo, o NIA provavelmente só precisa de um botão/link de compra apontando pra fora e um webhook de liberação de acesso — não é e-commerce completo.
