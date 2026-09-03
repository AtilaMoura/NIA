# FASE 2 — Índice do curso + navegação por tópico

Projeto: `emaus-web/` (Next 16, App Router, rotas sem prefixo `/formacao`).
Sem login — usuário fixo `ALUNO_USER_ID = 1` (de `_lib/config.ts`).

Depende da FASE 0 (kit `_ui/`, tokens `--tm-*`, layout). Não toca em `frontend/`.

---

## Backend (no `backend/`)

### B1 — Modelo `TopicoProgress`  (`app/models/models.py`)

Progresso **por tópico** — hoje `Progress` é só por módulo, não serve.

| Coluna | Tipo | Nota |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | Integer FK `users.id` `ondelete=CASCADE`, index | |
| `topico_id` | Integer FK `topicos.id` `ondelete=CASCADE`, index | |
| `status` | String(20), default `'nao_iniciado'` | CHECK `IN ('nao_iniciado','em_andamento','concluido')` |
| `iniciado_em` | DateTime(tz) | setado na 1ª vez que vira `em_andamento` |
| `concluido_em` | DateTime(tz) | setado quando vira `concluido` |
| `time_spent_s` | Integer, default 0 | reservado p/ FASE 3 (ainda não populado) |
| `created_at` | DateTime(tz) `server_default=func.now()` | |
| `updated_at` | DateTime(tz) `onupdate=func.now()` | |

- `UniqueConstraint(user_id, topico_id)` — 1 registro por par.
- Nunca deleta — só upsert de `status` (soft, conforme padrão do projeto).
- Tabela criada pelo `create_all` no boot do `main.py` (backend roda com `--reload`).

### B2 — Schema  (`app/schemas/topico_progress.py`)

```py
class TopicoProgressUpsert(BaseModel):
    user_id: int
    status: Literal["nao_iniciado", "em_andamento", "concluido"]

class TopicoProgressOut(BaseModel):
    id: int
    user_id: int
    topico_id: int
    status: str
    iniciado_em: datetime | None = None
    concluido_em: datetime | None = None
    class Config: from_attributes = True
```

### B3 — Router  (`app/routers/topico_progress.py`, registrado no `main.py`)

- `GET /topico-progress/?user_id={id}` → `list[TopicoProgressOut]` (todos os registros do aluno).
- `PUT /topico-progress/{topico_id}` body `TopicoProgressUpsert` → upsert:
  - cria se não existe; senão atualiza `status`.
  - `em_andamento` e `iniciado_em` nulo → seta `iniciado_em = now()`.
  - `concluido` → seta `concluido_em = now()` (e `iniciado_em` se ainda nulo).
  - volta a `em_andamento`/`nao_iniciado` → **não** limpa `concluido_em` (histórico), só muda `status`.
  - 404 se o `topico_id` não existe.

### B4 — CORS  (`app/main.py`)

`allow_origins` hoje: `["http://localhost:3000", "http://localhost:4000"]`.
Adicionar `"http://localhost:4200"` (porta do dev server do emaus-web). Necessário pro
`PUT` de progresso da FASE 3, que roda no navegador.

---

## Frontend (no `emaus-web/`)

### F1 — `app/_lib/api.ts`  (estender)

```ts
export type TopicoProgress = {
  id: number; user_id: number; topico_id: number;
  status: "nao_iniciado" | "em_andamento" | "concluido";
  iniciado_em: string | null; concluido_em: string | null;
};
export function listTopicoProgress(userId: number): Promise<TopicoProgress[]>   // GET
export function setTopicoProgress(topicoId, userId, status): Promise<TopicoProgress>  // PUT
```

### F2 — `app/_lib/arvore.ts`  (helper, sem JSX)

`montarArvore(courseId: number)` — server-side, faz em paralelo:
`getCourse`, `listModules`, `listLessons`, `listTopicos()`, `listTopicoProgress(ALUNO_USER_ID)`.

Monta e devolve:

```ts
type EstadoTopico = "concluido" | "atual" | "disponivel" | "em_preparacao";
type TopicoNo   = { id; titulo; referencia_biblica; topico_index; estado: EstadoTopico };
type AulaNo     = { id; titulo; lesson_index; topicos: TopicoNo[] };
type ModuloNo   = { id; titulo; descricao; module_index; aulas: AulaNo[] };
type ArvoreCurso = {
  curso: Course;
  modulos: ModuloNo[];
  resumo: { totalTopicos; concluidos; percent };   // percent = round(concluidos/total*100), 0 se total=0
  proximoTopico: { id; titulo } | null;            // 1º "atual" na sequência do curso
};
```

Regras de estado (avaliadas na ordem do curso: módulo→aula→tópico por índice):
1. `em_preparacao` se `!topico.content || !topico.is_approved`.
2. senão `concluido` se `progress[topico.id]?.status === "concluido"`.
3. senão: o **primeiro** tópico que sobrar (não concluído, não em preparação) na sequência inteira do curso vira `atual`; os demais viram `disponivel`.

`proximoTopico` = esse `atual` (ou `null` se não houver — tudo que está pronto já foi concluído).

### F3 — `app/curso/[courseId]/page.tsx`  (Server Component)

- `courseId` fora de `TEOLOGIA_COURSE_IDS` → `notFound()`.
- `CabecalhoApp` (nome via `getUser(ALUNO_USER_ID)`, links: "Início" → `/inicio`, "Curso" ativo).
- Título do curso + `BarraProgresso valor={resumo.percent} rotulo="Progresso do curso"` +
  linha "`{concluidos} de {total} tópicos concluídos`".
- Lista de módulos em **accordion** (`./arvore-ui.tsx`, `"use client"`):
  - fechado por padrão, exceto o módulo que contém o `proximoTopico` (aberto).
  - cabeçalho: `Módulo {n} · {titulo}` + contador `{concluidosDoModulo}/{totalDoModulo}`.
  - corpo: aulas → tópicos. Cada tópico é uma linha com `Selo estado={...}` + título +
    `Chip tom="info"` da `referencia_biblica` (se houver).
  - tópico `concluido`/`atual`/`disponivel` → `<Link href={\`/topico/${id}\`}>` (linha inteira clicável).
  - tópico `em_preparacao` → sem link, opacidade reduzida, `title="Conteúdo em preparação"`.
- `Rodape`.

### F4 — `app/inicio/page.tsx`  (Server Component)

- `CabecalhoApp` (mesma coisa).
- Hero em `Card`:
  - se `proximoTopico` != null: "Continue de onde parou" + título do tópico +
    `LinkBotao href={\`/topico/${proximoTopico.id}\`}` "Continuar".
  - se null e `total > 0`: "Você está em dia" + "Os próximos tópicos ainda estão em preparação." +
    `LinkBotao href="/curso/8" variante="fantasma"` "Ver o curso".
  - se `total === 0`: "O conteúdo do curso está sendo preparado."
- `BarraProgresso` do curso + `LinkBotao` "Ver todo o curso" → `/curso/8`.
- `Rodape`.

### F5 — `app/page.tsx`

Trocar o placeholder por `redirect("/inicio")` (de `next/navigation`).

### F7 — Housekeeping (`PLANO_FRONT_OBREIRO.md`)

Atualizar a seção "Estado" e a tabela de rotas: FASE 0 caiu em `emaus-web/` (projeto
separado, opção C), rotas sem prefixo `/formacao`. Marcar FASE 2 como `[~]`.

---

## Aceite da FASE 2

1. `cd emaus-web && npx tsc --noEmit` → 0 erros.
2. Backend: `PUT /topico-progress/1` body `{"user_id":1,"status":"concluido"}` grava;
   `GET /topico-progress/?user_id=1` retorna o registro com `concluido_em` preenchido.
3. `GET localhost:4200/curso/8` → 200. Árvore: Módulo 26 → Aula 57 → T1..T5;
   T1–T3 com link (T1/T2/T3 têm content aprovado), T4–T5 "em preparação".
   Demais aulas do curso 8 aparecem sem tópicos / "em preparação".
4. `GET localhost:4200/inicio` → hero aponta pro primeiro tópico não concluído
   (T1 no estado limpo). Marcando T1–T3 concluídos via `curl`, o hero passa a mostrar
   "Você está em dia" (T4/T5 em preparação).
5. `GET localhost:4200/` → redireciona pra `/inicio`.
6. Nada em `frontend/` foi tocado.

## Estado

- [~] Implementada 2026-09-03. `tsc --noEmit` 0 erros; aceites 1–6 verificados via `curl`.
  Ajuste vs. spec: a `montarArvore` também expõe `contarModulo(m)` (usado no cabeçalho do
  accordion). Pendente: conferência visual no navegador.
