# Auditoria — T194 "Sorry, I don't understand", "Can you repeat that?", "Can you speak more slowly?"

Conteúdo auditado: `backend/_criar_topico194_ingles.py` → `_topico194_ingles_final.json` (16 slides,
7 imagens, 13 perguntas). Dossiê: `topico194-quando-nao-entendo.md`. Data: 2026-10-14.

**Resultado: 0 pendências → liberado para publicar.**

## 1. Fato (afirmação → fonte)

| # | Afirmação no tópico | Onde | Fonte do dossiê | Status |
|---|---|---|---|---|
| 1 | O CEFR descreve o A1: conversa simples desde que o outro repita ou reformule mais devagar | s1, Resumo, Reflexão | 4 (citação lida no PDF) | ok |
| 2 | "Sorry?" como pergunta pede repetição; Oxford registra esse uso | s2 | 3 (sorry, exclamation) | ok |
| 3 | Dizer "Sorry?" com a voz subindo no fim | s2, Resumo | 5 ("raise your intonation at the end") | ok |
| 4 | Engoo: nativos dizem "What?", é difícil não soar grosseiro, eles não recomendam | s2, ck1_2, ck5_2 | 5 | ok (atribuído à escola) |
| 5 | "Sorry, I don't understand." = não entendi; o aluno da cena do British Council diz isso | s3, s6 | 1 (diálogo: "Sorry, Bob, I don't understand.") | ok |
| 6 | "I don't understand." sem o "Sorry" também está certo | s3 | 1 (lista: "I don't understand.") | ok — "fica mais gentil" com o Sorry: o Sorry é pedido de desculpa (3, sorry); afirmação didática leve, mantida |
| 7 | Português nega com "não" antes do verbo; inglês usa uma palavra a mais ("don't") | s3 | 6 | ok — sem ensinar a regra do do/don't (proibido) |
| 8 | "Can you repeat that, please?" | s4 | 2; 3 (repeat) | ok |
| 9 | "Could you say that again, please?" | s4 | 1; 3 (again) | ok |
| 10 | Os dois aparecem em lições para iniciantes | s4 | 1 (A1), 2 | ok |
| 11 | As lições usam "can" e "could"; as duas funcionam | s4 | 1, 2 | ok — sem dizer qual é "mais educada" (não lido em fonte) |
| 12 | Oxford define "please" como o jeito educado de pedir | s4 | 3 (please) | ok |
| 13 | "Can you speak more slowly, please?" | s5 | 2 ("Can you speak more slowly?"); 3 (slowly) + 12 | ok |
| 14 | "Can you repeat that more slowly, please?" está na lista da lição A1 do British Council | s5 | 1 | ok |
| 15 | Oxford registra "slower" e "more slowly"; o curso usa "more slowly" (forma das lições) | s5 | 3 (Which Word?); 1, 2 | ok |
| 16 | Cena do martelo: ouvido entupido → "Could you say that again, please?"; Paul oferece a chave inglesa; "Sorry, Bob, I don't understand."; Bob explica onde está; "Could you repeat that more slowly, please?"; Bob repete devagar; Paul acha o martelo | s6 | 1 (transcrição) | ok — conferido fala por fala; Paul diz "Could you repeat…" no diálogo e a lista diz "Can you repeat…": as duas aparecem no tópico, de acordo com a fonte |
| 17 | A lição pede, no fim, usar essas frases da próxima vez que precisar conferir se entendeu | s6 | 1 ("Try and use some of these phrases the next time…") | ok |
| 18 | Traduções: Sorry? = Como?/Desculpe?; repeat = repetir; again = de novo; speak = falar; more slowly = mais devagar; that = isso | vocab | 3 (definições) | ok |

**Removido/ajustado durante a escrita (minhas afirmações sem fonte):**
- "Com a voz descendo, 'Sorry.' vira só pedido de desculpas" → não lido em fonte; saiu (ficou só a regra da voz subindo, fonte 5).
- "'more slower' não existe" → não lido em fonte; saiu (ficou "repare no -ly").
- "More slowly, please" solto (título da grade) → nenhuma fonte ensina essa forma; título e conteúdo usam a frase completa (dossiê, "Ajuste de título").

## 2. Erros dos rascunhos que NÃO entraram

Os dois rascunhos saíram do **gpt-oss-120b (Groq)**: o Gemini deu 503/500 em todos os modelos da
cadeia "conteudo" e o Qwen recusou por tamanho. Nada do texto deles foi aproveitado.

| Rascunho | Erro | Por que não entra |
|---|---|---|
| conteudo | "I don't understand you" soaria rude, "parece culpar o falante" | sem fonte |
| conteudo | "I didn't catch that", "I don't understand the instructions", "Please speak more slowly" | fora da lista fechada |
| conteudo | Explica "do" auxiliar, contração "don't = do not", comparativo de advérbio com "more" | gramática proibida no M0 (chunk) |
| conteudo | "could adiciona polidez", "Could… mais polido que Can" | não lido em fonte |
| conteudo | "Can you repeat? → falta that e please para soar natural" | sem fonte |
| conteudo | Cena do martelo com falas inventadas ("I need the hammer", "Ah! The hammer! Yes, it's here") e sem a confusão com a chave inglesa | contradiz a transcrição (fonte 1) |
| segunda_opiniao | "slower soa estranho porque é adjetivo… evite slower" | **errado**: Oxford registra "Can you speak slower/more slowly?" (fonte 3) |
| segunda_opiniao | Cena invertida: Paul explica "como consertar um martelo" e Bob não entende | **errado**: na fonte é Bob quem pede o martelo e Paul quem não entende |
| segunda_opiniao | Card "What?" com "I didn't catch that"; diálogo com "café at 3 p.m."; card "instruction" | fora da lista fechada |
| segunda_opiniao | "Can you repeat it? soa incompleto e pode ser interpretado como ordem" | sem fonte |
| segunda_opiniao | Descrição do A1 do CEFR além do que a grade de autoavaliação diz | não lido na fonte |
| segunda_opiniao | "Can you + verbo (base form) + more slowly" | gramática proibida no M0 |

## 3. Palavra por palavra (lista fechada)

Conferência automática de todo inglês do tópico (cards, exemplos, ditados, respostas aceitas,
opções, respostas-modelo, itens de classificar e trechos entre aspas): **nenhuma palavra fora da
lista**, exceto:
- "What?", "I no understand", "slower" → formas de contraste ("evite"), previstas no dossiê;
- "Bob" → nome na cena;
- "do not" → só como variante ACEITA no ditado ck2_2 (não ensinada; aceitar não ensina nada novo);
- "How do you say…?", "What does … mean?", "How do you spell…?" → só no rótulo do próximo tópico.
Distratores ("No.", "Again!", "Slowly!", "What? Again!") usam só palavras da lista ou de contraste.
Os 6 blocos da lista aparecem todos em card `vocab`; nenhum bloco a mais.

## 4. Pedagogia
- Primeiro tópico do curso: explicação em português, inglês só nos blocos; nenhuma gramática
  explicada (regra da grade); ordem do mais curto ("Sorry?") ao mais longo ("Can you repeat that
  more slowly, please?").
- Toda pergunta é respondível com o que veio antes dela: ck1 (s2), ck2 (s3), ck3 (s4), ck4 (s5),
  ck5 (s2–s6), ck6/ck7 (tudo). ck3_2 pergunta "again", traduzido no card do s4.
- Tipos variados: 3 mc, 1 tf, 2 lacuna, 3 ditado, 1 associar, 1 classify, 2 open (com
  resposta-modelo só com blocos da lista).
- Caso real: a cena do British Council (inclui o que deu errado: Paul entende a ferramenta errada).

## 5. Continuidade
- Não há tópico anterior (é o primeiro do curso). O Resumo vira o "↩ Relembrando" do T195: cada
  bullet se sustenta sozinho (conferido).
- Não invade o T195 (How do you say / What does … mean / spell / alfabeto) nem o T198 (You mean /
  Exactly / Do you mean / Is this it / Yes, that's right — essas falas da cena do British Council
  ficaram de fora de propósito). "I can't hear you very well" (traz can't) também ficou de fora.

## 6. Direito autoral
- British Council: cena recontada em português; só falas curtas do Paul citadas em inglês.
- Oxford, Engoo, elon.io, ELTeach: paráfrase atribuída; nenhum trecho longo copiado.

## 7. Estrutura
- `validar_topico()` → `[]`; ids de pergunta e de item únicos (`[]` duplicados).
- Render local (tema `caderno-escolar`): 0 `None`.
- Capa com `imagem_capa`; 6 imagens inline (meta 0,7–1 por slide de conteúdo: 6/7); `fluxo` em
  s1 e s6 (nenhum `diagrama`); Reflexão "💭 Pra pensar" + Resumo "📌 Resumo do tópico".
