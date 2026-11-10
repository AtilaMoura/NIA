# Dossiê — "Antigo e Novo Testamento: os 66 livros em um mapa"

Curso **Obreiro ACP** (Course 15 em produção) · M1 "A Palavra: a base do obreiro" · Aula 1.1 (lesson 157) · **`Topico.id=218`** (2º) · 2026-11-10.
Regras do curso: `docs/processo-topico/obreiro-acp.md` (confessional, linguagem de iniciante, sem nota de neutralidade, sem slide de tradições,
texto bíblico ACF conferido, sem número sem fonte lida).

**Público:** quem não conhece bem a Bíblia. Explicar na mesma frase: Testamento, Pentateuco, profeta, evangelho, epístola, apocalipse.

**Costura:** vem depois do **T217** (que disse que a Bíblia é uma "biblioteca" de livros, escrita por muitas pessoas, soprada por Deus) e
anunciou "o mapa". **T219** ensina a achar versículo (livro, capítulo, versículo) → o T218 **só apresenta o mapa dos 66 livros em grupos**;
não ensina a citar referência, não conta a história do cânon (como os livros foram reunidos) e não entra em autoria detalhada.

## Fonte principal: o índice de livros da ACF (primária)

`https://www.bibliaonline.com.br/acf/livros` (lido em 2026-11-10; dados estruturados da página): **66 livros, nesta ordem**; os 39 primeiros
marcados "Antigo Testamento" (Gênesis → Malaquias) e os 27 últimos "Novo Testamento" (Mateus → Apocalipse). Números de capítulos do índice:
o livro com **mais** capítulos é Salmos (150); com **menos**, Obadias, Filemom, 2 João, 3 João e Judas (1 cada). Soma dos capítulos dos cinco
"profetas maiores" (Isaías 66, Jeremias 52, Lamentações 5, Ezequiel 48, Daniel 12) = **183**; dos doze "menores" = **67**.

### Os grupos (agrupamento de estudo — os nomes dos grupos NÃO estão no texto bíblico; a ordem dos livros, sim)

| Grupo | Livros | Qtde |
|---|---|---|
| **Antigo Testamento (39)** | | |
| A Lei (Pentateuco) | Gênesis, Êxodo, Levítico, Números, Deuteronômio | 5 |
| Livros de história | Josué, Juízes, Rute, 1 e 2 Samuel, 1 e 2 Reis, 1 e 2 Crônicas, Esdras, Neemias, Ester | 12 |
| Poesia e sabedoria | Jó, Salmos, Provérbios, Eclesiastes, Cantares | 5 |
| Profetas maiores | Isaías, Jeremias, Lamentações, Ezequiel, Daniel | 5 |
| Profetas menores | Oséias, Joel, Amós, Obadias, Jonas, Miquéias, Naum, Habacuque, Sofonias, Ageu, Zacarias, Malaquias | 12 |
| **Novo Testamento (27)** | | |
| Evangelhos | Mateus, Marcos, Lucas, João | 4 |
| História da igreja | Atos | 1 |
| Cartas de Paulo | Romanos, 1 e 2 Coríntios, Gálatas, Efésios, Filipenses, Colossenses, 1 e 2 Tessalonicenses, 1 e 2 Timóteo, Tito, Filemom | 13 |
| Outras cartas | Hebreus, Tiago, 1 e 2 Pedro, 1, 2 e 3 João, Judas | 8 |
| Profecia | Apocalipse | 1 |

Soma conferida por script (`_conferir_mapa_218.py`): 5+12+5+5+12 = 39 · 4+1+13+8+1 = 27 · 39+27 = 66.

## Texto bíblico real — ACF (bibliaonline.com.br), baixado por `backend/_textos_acf_topico218.py`

Arquivo: `backend/_textos_biblicos_topico218.json` (41 passagens). Usados no texto (todos conferidos letra por letra):

| Ref. | Texto (ACF) | Uso |
|---|---|---|
| Lc 24:44 | "…tudo o que de mim estava escrito na lei de Moisés, e nos profetas e nos Salmos." | Jesus já usava grupos do AT |
| Lc 24:27 | "E, começando por Moisés, e por todos os profetas, explicava-lhes o que dele se achava em todas as Escrituras." | |
| Hb 1:1-2 | "Havendo Deus antigamente falado muitas vezes, e de muitas maneiras, aos pais, pelos profetas, a nós falou-nos nestes últimos dias pelo Filho…" | do AT ao NT |
| Lc 22:20 | "…Este cálice é o novo testamento no meu sangue, que é derramado por vós." | "testamento" |
| Jr 31:31 | "Eis que dias vêm, diz o Senhor, em que farei uma aliança nova com a casa de Israel e com a casa de Judá." | "aliança nova" |
| Gn 1:1 | "No princípio criou Deus os céus e a terra." | 1º livro |
| Sl 23:1 | "O Senhor é o meu pastor, nada me faltará." | poesia |
| Pv 1:1 | "Provérbios de Salomão, filho de Davi, rei de Israel;" | sabedoria |
| Is 1:1 | "Visão de Isaías, filho de Amós, que ele teve a respeito de Judá e Jerusalém…" | profeta |
| Mt 1:1 | "Livro da geração de Jesus Cristo, filho de Davi, filho de Abraão." | 1º do NT |
| Mc 1:1 | "Princípio do Evangelho de Jesus Cristo, Filho de Deus;" | evangelho |
| Lc 1:1-4 / At 1:1-2 | Lucas: "…ó excelente Teófilo…"; Atos: "Fiz o primeiro tratado, ó Teófilo, acerca de tudo que Jesus começou, não só a fazer, mas a ensinar" | Atos continua o 3º Evangelho |
| Rm 1:1 | "Paulo, servo de Jesus Cristo, chamado para apóstolo, separado para o evangelho de Deus." | carta de Paulo |
| Tg 1:1; Jd 1:1; 1Pe 1:1; 2Pe 1:1 | começam com Tiago / Judas / Pedro / Simão Pedro | outras cartas |
| 2Jo 1:1; 3Jo 1:1 | "O presbítero à senhora eleita…" / "O presbítero ao amado Gaio…" | cartas |
| Hb 1:1 | o texto **não** nomeia o autor | cuidado: não afirmar autor |
| Ap 1:1-3 | "Revelação de Jesus Cristo, a qual Deus lhe deu, para mostrar aos seus servos as coisas que brevemente devem acontecer…" | apocalipse = revelação |
| Mt 22:29 | "Errais, não conhecendo as Escrituras, nem o poder de Deus." | **caso que deu errado** |
| 2Tm 3:16-17 | (já visto no T217) | costura |
| At 17:11 | "…examinando cada dia nas Escrituras se estas coisas eram assim." | caso real: examinar |

**Conferência dos 13 começos:** os versículos 1 das 13 cartas de Paulo (Rm a Fm) começam com "Paulo" (em Fp e 1-2Ts, "Paulo e Timóteo" / "Paulo, e Silvano, e Timóteo").
Hebreus não traz nome no texto → vai em "outras cartas" **sem dizer quem escreveu**.

## Fontes

| # | Tipo | Referência | Acesso | O que usei |
|---|---|---|---|---|
| 1 | Primária | Texto bíblico ACF + índice de livros (https://www.bibliaonline.com.br/acf/livros) | 2026-11-10 (lidos) | 66 livros em ordem, 39+27, nº de capítulos, todas as citações |
| 2 | Léxico | Blue Letter Bible, Strong G1242 *diathḗkē* (https://www.blueletterbible.org/lexicon/g1242/kjv/tr/0-1/): "disposition, arrangement… a testament or will; a compact, a covenant" | 2026-11-10 (lida) | "Testamento" na Bíblia em português traduz uma palavra que também quer dizer **aliança** |
| 3 | Léxico | BLB Strong G2098 *euangélion*: "good tidings" (https://www.blueletterbible.org/lexicon/g2098/kjv/tr/0-1/) | 2026-11-10 (lida) | evangelho = boa notícia |
| 4 | Léxico | BLB Strong G602 *apokálypsis*: "an uncovering… a disclosure of truth" (https://www.blueletterbible.org/lexicon/g602/kjv/tr/0-1/) | 2026-11-10 (lida) | apocalipse = revelação (o 1º versículo do livro já diz "Revelação de Jesus Cristo") |
| 5 | Referência | Wikipédia (pt), "Cânone bíblico" (https://pt.wikipedia.org/wiki/C%C3%A2none_b%C3%ADblico): "Todas as grandes tradições cristãs aceitam os protocânone hebraico inteiramente… todas elas, com exceção dos protestantes, aceitam também os livros deuterocanônicos"; protestantes defendem o cânone da Bíblia hebraica e o católico para o NT (27 livros) | 2026-11-10 (lida) | **uma frase** sobre a Bíblia católica ter livros a mais no AT (sem número) |
| 6 | Dado | Pró-Livro 2024 (já usado no T217) | — | não repetido |
| 7 | Caso real (bíblico) | At 17:11 — os de Bereia examinavam as Escrituras todos os dias | — | Estudar com método; o mapa ajuda a achar o livro |
| 8 | Caso que deu errado (bíblico) | Mt 22:29 — "Errais, não conhecendo as Escrituras" | — | Quem não conhece a Bíblia erra; conhecer o mapa é o 1º passo |

Tipos cobertos: primária, léxico, referência, caso real, caso que deu errado, dado (índice) — **6 de 8**; sem comentarista moderno neste tópico (o assunto é um mapa, não uma interpretação).
**Fontes que não consegui ler:** SBB, Britannica, ag.org (403). Nada delas entra.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| A Bíblia tem 66 livros: 39 no AT e 27 no NT | 1 | ok (índice da ACF) |
| Ordem dos livros e agrupamentos (Lei 5, história 12, poesia 5, profetas maiores 5, menores 12; Evangelhos 4, Atos 1, cartas de Paulo 13, outras 8, Apocalipse 1) | 1 | ok — **grupos são de ensino**; o texto diz isso |
| "Maiores" e "menores" = tamanho, não importância (183 x 67 capítulos) | 1 | ok — contagem feita no índice |
| Jesus falou da "lei de Moisés, profetas e Salmos" (Lc 24:44) | 1 | ok |
| "Testamento" = aliança (Lc 22:20 "novo testamento"; Jr 31:31 "aliança nova"; Strong G1242) | 1, 2 | ok |
| Evangelho = boa notícia; Apocalipse = revelação | 3, 4, 1 | ok |
| As 13 cartas de Paulo começam com o nome dele; Hebreus não traz nome | 1 | ok (versículos lidos) |
| Atos é o "segundo volume" do 3º Evangelho: ambos a Teófilo | 1 | ok — não afirma que "Lucas" escreveu (nome não consta no texto lido) |
| Alguns livros têm 1 capítulo; Salmos tem 150 | 1 | ok |
| Outras tradições (como a católica) têm mais livros no AT | 5 | ok — **1 frase**, sem número |

## Divergências entre fontes
- **66 × mais livros:** divergência real entre igrejas. Regra do curso: 1 frase e volta à posição da ACP (66, como nas Bíblias evangélicas em português).
  Nota: a Declaração de Fé da ACP não chegou; "66 livros" é o que a Bíblia ACF lida traz.
- **Autoria de Hebreus e de alguns livros:** discutida; o tópico **não** afirma autor onde o texto não nomeia.
- **Agrupamentos:** variam entre manuais (ex.: a Bíblia hebraica agrupa em Lei, Profetas e Escritos). O tópico usa o agrupamento mais comum nas Bíblias em português e diz que é um agrupamento de estudo.

## O que ficou de fora (e por quê)
- Como achar versículo (livro, capítulo, versículo) → **T219**. Não ensinar siglas (Gn, Mt) além de nomes completos.
- História da formação do cânon, manuscritos, Septuaginta, deuterocanônicos em detalhe → outra aula.
- Resumo de cada livro → o curso continua; aqui só o mapa.
- Datas de escrita e autoria detalhada → o T217 já mostrou que são pessoas reais; detalhes não são do nível de quem começa.
- Comentário de Guzik/clássicos → o tópico é mapa, não exegese.
