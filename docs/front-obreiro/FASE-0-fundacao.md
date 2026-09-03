# FASE 0 — Fundação do segmento `/formacao`

Segmento novo no app Next existente (`frontend/`). Não toca em `app/aluno/*`, `app/components/*`,
`app/globals.css` (exceto adicionar 1 `@import` no fim, se necessário — ver F0.2). Tudo isolado
em `app/formacao/`.

Stack: Next 16 App Router, React 19, TypeScript estrito, Tailwind v4. Server Components por
padrão; `"use client"` só onde precisa de estado/efeito.

---

## F0.1 — Config + cliente de API

**`app/formacao/_lib/config.ts`**
```ts
export const TEOLOGIA_COURSE_IDS = [8] as const;      // hardcoded até Tenant existir
export const THEME_TOPICO = "trigo-maduro";           // tema do render de slides
export const API_URL =
  typeof window === "undefined"
    ? process.env.API_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
    : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export const API_URL_PUBLICA = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
```

**`app/formacao/_lib/api.ts`** — fetch tipado. `fetchJson<T>(path, init?)` com `cache: "no-store"`,
`Content-Type: application/json`, lança `Error` com status+corpo em `!res.ok`.

Tipos (campos reais do backend, conferidos):
```ts
export type Course = { id:number; title:string; description:string|null; level:string; status:string; modules_count:number; duration_hours:number; ai_quality_score:number|null };
export type Module = { id:number; course_id:number; module_index:number; title:string; description:string|null; lessons_count:number };
export type Lesson = { id:number; module_id:number; lesson_index:number; title:string; content:string|null; is_approved:boolean; estimated_read_time_minutes:number|null };
export type Topico = { id:number; lesson_id:number; topico_index:number; titulo:string; referencia_biblica:string|null; content:string|null; is_approved:boolean; generated_by:string|null; reviewed_by:string|null; estimated_read_time_minutes:number|null };
export type UserMe = { id:number; name:string|null; email:string; role:string };
export type UserPrefs = { id:number; name:string|null; email?:string; preferred_panel_mode:"light"|"dark"; [k:string]:unknown };
```

Funções:
- `login(email,senha): Promise<{access_token:string}>` → `POST /auth/login` body `{email, password:senha}`
- `register(nome,email,senha)` → `POST /auth/register` body `{name:nome, email, password:senha}`
- `me(token): Promise<UserMe>` → `GET /auth/me` header `Authorization: Bearer <token>`
- `listCourses(): Promise<Course[]>` → `GET /courses/`
- `getCourse(id)` → `GET /courses/{id}`
- `listModules(): Promise<Module[]>` → `GET /modules/`  (sem filtro no backend; filtrar no front)
- `listLessons(): Promise<Lesson[]>` → `GET /lessons/`
- `listTopicos(lessonId?): Promise<Topico[]>` → `GET /topicos/` ou `GET /topicos/?lesson_id={id}`
- `getTopico(id): Promise<Topico>` → `GET /topicos/{id}`
- `topicoRenderUrl(id, { theme, userId }): string` → `${API_URL_PUBLICA}/topicos/{id}/render?theme=...&user_id=...` (SEMPRE URL pública — vira src de iframe no navegador)
- `getUser(id): Promise<UserPrefs>` → `GET /users/{id}`
- `updateUser(id, data): Promise<UserPrefs>` → `PUT /users/{id}`
- `listProgress(): Promise<unknown[]>` → `GET /progress/` (tipar depois, na Fase 4)

---

## F0.2 — Tema + layout do segmento

**`app/formacao/formacao.css`** — importado só pelo layout do segmento. Tokens `--tm-*`.
Claro no `:root [data-tm-theme="light"]` e no default; escuro em `[data-tm-theme="dark"]`.

Claro (valores dos `curso de obreiro/topico*-completo.html`):
```
--tm-bg:#faf6ee; --tm-surface:#ffffff; --tm-surface-2:#f3ece0;
--tm-ink:#2b241c; --tm-ink-muted:#6b5f4f; --tm-border:#e4d8c3;
--tm-accent:#8a5a2b; --tm-accent-2:#b8763a; --tm-gold:#b8923e;
--tm-verse-bg:#fbf3e0; --tm-verse-border:#c9a24a;
--tm-good:#4f7a3a; --tm-warn:#a35a1e; --tm-danger:#a5352b;
```
Escuro (desenhado — marrom quente, não preto):
```
--tm-bg:#1b1610; --tm-surface:#241d15; --tm-surface-2:#2e261c;
--tm-ink:#f1e7d6; --tm-ink-muted:#b0a184; --tm-border:#3c3327;
--tm-accent:#d79b5b; --tm-accent-2:#e3ac6a; --tm-gold:#dcb87a;
--tm-verse-bg:#2a2114; --tm-verse-border:#7a5f2e;
--tm-good:#7fae62; --tm-warn:#d08a4e; --tm-danger:#d97b6f;
```
Comuns (ambos os modos):
```
--tm-radius:14px; --tm-radius-lg:20px; --tm-radius-pill:999px;
--tm-font-display:'Fraunces', Georgia, 'Times New Roman', serif;
--tm-font-body:'Source Sans 3', -apple-system, 'Segoe UI', sans-serif;
--tm-shadow: 0 1px 2px rgba(43,36,28,.06), 0 8px 24px rgba(43,36,28,.06);
--tm-maxw: 1180px;
```
Escala de fonte (F4.3 usa): `[data-tm-fontsize="sm"]{--tm-fs:15px} ...="md"{--tm-fs:17px} ...="lg"{--tm-fs:19px}`, default 17px.

Também no `formacao.css`: reset leve escopado em `.formacao-root` (box-sizing, `img{max-width:100%}`),
e classe utilitária `.formacao-root { background:var(--tm-bg); color:var(--tm-ink); font-family:var(--tm-font-body); font-size:var(--tm-fs,17px); min-height:100vh; }`.

**`app/formacao/layout.tsx`** (Server Component):
- Importa `./formacao.css`.
- Carrega Fraunces + Source Sans 3 via `next/font/google` (`Fraunces` com subsets latin, weights 400/600/700, variable `--tm-font-display-loaded`; `Source_Sans_3` weights 400/500/600/700). Aplica as variáveis no wrapper. (Ou `<link>` do Google Fonts se `next/font` complicar com a var custom — aceitável.)
- Lê o cookie `tm_theme` (`"light"|"dark"`, default `"light"`) e `tm_fontsize` (default `"md"`) via `cookies()` do `next/headers` e põe `data-tm-theme` / `data-tm-fontsize` no `<div class="formacao-root">`.
- Renderiza `{children}` dentro de `.formacao-root`. **Não** re-renderiza `<html>/<body>` (o root layout já faz isso).

**`app/formacao/_lib/theme.ts`** — helper client `setTmTheme(v)` / `setTmFontsize(v)` que grava o cookie (`document.cookie = ...; path=/formacao`) e dá `location.reload()` OU seta o atributo no DOM na hora + grava cookie (preferir sem reload). Exporta `useTmTheme()` simples se ajudar.

---

## F0.3 — Kit de componentes `app/formacao/_ui/`

Todos client-safe (sem `"use client"` a menos que precise de handler), só tokens `--tm-*`,
`className` opcional passado adiante, tipagem estrita. Mobile-first.

- **`Botao.tsx`** — `variante?: "primario"|"fantasma"|"perigo"` (default primario), `tamanho?: "sm"|"md"` , `as?: "button"|"a"`, aceita `href`. Primário: fundo `--tm-accent`, texto claro, `--tm-radius-pill`. Fantasma: borda `--tm-border`, texto `--tm-ink`. Estados hover/focus-visible (anel `--tm-accent`), disabled.
- **`Card.tsx`** — `<section>` com `background:--tm-surface`, `border:1px solid --tm-border`, `border-radius:--tm-radius-lg`, `--tm-shadow`. Slot `children`. `interativo?` boolean → hover eleva.
- **`Chip.tsx`** — pílula pequena, `tom?: "neutro"|"info"|"bom"|"aviso"` , usada pra referência bíblica / metadados.
- **`BarraProgresso.tsx`** — `valor:number` (0-100), `rotulo?:string`. Trilho `--tm-surface-2`, preenchimento `--tm-accent`. `role="progressbar"` com aria.
- **`Selo.tsx`** — estado de tópico: `estado: "concluido"|"atual"|"disponivel"|"em_preparacao"`. Ícone + texto, cores: concluído=`--tm-good`, atual=`--tm-accent`, disponível=`--tm-ink-muted`, em_preparacao=`--tm-border`/tracejado.
- **`Avatar.tsx`** — iniciais do nome num círculo `--tm-surface-2` / texto `--tm-accent`. `nome:string`, `tamanho?:"sm"|"md"`.
- **`CabecalhoApp.tsx`** — `"use client"`. Marca "Formação" (Fraunces) à esquerda, navegação no centro/direita (`children` = links), `Avatar` + nome à direita. Abaixo de `640px`: marca + avatar na primeira linha, nav em linha própria full-width com scroll horizontal se não couber. `position: sticky; top:0`, fundo `--tm-bg` com leve blur/borda inferior.
- **`Rodape.tsx`** — discreto: "NIA · Formação" + link "Preferências". `border-top:1px solid --tm-border`, texto `--tm-ink-muted`, `font-size:12.5px`.

Cada componente: no máx. ~40 linhas, sem libs novas.

---

## F0.4 — Página de verificação

**`app/formacao/dev/page.tsx`** (sem link em menu nenhum) — renderiza uma vez cada componente
do `_ui/` com dados fake, e dois botões no topo que alternam `data-tm-theme` entre light/dark
(client, via helper do F0.2) pra conferência visual rápida. Um `<h1>` "Kit /formacao" e seções
rotuladas por componente.

---

## Aceite da FASE 0

1. `cd frontend && node node_modules/typescript/bin/tsc --noEmit` → 0 erros.
2. `npm run dev` sobe sem erro; `curl -s localhost:3000/formacao/dev` → 200 com o markup dos componentes.
3. Alternar o botão de tema em `/formacao/dev` troca todas as cores sem reload e sem quebrar contraste nos 2 modos.
4. Nada em `app/aluno/*`, `app/components/*` ou o bloco de "humor" do `globals.css` foi alterado.
