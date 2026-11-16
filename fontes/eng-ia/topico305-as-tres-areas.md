# Dossiê — As três áreas: pasta de trabalho, preparação e histórico

Curso 16 (privado) · Módulo F · Aula F1 "Git por dentro" · Tópico 2 de 3 · `Topico.id=305` (prod).
Vizinhos: **304 "O que o Git guarda"** (repositório, `.git`, commit por dentro, hash, trailer; publicado 2026-11-15) → **306 "Prática: o repositório de treino e o histórico do NIA"** (`init -b main`, 3 commits, `log --oneline`, `show`, HEAD, `HEAD~1`, `git -C`).
**Proibido aqui:** branch, remoto, push; criar o `treino-git` e o exercício completo (306); `log`/`show`/HEAD~1 como exercício (306).
Do 304 o aluno já sabe: `.git` tem objects, refs, HEAD, config; o index "só aparece depois do primeiro uso e guarda a área de preparação"; commit = foto + pai; hash do conteúdo; blob/tree/commit.
Rascunho de base: Central `estudo/engenharia-ia/diagnostico/sessao-2.json` (F1, 2º bloco de texto e passos 2–4).

## Fontes
| # | Tipo | Referência | Acesso | O que usei |
|---|---|---|---|---|
| 1 | Primária / livro-texto | *Pro Git*, cap. 1.3 "What is Git?", seção "The Three States" — git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F | 2026-11-14 | três estados (modified, staged, committed) e três seções (working tree, staging area, Git directory) — lido no T304. |
| 2 | Primária / livro-texto | *Pro Git*, cap. 2.2 "Recording Changes to the Repository" — git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository | 2026-11-16 | "Tracked files are files that were in the last snapshot, as well as any newly staged files; they can be unmodified, modified, or staged"; "Untracked files are everything else"; `git status` é "the main tool you use to determine which files are in which state"; cabeçalhos "Untracked files", "Changes to be committed", "Changes not staged for commit"; `git add` "to begin tracking new files, to stage files, and to do other things like marking merge-conflicted files as resolved"; "add precisely this content to the next commit"; "Git stages a file exactly as it is when you run the git add command"; "If you modify a file after you run git add, you have to run git add again"; arquivo "listed as both staged and unstaged"; `status -s`: "the left-hand column indicates the status of the staging area and the right-hand column indicates the status of the working tree", `??`, `A`, `M`, exemplo `MM`; `git diff` "compares what is in your working directory with what is in your staging area"; `--staged` "compares your staged changes to your last commit"; "(--staged and --cached are synonyms)"; "git diff by itself doesn't show all changes made since your last commit — only changes that are still unstaged"; `commit` sem `-m` "launches your editor of choice"; `commit -a` "makes Git automatically stage every file that is already tracked before doing the commit" e "be careful; sometimes this flag will cause you to include unwanted changes". |
| 3 | Primária / livro-texto | *Pro Git*, cap. 2.4 "Undoing Things", "Unstaging a Staged File with git restore" — git-scm.com/book/en/v2/Git-Basics-Undoing-Things | 2026-11-16 | `git restore --staged <file>` tira da preparação; "the command you use to determine the state of those two areas also reminds you how to undo changes to them"; "From Git version 2.23.0 onwards, Git will use git restore instead of git reset for many undo operations". |
| 4 | Primária (manual) | git-scm.com/docs/git-add | 2026-11-16 | "The "index" (also known as the "staging area") is what you use to prepare the contents of the next commit"; "It only adds the content of the specified file(s) at the time the add command is run"; `-p`/`--patch`: "Interactively choose hunks of patch between the index and the work tree and add them to the index". |
| 5 | Primária (manual) | git-scm.com/docs/git-diff | 2026-11-16 | `git diff`: "changes you made relative to the index (staging area for the next commit)"; `--cached`: "changes you staged for the next commit relative to the named <commit>", padrão HEAD; "--staged is a synonym of --cached". |
| 6 | Material de instituição (independente) | MIT, *The Missing Semester of Your CS Education* (2020), aula "Version Control (Git)", seção "Staging area" — missing.csail.mit.edu/2020/version-control/ | 2026-11-16 | a área de preparação permite "specify which modifications should be included in the next snapshot"; cenários: "two separate features, and you want to create two separate commits" e "debugging print statements added all over your code, along with a bugfix"; "git add -p: interactive staging". |
| 7 | Oficial (fornecedor) | GitHub Docs, "Removing sensitive data from a repository" | 2026-11-16 | "as a first step you need to revoke and/or rotate that secret"; "You cannot remove sensitive data from other users' clones of your repository"; continua acessível em forks. Não diz literalmente "apagar num commit novo não basta" (só implica: remover exige reescrever o histórico). |
| 8 | Dado / estatística | GitGuardian, *State of Secrets Sprawl 2025* — gitguardian.com/state-of-secrets-sprawl-report-2025 | 2026-11-16 | "In 2024, we found 23,770,171 new hardcoded secrets added to public GitHub repositories." |
| 9 | Caso real (Central) | Commit `c1b0e13` da Central (14/11/2026, CEN-T-052) + registro da sessão de trabalho | 2026-11-16 | 15 arquivos, inclusive `central/routers/api.py` (+26) e `web/css/central.css` (+17). Outra sessão do Claude mexia ao mesmo tempo em `api.py`, `central.css`, `tarefa.py` e outros; a IA pôs na preparação só os trechos dela (com comandos de baixo nível, `hash-object`/`update-index`), e as mudanças da outra sessão ficaram de fora, intactas. |
| 11 | Primária (manual instalado) | `git-add.html` do Git 2.46.0, opções `-A/--all` e `--no-all` | 2026-11-16 | o add atualiza o index "by adding new files that are unknown to the index" e, com `-A`, "adds, modifies, and removes index entries to match the working tree". |
| 10 | Ensaio (dado real) | Repositório descartável, Git 2.46.0.windows.1, PowerShell, 2026-11-16 | 2026-11-16 | saídas reais abaixo. |

Tipos: primária/livro-texto (1–5), material de instituição (6), fornecedor (7), dado (8), caso real (9), ensaio (10), caso que deu errado (7+8) → **6 tipos**.

## Saídas reais (ensaio; autor "Atila", e-mail de exemplo)
```
> Set-Content notas.txt "Minha primeira linha"; git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notas.txt

nothing added to commit but untracked files present (use "git add" to track)

> git add notas.txt; git status
...
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   notas.txt

> git commit -m "primeiro commit: cria notas.txt"
[main (root-commit) d29936d] primeiro commit: cria notas.txt
 1 file changed, 1 insertion(+)
 create mode 100644 notas.txt

> git status
On branch main
nothing to commit, working tree clean

> Add-Content notas.txt "Segunda linha"; git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   notas.txt

no changes added to commit (use "git add" and/or "git commit -a")

> git diff
diff --git a/notas.txt b/notas.txt
index 070f62d..1491e1c 100644
--- a/notas.txt
+++ b/notas.txt
@@ -1 +1,2 @@
 Minha primeira linha
+Segunda linha

> git add notas.txt; git diff        → (nada)
> git diff --staged                  → o mesmo diff acima

> Add-Content notas.txt "Terceira linha"; git status
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   notas.txt

Changes not staged for commit:
  ...
	modified:   notas.txt

> Set-Content tarefas.txt "comprar cabo"; git status -s
MM notas.txt
?? tarefas.txt

> git restore --staged notas.txt; git status -s
 M notas.txt
?? tarefas.txt

> git add .; git status -s
M  notas.txt
A  tarefas.txt          ← o arquivo novo entrou junto
```
Observação do ensaio: antes do 1º commit a dica para tirar da preparação é `git rm --cached`; depois, `git restore --staged`.
`070f62d` no diff = o mesmo blob de "Minha primeira linha" visto no T304 (`070f62d9…`).

## Afirmações centrais
| Afirmação | Fontes | Status |
|---|---|---|
| Três áreas: pasta de trabalho, área de preparação (index/staging), histórico (.git) | 1, 4, 6 | ok |
| Arquivo novo é untracked até o primeiro add; tracked = estava no último commit ou foi preparado | 2, 10 | ok |
| `git status` diz em que estado cada arquivo está; cabeçalhos e dicas reais | 2, 10 | ok |
| `git add` põe na preparação o conteúdo do arquivo **naquele momento**; mudou depois, precisa de outro add (arquivo aparece nas duas listas) | 2, 4, 10 | ok |
| `git commit` grava no histórico só o que está na preparação | 2, 1, 10 (após restore, notas.txt modificado fica fora) | ok |
| `git diff` = pasta de trabalho × preparação (só o que ainda não foi preparado) | 2, 5, 10 | ok |
| `git diff --staged` (= `--cached`) = preparação × último commit (o que vai entrar) | 2, 5, 10 | ok |
| `status -s`: coluna esquerda = preparação, direita = pasta; `??`, `A`, `M`, `MM` | 2, 10 | ok |
| `git restore --staged` tira da preparação sem perder a mudança; `git status` ensina como desfazer | 3, 10 | ok |
| `restore` existe a partir do Git 2.23.0 | 3 | ok |
| Por que a preparação existe: escolher o que entra; duas features → dois commits; tirar print de debug | 6 (+ 2 "add precisely this content") | ok |
| `git add -p` escolhe trechos (hunks) de um arquivo | 4, 6 | ok |
| `commit -a` prepara tudo o que já é rastreado e pode incluir mudança indesejada; não pega arquivo novo | 2 (untracked não é "already tracked"), rascunho F1 ensaiado | ok |
| `commit` sem `-m` abre o editor | 2 | ok |
| `git add .` prepara tudo da pasta, inclusive arquivo novo | 11, 10 (`A  tarefas.txt`) | ok |
| Segredo que entrou num commit: revogar/trocar primeiro; não dá para tirar dos clones | 7 | ok |
| 23.770.171 segredos novos em repositórios públicos do GitHub em 2024 | 8 | ok (só 1 fonte: é dado do próprio levantamento, atribuído) |
| Caso c1b0e13: só os trechos da IA entraram; os da outra sessão ficaram fora | 9 | ok |

## Caso real
- Central `c1b0e13` (ver #9). Mostra a preparação seletiva num caso de verdade: dois agentes mexendo nos mesmos arquivos, e um commit que leva só o trabalho de um. Para o aluno, o jeito normal de fazer isso é `git add -p`; a IA usou comandos de baixo nível.

## Caso que deu errado
- Preparar tudo sem olhar (`git add .`, `commit -a`) leva para o histórico o que não devia, por exemplo um arquivo com senha. GitHub: o primeiro passo é revogar/trocar o segredo, e as cópias em clones não podem ser apagadas (#7). Escala: 23,77 milhões de segredos novos em commits públicos no GitHub em 2024 (#8). O tópico não ensina remoção do histórico (assunto de F8/Módulo 5), só por que olhar o `git diff --staged` antes do commit.

## Divergências
- Pro Git chama a preparação de "staging area"; o manual do `git add` diz "index (also known as the staging area)". Mesma coisa; o tópico usa "área de preparação (index)".
- Dica do `git status` muda conforme o estado: `git rm --cached` antes do primeiro commit, `git restore --staged` depois (#10). Pro Git mostra exemplos antigos com `git reset HEAD` (#3).

## O que ficou de fora
- Criar o `treino-git` e o exercício completo → 306. Aqui nada cria repositório: o aluno lê as saídas reais do ensaio.
- `git restore <arquivo>` (descartar mudança da pasta) → perigoso; só citado como "a dica que o Git mostra", sem ensinar.
- `.gitignore` em detalhe e remoção de segredo do histórico → F8 / Módulo 5.
- Branch, merge, remoto → F2/F3.
