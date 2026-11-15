# Auditoria — Tópico 304 "O que o Git guarda: repositório, commit e a pasta .git"

Curso 16 (privado) · Módulo F · Aula F1 · 2026-11-14 · auditor: Claude (Opus 5.5).
Conteúdo auditado: `backend/_criar_topico304_eng_ia.py` → `_topico304_eng_ia_final.json`. Dossiê: [topico304-o-que-o-git-guarda.md](topico304-o-que-o-git-guarda.md) (fontes #1–#13).

## 1. Fato (afirmação → fonte → status)
| Slide | Afirmação | Fonte | Status |
|---|---|---|---|
| s1 | NIA tinha 170 commits em 14/11/2026, 148 com Co-Authored-By | #10 (`rev-list --count`, `--grep -i`) | ok |
| s1 | Curso 5 ensina o LLM por dentro | GRADE_ENG_IA.md decisão 4 | ok |
| s2 | Repositório = projeto + `.git`; Pro Git: metadados e banco de objetos | #1, #3 | ok |
| s2 | `.git` recém-criada: hooks, info, objects, refs, config, description, HEAD (Git 2.46, Windows) | #11 (saída real), #3 | ok |
| s2 | objects = conteúdo; refs = ponteiros para commits; HEAD = onde você está; index aparece depois e guarda a preparação | #3 | ok |
| s2 | Copiar a `.git` leva quase tudo; apagar a `.git` apaga o histórico, arquivos visíveis ficam | #3 (+ consequência direta: histórico só existe na .git, #1) | ok |
| s4 | Git pensa em snapshots, não em diferenças; arquivo igual vira referência | #1 | ok |
| s4 | Cada commit aponta para o pai; o primeiro não tem pai | #2, #10, #11 | ok |
| s4 | 7fdbe90 de 22/11/2025 "Colocando o projeto no git", sem pai; 0e713a3 = T220; 3e6b16e de 11/11/2026 = T221, pai 0e713a3; 163 commits entre 7fdbe90 e 0e713a3 | #10 (log, cat-file, rev-list 166 − 3) | ok (corrigido: a 1ª versão dizia 167) |
| s4 | Quase toda operação é local | #1, #9 | ok |
| s5 | `cat-file -t` dá o tipo, `-p` mostra o conteúdo; `-C` escolhe a pasta | #2; `-C`: rascunho F1 ensaiado + saídas reais #10 | ok |
| s5 | Saída do `cat-file -p 3e6b16e` | #10, copiada; e-mails ocultos | ok (conferida caractere a caractere com a saída) |
| s5 | Data = segundos desde 1970 + fuso | #13, #2 | ok |
| s5 | author = quem escreveu; committer = quem aplicou por último | #4 | ok |
| s5 | author vem de user.name/user.email | #2 | ok |
| s7 | SHA-1, 40 hexadecimais, calculado do conteúdo; endereçado por conteúdo, chave-valor | #1, #2 | ok |
| s7 | blob = conteúdo sem nome; tree = nomes → hashes; commit = tree raiz + pai + autor + mensagem | #2, #10 | ok |
| s7 | tree do 3e6b16e e `hash-object .gitignore` = 1ff680c… (iguais) | #10 (saídas reais) | ok |
| s7 | `^{tree}` entre aspas simples no PowerShell; `hash-object` sem `-w` não grava | #2 (aspas); manual `git-hash-object` do Git 2.46: "Computes the object ID value…" e `-w` = "Actually write the object into the object database" | ok |
| s7 | Hash completo de 3e6b16e; mínimo 4 caracteres sem ambiguidade; log abreviado usa 7; objects/xx/ + 38 | #10, #12, #2 | ok |
| s8 | SHAttered: 23/02/2017, CWI Amsterdam + Google, dois PDFs diferentes, mesmo SHA-1, 1ª colisão real | #8, #7 | ok |
| s8 | Git ≥ 2.13.0: SHA-1 endurecido, não vulnerável ao SHAttered; SHA-1 ainda fraco; SHA-256 escolhido no fim de 2018; `objectFormat = sha256` | #7 | ok |
| s8 | "o padrão ainda é SHA-1" | #12 ("is moving towards using SHA256 as the default"), #10 (NIA e ensaio novo saem `sha1` no Git 2.46) | ok |
| s8 | NIA: `sha1` | #10 | ok |
| s10 | Trailer: chave e valor com dois-pontos, bloco no fim, linha em branco antes; Signed-off-by, Reviewed-by, Helped-by | #5 | ok |
| s10 | GitHub: uma linha `Co-authored-by: nome <e-mail>` por coautor, depois de linha em branco; e-mail ligado à conta para contar contribuição | #6 | ok |
| s10 | Claude Code grava `Co-Authored-By`; mesmo trailer | #10 (mensagem real) + divergência registrada no dossiê | ok (não afirma regra de maiúscula) |
| s10 | Central: `pessoa_de` procura o trailer antes do login/nome/e-mail | #10 (código lido) | ok |
| s11 | `cat-file -p HEAD` mostra o último commit | #2 (cat-file), HEAD como ponteiro #3 | ok |
| s11 | Levar para o GitHub é outro passo (F3) | GRADE | ok (sem ensinar push) |

**Fato de alto risco refeito (busca independente):** o hash do `.gitignore` foi recalculado (`hash-object`) e conferido contra a tree; a data do 3e6b16e conferida com `log --date=iso` (2026-11-11 10:11:21 -0300 = timestamp 1794402681); a contagem de commits recalculada com `rev-list`; SHAttered conferido em duas fontes (#7 manual do Git, #8 shattered.io).

## 2. Erros dos rascunhos que NÃO entraram
| Rascunho | Erro | Por quê ficou de fora |
|---|---|---|
| gpt-oss-120b | Saída de `cat-file -p` com hashes inventados (`8b1a2c3d…`) e e-mail `atila@gardencenter.com` | Viola a regra "saída real"; usei a saída real do NIA |
| gpt-oss-120b | "O Git passou a incluir um prefixo de tipo antes do hash" como resposta ao SHAttered | Falso: o cabeçalho de tipo sempre existiu; a resposta foi o SHA-1 endurecido (#7) |
| gpt-oss-120b | Linha do tempo "2018–2020 hardening" | Errado: SHA-1 endurecido na 2.13.0 (#7) |
| gpt-oss-120b | SHA-256 tem espaço "2^128 vezes maior" | Errado (256 − 160 = 96 bits) e fora do dossiê |
| gpt-oss-120b | `git log --show-signature` extrai coautores | Falso (é assinatura GPG) |
| gpt-oss-120b | SHAttered "liderado pelo Google" | Incompleto: CWI Amsterdam + Google (#8) |
| gpt-oss-120b | Fluxo com staging/"nothing to commit" | Assunto do tópico 305 |
| Gemini 3.5 Flash | NIA descrito como "agente de vendas do Garden Center", tool `check_stock` | Inventado (vazou do `PERFIL_TECH`); o NIA é a plataforma de cursos |
| Gemini 3.5 Flash | "Se o .gitignore estiver vazio, retorna e69de29…" | Fora do dossiê e o `.gitignore` do NIA não está vazio |
| Gemini 3.5 Flash | biblioteca `sha1dc` "de Marc Stevens"; Linus Torvalds em 2005; PDFs "fundo vermelho e azul"; cabeçalho `tipo tamanho\0` | Nada disso está no dossiê → removido |
| Gemini 3.5 Flash | "Nas aulas anteriores…" | Este é o 1º tópico do curso |
| Gemini 3.5 Flash | "o trailer NÃO pode ter texto comum abaixo dele, senão…" | Regra mais detalhada do que a fonte lida (#5 diz só que o bloco fica no fim); não usado |

Aproveitado dos rascunhos: a ideia do contraste "coautoria escrita solta × trailer" (Gemini) e o alerta "apagar a .git" (gpt-oss), reescritos a partir de #3 e #5.

**Achado para a tarefa NIA-T-028 (não é deste tópico):** o `PERFIL_TECH` tem `contexto_curso` fixo do Garden Center; para este curso os rascunhos vão sempre puxar esse contexto. Registrar como pendência (mexer em `perfis.py` é código de `backend/app`, fora do `/criar-topico`).

## 3. Pedagogia
- Toda pergunta é respondível com o ensinado: ck1 (s2), ck2 (s5 e o 7fdbe90 de s4), ck3_1 (s7, hash não depende do nome; o caso do `.gitignore`), ck3_2 (s8), ck4_1 (cards de s7), ck4_2 (s5), ck4_3 (s7 box "o mesmo hash"), ck4_4 (s11). ok
- Ordem: repositório → foto → commit por dentro → hash → caso que deu errado → trailer → aplicação. Exemplo real antes da abstração em s5 e s7. ok
- Pergunta prática "o que este comando vai mostrar?" (ck3_1) e "qual comando você roda?" (ck4_2, ck4_4): exigência do eng-ia.md cumprida.
- Nível: não ensina lógica nem sintaxe; parte do que o Atila já vê a IA fazer. ok

## 4. Direito autoral
Pro Git (CC BY-NC-SA 3.0): só paráfrase atribuída ("o Pro Git define…", "segundo o Pro Git"); nenhuma citação longa. Manual do Git e GitHub Docs: paráfrase. ok

## 5. Continuidade
1º tópico do curso: sem anterior. Não invade o 305 (as três áreas só aparecem como "o index… assunto do próximo tópico") nem o 306 (nenhum `init`/commit na mão; HEAD só citado; treino-git só mencionado). Branch e push só nomeados como "aula de branch" / "aula F3". ok

## 6. Estrutura
- `validar_topico()` = `[]`; render no tema `menta-grafite`: 0 `None`; 9 blocos `codigo` (contados no DOM do render; conferidos no navegador: claro, escuro, 375 px sem rolagem lateral da página, Copiar com recurso Ctrl+C).
- Capa com `imagem_capa`, `roteiro`, `badges_capa`; `fluxo` (s4), nenhum `diagrama`; `cols2` (s5, s10); Reflexão "💭 Pra pensar" + Resumo `summary` "📌" (s12); bullets do resumo se sustentam sozinhos.
- Perguntas: mc, tf, associar, lacuna, classify e **2 open** (ck4_3, ck4_4); 18 ids únicos no tópico.
- Imagens: capa + 4 inline em 8 slides de conteúdo (0,5 por slide, dentro da meta 0,4–0,6 do eng-ia.md); nenhuma com comando ou texto.

## 7. Checklist do curso (eng-ia.md)
- [x] Comandos no bloco `codigo` com `linguagem` e `titulo`; PowerShell primeiro.
- [x] Nos projetos reais, só leitura (`cat-file`, `hash-object` sem `-w`, `rev-parse`, `Get-ChildItem`).
- [x] Sem segredo, `.env`, token, IP ou dado de cliente; e-mails trocados por `<e-mail>`. Hash, nome de arquivo e caminho local podem aparecer (curso privado).
- [x] Fecha com "onde isso aparece no seu trabalho" (s11) e o caso da Central (s10).
- [x] Saídas mostradas são as reais (rodadas em 14/11/2026).

## Resultado
**0 pendências de fato.** Aprovado para imagens. Publicação **bloqueada por dependência de código**: o tópico usa o bloco `codigo` (NIA-T-029), que ainda não está em produção; publicar antes faria a produção renderizar 11 blocos desconhecidos. PUT só depois do deploy do Atila.
