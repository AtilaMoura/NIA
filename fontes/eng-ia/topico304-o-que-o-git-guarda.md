# Dossiê — O que o Git guarda: repositório, commit e a pasta .git

Curso 16 (Engenharia de Software com IA, privado) · Módulo F · Aula F1 "Git por dentro" · Tópico 1 de 3 · `Topico.id=304` (prod).
Vizinhos: (nenhum antes, é o 1º do curso) → **305 "As três áreas: pasta de trabalho, preparação e histórico"** → 306 "Prática: o repositório de treino e o histórico do NIA".
**Proibido aqui** (é de tópico seguinte): branch, remoto, `push`, as três áreas em detalhe (`add`/`status`/`diff`, tópico 305), `init`/`log`/`HEAD~1` como exercício (tópico 306).
Rascunho de base: Central `estudo/engenharia-ia/diagnostico/sessao-2.json` (F1, bloco "Explicação").

## Fontes
| # | Tipo | Referência | Acesso em | O que usei |
|---|---|---|---|---|
| 1 | Primária / livro-texto | Chacon & Straub, *Pro Git* 2ª ed., cap. 1.3 "What is Git?" — git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F (CC BY-NC-SA 3.0) | 2026-11-14 | Snapshots, não diferenças ("Git thinks of its data more like a series of snapshots of a miniature filesystem"); arquivo igual vira "just a link to the previous identical file it has already stored"; quase toda operação é local; "Everything in Git is checksummed before it is stored and is then referred to by that checksum"; SHA-1 de "40-character string composed of hexadecimal characters"; "Git stores everything in its database not by file name but by the hash value of its contents"; "The Git directory is where Git stores the metadata and object database for your project." |
| 2 | Primária / livro-texto | *Pro Git*, cap. 10.2 "Git Objects" — git-scm.com/book/en/v2/Git-Internals-Git-Objects | 2026-11-14 | "Git is a content-addressable filesystem"; "a simple key-value data store"; três tipos: blob, tree, commit; o commit "specifies the top-level tree…; the parent commits if any…; the author/committer information (… user.name and user.email … and a timestamp); a blank line, and then the commit message"; 1º commit sem pai; `git cat-file -p` e `-t`; objetos em `.git/objects`, subpasta = 2 primeiros caracteres, arquivo = 38 restantes; no PowerShell, `{}` entre aspas simples (`'master^{tree}'`). |
| 3 | Primária / livro-texto | *Pro Git*, cap. 10.1 "Plumbing and Porcelain" — git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain | 2026-11-14 | Conteúdo de `.git` recém-criado: config, description, HEAD, hooks/, info/, objects/, refs/; "four important entries: the HEAD and (yet to be created) index files, and the objects and refs directories"; objects guarda o conteúdo, refs guarda ponteiros para commits, HEAD aponta para a branch atual, index guarda a área de preparação; "If you want to back up or clone your repository, copying this single directory elsewhere gives you nearly everything you need." |
| 4 | Primária | *Pro Git*, cap. 2.3 "Viewing the Commit History" — git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History | 2026-11-14 | `git log` em "reverse chronological order", com SHA-1, autor, e-mail, data, mensagem; "The author is the person who originally wrote the work, whereas the committer is the person who last applied the work." |
| 5 | Primária (manual) | git-scm.com/docs/git-interpret-trailers | 2026-11-14 | "A trailer in its simplest form is a key-value pair with a colon as a separator"; "The trailer block needs to be preceded by a blank line"; "at the end of the commit message"; exemplos Signed-off-by, Reviewed-by, Helped-by. |
| 6 | Oficial (fornecedor) | GitHub Docs, "Creating a commit with multiple authors" — docs.github.com/…/creating-a-commit-with-multiple-authors | 2026-11-14 | "Add one `Co-authored-by: name <name@example.com>` line for each co-author"; linha em branco depois da descrição; e-mail precisa estar associado à conta no GitHub para contar como contribuição. **Não** afirma em detalhe como a tela mostra os coautores → o tópico não descreve a tela do GitHub. |
| 7 | Primária (manual) | git-scm.com/docs/hash-function-transition | 2026-11-14 | "the SHAttered attack … demonstrated a practical SHA-1 hash collision"; "Git v2.13.0 and later subsequently moved to a hardened SHA-1 implementation by default, which isn't vulnerable to the SHAttered attack, but SHA-1 is still weak"; "In late 2018 the project picked SHA-256 as its successor hash"; config `objectFormat = sha256`. |
| 8 | Caso que deu errado / pesquisa | shattered.io (CWI Amsterdam + Google) | 2026-11-14 | 23/02/2017: "the first real collision for the SHA-1 hash function"; "Two PDF files, visibly different and carrying different content, share one identical SHA-1 value"; "Git added collision detection". |
| 9 | Livro (independente) | Winters, Manshreck & Wright, *Software Engineering at Google*, cap. 16 — abseil.io/resources/swe-book/html/ch16.html | 2026-11-14 | "A VCS is a system that tracks revisions (versions) of files over time"; "version control is the engineer's primary tool for managing the interplay between raw source and time"; DVCS: "downloading the entire codebase and having access to it locally". |
| 10 | Caso real (projeto do Atila) | Repositório NIA, saídas reais de `git` rodadas em 2026-11-14 (abaixo) | 2026-11-14 | Commit `3e6b16e` por dentro; tree; blob do `.gitignore`; 1º commit `7fdbe90` sem pai; 170 commits, 148 com `Co-Authored-By`; formato de objeto `sha1`. |
| 12 | Primária / livro-texto | *Pro Git*, cap. 7.1 "Revision Selection", seção "Short SHA-1" e nota "A short note about SHA-1" — git-scm.com/book/en/v2/Git-Tools-Revision-Selection | 2026-11-14 | "as long as that partial hash is at least four characters long and unambiguous"; `--abbrev-commit` "defaults to using seven characters but makes them longer if necessary"; "Generally, eight to ten characters are more than enough to be unique within a project"; colisões podem ser sintetizadas (cita shattered.io). |
| 13 | Primária (manual instalado) | `git-commit.html` do Git 2.46.0 (C:\Program Files\Git\mingw64\share\doc\git-doc), seção DATE FORMATS, "Git internal format" | 2026-11-14 | `<unix-timestamp> <time-zone-offset>`, o timestamp é o "number of seconds since the UNIX epoch". |
| 11 | Ensaio (dado real) | Repositório descartável no scratchpad, Git 2.46.0.windows.1, PowerShell | 2026-11-14 | `.git` recém-criado; 1º commit sem `parent`; 2º commit com `parent` e trailer; pastas de 2 caracteres em `.git/objects`. |

Tipos cobertos: primária/oficial (1–7), livro-texto (1–4, 9), caso que deu errado (8), pesquisa (8), caso real (10), dado real/ensaio (10, 11), fornecedor (6) → **6 tipos**. Atlassian (git-init, what-is-version-control) foi tentado e a página não carregou o corpo: não usado.

## Saídas reais (copiar para o tópico só destas)
NIA (`git -C C:\Users\amand\OneDrive\Documentos\NIA …`), e-mails trocados por `<e-mail>` no tópico:
```
> git cat-file -t 3e6b16e
commit
> git cat-file -p 3e6b16e
tree 08d9ec5230926f1878fcce0086b43cf3321957f2
parent 0e713a35c77c46ac87aa1c0356a911ec46b4a451
author AtilaMoura <e-mail> 1794402681 -0300
committer AtilaMoura <e-mail> 1794402681 -0300

obreiro-acp T221 Observar, entender, aplicar (2º da Aula 1.2): dossiê com fontes lidas, auditoria e fila

Co-Authored-By: Claude Opus 5.5 <e-mail>
> git rev-parse 3e6b16e
3e6b16ed302d9eead5ba9badf528de436405eba0
> git cat-file -p '3e6b16e^{tree}'   (primeiras linhas)
040000 tree 1805d812aa9130c50b88ba5ce2dd36317e91d3f2	.agente-front
100644 blob c89a5adca597f47096b39c0bf3b981f0bfe2a1dd	.dockerignore
…
100644 blob 1ff680c6205d8052c927c63392132ac743231715	.gitignore
> git hash-object .gitignore
1ff680c6205d8052c927c63392132ac743231715
> git log -1 --format="%h %ad" --date=iso 3e6b16e
3e6b16e 2026-11-11 10:11:21 -0300
> git rev-list --max-parents=0 HEAD
7fdbe90a091ae5dc9ce386e0259bb0f1ce45183b
> git cat-file -p 7fdbe90   (sem linha parent)
tree e89a6058f273967953699034aa5173dd84a06d8b
author … / committer …
Colocando o projeto no git          (2025-11-22)
> git rev-list --count HEAD          → 170
> git rev-list --count 3e6b16e       → 166 (logo, entre 7fdbe90 e 0e713a3 há 163)
> git rev-list --count -i --grep="Co-Authored-By" HEAD → 148
> git rev-parse --show-object-format → sha1
```
Ensaio (repositório descartável, `Get-ChildItem -Force .git` logo depois do `git init -b main`): `hooks info objects refs config description HEAD`.

## Afirmações centrais
| Afirmação | Fontes | Status |
|---|---|---|
| Repositório = projeto + a pasta `.git`, onde ficam os metadados e o banco de objetos | 1, 3, 9 | ok |
| Commit = foto (snapshot) do projeto inteiro, não lista de diferenças; arquivo que não mudou vira referência ao já guardado | 1, (9 "tracks revisions") | ok |
| Objeto commit contém: tree, pai(s), author, committer (nome, e-mail, data/hora), linha em branco, mensagem | 2, 10, 11 | ok (visto na saída real) |
| O primeiro commit não tem pai | 2, 10, 11 | ok |
| Os commits ligados pelo pai formam o histórico; `git log` mostra do mais novo ao mais velho | 2, 4 | ok |
| Data no objeto commit = segundos desde 1970 (época UNIX) + fuso | 13, 2 | ok |
| Author = quem escreveu; committer = quem aplicou | 4 | ok (só primária; conceito simples, baixo risco) |
| Três tipos de objeto: blob (conteúdo de arquivo), tree (pasta: nomes → hashes), commit | 2, 10 | ok |
| Hash SHA-1 = 40 caracteres hexadecimais, calculado a partir do conteúdo; o Git guarda pelo hash, não pelo nome | 1, 2, 10 (`.gitignore` = blob da tree) | ok |
| Mesmo conteúdo → mesmo hash; conteúdo diferente → hash diferente (por isso o Git percebe corrupção) | 1, 2, 10 | ok |
| Abreviação: os primeiros caracteres bastam se não forem ambíguos (`3e6b16e` → hash completo) | 12, 10 (rev-parse real) | ok — mínimo 4, sem ambiguidade; o `log --oneline` mostra 7 |
| Objetos em `.git/objects/xx/yyyy…` (2 + 38 caracteres) | 2, 11 | ok |
| `.git` recém-criado tem config, description, HEAD, hooks, info, objects, refs; o index só aparece depois | 3, 11 | ok |
| Copiar a pasta `.git` leva quase tudo do repositório; apagar a `.git` = perder o histórico (os arquivos da pasta continuam) | 3 (+ dedução direta de 1/3) | ok — formulado como consequência: "o histórico mora na .git" |
| Quase tudo é local; o commit fica no seu computador | 1, 9 | ok (sem falar de push: é F3) |
| Trailer = linha `Chave: valor` no fim da mensagem, depois de linha em branco | 5, 6 | ok |
| `Co-authored-by: nome <e-mail>` é a forma que o GitHub documenta para coautoria | 6 | ok |
| A Central atribui ao Claude o commit que tem o trailer dele, antes de olhar o author | 10 (código `pessoa_de`) | ok |
| SHAttered (2017, CWI + Google): 1ª colisão real de SHA-1, dois PDFs diferentes com o mesmo hash | 7, 8, 12 | ok |
| Git ≥ 2.13.0 usa SHA-1 endurecido, não vulnerável ao SHAttered; SHA-256 escolhido como sucessor (fim de 2018), `objectFormat = sha256` | 7 (+8 "Git added collision detection") | ok |
| NIA hoje usa `sha1` | 10 | ok |

## Casos reais
- **NIA, commit `3e6b16e` (11/11/2026)**: o tópico T221 do Obreiro ACP. Por dentro: tree, parent `0e713a3`, author e committer AtilaMoura, mensagem e o trailer `Co-Authored-By: Claude Opus 5.5`. Mostra que o "autor" no Git é a configuração da máquina (AtilaMoura) e a IA aparece só no trailer.
- **NIA, 1º commit `7fdbe90` (22/11/2025)** "Colocando o projeto no git": sem pai.
- **148 de 170 commits** do NIA têm o trailer de coautoria (na data do tópico): quase todo o histórico foi feito com a IA.
- **Central de Projetos**, `central/services/atividade_itens.py`, função `pessoa_de` (lida em 2026-11-14): para decidir de quem é um commit, procura primeiro o `trailer` de cada pessoa do `projetos.json` na mensagem (o do Claude), depois login do GitHub, nome do Git e e-mail. Ou seja: na Central, o commit com `Co-Authored-By: Claude` conta como do Claude, embora o author seja AtilaMoura.
- O `.gitignore` do NIA tem hash `1ff680c…`, o mesmo que aparece na tree do commit: o Git achou o arquivo pelo conteúdo.

## Caso que deu errado
- **SHAttered (23/02/2017)**: pesquisadores do CWI Amsterdam e do Google produziram dois PDFs diferentes com o mesmo SHA-1. Como o Git identifica tudo pelo hash, isso ameaçava a garantia "hash igual = conteúdo igual". Resposta do Git: SHA-1 endurecido a partir da 2.13.0 (detecta esse ataque) e plano de troca para SHA-256 (escolhido no fim de 2018).

## Divergências entre fontes
- shattered.io fala em "collision detection"; o manual do Git fala em "hardened SHA-1 implementation". É a mesma mitigação descrita com palavras diferentes; o tópico usa "SHA-1 endurecido, que detecta esse tipo de ataque".
- GitHub escreve `Co-authored-by` (minúsculas); o Claude Code grava `Co-Authored-By`. O manual de trailers não fixa maiúsculas; o tópico mostra os dois como o mesmo trailer, sem afirmar regra de maiúscula.

## O que ficou de fora (e por quê)
- `add`/`status`/`diff` e a área de preparação em detalhe → tópico 305. Aqui só a frase "antes do commit você escolhe o que entra; é o próximo tópico".
- `git init` e criar commits na mão → tópico 306 (prática). Aqui só leitura no NIA e as saídas do ensaio.
- HEAD e refs: só citados como "arquivos da .git"; HEAD vira assunto no 306 e branch na F2.
- Remoto, `push`, "ahead by N" → F3. Packfiles, `git gc`, formato interno zlib → fora do nível.
- Como o GitHub desenha os coautores na tela → a fonte não detalha; não afirmado.
