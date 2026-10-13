# Auditoria — Tópico 70 "Como os 66 livros se formaram" (Lc 24:44)

Obreiro I (Course 8) · `Topico.id=70` · 2026-10-13 · régua: `fontes/obreiro/topico70-formacao-canon.md`.
Conteúdo auditado: `backend/_criar_topico70_obreiro.py` → `_topico70_obreiro_final.json` (17 slides).
**Resultado: 0 pendências.** `is_approved` = aprovação estrutural e de fontes; a leitura doutrinária
do professor teólogo e do pastor continua recomendada (arquivo no item 9) — **este é um tópico de
neutralidade forte**.

## 1. Citações bíblicas (bloco `quote`) — conferidas letra por letra contra a fonte

Script de checagem rodado sobre o JSON final: toda citação "(Almeida)" está contida no texto de
`_textos_biblicos_topico70.json` (com a correção abaixo) → **0 divergências**.

| Citação | Status |
|---|---|
| Lucas 24:44-45 | ok — ACF confere o sentido |
| Deuteronômio 31:24-26 | ok — ACF: "arca da aliança" (Almeida: "arca do pacto") |
| Neemias 8:8 | ok |
| Colossenses 4:16 | ok |
| 2 Pedro 3:15-16 | **corrigido**: a fonte traz "mas quais há" → "nas quais há" (mesmo erro visto no T66); ACF: "entre as quais" |
| Judas 3 | ok |
| Lucas 1:1-4 | **não citado**: a fonte veio com "depois de haver investido tudo" e pontuação quebrada → só paráfrase |

Trechos bíblicos curtos dentro de parágrafos e caixas (Êx 24:4; Js 24:26; 2Rs 22:8; Rm 3:2;
Jo 20:31; 1Tm 5:18; 2Pe 3:16; Jd 3) também conferidos contra a fonte: **0 fora**.

## 2. Afirmações do tópico → fonte

| Slide | Afirmação | Fonte (#) | Status |
|---|---|---|---|
| s1 | "Cânon" vem do grego *kanōn*: régua, vara de medir; regra ou padrão | 2 | ok |
| s1 | 39 + 27 = 66, presentes em todas as Bíblias cristãs; a católica tem 73 (mais 7 no AT) | 10, 11 (contas no item 3) | ok — "todas" = as duas tradições comparadas; ver s11 |
| s2 | Três partes: Lei de Moisés, Profetas, Salmos | 1 (Lc 24:44) | ok |
| s2 | Josefo: "apenas vinte e dois"; 5 + 13 + 4; ninguém ousou acrescentar nem tirar | 3 | ok — sem data (a fonte lida não dá) |
| s2 | Contagem antiga: doze profetas como um livro; os dois livros dos Reis como um (Atanásio, "bispo do século 4") | 6 (carta de 367) | ok — "não necessariamente o conteúdo": não se afirma que os 22 = 39 |
| s4 | Escrito / guardado / reencontrado / lido e explicado | 1 (Êx 24:4; Js 24:26; Jr 36:4; Dt 31:26; 2Rs 22:8; Ne 8) | ok |
| s4 | "Não foram escolhidos numa votação: foram recebidos, guardados e lidos" | 1 (Rm 3:2 + as passagens acima) | ok — descreve o que o texto mostra |
| s5 | Lucas investigou a partir das testemunhas oculares (paráfrase); João: por que escreveu | 1 (Lc 1:1-4; Jo 20:31) | ok |
| s5 | 1Tm 5:18 junta Dt 25:4 e a frase de Lc 10:7 sob "diz a Escritura" | 1 | ok — as duas frases conferidas nas três passagens |
| s5 | Pedro põe as cartas de Paulo ao lado das "outras Escrituras" | 1 (2Pe 3:16) | ok |
| s7 | Marcião: rejeitou a Lei e os Profetas, mutilou Lucas, desmembrou cartas de Paulo, pôs-se acima dos apóstolos | 4 | ok |
| s7 | "No século 2" | 5 (o Fragmento Muratoriano, de c. 170, já cita Marcião) | ok |
| s7 | O Fragmento Muratoriano não aceita escritos ligados a Marcião | 5 (linhas 81-84) | ok — **corrigido**: a 1ª versão dizia que Marcião "provocou" as listas (tese sem fonte) |
| s8 | Muratoriano: lista mais antiga conhecida do NT; Lucas 3º, João 4º; cartas de Paulo; Hermas "depois do tempo deles" | 5 | ok |
| s8 | Atanásio, 367: 4 + 1 + 7 + 14 + 1 = 27; "fontes de salvação… ninguém acrescente nem tire" | 6 | ok — reconferido em busca independente; não se diz "primeira lista" |
| s8 | Jerônimo, c. 391: Sabedoria, Eclesiástico, Judite e Tobias "não estão no cânon" | 7 | ok — a fonte diz "livro de Jesus, filho de Sirac" = Eclesiástico |
| s8 | Cartago, 397: inclui Tobias, Judite, dois de Macabeus; "recebemos de nossos pais…" | 8 | ok |
| s8 | No NT, a lista de Cartago coincide com a de Atanásio | 6, 8 (27 = 27, item 3) | ok — **corrigido**: antes dizia "as listas coincidem" (o Muratoriano não coincide) |
| s10 | Westminster (1647): 39 + 27; I.3 citado | 11 | ok — citação literal, 20 palavras |
| s10 | Trento (1546) publicou a lista; Catecismo repete; 46 + 27; nº 120 citado | 9, 10 | ok — citação literal |
| s10 | "Deuterocanônicos" × "apócrifos" = os mesmos livros | 12 | ok |
| s11 | Onde concordam: 27 do NT; os 39 estão na Bíblia católica; ambos afirmam que são Palavra de Deus | 10, 11 | ok |
| s11 | Diferença 1: sete livros; Jerônimo × Cartago | 7, 8, 9, 11 | ok |
| s11 | Diferença 2: Tradição Apostólica levou a Igreja a discernir × autoridade não depende do testemunho da Igreja, mas de Deus | 10 (nº 120), 11 (I.4) | ok |
| s11 | Ortodoxos: "não foram estudados aqui" | — | ok — **corrigido**: a 1ª versão dizia que têm "as suas próprias listas" (sem fonte lida) |
| s13 | Três atitudes do obreiro; Jd 3 | 1 + síntese do tópico | ok — aplicação, sem fato novo |

## 3. Contas (script)

Westminster AT = 39; Catecismo AT = 46; diferença = 7 (Tobias, Judite, 1 e 2 Macabeus, Sabedoria,
Eclesiástico/Ben-Sirá, Baruc); totais 66 e 73. Atanásio NT = 27; Cartago NT = 4+1+13+1+2+3+1+1+1 = 27.

## 4. Checklist do curso — neutralidade

- [x] Nenhuma frase diz que um lado "acrescentou" ou "tirou" livros (busca no JSON final por
      "acrescent", "tirou", "retir", "remov": só aparecem nas citações de Josefo e Atanásio e no caso de Marcião).
- [x] O que é comum vem ANTES da diferença (s10 e s11).
- [x] Cada tradição fala com as próprias palavras (Westminster I.3; Catecismo nº 120), no formato novo de dois slides.
- [x] A história antiga aparece com um testemunho de cada lado (Jerônimo × Cartago), e a lista de
      Atanásio é mostrada como é (o 2º slide de listas não a usa pra dar razão a ninguém).
- [x] "Este curso não toma partido" + remissão ao pastor (s11, s13, resposta-modelo do ck5_3).
- [x] Ap 22:18-19 não é usado. Nenhuma denominação é criticada.
- [x] O título "66 livros" é explicado logo no s1 como o conjunto comum, com o número católico ao lado.
- [x] Toda referência citada de passagem que sustenta o argumento virou `quote` ou trecho literal conferido.

## 5. Rascunhos (Gemini 2.5 Flash e Groq) — o que NÃO entrou

Nenhum texto dos rascunhos entrou. Erros encontrados:

- **Groq:** citação **inventada** da Confissão de Westminster ("A autoridade final da Palavra de Deus
  está em Deus mesmo; nada de humano pode acrescentar ou retirar…" — não existe no I.4); "o cânon é a
  coleção de 66 livros" (toma partido); Lutero e Calvino, Septuaginta e "critérios: autoria
  apostólica, ortodoxia e uso litúrgico" sem fonte no dossiê; deuterocanônicos como "segunda
  categoria" (a própria fonte católica lida adverte contra essa leitura); blocos inválidos.
- **Gemini:** Westminster datada de "1646" (é 1647); Marcião "aceitando apenas dez" cartas e ano
  "140" (fora do dossiê); "acréscimos de Ester e Daniel" e Septuaginta (fora do dossiê); os sete
  livros "não faziam parte do cânon hebraico original" (argumento de um lado dito como fato);
  afirmou que os ortodoxos têm os mesmos 27 livros (sem fonte lida); "não é uma lista criada por
  homens, a comunidade só reconheceu" dito como fato (é uma das duas posições).

## 6. Pedagogia

- Ordem: pergunta simples → texto central → AT → NT → caso que deu errado → listas → tradições →
  aplicação. Narrativa e exemplo antes de nomes e datas.
- Perguntas respondíveis com o ensinado (ck1: s1, s2; ck2: s4, s5; ck3: s7, s8; ck4: s10, s11;
  ck5: s8, s4–s5, s10–s13).
- Tipos: 3 `mc`, 4 `tf`, 1 `associar`, 1 `classify`, 2 `open`. Ids únicos.

## 7. Continuidade

- Abre a Aula 58 retomando a Aula 60 em uma frase; cumpre o que o T69 deixou ("história do cânon → T70").
- Não resume o enredo do AT nem do NT (T71, T72); Lc 24:27 não é desenvolvido (T73).
- `proximo_topico_label` = "Antigo Testamento: criação, aliança, reino e exílio". O "📌 Resumo" se
  sustenta sozinho (vira o "↩ Relembrando" do T71).

## 8. Direito autoral

Fontes antigas e confissões em domínio público, citadas curto e traduzidas; Catecismo: uma frase
atribuída; Guzik não foi usado no texto.

## 9. Estrutura

`validar_topico()` = `[]`; ids duplicados = nenhum; render (trigo-maduro) com 0 `None`; capa com
`imagem_capa`; 1 `fluxo`, nenhum `diagrama`; Reflexão "💭" + Resumo "📌".
Versão de leitura para o teólogo e o pastor: `curso de obreiro/topico70-formacao-canon-completo.html`.

## 10. Imagens (8: capa + 7; 10 slides de conteúdo → densidade 0,70)

Estilo editorial bíblico semi-realista (mesmo texto de estilo do T69). Todas olhadas uma a uma.

| Arquivo | Resultado |
|---|---|
| t70-capa-canon, t70-biblioteca, t70-tres-partes, t70-esdras, t70-marciao, t70-listas, t70-obreiro | ok |
| t70-carta | **refeita** — a 1ª saiu com interruptor de luz na parede e envelope moderno |

## 11. Áudio (36 blocos, MP3)

- Narrações: **todas escritas à mão** (`backend/_narracoes_topico70.py`). A geração automática ficou
  lenta (503 em série) e as 9 que saíram tomavam partido — "biblioteca composta por 66 livros",
  "o conteúdo permanece o mesmo", "o próprio Cristo valida", "garantindo a integridade do cânone" —
  inaceitável num tópico de neutralidade. Guardadas em `_audio_topico70_geradas_descartadas.json`.
  Como as citações não têm áudio, a narração vizinha traz o versículo em paráfrase próxima.
- Voz: `gemini-3.8-flash-tts`, 36/36.
- **A voz inventou conteúdo:** no bloco do Fragmento Muratoriano (s8-b1), depois da narração, o áudio
  seguia com três frases que não existem no texto ("a segunda é do ano 200, chamada Cânon de
  Alexandria…", "…ano 300, Cânon de Atanásio…", "…ano 382, Concílio de Roma…") — todas falsas ou
  sem fonte. Pego pelo conferidor (+43 palavras). Corrigido cortando o WAV em 26,6 s.
- Corte corrigido: o fim da narração do s5-b1 (o pedido de Paulo em Colossenses) tinha ficado no
  começo do s5-b3; devolvido ao arquivo certo (ponto achado medindo as pausas do WAV).
- "Obrigado." no fim do s11-b1 é invenção do Whisper (medido: silêncio depois de 30,0 s).
- `_conferir_audio.py 70 8`: 0 com problema. Produção: 44 mídias (36 MP3 + 8 imagens) em 200; diagnóstico sem ✗.
