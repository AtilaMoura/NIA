# Auditoria — T195 "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto

Conteúdo auditado: `backend/_criar_topico195_ingles.py` → `_topico195_ingles_final.json` (17 slides,
7 imagens, 15 perguntas, 31 cards de vocabulário). Dossiê: `topico195-como-se-diz.md`. Data: 2026-10-28.

**Resultado: 0 pendências → liberado para imagens e publicação.**

## 0. Como o conteúdo foi produzido

Rascunhos por IA gerados com o `python` do sistema (o venv do backend não tem `google-genai`; a 1ª tentativa
com o venv falhou na importação e foi refeita). O Gemini deu 503/504/500 em todos os modelos da cadeia
"conteudo"; saíram: **"conteudo" = Qwen (Groq), 7 assuntos** e **"segunda_opiniao" = gpt-oss-120b (Groq), 6
assuntos**. Comparados com o dossiê ponto por ponto; **nada do texto deles foi aproveitado** (a versão final foi
escrita do dossiê, como no T194).

## 2b. Erros dos rascunhos que NÃO entraram

| Rascunho | Erro / problema | Onde |
|---|---|---|
| gpt-oss-120b | **"A letra 'J' não é 'jota', é 'djee'"** — errado: J = "jay" /dʒeɪ/; "djee" é o G (tabela, fonte 4) | alfabeto |
| gpt-oss-120b | **"How is written…?"** apresentada como forma de perguntar a grafia — não existe nas fontes; a forma é "How do you spell…?" | s grafia |
| gpt-oss-120b | **"What does … means?"** e **"What is … mean?"** — gramática errada (a primeira troca "mean" por "means"; a segunda mistura as duas perguntas) | s significado |
| gpt-oss-120b | "O W não é 'uve'; o H não é 'hache'" — comparações com nomes que **não são do português** (uve = V em Portugal; hache = espanhol) | alfabeto |
| gpt-oss-120b | Vocabulário fora da lista fechada: "A as in Apple", "bizarre", "environment", "teacher", "house", "laptop", "What is a laptop?" | exemplos |
| Qwen | **Explica a gramática** ("Present Simple", "verbos auxiliares 'do' e 'does'", "terceira pessoa do singular") — proibido neste tópico (é do M1) | slides 2–3 |
| Qwen | Palavras fora da lista: "schedule", "curious", "name", "write", "read", "phone"; sem o "double-u" no alfabeto; título "Trio de Perguntas de Resgate" (jargão sem fonte) | vários |
| Qwen | Acertou: agrupar letras por som e a variação zee × zed (já no dossiê) — ideia já presente na versão final | alfabeto |

## 1. Fato (afirmação → fonte)

| # | Afirmação no tópico | Onde | Fonte do dossiê | Status |
|---|---|---|---|---|
| 1 | O CEFR descreve o A1 como conversa possível se o outro ajudar o aluno a formular o que quer dizer | s1 | 5 ("help me formulate what I'm trying to say") | ok |
| 2 | "How do you say that in English?" pergunta como se diz algo em inglês | s1, s2, ck1, ck2, ck5, Resumo | 1 ("How do you say this in English?"), 2 (cartão "How do you say … in English?"; Stage 4 "How do you say that in English?") | ok — "that" no lugar de "this" para não criar palavra nova |
| 3 | O material da NGL ensina a frase para o aluno usar quando quer saber uma palavra | s2 | 1 ("When you want to know a word, say…") | ok |
| 4 | O British Council usa a mesma pergunta nos cartões, com reticências | s2 | 2 | ok (reformulado: antes dizia que "no lugar das reticências entra a palavra em português", inferência minha) |
| 5 | "What does it mean?" é o que se pergunta quando não se entende | s3, ck6, Resumo | 1 ("When you don't understand, ask: 'What does it mean?'") | ok |
| 6 | "What does … mean?" é o formato com a palavra; o Oxford dá o mesmo formato | s3 | 2; 3 (mean: *What does 'lark' mean?*) | ok |
| 7 | "mean" = significar, querer dizer | s3 | 3 (mean, "have as meaning") | ok |
| 8 | Quando você quer escrever uma palavra, diga "How do you spell that?" | s4 | 1 | ok |
| 9 | "spell" = dizer ou escrever as letras de uma palavra na ordem certa | s4 | 3 (spell, def. 1) | ok |
| 10 | O Oxford mostra o formato C-A-T spells "cat" | s4 | 3 (spell, def. 3) | ok |
| 11 | Nomes das 26 letras e IPA (A /eɪ/ … Z /ziː/) | s5, s6 | 4 (tabela, nomes do OED) | ok — conferido letra por letra contra a tabela lida (A eɪ, B biː, C siː, D diː, E iː, F ɛf, G dʒiː, H eɪtʃ, I aɪ, J dʒeɪ, K keɪ, L ɛl, M ɛm, N ɛn, O oʊ, P piː, Q kjuː, R ɑːr, S ɛs, T tiː, U juː, V viː, W ˈdʌbəl.juː, X ɛks, Y waɪ, Z zɛd/ziː) |
| 12 | W se diz "double-u" | s6, ck4_3 | 4 | ok |
| 13 | Z: "zee" no inglês americano; a tabela lista "zed" e "zee" | s6, s7, ck5_2, Resumo | 3 (Z, NAmE /zi/); 4 | ok (corrigido: antes dizia "zed é o nome principal" e "em outros países" — a fonte não diz isso; agora só "também existe") |
| 13b | Agrupamento das letras por som (ei / i / é / ai / ...) | s6 (box) | 4 (derivado da IPA da tabela) | ok — conferido: /eɪ/ A, H(/eɪtʃ/), J, K · /iː/ B C D E G P T V (+Z americano) · /ɛ/ F L M N S X · /aɪ/ I, Y(/waɪ/) · O /oʊ/ · R /ɑːr/ · Q/U/W em /juː/ |
| 14 | E soa "i" e I soa "ai"; G "dji" e J "djei" | cards E, G, I, J; ck4 | 4 (IPA) | ok |
| 15 | A leitura em português dos nomes ("ei", "bi", "dâbliu"…) | cards | — | ok como ajuda didática, rotulada "(aprox.)" no próprio card; não é afirmação de fonte |
| 16 | As perguntas combinam com as do tópico anterior (Sorry? How do you spell that? / Sorry, I don't understand. What does it mean?) | s7, ck6_1 | 1 ("When you don't understand, ask…") + T194 publicado | ok |
| 17 | O inglês usa uma palavra a mais ("do") onde o português já tem a pergunta pronta | s2 (cols2 + box) | observação de contraste, mesma linha do "don't" do T194 (fonte elon.io lá) | ok — **sem** ensinar a regra do do/does (proibido) |
| 18 | A letra e o som do R ("ar"), do H ("tch") | cards R, H | 4 (/ɑːr/, /eɪtʃ/) | ok |
| 19 | Traduções: say = dizer; spell = soletrar; mean = significar; in English = em inglês | vocab | 3; 1 | ok |

**Removido/ajustado durante a escrita (minhas afirmações sem fonte):**
- "O Oxford mostra *How do you spell your surname?*" no card de "slowly" → **saiu**: "your" e "surname" não estão na
  lista fechada (dossiê, "Proibido"). Ficou a resposta soletrada "ess, el, o, double-u, el, wy".
- "Zed é o nome principal / usado em outros países" → **removido** (ver linha 13).
- "No lugar das reticências você pode usar a palavra em português" → **reformulado** (linha 4).
- "Brasileiro confunde E×I e G×J" como fato → **não escrito** como fato; o tópico só diz "preste atenção na
  vogal" (observação didática, sem estatística).

## 2. Lista fechada, palavra por palavra

Inglês que aparece no conteúdo (explicações, exemplos, respostas e perguntas), conferido contra a lista:

- **Novas deste tópico (permitidas):** how · do · does · in · English · what · mean · spell · it — e as
  letras A–Z com seus nomes (ay/bee/…/zee, double-u), mais os rótulos "Letter X" dos cards.
- **Do T194 (já ensinadas):** sorry · I · don't · understand · can · you · repeat · that · say · please ·
  slowly · speak · more · again · could.
- **Palavras-alvo entre aspas:** só "slowly" (T194) e, em português, "devagar" · "de novo".
- Conferido que **NÃO** aparecem: "your", "surname", "name", "this", "difference", "example", "pronounce",
  "write", "read", "listen" (T197), "You mean…?", "Exactly" (T198), "What do you mean?", números/telefone (M2),
  "May I…", "board".
- Nome de letra usado só como respelling de apoio (não é palavra nova a aprender): "eye" na explicação do
  ck5_3 (letra I). Aceito.

## 3. Pedagogia (toda pergunta é respondível com o que foi ensinado ATÉ ali)

| Checkpoint | Usa | Ensinado antes? |
|---|---|---|
| ck1_1, ck1_2 (após s2) | "Sorry?", "Sorry, I don't understand.", "Can you repeat that, please?" (distratores), "How do you say that in English?" | T194 + s2 ✔ — nenhuma opção usa "mean" ou "spell" (só ensinadas em s3/s4) |
| ck2_1, ck2_2 (após s3) | "How do you say…", "What does … mean?", "Sorry?", "Can you repeat…" | T194 + s2 + s3 ✔ |
| ck3_1, ck3_2 (após s4) | "How do you spell that?", "What does it mean?", "Can you speak more slowly, please?", "Sorry?" | T194 + s2–s4 ✔ |
| ck4_1–3 (após s5–s6) | letras e nomes (E, I, B, Y, T; J/G/K/Y; W) | cards s5/s6 ✔ |
| ck5_1–3 (após s7) | as 3 perguntas, Z, soletrar "again" | s2–s7 ✔ ("again" é do T194) |
| ck6_1, ck6_2, ck7_1 | tudo acima | ✔ |

- Ordem do simples ao complexo: 3 perguntas isoladas → alfabeto → junção. Exemplo antes de abstração ✔.
- Tipos de pergunta: mc 4 · lacuna 3 · tf 2 · ditado 2 · classify 1 · associar 1 · open 2 → **≥1 tf/classify/associar
  e 2 abertas ✔**. Ids de pergunta e de item únicos (script: "ids duplicados: []").
- O ditado do ck6_1 aceita com/sem vírgula, ponto e contração ("do not").
- Ressalva técnica (não é erro de conteúdo): os botões 🔊 dos cards de letra dependem da voz en-US do navegador
  dizendo o NOME da letra a partir de "Letter X". Foi o desenho escolhido para a voz não ler "A" como artigo.
  **Conferir de ouvido no navegador após publicar** (item de verificação do Atila, 1 minuto).

## 4. Direito autoral
Nenhum trecho copiado: as perguntas são frases curtas de uso comum (blocos), a tabela das letras são fatos
(nomes e IPA), as explicações são minhas. Citações curtas (≤8 palavras) atribuídas: NGL/ELTeach, British Council,
Oxford. ✔

## 5. Continuidade
- Não repete o T194; liga com ele (fluxo s1, box s7, ditado ck6_1). Não invade o T196 (prática de conversa) nem
  a Aula 2 (T197–T199). O Resumo é autossuficiente (cada bullet se sustenta sozinho) → alimenta o
  "↩ Relembrando" do T196.
- Reflexão "💭 Pra pensar" + Resumo "📌" presentes ✔. `imagem_capa` ✔. `fluxo` (nenhum `diagrama`) ✔.

## 6. Estrutura
`validar_topico()` = `[]` · render com tema `caderno-escolar`: 0 ocorrências de "None" · 31 cards de vocab ·
nenhum checkpoint vazio ✔.

**Pendências: 0.**
