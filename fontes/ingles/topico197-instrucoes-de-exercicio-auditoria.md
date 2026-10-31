# Auditoria — T197 As instruções de todo exercício: read, listen, write, answer, choose, match, repeat

Data: 2026-10-31 · Conteúdo auditado: `backend/_criar_topico197_ingles.py` → `_topico197_ingles_final.json`
(16 slides, 7 imagens, 14 perguntas) · Dossiê: `topico197-instrucoes-de-exercicio.md`.

**Resultado: 0 pendências BLOQUEANTES. 2 itens "pendente de conferência humana" (declarados abaixo, não são fato
afirmado como verificado): (a) a frase "Match the words and the pictures." é exemplo próprio; (b) a tradução de
"match" = "ligar/combinar" não foi conferida em dicionário (todos bloquearam o acesso automatizado).**

## 1. Lista fechada (palavra por palavra)

Conferido por script: todo inglês do JSON (termos e exemplos dos cards, frases do fluxo, opções, ditados, respostas
aceitas, respostas-modelo, citações entre aspas nas caixas) foi comparado com a lista fechada do dossiê (7 verbos +
text, questions, correct, name, number, words, pictures, after, me, the, and, a, or + as palavras do T194–T196).
- Palavras fora da lista: **nenhuma** nas frases que o aluno deve produzir ou reconhecer.
- O script achou um trecho em inglês fora da lista (citação do British Council com "to", "voicemail", "message") numa
  caixa explicativa do slide 6. **Corrigido:** o trecho em inglês foi retirado; a caixa descreve a fonte em português.
- Nenhuma frase proibida (You mean…, Exactly, Fill in the blanks, Complete the sentences, Draw lines, tick, colour,
  watch the video, Open your book, May I…). "best" (Cambridge Movers) não aparece no tópico.

## 2. Afirmações × fontes (todas LIDAS nesta rodada, 2026-10-31)

| Afirmação no tópico | Fonte lida | Status |
|---|---|---|
| "Listen and repeat." é instrução de sala de aula | ELTeach U2 L2 (a. e b.: "…listen and repeat.") | ok |
| "Repeat after me, please." | ELTeach U2 L2 ("Repeat after me, please." / "Repeat after me:") | ok |
| "Choose the correct answer." (múltipla escolha) | ELTeach U2 L2 Practice 1 | ok |
| "Read the text." / ler o texto e fazer os exercícios | British Council A1 ("read the text and do the exercises") + Cambridge Movers ("Read the text and choose the best answer.") | ok |
| "Answer the questions." | Cambridge Young Learners Sample Papers Vol.1, A1 Movers Reading and Writing, p.15 do caderno; BC A1 listening ("answer the questions") | ok |
| "Listen and write a name or a number." | Cambridge Pre A1 Starters Listening, Part 2 ("Read the question. Listen and write a name or a number.") | ok — o tópico usa a parte "Listen and write a name or a number." como bloco |
| Verbo no começo da instrução | todas as citações acima | ok (observação sobre as citações; escrita como "nas instruções reais que lemos") |
| Provas básicas da Cambridge e atividades A1 do BC usam essas instruções | Cambridge (Pre A1/A1), BC ("A1 Elementary") | ok |
| Atividades A1 de vocabulário treinam "matching words and pictures" | BC *Daily routine vocabulary* | ok |
| "Match the words and the pictures." | — (exemplo próprio a partir da linha anterior) | **declarado como exemplo no próprio card** |
| match = "ligar/combinar" | — (dicionários bloqueados) | **pendente de conferência humana** |
| "Listen and answer the questions." (slide 6) | combinação de BC (ouvir o áudio e responder) + Cambridge | **declarado como combinação no próprio slide** |
| Níveis A1/A2 de cada verbo | não lidos (Oxford 403) | **o tópico não afirma nível por verbo** |
| "Os números em si você aprende no Módulo 3" | `GRADE_INGLES.md` (M2 = "Módulo 3" no app) | ok |
| Na lição da fonte, a classe repete a frase em coro | ELTeach (Ms. Choi / Class) | ok |

## 3. Cuidados que a leitura revelou

- A fonte 3 (BC) não traz o texto das tarefas Task 1/Task 2 (arquivos externos): o tópico **não cita** enunciado dessas tarefas.
- "Match" e "Repeat" não aparecem em instruções dos 2 volumes de sample papers nem no Starters classroom activities:
  "Repeat" tem fonte (ELTeach); "Match" não tem instrução literal → tratado como acima.
- A página *Useful learner phrases* (BC TeachingEnglish) deu timeout nesta rodada: nada do T197 depende dela.
- Trechos que eu havia escrito e **retirei** por não terem fonte: explicação de gramática ("verbo no começo, 'the' antes do
  substantivo") e "usa a primeira em quase toda atividade de vocabulário" (ELTeach mostra "listen and repeat" 2 vezes,
  não "quase toda atividade") — trocados por textos que só repetem o que as fontes mostram.

## 4. Pedagogia e continuidade

- Costura: abre a Aula 2 retomando a Aula 1 (ligação "Sorry, I don't understand. What does "match" mean?" no fluxo do slide 1
  e no slide 6); fecha apontando o T198.
- Nenhuma pergunta usa palavra ainda não ensinada ATÉ aquele ponto: ck1 só tem listen/repeat/read/answer/choose
  (as opções são instruções já mostradas nos slides 2 e 3 — "Read the text.", "Answer the questions." e "Choose the correct
  answer." aparecem como distratores no ck1 ANTES de ensinadas no slide 3/4). **Ver item 6 (revisar).**
- Dificuldade: reconhecimento (mc, tf, associar) → produção (lacuna, ditado) → escrita livre (2 abertas).
- Sem gramática explicada; "do/does/can" continuam como blocos da Aula 1.

## 5. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (sem `diagrama`) ✔ · Reflexão "💭 Pra pensar" + Resumo ✔.
- Perguntas: 14 — associar 1, tf 2, mc 4, lacuna 3, ditado 2, **open 2** ✔ (≥1 tf/associar ✔).
- Ids únicos: 0 duplicados ✔. Enunciado duplicado ck4/ck6 detectado pelo validador → **corrigido** (ck6_1 trocado).
- `validar_topico()` vazio ✔.
- Selo da capa dizia 15 perguntas; corrigido para 14.

## 6. Item aberto da própria auditoria (resolvido antes de publicar)

O ck1_1 usa como distratores "Read the text.", "Answer the questions." e "Choose the correct answer." — instruções que só
são ensinadas nos slides 3 e 4, DEPOIS do ck1. A regra do curso é "nenhuma pergunta usa o que ainda não foi ensinado até
aquele ponto". **Correção aplicada antes da publicação:** distratores do ck1_1 trocados por frases já vistas na Aula 1
("Sorry?", "How do you spell that?", "Can you repeat that, please?"). Ver conferência final abaixo.

## 7. Conferência final (após publicação)

- ck1_1 corrigido (distratores só com frases da Aula 1) — aplicado no `_criar_topico197_ingles.py` e republicado.
- Texto "Escrever aparece em muitas instruções" trocado por "também aparece nas instruções dos materiais que lemos" (sem generalizar além das fontes).
- Alt da capa e do slide 1 diziam "sete" (cartões/setas); as imagens têm 6 → trocado por "vários".
- Áudio: 15 blocos; o `_conferir_audio.py` marcou 1 com problema (slide 4, bloco 3, semelhança 0.38) e o "fim:" mostrou outro
  cortado (slide 4, bloco 0, terminava em "…manda"). Narrações reescritas e só esses blocos regravados (2 rodadas);
  conferência final 0 problemas e os 15 mp3 respondendo 200.
- Diagnóstico final: sem nenhum ✗.
