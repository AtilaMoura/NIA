# Auditoria — Tópico 305 "As três áreas: pasta de trabalho, preparação e histórico"

Curso 16 (privado) · Módulo F · Aula F1 · 2026-11-16 · auditor: Claude (Opus 5.5).
Conteúdo: `backend/_criar_topico305_eng_ia.py` → `_topico305_eng_ia_final.json`. Dossiê: [topico305-as-tres-areas.md](topico305-as-tres-areas.md) (#1–#11).

## 1. Fato
| Slide | Afirmação | Fonte | Status |
|---|---|---|---|
| s1 | O index na .git guarda a preparação (visto no 304) | 304 / #4 | ok |
| s2 | Três seções (Pro Git); index "também conhecido como área de preparação", usado para preparar o próximo commit | #1, #4 | ok |
| s2 | add → preparação; commit grava o que está na preparação; histórico na .git | #2, #4, #10 | ok |
| s2 | untracked = não estava no último commit e não foi preparado; tracked = estava ou foi preparado; sem mudança/modificado/preparado | #2 | ok |
| s4 | git status = ferramenta principal para saber o estado | #2 | ok |
| s4 | 3 saídas (untracked; to be committed com `git rm --cached`; commit d29936d + working tree clean) | #10, copiadas | ok (conferidas com a saída do ensaio) |
| s4 | significado dos 4 cabeçalhos | #2, #10 | ok |
| s4 | o status mostra como desfazer (Pro Git); `rm --cached` antes do 1º commit, `restore --staged` depois | #3, #10 | ok |
| s5 | add copia o conteúdo daquele momento; mudou depois → outro add; arquivo nas duas listas | #2, #4, #10 | ok |
| s5 | saída "nas duas listas" | #10 | ok (passo 9 do ensaio) |
| s5 | commit grava a preparação, não o disco; a 3ª linha fica fora | #2, #10 (após restore só `M` na direita) | ok |
| s7 | diff = pasta × preparação; --staged = preparação × último commit; --cached sinônimo | #2, #5 | ok |
| s7 | saída do diff; diff vazio depois do add; --staged mostra o mesmo diff | #10 | ok |
| s7 | "git diff sozinho não mostra tudo… só o que ainda não foi preparado" | #2 | ok |
| s7 | status -s: esquerda = preparação, direita = pasta; ??, M, A; `MM`/`??` reais | #2, #10 | ok |
| s7 | restore --staged tira da bandeja sem perder; a partir do 2.23 | #3, #10 | ok |
| s8 | MIT: escolher o que entra; duas funcionalidades → dois commits; prints de depuração + correção | #6 | ok |
| s8 | git add -p escolhe pedaços (hunks) | #4, #6 | ok |
| s8 | c1b0e13: 14/11/2026, página Estudo, outra sessão nos mesmos arquivos (api.py, central.css), 15 arquivos, só os trechos da IA, comandos de baixo nível | #9 (`git show --stat` + registro da sessão) | ok |
| s10 | `git add .` prepara tudo, inclusive arquivo novo | #11, #10 | ok (corrigido: faltava fonte na 1ª versão) |
| s10 | commit -a prepara o que já é rastreado; pode incluir mudança indesejada; não pega arquivo novo | #2 | ok |
| s10 | GitHub: revogar/trocar primeiro; não dá para apagar das cópias clonadas | #7 | ok |
| s10 | 23.770.171 segredos novos em repositórios públicos do GitHub em 2024 (State of Secrets Sprawl 2025, GitGuardian) | #8 | ok (atribuído; dado do próprio levantamento) |
| s11 | status/diff/diff --staged só leem | #2, #5 (comparam, não gravam) | ok |

Fato de alto risco refeito: o comportamento do `git add .` com arquivo novo foi rodado (#10) e lido no manual (#11); a saída do status em duplo estado foi gerada de novo no ensaio; o número do GitGuardian conferido literalmente na página.

## 2. Erros dos rascunhos que não entraram
| Rascunho | Erro | Motivo |
|---|---|---|
| Gemini 3.5 Flash | c1b0e13 como "correção emergencial de endpoint" com `git add -p central/routes.js` e "logs de depuração" | Inventado: o caso real é preparação seletiva entre duas sessões (#9) |
| Gemini 3.5 Flash | atalhos "adicionam indistintamente… arquivos não rastreados" (vale para `add .`, não para `commit -a`) | Mistura os dois; corrigido com #2 |
| Gemini 3.5 Flash | arquivos `src/courses/llm.ts`, `roteador.py`, "licença MIT", "push e scrapers" | Fora do dossiê / fora do escopo (remoto é F3) |
| qwen3.8-27b | saída de status com "Your branch is up to date with 'origin/main'" e `src/agenda.py` | Saída inventada; usado só o ensaio |
| qwen3.8-27b | Garden Center (cacto.txt, garden-center, "estoque") | Proibido no pedido; vazou do PERFIL_TECH |
| qwen3.8-27b | c1b0e13 com "prints em módulo de cálculo de preço", `git add -p src/calc…` | Inventado |
| qwen3.8-27b | `commit -a` "captura config.env" novo | Falso: -a não pega untracked (#2) |
| qwen3.8-27b | "a maioria dos vazamentos ocorreu por comandos genéricos" | Não está na fonte (#8) |
| ambos | lista de teclas do `add -p` (y/n/q…) | Não lida em fonte; fora |

Aproveitado: "o commit grava a preparação, não o disco" (Gemini) e a ideia dos cards do `status -s`.

## 3. Pedagogia
- Perguntas respondíveis: ck1 (s2), ck2_1 (box de cabeçalhos s4), ck2_2 (s5), ck3_1 (cols2 s7 + restore), ck3_2 (s7 "diff vazio"), ck4_1 (s10), ck4_2 (s7), ck4_3 (s8), ck4_4 (s11). ok
- Prática "o que este comando vai mostrar?" (ck3_2) e "qual comando…?" (ck4_2, ck4_4). ok
- Ordem: áreas → status → add no tempo → diff → por quê → risco → aplicação.

## 4. Direito autoral
Pro Git, manuais, MIT, GitHub e GitGuardian em paráfrase atribuída; saídas são do ensaio próprio. ok

## 5. Continuidade
Usa o vocabulário do 304 (index, foto, .git, blob `070f62d` no diff). Não invade o 306: nenhum passo cria repositório; os comandos que alteram ficam como "você roda no próximo tópico". Branch/remoto/push não ensinados; diff por dentro → F5; .env → F8. ok

## 6. Estrutura
`validar_topico()` = `[]`; render `menta-grafite`: 0 `None`, 14 blocos `codigo`; fluxo (s2), cols2 (s2, s7), cards (s7); Reflexão + Resumo 📌 (s12), bullets autossuficientes; perguntas mc, tf, associar, classify, lacuna, 2 open; 18 ids únicos; capa + 4 inline em 9 slides de conteúdo (0,44; meta do curso 0,4–0,6).

## 7. Checklist do curso
- [x] Comandos em `codigo` com linguagem e título, PowerShell.
- [x] Nos projetos reais só leitura (status, diff); add/commit/restore marcados como "só no treino".
- [x] Sem segredo, `.env` real, token, IP ou dado de cliente.
- [x] Aplicação no trabalho (s11) e caso real (s8).
- [x] Saídas reais (ensaio 2026-11-16).

## Resultado
**0 pendências.** Liberado para imagens e publicação (o bloco `codigo` está em produção desde 2026-11-15).
