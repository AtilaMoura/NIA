# Especificação — Engenharia de Software com IA (curso privado; Course.id = 16 em produção)

Segue a [BASE](BASE.md). Grade: [GRADE_ENG_IA.md](GRADE_ENG_IA.md). Status: **APROVADA** (NIA-T-028).
Produção: curso 16, Módulo F id 60, aulas 181–188, tópicos 304–327 (criados em 2026-11-14).

- **Tema:** `menta-grafite` (diferente do `azul-petroleo` do Curso 5).
- **Estilo das imagens:** `isometrico-claro` com a paleta do tema (grafite, menta, verde-água, toque âmbar); `sketchnote`
  só se um resumo pedir. Prompt-base no `_criar_topico304_eng_ia.py` (constante `ESTILO`).
- **Pendências de código (vão no deploy do Atila, fora do /criar-topico):** `TEMA_POR_CURSO[16] = "menta-grafite"` em
  `emaus-web/app/_lib/config.ts`; `PERFIL_TECH.contexto_curso` fixo no Garden Center faz o rascunho da IA inventar
  contexto (visto no T304) — criar um perfil próprio para este curso.
- **Perfil de agente:** `PERFIL_TECH` (`backend/app/agents/perfis.py`).
- **Público:** só o Atila (curso privado). Nível: já programou na mão; não ensinar lógica nem sintaxe básica.

## Passo 1 — Fonte
- Fonte primária = documentação oficial, lida (WebFetch), nunca de memória:
  - Git: livro **Pro Git** (git-scm.com/book, licença CC BY-NC-SA 3.0: trecho curto citado com atribuição; o resto em
    paráfrase) e as páginas de manual em git-scm.com/docs.
  - GitHub: docs.github.com (PR, Actions, `gh`).
  - Testes: docs do pytest e do vitest.
  - CI/CD: docs do GitHub Actions; Martin Fowler ("Continuous Integration"); DORA/Accelerate para as métricas.
  - Claude Code, MCP e Agent SDK: docs oficiais da Anthropic e a especificação em modelcontextprotocol.io.
- Fonte independente (a 2ª de cada afirmação central): Atlassian Git Tutorials, livro *Software Engineering at Google*
  (abseil.io/resources/swe-book, leitura gratuita), MDN quando for web.
- **O próprio projeto do Atila é fonte de caso real**: commit, PR, workflow, teste e configuração reais, citados pelo
  caminho e pelo hash. Comando que aparece no tópico tem que ter sido **rodado de verdade** (ensaio numa pasta temporária)
  antes de publicar; a saída mostrada é a saída real.
- Caso que deu errado, quando couber: `git push --force` que apaga trabalho, segredo commitado (e por que apagar o arquivo
  não resolve), merge sem revisão que quebrou produção, e os 3 defeitos que o GLM deixou passar (LEIA-ME do OpenCode).

## Passo 2 — Escrita
- O Atila **não consegue revisar fato técnico** deste curso (é o que ele está aprendendo): mesma regra do curso de Redes.
  Toda opção de comando, nome de arquivo e comportamento vem da documentação oficial.
- Comandos sempre no bloco **`codigo`** (NIA-T-029), com `linguagem` (`powershell`, `bash`, `python`, `json`, `yaml`,
  `diff`) e `titulo` curto. Exemplo para Windows primeiro (PowerShell); Git Bash só quando for diferente.
- Exercício que **altera** algo: sempre no repositório de treino `C:\Users\amand\treino-git`. Nos projetos reais, só
  leitura (`log`, `show`, `diff`, `branch`, `worktree list`, `gh pr view/diff/checks`, `gh run view`).
- Nunca mostrar segredo, `.env`, token, IP interno de cliente, nem dado de cliente (nome de condomínio, telefone, valor).
  Hash de commit, número de PR e nome de arquivo podem aparecer (curso privado).
- Fechar todo tópico com aplicação: "onde isso aparece no seu trabalho" (CMPort, NIA, Verdinho, Central).
- Mecanismo = `fluxo` (ex.: pasta de trabalho → preparação → histórico). Comparação = `cols2`.
- Perguntas: além do mínimo da BASE, pelo menos 1 pergunta prática do tipo "o que este comando vai mostrar?" ou "qual
  comando você roda para…?".

## Passo 6 — Imagens
- Meta mais baixa que nos outros cursos (0,4–0,6 por slide de conteúdo): aqui o que ensina é o `fluxo` e o `codigo`.
  Imagem nunca com texto de comando dentro (a IA de imagem inventa letras).

## Passo 7 — Áudio
- Narração nunca lê comando caractere por caractere: descreve ("o comando git status, que mostra o que mudou").
  Siglas faladas por extenso na 1ª vez (PR = pull request, CI = integração contínua).
