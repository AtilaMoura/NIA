# Auditoria — T199 Juntando tudo: uma aula inteira em inglês simples

Data: 2026-11-03 · Conteúdo auditado: `backend/_criar_topico199_ingles.py` → `_topico199_ingles_final.json`
(16 slides, 7 imagens, 13 perguntas) · Dossiê: `topico199-juntando-tudo-aula-inteira.md`.

**Resultado: 0 pendências BLOQUEANTES.** Tópico de síntese sem palavra nova. Os itens "pendente de conferência humana" são os
herdados dos T197/T198 (declarados no dossiê e abaixo), não novos.

## 1. Lista fechada (palavra por palavra)

Conferido por script: todo inglês do JSON (cartões, falas "Você:/Professor:", frases entre aspas, opções, ditados, respostas
aceitas, respostas-modelo, rótulos) contra a UNIÃO T194–T198.
- **Palavras fora da lista: nenhuma.** O script marcou só português (as alternativas em português do `ck5_2` e a palavra "Como?").
- Nenhuma frase proibida: Excuse me, Thank you, Okay, Good, Very good, hello, What do you mean?, I can't hear you very well, May I…?,
  Fill in the blanks, Complete the sentences.
- As falas do professor que precisariam de palavra fora da lista aparecem em português entre colchetes (ex.: "[Ele explica em
  português: "de novo".]").
- Soletrações conferidas letra por letra: "again" = A-G-A-I-N ✔ (ay · gee · ay · eye · en); "A-N-A" (nome de exemplo, só letras).

## 2. Afirmações × fontes

| Afirmação no tópico | Fonte (lida em tópico anterior) | Status |
|---|---|---|
| Todas as frases em inglês (pedidos, perguntas, instruções, confirmações) | dossiês T194–T198 (British Council, ELTeach, Cambridge Young Learners, vídeo Teacher Abelhinha) | ok — nenhuma frase nova |
| "Match the words and the pictures." é exemplo montado pelo curso | T197 (nenhuma fonte traz "match" como instrução) | **declarado no próprio slide da Cena 3** |
| "Exactly." / "You mean …?" | T198 (só o vídeo; BC só traz "Do you mean …?") | herdado, declarado no dossiê |
| A1 no CEFR: conversa simples se o outro repete, fala devagar e ajuda a formular | CEFR (lido no T194) | ok — paráfrase em português, sem citação em inglês |
| "Eu consigo pedir ajuda em inglês quando não entendo." | `GRADE_INGLES.md` (mapa do M0, aprovado 2026-10-07) | ok |
| "Em cinco tópicos você montou um kit…" | T194, T195, T196, T197, T198 | ok |
| "O próximo módulo volta para a base do inglês, com o -s da 3ª pessoa: he, she e it" | `GRADE_INGLES.md` (M1 Aula 2) | ok — corrigido: antes dizia "o presente simples", que a grade não usa para o próximo módulo |
| A aula é uma simulação | dossiê | **declarado na capa ("aula simulada") e no dossiê** |

## 3. Pedagogia e continuidade

- Retoma T194–T198 no slide 1 (mapa em 5 passos) e fecha com a frase "Eu consigo…" do M0; "Próximo" aponta o Módulo 2 (M1 da grade).
- Cada cena usa grupos de frases em ordem crescente: som (Cena 1) → palavra (Cena 2) → instrução + confirmação (Cena 3) → tudo junto (Cena 4).
- Nenhuma pergunta usa algo ainda não ensinado: os checkpoints só usam frases dos T194–T198, e as instruções do Cena 2/3/4
  já foram mostradas no T197.
- Dificuldade: reconhecimento (classify, mc, tf, associar) → produção (lacuna, ditado) → escrita livre (2 abertas).
- Sem gramática explicada.

## 4. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (sem `diagrama`) ✔ · Reflexão "💭 Pra pensar" + Resumo ✔.
- Perguntas: **13** — classify 1, tf 2, mc 4, lacuna 1, associar 1, ditado 2, **open 2** ✔ (≥1 tf/classify/associar ✔).
- Ids únicos: 0 duplicados ✔ · `validar_topico()` vazio ✔ · selo da capa = 13 perguntas ✔.
- Áudio dos exemplos em inglês: voz en-US dos cards; narração em português por bloco depois.
