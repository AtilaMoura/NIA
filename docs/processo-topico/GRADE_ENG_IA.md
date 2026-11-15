# Grade do curso "Engenharia de Software com IA" (curso novo no Emaús, PRIVADO)

**Status:** PROPOSTA, esperando a aprovação do Atila. Nada foi criado no banco.
Tarefa: NIA-T-028. Especificação: [eng-ia.md](eng-ia.md). Regras gerais: [BASE.md](BASE.md).

## Decisões do Atila (2026-11-14)
1. Nome: **Engenharia de Software com IA**. Curso **privado** (`visibilidade='privado'`, como o de Vendas): os exemplos
   usam os projetos reais dele (CMPort, NIA, Verdinho, Central), os PRs e os caminhos da máquina.
2. Estudo pessoal com foco em **engenheiro de IA**, 1h por dia. Ele já programou na mão: nada de lógica básica.
3. Origem: diagnóstico na Central (Sessão 1, corrigida em 14/11). O fluxo (Git, PR, CI), os hooks, a configuração e o
   MCP vieram com nota 0. Por isso o curso **abre com Fundamentos**; os módulos de IA vêm depois, sobre essa base.
4. Não repete o **Curso 5 (Engenharia de Agentes LLM)**, que ensina como o LLM e o agente funcionam por dentro. Este
   curso ensina a **construir e entregar software usando IA como ferramenta**; quando precisar do "por dentro", aponta
   para o tópico do Curso 5.
5. Comandos de terminal vão no bloco novo **`codigo`** (NIA-T-029, com botão Copiar).
6. As aulas F1 e F2 escritas na página Estudo da Central (`Central-Projetos/estudo/engenharia-ia/diagnostico/sessao-2.json`
   e `sessao-3.json`, ensaiadas em 14/11) são **rascunho e base** dos tópicos 1 a 6; passam pelo dossiê e pela auditoria
   como qualquer tópico.

## Formato
Cada aula = 3 tópicos (~20 min cada, somando 1h). O 3º tópico de cada aula costuma ser **Prática**: exercício no
repositório de treino (`C:\Users\amand\treino-git`, local, fora do OneDrive) ou leitura de um projeto real (só comandos de
leitura). Todo tópico fecha com aplicação num projeto do Atila.

## Módulo F — Fundamentos (detalhado; 8 aulas, 24 tópicos)

| Aula | Tópico | O que ensina | Proibido (é de tópico seguinte) |
|---|---|---|---|
| F1 · Git por dentro | 1. O que o Git guarda: repositório, commit e a pasta `.git` | commit = foto + autor + data + mensagem + pai; hash; o trailer Co-Authored-By | branch, remoto |
| | 2. As três áreas: pasta de trabalho, preparação e histórico | `status`, `add`, `diff`, `diff --staged`, `commit`; por que a bandeja existe | branch |
| | 3. Prática: o repositório de treino e o histórico do NIA | `init -b main`, 3 commits, `log --oneline`, `show`, HEAD e `HEAD~1`; `git -C` no NIA | merge |
| F2 · Branch, merge e worktree | 4. Branch é uma etiqueta: `switch`, fast-forward e merge commit | criar/trocar branch; os dois tipos de merge; `log --graph --all` | conflito |
| | 5. Conflito: por que acontece e como resolver | marcadores `<<<<<<<`/`=======`/`>>>>>>>`; resolver, `add`, `commit`; quando a decisão é humana | remoto |
| | 6. Worktree: duas pastas, um repositório | `worktree add/list/remove`; o `+` no `git branch`; os worktrees que a IA deixou no CMPort | PR |
| F3 · Remoto e GitHub | 7. Remoto: `origin`, `clone`, `fetch`, `pull` e `push` | commit é local; "ahead by N"; `fetch` × `pull` | PR |
| | 8. Dois remotes e fork: o caso do PinkBella e da Vercel | `remote -v`, push para dois destinos, fork × clone | revisão |
| | 9. Prática: o que está só no seu computador | conferir os 3 repositórios (Central, NIA, CMPort); remoto local simulado no treino | — |
| F4 · Pull Request e revisão | 10. Pull Request: o pedido para juntar uma branch | o que é PR, base × compare, diff, checks | CI por dentro |
| | 11. Revisão: comentário, aprovação, squash e merge | os 3 jeitos de fazer merge no GitHub; por que squash | — |
| | 12. Prática: lendo o PR #265 do CMPort com `gh` | `gh pr view`, `gh pr diff`, `gh pr checks` (só leitura) | — |
| F5 · Como ler um diff | 13. Anatomia de um diff: hunk, `+`/`-` e contexto | `@@ -a,b +c,d @@`; diff de arquivo novo, removido, renomeado | — |
| | 14. A lista de revisão: transação, corrida, segredo e efeito colateral | a lista do LEIA-ME do OpenCode, com os 3 defeitos reais que o GLM deixou passar | — |
| | 15. Prática: revisar um diff real feito pela IA | o diff da página Estudo da Central (commit `c1b0e13`) | — |
| F6 · Testes | 16. Por que testar: unitário, integração e a pirâmide | o que cada um pega; teste × verificação manual | TDD |
| | 17. pytest e vitest: ler e rodar uma suíte | `pytest -q`, `-k`, `-x`; fixture; ler `tests/test_estudo.py` | — |
| | 18. TDD do bug: o teste que falha primeiro | o fluxo da Central (teste falhando → correção → `revisar --teste`); exercício no treino | — |
| F7 · CI/CD | 19. Integração contínua: o que roda a cada PR | GitHub Actions: workflow, job, step, runner | deploy |
| | 20. Entrega contínua: homologação, produção e runner próprio | o `deploy.yml` e o `deploy-selfhosted.yml` do CMPort, as duas rotas | — |
| | 21. Quando o CI quebra: ler o log e decidir | `gh run list/view --log-failed`; teste quebrado × ambiente quebrado | — |
| F8 · Configuração, terminal e ágil | 22. Arquivos de configuração: JSON, YAML, `.env` e os três níveis de settings | sintaxe; segredo nunca no Git; usuário × projeto × local no Claude Code | hooks (M1) |
| | 23. Terminal no Windows: PowerShell × Git Bash, PATH e venv | por que `python` ≠ `.venv\Scripts\python`; o que é PATH | — |
| | 24. Ágil na prática: kanban, WIP e definição de pronto | a própria Central como exemplo (estados, revisão, "só o Atila move para feito") | — |

Fechamento do módulo: prova do módulo (padrão [PROVA.md](PROVA.md)) + reteste das competências `fluxo` e `cc-config`
na página Estudo da Central, para comparar com o diagnóstico.

## Módulos seguintes (esboço; o detalhe tópico a tópico vem numa revisão desta grade, antes de criar cada módulo)

| Módulo | Aulas previstas | Entrega prática |
|---|---|---|
| 1 · Claude Code a fundo | contexto e memória · settings e permissões · hooks · skills e comandos · subagentes · plugins, headless e Agent SDK | o setup das 3 contas auditado e enxuto |
| 2 · MCP | o protocolo · servidor stdio em Python · segurança em MCP · o MCP da Central | servidor MCP expondo o `tarefa.py` (sem a tool `fechar`) |
| 3 · IA em produção | evals · custo e latência · guardrails e prompt injection · RAG aplicado (ponte com o Curso 5) | bateria de evals do agente do Verdinho |
| 4 · Arquitetura | camadas · multi-tenant · eventos e filas · idempotência e concorrência | revisão de arquitetura do NIA |
| 5 · Engenharia de produção | observabilidade · segurança e LGPD · Docker e deploy | testes e CI no Obreiros ou no MultiDisparo |
| 6 · Linguagens atuais | Python moderno · TypeScript avançado · Next 16 (Server Components, Server Actions) · Node moderno | refatoração guiada em código seu |
| 7 · Dados | SQL analítico · pandas e Polars · DuckDB · visualização | painel de métricas (Verdinho ou CMPort) |
| 8 · ML aplicado | classificação · clustering · embeddings · avaliação | classificador clássico × LLM nas conversas do Verdinho |
| ⏸ Codex e multiagente | entra quando o Atila assinar o plano do ChatGPT | Codex como 2º revisor de PR |

## Criação no banco (depois da aprovação)
Script `backend/_criar_curso_eng_ia.py`, no modelo do `_criar_curso_vendas_internet.py`: pela API, idempotente (procura
pelo título antes de criar), local primeiro e depois `prod` com `NIA_EMAIL`/`NIA_SENHA`. Cria o curso privado, o
**Módulo F com as 8 aulas e os 24 tópicos vazios** (só título). Os módulos 1 a 8 entram depois, em nova rodada do script,
quando a grade de cada um for detalhada e aprovada. O Atila vê o plano do script antes de rodar em produção.
