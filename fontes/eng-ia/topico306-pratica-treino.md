# Dossiê — Prática: o repositório de treino e o histórico do NIA

Curso 16 (privado) · Módulo F · Aula F1 "Git por dentro" · Tópico 3 de 3 (prática) · `Topico.id=306` (prod).
Vizinhos: **305 "As três áreas"** (status, add, diff, diff --staged, commit, restore --staged, status -s; publicado 2026-11-16) → **307 "Branch é uma etiqueta: switch, fast-forward e merge commit"** (abre a F2).
**Proibido aqui:** branch (criar/trocar), merge, remoto, push. HEAD só como "onde você está"; dizer que `main` é o nome da linha principal e que branch é a próxima aula.
Do 304/305 o aluno já sabe: .git, commit = foto + pai + autor + mensagem, hash, `cat-file -p`, trailer; três áreas, status/add/diff/commit.
**Continuidade com a F2:** o rascunho da F2 (Central `sessao-3.json`) começa com `git commit -am "guarda a terceira linha"`, contando que o `notas.txt` ficou modificado no fim desta prática. Então a prática termina com o `notas.txt` modificado e diz para deixar assim.
Estado da máquina (2026-11-16): `C:\Users\amand\treino-git` **não existe** → este tópico cria. `core.autocrlf=true` no sistema; identidade global `AtilaMoura`.

## Fontes
| # | Tipo | Referência | Acesso | O que usei |
|---|---|---|---|---|
| 1 | Primária (manual) | git-scm.com/docs/git-init | 2026-11-16 | "creates an empty Git repository - basically a .git directory"; `-b <branch-name>`/`--initial-branch`: "Use <branch-name> for the initial branch"; sem a opção, nome padrão hoje `master` (configurável por `init.defaultBranch`) e "this will change to main when Git 3.0 is released". |
| 2 | Primária / livro-texto | *Pro Git*, 1.6 "First-Time Git Setup" | 2026-11-16 | "every Git commit uses this information, and it's immutably baked into the commits you start creating"; `--global` uma vez só; `git config --list` e `git config user.name` para conferir; padrão `master` e `git config --global init.defaultBranch main`. |
| 3 | Primária (manual) | git-scm.com/docs/git-log + manual local 2.46 | 2026-11-16 | "Shows the commit logs"; "reverse chronological order by default"; `--oneline` "is a shorthand for --pretty=oneline --abbrev-commit used together" (manual local). |
| 4 | Primária (manual) | git-scm.com/docs/git-show + manual local 2.46 | 2026-11-16 | "For commits it shows the log message and textual diff"; `--stat` "Generate a diffstat" (manual local). |
| 5 | Primária (manual) | git-scm.com/docs/gitrevisions | 2026-11-16 | HEAD "names the commit on which you based the changes in the working tree"; `<rev>~<n>` "the <n>th generation ancestor… following only the first parents"; `<rev>~3` = `<rev>^^^`; `<rev>^` = primeiro pai. |
| 6 | Primária (manual) | git-scm.com/docs/git, opção `-C` | 2026-11-16 | "Run as if git was started in <path> instead of the current working directory". |
| 7 | Livro-texto | *Pro Git*, 3.1 "Branches in a Nutshell" | 2026-11-16 | HEAD "is a pointer to the local branch you're currently on" (só para explicar o `ref: refs/heads/main`). |
| 8 | Material de instituição (independente) | MIT Missing Semester, "Version Control (Git)" (lido no 305) | 2026-11-16 | comandos básicos (`git init`, `git add`, `git commit`, `git log`) — mesma sequência da prática. |
| 9 | Oficial (fornecedor) | GitHub Docs, "Creating a commit with multiple authors" (lido no 304) | 2026-11-14 | e-mail precisa estar associado à conta para contar como contribuição → identidade errada tem consequência. |
| 10 | Ensaio (dado real) | Prática completa rodada em pasta descartável, PowerShell 5.1, Git 2.46.0.windows.1, identidade real do Atila (e-mail oculto) | 2026-11-16 | todas as saídas abaixo. |
| 11 | Caso que deu errado (ensaio) | Commit sem identidade configurada (config global vazia) | 2026-11-16 | saída "Author identity unknown … Please tell me who you are". |
| 12 | Caso real | Repositório NIA: `git log --oneline -5` e `git show --stat 3e6b16e` (2026-11-16) | 2026-11-16 | saídas reais. |

Tipos: primária (1–6), livro-texto (2, 7), instituição (8), fornecedor (9), ensaio/dado (10), caso que deu errado (11), caso real (12) → **7 tipos**.

## Saídas reais do ensaio (e-mail trocado por `<e-mail>`; hashes do ensaio — os do aluno serão outros)
```
> git config user.name            → AtilaMoura
> git config user.email           → <e-mail>

> mkdir C:\Users\amand\treino-git; cd C:\Users\amand\treino-git; git init -b main
Initialized empty Git repository in C:/Users/amand/…/treino-git/.git/
> git status
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)

> Set-Content notas.txt "Minha primeira linha"; git add notas.txt; git commit -m "primeiro commit: cria notas.txt"
[main (root-commit) bb5b032] primeiro commit: cria notas.txt
 1 file changed, 1 insertion(+)
 create mode 100644 notas.txt
> git log
commit bb5b032bca7ffaff315e1da62ecd8ef9358664c5
Author: AtilaMoura <e-mail>
Date:   Mon Nov 16 08:49:47 2026 -0300

    primeiro commit: cria notas.txt

> Add-Content notas.txt "Segunda linha"; git add notas.txt; git commit -m "acrescenta a segunda linha"
[main 6910cb0] acrescenta a segunda linha
 1 file changed, 1 insertion(+)

> Set-Content tarefas.txt "comprar cabo"; Add-Content notas.txt "Terceira linha"; git add tarefas.txt; git commit -m "cria tarefas.txt"
[main 5682d4d] cria tarefas.txt
 1 file changed, 1 insertion(+)
 create mode 100644 tarefas.txt
> git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   notas.txt

no changes added to commit (use "git add" and/or "git commit -a")
> git log --oneline
5682d4d cria tarefas.txt
6910cb0 acrescenta a segunda linha
bb5b032 primeiro commit: cria notas.txt

> git show HEAD~1
commit 6910cb0294c24543271a0148416c4eab9936e59a
Author: AtilaMoura <e-mail>
Date:   Mon Nov 16 08:49:47 2026 -0300

    acrescenta a segunda linha

diff --git a/notas.txt b/notas.txt
index 070f62d..1491e1c 100644
--- a/notas.txt
+++ b/notas.txt
@@ -1 +1,2 @@
 Minha primeira linha
+Segunda linha

> git cat-file -p HEAD
tree c681e482efe422d15cf33918b83070afeb42ee94
parent 6910cb0294c24543271a0148416c4eab9936e59a
author AtilaMoura <e-mail> 1794829787 -0300
committer AtilaMoura <e-mail> 1794829787 -0300

cria tarefas.txt
> git rev-parse HEAD~1   → 6910cb0294c24543271a0148416c4eab9936e59a
> git rev-parse HEAD~2   → bb5b032bca7ffaff315e1da62ecd8ef9358664c5
> Get-Content .git\HEAD  → ref: refs/heads/main
> git show --stat HEAD
commit 5682d4d2d89331f1aefcd9f02b7808407f750b70
Author: AtilaMoura <e-mail>
Date:   Mon Nov 16 08:49:47 2026 -0300

    cria tarefas.txt

 tarefas.txt | 1 +
 1 file changed, 1 insertion(+)
```
Sem aviso de CRLF no ensaio (Windows, `core.autocrlf=true`).

Caso que deu errado (#11), commit sem `user.name`/`user.email` (máquina e usuário ocultos):
```
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got '<usuário>@<máquina>')
```

NIA (#12), 2026-11-16:
```
> git -C C:\Users\amand\OneDrive\Documentos\NIA log --oneline -5
1488626 eng-ia T305 As três áreas (curso 16, F1): …
ffab49c deploy 2026-11-15 feito: bloco codigo (NIA-T-029) e tema do curso 16 nas 2 VMs; …
4de08b9 emaus: tema menta-grafite para o curso 16 (…)
e063a29 NIA-T-029 bloco "codigo" no renderizador de tópicos: …
4f6d4b1 eng-ia T304 O que o Git guarda (curso 16, F1): …
> git -C …\NIA show --stat 3e6b16e
commit 3e6b16ed302d9eead5ba9badf528de436405eba0
Author: AtilaMoura <e-mail>
Date:   Wed Nov 11 10:11:21 2026 -0300

    obreiro-acp T221 Observar, entender, aplicar (2º da Aula 1.2): dossiê com fontes lidas, auditoria e fila

    Co-Authored-By: Claude Opus 5.5 <e-mail>

 docs/processo-topico/FILA.md                       |  2 +-
 ...opico221-observar-entender-aplicar-auditoria.md | 63 ++++++++++++++++++++++
 .../topico221-observar-entender-aplicar.md         | 61 +++++++++++++++++++++
 3 files changed, 125 insertions(+), 1 deletion(-)
```

## Afirmações centrais
| Afirmação | Fontes | Status |
|---|---|---|
| `git init` cria repositório vazio (a pasta .git) | 1, 10 | ok |
| `-b main` dá o nome `main` à linha inicial; sem ela hoje o padrão é `master` (configurável; muda para `main` no Git 3.0) | 1, 2 | ok |
| Identidade (user.name/email) vai em todo commit e fica gravada para sempre nele; conferir com `git config user.name` | 2, 10 | ok |
| Sem identidade o commit falha com "Author identity unknown" | 11 | ok |
| E-mail errado: GitHub não conta como contribuição | 9 | ok |
| `git log` lista do mais novo ao mais velho; `--oneline` = uma linha, hash curto | 3, 10 | ok |
| `git show` mostra mensagem e diff; `--stat` mostra resumo por arquivo | 4, 10, 12 | ok |
| HEAD = o commit em que você está trabalhando; aponta para a linha atual (`ref: refs/heads/main`) | 5, 7, 10 | ok |
| `HEAD~1` = pai de HEAD; `HEAD~2` = avô; seguem o primeiro pai | 5, 10 (rev-parse bate com o parent do cat-file e com o log) | ok |
| `-C <pasta>` roda o Git como se estivesse naquela pasta | 6, 12 | ok |
| Hashes do aluno serão diferentes (commit inclui autor e data; hash vem do conteúdo) | 304 (#2 do dossiê 304: commit contém author/date; hash do conteúdo) | ok |
| No fim, `notas.txt` fica modificado (a 3ª linha não foi preparada) | 10, 305 | ok |

## Caso real
- NIA: `log --oneline -5` mostra os commits destes próprios tópicos e do deploy; `show --stat 3e6b16e` mostra 3 arquivos, 125 inserções, 1 remoção, com trailer de coautoria.

## Caso que deu errado
- Commit numa máquina sem identidade → erro (#11). Pior quando a identidade está errada e nada avisa: o nome e o e-mail ficam gravados para sempre nos commits (#2), e o GitHub não liga os commits à conta se o e-mail não estiver associado (#9).

## Divergências
- Nome da linha inicial: o manual diz que o padrão ainda é `master` e vai para `main` no Git 3.0; o Pro Git ensina a configurar `init.defaultBranch main`. O tópico usa `-b main` explícito para não depender disso.

## O que ficou de fora
- Configurar identidade (`git config --global user.name …`) como passo: o Atila já tem; o tópico só manda conferir (leitura). Se faltar, a própria mensagem de erro mostra os comandos.
- `git log` com `--graph --all` e branch → F2. `HEAD^2` (segundo pai de merge) → F2.
- `.gitignore`, remoto → F3/F8.
