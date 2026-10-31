# Auditoria — T196 Prática: pedir ajuda numa conversa curta

Data: 2026-10-31 · Conteúdo auditado: `backend/_criar_topico196_ingles.py` → `_topico196_ingles_final.json`
(16 slides, 7 imagens, 14 perguntas) · Dossiê: `topico196-pratica-pedir-ajuda.md`.
**Resultado: 0 pendências.**

## 1. Lista fechada (palavra por palavra)

Conferido por script: toda frase em inglês do JSON (termos e exemplos dos cards, falas "Você:/Professora:" dos
diálogos, opções, ditados, respostas aceitas, respostas-modelo, caixas de contraste) foi comparada com a união
T194+T195 (sorry, I, don't, understand, can, could, you, repeat, that, say, again, speak, more, slowly, please,
how, do, does, in, English, what, mean, spell, it + letras da soletração).
- **Palavras fora da lista: nenhuma**, exceto "no" em "Sorry, I no understand." — que é o **contraste de erro**
  do T194 (marcado ❌ no slide "Cuidado com os erros comuns"), não é frase para o aluno usar.
- "How you say that in English?" aparece só como ❌ de contraste (igual ao T195).
- Nenhuma frase proibida (You mean…?, Exactly, read/listen/write…, What is…, Thank you, Excuse me, your name…).

## 2. Afirmações

| Afirmação no tópico | Fonte | Status |
|---|---|---|
| As 5 frases de "falta o som" e as 3 de "falta a palavra" | T194 (fontes 1–3) e T195 (fontes 1–3) | ok |
| "Sorry, I don't understand." avisa que NÃO entendeu (ck1_2) | T194 fonte 1 | ok |
| "more slowly" = mais devagar | T194 fonte 3 (Oxford, *slowly*) | ok |
| "What does "again" mean?" → "de novo" | T194 fonte 3 (Oxford, *again*) | ok |
| Quem responde "How do you spell that?" diz as letras uma a uma (S-L-O-W-L-Y; P-L-E-A-S-E; A-G-A-I-N) | T195 fonte 3 (Oxford, *spell*) + fonte 4 (letras) | ok — soletrações conferidas letra por letra: slowly = S-L-O-W-L-Y ✔, please = P-L-E-A-S-E ✔ |
| Na lição do British Council a personagem pede de novo, mais devagar, e acha o que procurava | T194 fonte 1 (cena do martelo) | ok |
| "What?" seco pode soar rude; "Sorry?" com a voz subindo | T194 fonte 5 (Engoo) | ok, atribuído |
| Mostrar ao aluno como pedir ajuda o encoraja a usar inglês por conta própria | T194 fonte 2 (ELTeach: "This will encourage students to use English on their own") | ok — o slide escreve "encorajaria", atribuído à NGL |
| "I no understand" está errado; o inglês usa "don't" | T194 fonte 6 (elon.io) | ok, sem ensinar a regra |
| Diálogos | exemplos próprios, só com a lista fechada; não copiam a cena do martelo | ok (nenhum texto com copyright) |

Nota: não houve rascunho de IA neste tópico (sem palavra nova); a versão final saiu direto do dossiê.

## 3. Ideias descartadas no planejamento (não entraram)

- Cena com "[ela diz 'Thank you']" / "Yes, that's right" na professora: descartada (palavras não ensinadas; "Exactly/Yes" são do T198).
- "What is … in English?" e "Excuse me, ...": descartados (fora da lista).
- Uma 4ª conversa pedindo "your name": descartada (your/name não ensinadas).

## 4. Pedagogia e continuidade

- Prática pura: nenhuma gramática explicada; "do/does/can/could" só como bloco pronto.
- Costura: retoma T194 (som) e T195 (palavra) no slide 1 e fecha a Aula 1; "Próximo" aponta o T197 (Aula 2).
- Cada pergunta usa só o que já foi ensinado ATÉ aquele ponto do curso (nenhuma palavra do M1 em diante).
- Dificuldade: reconhecimento (associar, mc, tf) → produção (lacuna, ditado) → escrita livre (2 abertas).
- Armadilha do português com fonte: "How you say…", "I no understand".

## 5. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (sem `diagrama`) ✔ · Reflexão "💭 Pra pensar" + Resumo ✔.
- Perguntas: 14 — associar 1, classify 1, tf 2, mc 4, lacuna 2, ditado 2, **open 2** ✔ (≥1 tf/classify/associar ✔).
- Ids de pergunta e de item únicos no tópico (script: 0 duplicados) ✔.
- `validar_topico()`: vazio ✔.
- Áudio dos exemplos em inglês: voz en-US dos cards (padrão do curso); narração em português por bloco depois.
