# FASE 5 — Área de revisão do professor

Sem login (mesma linha da FASE 0-4) — sem controle de acesso real ainda; a rota fica só "não
linkada" no menu do aluno (link discreto no rodapé). Auth continua adiada (FASE 1, o usuário
avisa quando fazer).

Decisões confirmadas pelo usuário 2026-09-04 (sessão à noite):
- Revisão é **slide a slide**, sincronizada com o `<iframe>` do render (não texto livre solto).
- Por slide: **reação** (👍/👎), **texto opcional**, **pedido de imagem antes/depois do slide**,
  **nota sobre a imagem já presente no slide** (quando o slide tem uma).
- No fim da revisão de um tópico: **checklist de múltipla escolha** (profundidade, clareza,
  qualidade) + **observação final livre**. Esse checklist É o ato de aprovar/reprovar.
- O curso só fica disponível pro aluno depois de aprovado. O usuário (Atila) **define os
  perfis que aprovam cada curso** — não é uma lista fixa global, é por curso.
- Professor também **vê o progresso do aluno** (reaproveita a timeline da FASE 4).

---

## Governança — versão final do exemplo do usuário (2026-09-04, 3ª rodada)

Não é uma lista de pessoas por curso — é um sistema de **papéis** com regras configuráveis
**por curso**:

- **Papéis** (`User.role` ganha `admin_master` | `admin` | `professor`, além de `aluno`):
  `admin_master` = o usuário (Atila), controle total, sempre pode aprovar sozinho **se o curso
  permitir**. `admin` = outras pessoas com autoridade (ex: Pastor) mas menos alcance que o
  master. `professor` = foco em qualidade do curso e no aluno; é atribuído como **tutor** de
  cursos específicos (não de todos).
- **Por curso**, o master (ou um admin) configura:
  - `CourseTutor` — quais `professor`(es) são tutores DESSE curso (de um pool de N professores
    cadastrados).
  - `aprovacao_master_basta` (bool) — o `admin_master` pode aprovar sozinho, sem esperar
    professor nenhum?
  - `aprovacao_exige_todos_tutores` (bool) — entre os tutores atribuídos, precisa de **todos**
    aprovarem ou só **um** já libera?
- **Aprovar ≠ Publicar.** Aprovar é por TÓPICO (mecânica slide-a-slide + checklist já speced
  abaixo, inalterada). Publicar é do CURSO inteiro — passo separado, final, controlado pelas
  regras acima. Um curso **não publicado** pode aparecer no catálogo do aluno só com **cadeado**
  (reaproveita o padrão que já existe em `catalogo.ts` pros 11 cursos "em breve").

### Modelo de dados — camada de publicação (course-level, ADICIONAL ao que já estava speced)

`Course` (ou tabela nova `CourseConfig`, 1:1):
- `aprovacao_master_basta` bool, default false
- `aprovacao_exige_todos_tutores` bool, default false
- `publicado` bool, default false (calculado ou setado no ato de publicar — decidir: eu acho
  que deveria ser um botão explícito "Publicar" depois que a condição de aprovação bate, não
  100% automático, pra dar controle final a quem publica — CONFIRMAR com o usuário)

`CourseTutor` (nova): `id`, `course_id`, `user_id` (role deve ser `professor`), `created_at`.

`CourseAprovacao` (nova): `id`, `course_id`, `user_id`, `papel_no_momento`, `aprovado` bool,
`observacao`, timestamps. Upsert por `(course_id, user_id)`.

### Isso é MAIOR que a revisão de tópico e tem pré-requisitos que não existem hoje

- Só existe 1 usuário no banco (`aluno`, id 1). Pra essa camada funcionar de verdade precisa
  seedar os `admin`/`professor` reais (o usuário disse "3 admin e 5 professor" — nomes reais
  a definir).
- Não existe NENHUMA tela de criar/configurar curso no `emaus-web` hoje (cursos nascem no
  pipeline do NIA). "Escolher os tutores" e as regras de aprovação por curso precisam de uma
  tela nova — isso é, na prática, o **início de um painel admin**, não só "revisão".
- Proposta de fasear (ver decisão pedida ao usuário no final do arquivo):
  - **FASE 5a** (como já speced abaixo — revisão slide-a-slide + checklist por tópico) é
    autocontida, usa o que já existe, e já entrega valor imediato.
  - **FASE 5b** (papéis/tutores/regra de quórum/publicar) é o painel de governança do curso —
    maior, precisa de mais decisões (seed dos usuários reais, tela de configuração por curso).

---

## Modelo de dados

### `PerfilAprovador` (novo)
Quem pode aprovar um curso. Hardcoded via seed (não tem tela de cadastro nesta fase), mas vive
no banco pra o checklist referenciar um id estável.

| Campo | Tipo |
|---|---|
| `id` | PK |
| `course_id` | FK courses |
| `nome` | string (ex: "Pr. Fulano", "Teólogo Beltrano") |
| `ativo` | bool, default true |

### `TopicoComment` (novo) — anotação por slide
| Campo | Tipo | Uso |
|---|---|---|
| `id` | PK | |
| `topico_id` | FK | |
| `perfil_id` | FK `PerfilAprovador` | quem anotou |
| `slide_index` | int, nullable | índice do slide (null = comentário geral do tópico) |
| `reacao` | `'positivo'\|'negativo'`, nullable | |
| `imagem_sugerida` | `'antes'\|'depois'`, nullable | pedido de imagem nova |
| `sobre_imagem` | bool, default false | comentário é sobre a imagem já no slide |
| `texto` | texto, nullable | pode ser só reação, sem texto |
| `resolvido` | bool, default false | |
| `created_at`/`updated_at` | | |

Sem DELETE (soft — CLAUDE.md). Editar/resolver via `PUT`.

### `TopicoChecklist` (novo) — o ato de aprovar/reprovar
Upsert por `(topico_id, perfil_id)` — 1 checklist por perfil por tópico, igual ao padrão do
`TopicoProgress`.

| Campo | Tipo |
|---|---|
| `id` | PK |
| `topico_id` | FK |
| `perfil_id` | FK `PerfilAprovador` |
| `profundidade` | `'raso'\|'adequado'\|'aprofundado'` |
| `clareza` | `'confuso'\|'parcialmente_claro'\|'claro'` |
| `qualidade_geral` | `'fraca'\|'regular'\|'boa'\|'excelente'` |
| `observacao_final` | texto, nullable |
| `aprovado` | bool |
| `created_at`/`updated_at` | |

`Topico.is_approved` passa a ser **recalculado** a cada `PUT` de checklist: `True` só se todo
`PerfilAprovador` ativo do curso tiver um `TopicoChecklist.aprovado=True` pra aquele tópico
(pendente a confirmação da regra "todos vs. um" acima).

---

## Render — `topico.html.j2`

`showSlide(idx)` ganha, no fim da função, um `postMessage`:
```js
try {
  if (window.parent && window.parent !== window) {
    window.parent.postMessage({
      tipo: 'emaus:slide',
      indice: idx,
      total: slides.length,
      secao: slideEl.dataset.section || '',
      temImagem: !!slideEl.querySelector('img'),
    }, '*');
  }
} catch (e) {}
```
Backwards-compatible — nada muda pro aluno.

---

## Backend

- `models.py`: `PerfilAprovador`, `TopicoComment`, `TopicoChecklist`.
- `schemas/revisao.py`: schemas dos três.
- `routers/revisao.py`:
  - `GET /perfis-aprovadores/?course_id=`
  - `GET /topico-comments/?topico_id=` (+ sem filtro pra fila), `POST`, `PUT /{id}`
  - `GET /topico-checklists/?topico_id=`, `PUT /topico-checklists/{topico_id}` (upsert por
    `perfil_id` no body) — recalcula `Topico.is_approved` depois de salvar.
- Seed dos `PerfilAprovador` do curso 8 — via script simples ou inserido direto (definir nomes
  com o usuário antes de rodar).
- `GET /topicos/{id}/geracoes` — lê `conteudo_{groq,gemini}_topicoN.json` se existirem.

## Front (`emaus-web/`)

- `_lib/api.ts`: tipos + `listPerfisAprovadores`, `listTopicoComments`, `criarComentarioSlide`,
  `resolverComentario`, `getChecklist`, `salvarChecklist`.
- `_lib/config.ts`: seletor de "perfil atual" (sem login — dropdown na própria tela, guardado
  em cookie local, mesmo espírito do `ALUNO_USER_ID`).
- `/revisao` — fila de tópicos do curso 8 (rascunho / em revisão / aprovado), contador de
  comentários abertos, quantos perfis já aprovaram (`x/y`).
- `/revisao/topico/[id]` — iframe do render + painel lateral:
  - escuta `emaus:slide` → mostra "Slide {indice+1} de {total} — {secao}"
  - formulário de anotação do slide atual (👍/👎, texto, sugerir imagem antes/depois, nota de
    imagem se `temImagem`)
  - lista de anotações já feitas (por slide), marcar resolvido
  - ao chegar no fim (ou por botão): **checklist final** (3 perguntas de múltipla escolha +
    observação livre) → `salvarChecklist` → mostra se o tópico ficou aprovado (x/y perfis)
- `/revisao/topico/[id]/comparar` — Groq × Gemini lado a lado (só quando os 2 arquivos existem
  pro tópico; hoje só T2/T3).
- `/revisao/aluno/[userId]` — reaproveita a timeline de `/progresso` (componente compartilhado),
  somente leitura. `montarArvore` ganha parâmetro `userId` opcional.
- Link discreto "Área do professor" no `Rodape`.

---

## Testes
`tsc --noEmit` 0 erros · migration verificada · CRUD de comentários e checklist via curl ·
fluxo: anotar slides → checklist → tópico aprovado quando todos os perfis aprovam → `/topico/{id}`
do aluno reflete · `frontend/` intocado.

## Estado

- [x] **FASE 5a implementada e testada** (2026-09-04, depois da FASE 1/auth). Com login real
  já pronto, `PerfilAprovador` saiu do desenho — as anotações e o checklist usam
  `user_id` de verdade (do token), não mais um "perfil" hardcoded.
  - Backend: `TopicoComment`/`TopicoChecklist` (`models.py`), `schemas/revisao.py`,
    `routers/revisao.py` — `GET/POST/PUT /topico-comments/`, `GET/PUT
    /topico-checklists/`, tudo exigindo login com papel `master`/`admin`/`professor`
    (`_exigir_revisor`). `PUT /topico-checklists/{id}` recalcula `Topico.is_approved`:
    **1 aprovação de papel elevado já libera** nesta fase (quórum por curso fica pra FASE 5b).
    `topico.html.j2`: `showSlide()` ganhou `postMessage({tipo:'emaus:slide', indice, total,
    secao, temImagem})`.
  - Front: `_lib/revisao.ts` (`montarFilaRevisao`), `_lib/sessao.ts` (+`getToken()` pra
    Server Component autenticado), `_ui/LinhaDoTempoTopicos.tsx` (extraído de `/progresso`,
    reaproveitado). Proxies `app/api/revisao/{comentario,checklist}/route.ts`. Páginas:
    `/revisao` (fila: rascunho/em revisão/aprovado + comentários abertos),
    `/revisao/topico/[id]` (iframe + painel: reação 👍/👎 por slide, pedido de imagem
    antes/depois, nota sobre imagem, checklist final), `/revisao/alunos` +
    `/revisao/aluno/[userId]` (progresso do aluno, leitura). Link "Área de revisão" no
    `Rodape` só aparece pra quem tem o papel.
  - **Testado ao vivo**: aluno recebe 403 do backend e é redirecionado pelo middleware;
    master cria comentário de slide → resolve → salva checklist aprovando/reprovando →
    `Topico.is_approved` muda de verdade (confirmado no banco, testei reprovar e
    reaprovar o T1 e revertido pro estado funcional original). 7+ rotas novas → 200,
    `tsc` 0 erros, `py_compile` OK.
  - **Cortado desta rodada** (documentado, não implementado): `/revisao/topico/[id]/comparar`
    (Groq×Gemini) — os arquivos `curso de obreiro/conteudo_*.json` não estão montados no
    container Docker (`docker-compose.yml` só monta `./backend:/app`), precisaria de mudança
    no compose; baixo valor (só 2 tópicos têm os arquivos, não é gerado pelo pipeline
    padrão). Fica registrado pra quando/se fizer sentido.
- [x] **FASE 5b implementada e testada** (2026-09-04, mesma sessão). Usuário optou por manter
  os placeholders (Admin 1-3/Professor 1-5) em vez de nomes reais.
  - `Course` ganhou `aprovacao_master_basta`/`aprovacao_exige_todos_tutores` (ALTER). Reaproveitado
    `Course.status`/`published_at` que já existiam e não eram usados por ninguém (em vez de criar
    um `publicado` novo) — publicar seta `status='published'`.
  - Novas tabelas `CourseTutor` (quais professores são tutores de qual curso) e
    `CourseAprovacao` (aprovação/reprovação da PUBLICAÇÃO do curso — diferente do
    `TopicoChecklist` da 5a, que aprova um tópico).
  - `routers/governanca.py`: `GET /cursos/{id}/governanca`, `PUT /config` (master/admin),
    `PUT /aprovacao` (master/admin/professor-tutor — professor não-tutor toma 403), `POST
    /publicar` (master sempre; outros só se `_pode_publicar()` bate), `POST /despublicar`
    (só master).
  - Front: `/revisao/curso/[courseId]` — cartão de publicar/despublicar, config de tutores +
    regras (só admin/master editam), cartão "sua avaliação" (só quem pode aprovar), lista de
    quem já se posicionou. Proxies `app/api/revisao/{curso-config,curso-aprovacao,
    curso-publicar}/route.ts`.
  - **Testado ao vivo, cenário completo**: configurei 2 tutores + "exige todos" → professor
    não-tutor barrado (403) → tentativa de publicar sem aprovação nenhuma barrada (403) →
    1 tutor aprova, ainda barrado → 2º tutor aprova, publica com sucesso → despublicar como
    professor barrado (403, só master) → despublicado por master. Testei também
    `aprovacao_master_basta`. Config resetada pro estado limpo (sem tutor, sem regra, draft)
    ao final. `tsc` 0 erros, `py_compile` OK, 13 rotas → 200.
  - **Decisão consciente, não implementada nesta rodada**: o `status`/`is_public` do curso
    ainda **não gateia** `/curso/[id]` nem `/topico/[id]` pro aluno — fazer isso agora
    quebraria o curso 8 (que não tem tutor/aprovação configurada, ficaria inacessível) e
    arriscava quebrar o curso 9 que a sessão paralela estava testando. Fica registrado como
    o próximo passo natural quando fizer sentido coordenar com o catálogo (`catalogo.ts`).

**Nota (2026-09-04):** sessão de FASE 5a rodou em paralelo com outra sessão
(`english-course-structure`) editando o mesmo `emaus-web/`/`backend/` (curso 9 de Inglês).
Nenhuma colisão real — arquivos compartilhados foram relidos antes de cada edição.
