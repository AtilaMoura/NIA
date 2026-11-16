# Auditoria — Tópico 306 "Prática: o repositório de treino e o histórico do NIA"

Curso 16 (privado) · Módulo F · Aula F1 · 2026-11-16 · auditor: Claude (Opus 5.5).
Conteúdo: `backend/_criar_topico306_eng_ia.py`. Dossiê: [topico306-pratica-treino.md](topico306-pratica-treino.md) (#1–#12).

## 1. Fato
| Slide | Afirmação | Fonte | Status |
|---|---|---|---|
| s1 | treino-git em C:\Users\amand\treino-git, fora do OneDrive; mudar só no treino | eng-ia.md, GRADE | ok |
| s2 | identidade vai em todo commit e fica gravada para sempre | #2 | ok |
| s2 | saída de `git config user.name/email` | #10 | ok |
| s2 | saída "Author identity unknown" | #11 (ensaio) | ok, conferida |
| s2 | GitHub só conta contribuição se o e-mail estiver ligado à conta | #9 | ok |
| s3 | mkdir/cd/init -b main/status e saída | #10 | ok |
| s3 | init cria repositório vazio, basicamente a .git | #1 | ok |
| s3 | sem -b o padrão ainda é master; muda para main no Git 3.0 | #1, #2 | ok |
| s4 | 1º commit + log, saída; root-commit = sem pai | #10, 304 | ok |
| s4 | log do mais novo ao mais velho, hash/autor/data/mensagem | #3, 304 (#4) | ok |
| s6 | 2º e 3º commits, status com notas.txt modificado, log --oneline | #10 | ok |
| s6 | --oneline = --pretty=oneline --abbrev-commit | #3 (manual local 2.46) | ok |
| s7 | HEAD = commit em que baseou as mudanças; ~n = n-ésimo ancestral pelo primeiro pai | #5 | ok |
| s7 | show HEAD~1 (mensagem + diff), cat-file -p HEAD, rev-parse HEAD~1 iguais | #4, #10 | ok |
| s7 | `.git\HEAD` = `ref: refs/heads/main`; HEAD aponta para a branch local; a main aponta para o último commit | #10, #7, 304 (#3: refs guardam ponteiros para commits) | ok |
| s9 | -C roda como se estivesse na pasta | #6 | ok |
| s9 | log --oneline -5 do NIA e show --stat 3e6b16e, saídas | #12 | ok |
| s9 | --stat = resumo por arquivo; 3 arquivos, 125 +, 1 − | #4 (manual local: "Generate a diffstat"), #12 | ok |
| s10 | FILA.md: 1 entrou, 1 saiu (124 + nos dois dossiês = 61 + 63; total 125/1) | #12 (aritmética) | ok (corrigido: a 1ª versão dizia "2 linhas mexidas") |
| s11 | estado final ` M notas.txt` + 3 commits | #10, 305 (status -s) | ok |
| s11 | a F2 começa guardando a terceira linha | Central sessao-3.json | ok |
| s* | hashes do aluno serão outros (commit inclui autor e hora; hash do conteúdo) | 304 | ok |

Fato de alto risco refeito: a prática inteira foi rodada do zero (ensaio) com a identidade real; o erro de identidade foi provocado de verdade; `--oneline` e `--stat` lidos no manual instalado porque a leitura web voltou só em resumo.

## 2. Erros dos rascunhos que não entraram
| Rascunho | Erro |
|---|---|
| gpt-oss-120b | saída de `git log` com hash `a1b2c3d4e5f6g7h8…` (nem é hexadecimal), autor e data inventados |
| gpt-oss-120b | arquivo `notes.txt` (é `notas.txt`), "aula de grounding", "agente de vendas", `catalogo.csv` |
| gpt-oss-120b | `git log --stat -5` no NIA e caminho `/caminho/para/nia_repo` (não ensaiado) |
| Gemini 3.5 Flash | "ferramentas automáticas de inspeção do NIA usam o hash de 7 dígitos" (inventado) |
| Gemini 3.5 Flash | `echo` em vez de Set-Content, `roteador.py`/`config.json`, caminho `/home/atila/...` |
| Gemini 3.5 Flash | último passo "adicione a linha 'Rascunho de ideias…'" (diferente do ensaio e quebra a continuidade com a F2) |
| Gemini 3.5 Flash | "o Git checa user.name no .git/config local" (a busca é em vários níveis; fora do dossiê); bloco `vocab` de inglês |

## 3. Pedagogia
Prática passo a passo, cada comando com a saída real logo abaixo; checkpoints perguntam o que o aluno viu (ck1_1, ck2_2, ck3_1) e as abertas pedem a saída dele (ck4_3) e a explicação do estado (ck4_4). Todas respondíveis com o tópico e os anteriores.

## 4. Direito autoral
Manuais e Pro Git em paráfrase; saídas do ensaio próprio. ok

## 5. Continuidade
Usa 304 (root-commit, cat-file, 3e6b16e, 7fdbe90) e 305 (preparação, status -s). Não ensina branch/switch/merge (só "é a próxima aula"). Deixa o treino-git no estado que a F2 espera.

## 6. Estrutura
`validar_topico()` = `[]` (a 1ª versão tinha 25 min, fora da faixa; ajustado para 20); render menta-grafite: 0 `None`, 23 blocos `codigo`; fluxo (s7); Reflexão + Resumo 📌 (s12); mc, tf, associar, classify, lacuna, 2 open; 18 ids únicos; capa + 4 imagens em 9 slides de conteúdo (0,44).

## Resultado
**0 pendências.** Liberado para imagens e publicação.
