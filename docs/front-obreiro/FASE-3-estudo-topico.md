# FASE 3 — Estudo do tópico

Depende da FASE 2 (`TopicoProgress` no backend, `montarArvore`, `_lib/api.ts` estendido).
Sem login — `ALUNO_USER_ID = 1`.

---

## F5.1 — `app/topico/[topicoId]/page.tsx`  (Server Component)

- `getTopico(topicoId)`. Se não existe → `notFound()`.
- Se `!topico.content || !topico.is_approved` → tela "Este tópico ainda está em preparação"
  + `LinkBotao` "Voltar ao curso" (`/curso/8`). Não renderiza iframe.
- Descobre a aula (`listLessons` → `find id === topico.lesson_id`) e a posição do tópico na
  aula (via `listTopicos(lesson_id)`) pra montar "Tópico {i} de {n} · {título da aula}" e
  saber qual é o **próximo tópico** da mesma aula (se houver e tiver content aprovado).
- Layout:
  - Barra superior fina (não o `CabecalhoApp` cheio): `‹ Voltar ao curso` + título da aula +
    "Tópico {i} de {n}".
  - `<iframe>` ocupando o resto da viewport (`h-[calc(100vh-...)]`, `w-full`, `border-0`),
    `src = topicoRenderUrl(topicoId, { userId: ALUNO_USER_ID })` (usa `THEME_TOPICO =
    "trigo-maduro"` por padrão). `title` acessível. `sandbox` deixado permissivo
    (`allow-scripts allow-same-origin`) — o render tem JS de navegação de slides.
  - Rodapé de ação (`./topico-ui.tsx`, `"use client"`) — ver F5.2.

## F5.2 — `topico-ui.tsx`  (`"use client"`)

Recebe `topicoId`, `estadoInicial` (`concluido` | outro), `proximoTopicoId | null`.

- Ao montar (`useEffect`, 1x): se `estadoInicial !== "concluido"`, chama
  `setTopicoProgress(topicoId, ALUNO_USER_ID, "em_andamento")` (fire-and-forget, erro só
  no console — não trava a leitura).
- Estado local `concluido: boolean` (init do `estadoInicial`).
- Não concluído: `Botao` "Marcar como concluído" → `setTopicoProgress(..., "concluido")` →
  `concluido = true` (otimista; reverte e mostra aviso discreto se o PUT falhar).
- Concluído: `Chip tom="bom"` "Concluído" + CTA:
  - `proximoTopicoId` != null → `LinkBotao` "Próximo tópico" → `/topico/{proximoTopicoId}`.
  - senão → `LinkBotao variante="fantasma"` "Voltar ao curso" → `/curso/8`.
- `router.refresh()` depois de concluir, pra árvore/hero recalcularem no próximo acesso.

## F5.3 — Sem `postMessage` por enquanto

O render (`GET /topicos/{id}/render`) não emite evento de conclusão hoje. Conclusão é
manual pelo botão. Se depois o render passar a mandar `postMessage({tipo:"topico-concluido"})`,
dá pra ouvir aqui sem mudar o resto. Fica registrado, não implementado.

---

## Aceite da FASE 3

1. `cd emaus-web && npx tsc --noEmit` → 0 erros.
2. `GET localhost:4200/topico/1` → 200, iframe com o render do "Sacerdócio de Todos os
   Crentes" no tema `trigo-maduro`. Backend registra `em_andamento` pro tópico 1
   (`GET /topico-progress/?user_id=1`).
3. Clicar "Marcar como concluído" → `status=concluido`, `concluido_em` preenchido no banco,
   CTA muda pra "Próximo tópico" (→ `/topico/2`).
4. `/inicio` e `/curso/8` refletem: T1 concluído, hero aponta pro T2.
5. `GET localhost:4200/topico/4` (T4, sem aprovar) → tela "em preparação", sem iframe.
6. Nada em `frontend/` foi tocado.

## Estado

- [~] Implementada 2026-09-03 junto com a FASE 2. `tsc --noEmit` 0 erros; `/topico/1` (iframe)
  e `/topico/4` (em preparação) verificados via `curl`. Pendente: testar o botão "Marcar como
  concluído" no navegador + conferência visual.
