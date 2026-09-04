# FASE 4 — Progresso · Perfil · Preferências (+ fluxo do Tutor por tópico)

Depende das FASES 2/3 (`TopicoProgress`, `montarArvore`, `_lib/api.ts`, `/topico/[id]`).
Sem login — `ALUNO_USER_ID = 1`. Nada em `frontend/` é tocado. Nada commitado.

Decisões desta fase (confirmadas pelo usuário 2026-09-04):
- Tamanho de fonte **persiste no banco** (coluna nova em `users`), não só cookie.
- `/progresso` traz a linha do tempo dos tópicos **e** já cria o fluxo do Tutor por tópico
  (o `Progress.tutor_analysis` por módulo, alimentado por `/pipeline/licoes/{id}/avaliar`,
  não serve: é por módulo e dispara gamificação que o Emaús rejeitou).

---

## Parte A — Backend

### A1. Migrations (models + ALTER idempotente no startup)

`backend/app/models/models.py`:
- `TopicoProgress` ganha:
  - `tutor_veredito = Column(String(10))` — `'dominado'` | `'reforco'` | `None` (filtro rápido).
  - `tutor_analise = Column(JSONB)` — `{ ultima_avaliacao: {...}, historico: [ {resumo_diagnostico, veredito} ] }`.
  - `avaliado_em = Column(DateTime(timezone=True))`.
- `User` ganha:
  - `preferred_font_size = Column(String(4))` — `'sm'` | `'md'` | `'lg'` | `None` (default de UI = `md`).
  - CHECK `preferred_font_size IN ('sm','md','lg')` (nullable, então `NULL` passa).

`backend/app/main.py` — `Base.metadata.create_all` só cria tabela nova, não altera existente.
Adicionar `_ensure_colunas_extras(engine)` chamado logo após o `create_all`:
```python
def _ensure_colunas_extras(engine):
    """create_all não faz ALTER em tabela que já existe. Colunas da FASE 4 do
    front Emaús — idempotente (ADD COLUMN IF NOT EXISTS, Postgres)."""
    stmts = [
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS tutor_veredito VARCHAR(10)",
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS tutor_analise JSONB",
        "ALTER TABLE topico_progress ADD COLUMN IF NOT EXISTS avaliado_em TIMESTAMPTZ",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_font_size VARCHAR(4)",
    ]
    with engine.begin() as conn:
        for s in stmts:
            conn.exec_driver_sql(s)
        conn.exec_driver_sql(
            "DO $$ BEGIN "
            "IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='valid_preferred_font_size') THEN "
            "ALTER TABLE users ADD CONSTRAINT valid_preferred_font_size "
            "CHECK (preferred_font_size IN ('sm','md','lg')); END IF; END $$;"
        )
```

### A2. Schemas — `backend/app/schemas/topico_progress.py`

- `TopicoProgressOut` ganha `tutor_veredito: str | None`, `tutor_analise: dict | None`,
  `avaliado_em: datetime | None` (todos default `None`).
- Novo:
  ```python
  class AvaliarTopicoRequest(BaseModel):
      user_id: int
      resumo_texto: str
      modelo: str = "groq"
  ```

### A3. Endpoint — `POST /pipeline/topicos/{topico_id}/avaliar`

Em `backend/app/routers/pipeline.py`, ao lado de `avaliar_resumo` (o de lição).

- Mapa `_PERFIL_POR_CURSO = {8: "obreiro"}`, helper `_perfil_do_curso(db, course_id) -> str`
  (default `"tech"`). Resolve subindo `Topico -> Lesson -> Module -> course_id`.
- Valida: tópico existe; `topico.content`; `topico.is_approved` (senão 400 "não disponível").
- Monta `contexto_topico = f"{topico.titulo} — aula '{lesson.title}', módulo {module.module_index}"`.
- Lê `TopicoProgress` (user+topico); monta `historico` textual de `tutor_analise.historico`.
- Roda `TutorAgent(_service(modelo)).avaliar_resumo(resumo_texto, contexto_topico, historico,
  perfil=resolver_perfil(perfil_id))`.
- Upsert no `TopicoProgress`:
  - `tutor_veredito = resultado["veredito"]`
  - `historico.append({ "veredito", "resumo_diagnostico" })`; `tutor_analise = { ultima_avaliacao: resultado, historico }`
  - `avaliado_em = func.now()`
  - se `veredito == "dominado"`: `status = "concluido"`, `concluido_em = func.now()` (se vazio)
  - se `reforco`: `status = "em_andamento"` (não regride se já era `concluido`)
- **Sem** gamificação, **sem** tocar `Progress`.
- Erros: 429/rate-limit do Tutor → `raise HTTPException(503, "O tutor está sobrecarregado agora. Tente de novo em alguns minutos.")`. Outros → 500 com a mensagem.
- Retorno: `{ veredito, resumo_diagnostico, pontos_fortes, lacunas, reforco_sugerido, status }`.

### A4. `postMessage` no render — `backend/app/renderer/templates/topico.html.j2`

No fim de `buildSummary()`, depois de `document.getElementById('summaryText').value = ...`:
```js
try {
  if (window.parent && window.parent !== window) {
    window.parent.postMessage(
      { tipo: 'emaus:resumo', topico: TOPICO_NUMERO, texto: lines.join('\n') },
      '*'
    );
  }
} catch (e) {}
```
Backwards-compatible: o botão "Copiar resumo" e o fluxo manual continuam iguais.

---

## Parte B — Front (`emaus-web/`)

### B1. `_lib/api.ts`

- `TopicoProgress` ganha `tutor_veredito`, `tutor_analise`, `avaliado_em`.
- Tipos novos: `TutorLacuna { tema; evidencia; gravidade }`,
  `TutorReforco { necessario; foco; instrucao_para_gerar }`,
  `AvaliacaoTutor { veredito: "dominado"|"reforco"; resumo_diagnostico; pontos_fortes: string[];
  lacunas: TutorLacuna[]; reforco_sugerido: TutorReforco; status: StatusTopico }`.
- `Progress` tipado (campos usados: `id, user_id, course_id, module_id, status, tutor_analysis,
  time_spent_minutes, last_accessed_at`).
- `UserPrefs` ganha `preferred_font_size?: "sm" | "md" | "lg" | null`.
- `avaliarTopico(topicoId, userId, resumoTexto)` → `POST /pipeline/topicos/{id}/avaliar`.
- `listProgress()` retorna `Progress[]`.

### B2. `_lib/arvore.ts`

- `TopicoNo` ganha `iniciado_em: string | null`, `concluido_em: string | null`,
  `tutor_veredito: "dominado" | "reforco" | null`, `lesson_id`, `moduloTitulo`, `aulaTitulo`.
- `ArvoreCurso` ganha `linhaDoTempo: TopicoNo[]` (todos os tópicos na ordem do curso, já com
  módulo/aula anexados) e `resumo.tempoTotalMin` (soma do `time_spent_minutes` do `Progress`
  do curso — opcional, 0 se nada).
- `montarArvore` passa a receber o `progresso` completo (com datas) — já vem, só propagar os campos.

### B3. `/topico/[topicoId]` — painel do Tutor (mexe na FASE 3, sem quebrar o resto)

`topico-ui.tsx` (`AcoesTopico`):
- `useEffect` adiciona listener de `message`: aceita só `e.data?.tipo === "emaus:resumo"`
  (não valida origin estrito porque o render vem de `:8100` e o texto é inócuo — mas checa o
  shape). Guarda `resumo: string`.
- Quando há `resumo` e o tópico não está `concluido`: mostra painel "Avaliação do tutor" com
  `Botao` "Enviar meu resumo para o tutor".
- Ao enviar: `avaliarTopico(...)` → estado `avaliacao: AvaliacaoTutor | null` + `erroTutor`.
  - `veredito === "dominado"`: `Chip tom="bom"` "Tópico dominado" + `resumo_diagnostico` +
    troca o CTA pra "Próximo tópico" (o backend já marcou `concluido`); `router.refresh()`.
  - `veredito === "reforco"`: `Chip tom="aviso"` "Precisa de reforço" + `resumo_diagnostico`
    + `reforco_sugerido.foco` + lista de `lacunas` (tema + evidência). Mantém o botão
    "Marcar como concluído" (o aluno decide) e um "Enviar de novo" depois de reestudar.
  - erro 503 → aviso "O tutor está indisponível agora. Você pode marcar como concluído e
    pedir a avaliação depois."
- Fallback: se nenhum `emaus:resumo` chegou em ~4s **e** o tópico não está concluído, mostra
  um `<details>` "Colar o resumo manualmente" com `<textarea>` → mesmo `avaliarTopico`.
- O botão "Marcar como concluído" da FASE 3 continua existindo e funcionando.

### B4. `/progresso` — `app/progresso/page.tsx` (Server Component)

- `montarArvore(8)` + `getUser(1)`.
- `CabecalhoApp` com o menu novo (B8). Título "Seu progresso".
- Topo: `BarraProgresso` geral (`resumo.percent`) + "{concluidos} de {totalTopicos} tópicos" +
  tempo de estudo se `> 0`.
- Linha do tempo (`resumo` vazio → estado amigável "Você ainda não concluiu nenhum tópico.
  Comece pelo primeiro." + `LinkBotao` pro `proximoTopico`):
  - agrupada por módulo → aula; cada tópico:
    - `Selo` do estado + título + `Chip` da referência bíblica
    - se `concluido_em`: "Concluído em {data curta}"; se `estado === "atual"`/`em_andamento`
      e `iniciado_em`: "Em andamento desde {data}"
    - se `tutor_veredito`: `Chip` "Dominado" (bom) / "Reforço" (aviso) +
      `tutor_analise.ultima_avaliacao.resumo_diagnostico` numa linha `text-ink-muted`
    - tópico abrível → `Link` "Rever" pra `/topico/{id}`
- Helper `formatarData(iso)` local (`Intl.DateTimeFormat("pt-BR", { day:"numeric", month:"short" })`).

### B5. `/perfil` — `app/perfil/page.tsx` (Server) + `perfil-ui.tsx` (`"use client"`)

- Server: `getUser(1)` + `montarArvore(8)` (só o `resumo`).
- Mostra: `Avatar` grande (inicial), nome, e-mail, "{concluidos} de {totalTopicos} tópicos
  concluídos", nome do curso em andamento (se `proximoTopico`).
- `perfil-ui.tsx`: nome vira editável — `Botao` "Editar" → `<input>` + "Salvar"/"Cancelar" →
  `updateUser(1, { name })` → `router.refresh()`. Erro discreto se o PUT falhar.
- **Sem** pontos, nível, selos, streak (decisão travada do plano).

### B6. `/preferencias` — `app/preferencias/page.tsx` (Server) + `preferencias-ui.tsx` (`"use client"`)

- Server lê `getUser(1)` pra valor inicial (fallback pros cookies / defaults).
- `preferencias-ui.tsx`:
  - **Modo de exibição**: segmented (Claro / Escuro). `onChange` → `setTmTheme(v)` (aplica já)
    + `updateUser(1, { preferred_panel_mode: v })` (fire-and-forget, erro no console).
  - **Tamanho do texto**: 3 botões (Pequeno / Médio / Grande), cada um mostra um trecho de
    exemplo no próprio tamanho. `onChange` → `setTmFontsize(v)` + `updateUser(1, { preferred_font_size: v })`.
  - Aviso curto: "As preferências são aplicadas na hora e ficam salvas na sua conta."
- `AlternarTema` do cabeçalho: mantido (atalho rápido).

### B7. Sincronizar preferências salvas → cookie (SSR sem flash)

O `layout.tsx` lê cookies `tm_theme` / `tm_fontsize`. Como agora a fonte da verdade é
`users/1`, o `/inicio` (server) faz um "reconcile" leve: se `getUser(1).preferred_panel_mode`
/ `preferred_font_size` divergir do cookie, não dá pra `Set-Cookie` de Server Component —
então `preferencias-ui` grava **os dois** (cookie + banco) e o `layout` continua confiando no
cookie. `getUser` no server só alimenta o valor inicial da tela de preferências. (Sem
mudança no `layout.tsx`.)

### B8. Navegação — menu no avatar

`_ui/CabecalhoApp.tsx` + novo `_ui/MenuUsuario.tsx` (`"use client"`):
- O `Avatar` + nome viram um `<button>` que abre um menu (`Perfil` · `Progresso` ·
  `Preferências`). Fecha no `Escape` / clique fora / navegação.
- `AlternarTema` continua ao lado.
- Responsivo: o menu abre alinhado à direita, `max-w` da viewport.
- `/inicio`, `/curso/[id]` passam a usar o `CabecalhoApp` já com o menu (só trocar o
  componente interno — a API do `CabecalhoApp` não muda).

---

## Aceite da FASE 4

1. `cd emaus-web && node node_modules/typescript/bin/tsc --noEmit` → 0 erros.
2. `docker restart nia_backend`; startup não quebra; `\d topico_progress` e `\d users`
   mostram as colunas novas.
3. `GET /topico-progress/?user_id=1` traz `tutor_veredito`/`tutor_analise`/`avaliado_em`.
4. Fluxo do tutor: abrir `/topico/1`, ir até o último slide → o Emaús recebe o resumo →
   "Enviar para o tutor" → veredito aparece. `dominado` fecha o tópico; `/progresso` mostra
   o chip e o diagnóstico.
5. `POST /pipeline/topicos/1/avaliar` com um resumo de teste via `curl` → 200 com o JSON do
   veredito; registro em `topico_progress` atualizado.
6. `/perfil` → editar nome → salva (`GET /users/1` reflete).
7. `/preferencias` → trocar modo e tamanho → aplica na hora, recarregar mantém, `GET /users/1`
   mostra `preferred_panel_mode` / `preferred_font_size`.
8. Menu do avatar abre/fecha, leva às 3 telas, funciona em 360px.
9. `/progresso`, `/perfil`, `/preferencias` → HTTP 200. Nada em `frontend/` tocado.

## Estado

- [x] Implementada e testada com o backend no ar (2026-09-04).
  - Migration: `_ensure_colunas_extras()` rodou no startup; `\d topico_progress` mostra
    `tutor_veredito`/`tutor_analise`/`avaliado_em`, `users` tem `preferred_font_size` +
    constraint `valid_preferred_font_size`.
  - `POST /pipeline/topicos/2/avaliar` (reforço) e `/topicos/3/avaliar` (dominado → `status`
    vira `concluido`, `concluido_em` preenchido, idempotente em 3 chamadas). `historico`
    acumula. Dados de teste resetados depois (T1 concluído, T2 em andamento, T3 não iniciado).
  - `PUT /users/1 {preferred_font_size, preferred_panel_mode}` persiste (GET confirma);
    valor inválido → 500 (CHECK), mas o front só manda sm/md/lg | light/dark.
  - Front: `/`, `/inicio`, `/curso/8`, `/progresso`, `/perfil`, `/preferencias`, `/topico/1`
    → todos 200, sem erro no log do `next dev`. `tsc --noEmit` 0 erros.
  - **Pendente:** conferência visual no navegador + testar o fluxo do painel do Tutor
    clicando (o `postMessage` do render → "Enviar meu resumo" → veredito).
  - Quirk pré-existente: `PUT /users/{id}` responde `{}` (sem `db.refresh`) — o front faz
    `router.refresh()` e re-busca via `getUser`, então não afeta.
