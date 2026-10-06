# Auditoria — REVISÃO do T10 "Verbos normais x to be: o erro que trava tudo"

Conteúdo final: `backend/_criar_topico10_ingles.py` → `_topico10_ingles_final.json` (17 slides,
6 imagens — 4 mantidas + 2 novas —, 1 fluxo, 8 checkpoints / 9 perguntas). Dossiê:
`topico10-verbo-normal.md`. Versão anterior: `backend/_backup_topico10_2026-10-06.json`. 2026-10-06.

## 1. Lista fechada (checagem automática palavra por palavra)
Todo inglês do tópico (termos, exemplos, colunas, ditados, opções, enunciados, respostas-modelo)
comparado com a lista do dossiê + o vocabulário do T9. Fora: só "to be" (nome do verbo).
**0 palavra fora da lista** ✔.

## 2. Afirmação → fonte → status

| Seção | Afirmação | Fonte | Status |
|---|---|---|---|
| Achado | diagnóstico: "am live / am work / am like", 0/3, achado principal | 3 (`dia-00.md`) | ✔ |
| Regra | verbo normal com I/you/we/they na forma do dicionário, sem am/is/are | 1 | ✔ |
| Uso | present simple = rotina, hábito, coisas verdadeiras | 1, 4 | ✔ |
| Como decidir | ser/estar → to be; fazer → verbo normal | 1 + T9 (dedução didática dos dois usos) | ✔ |
| Negativa | don't + verbo ("We don't eat meat" no British Council) | 1 | ✔ |
| Duas negativas | to be nega com not (T9); verbo normal com don't | 1, 2 | ✔ |
| Diagnóstico | correção das frases reais | 3 | ✔ |

## 3. Erros pegos nesta revisão (corrigidos)
- **"I like playing video games" e "I like reading"** (versão anterior, inclusive na pergunta ck6_1):
  -ing ainda não ensinado → "I like video games. / I play video games."; ck6_1 retirada e trocada por
  **ck6_2** (id novo: "I don't play video games at home, but I like music.").
- **"at seven", "eight hours", "on Sundays"**: horas, números e dias da semana são tópicos posteriores
  do Módulo 1 → "I eat bread at breakfast", "I sleep well", "I don't work at home".
- **"Isso é o erro mais comum de quem fala português"**: sem fonte (busca não achou) → virou "foi o
  achado principal do seu diagnóstico", que é fato.
- Selo "11 perguntas" → "9 perguntas".

## 4. Respostas salvas do Atila
- ck1_1, ck2_1, ck3_1, ck4_1, ck5_1 **idênticas** (conferido por script). ck6_1 retirada (conteúdo
  com -ing). Novas: ck7_1 (associar), ck7_2 (lacuna), ck6_2 (ditado), ck8_1 (aberta).

## 5. Continuidade
- Sem he/she/it + verbo (-s), sem doesn't, sem "Do you…?", sem -ing, sem números/horas/dias.

## 6. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (cadeia caiu até o `gemma-4-31b-it`) e Groq (`gpt-oss-120b`). Os dois **anteciparam
a Aula 2 e tópicos futuros**: "works", "lives", "plays", "likes" (-s da 3ª pessoa), "doesn't",
"Do you…?" (pergunta com do) e "-ing" (working, playing) — exatamente o que o T10 não pode ensinar.
Nada entrou; versão final escrita do dossiê.

## 7. Pedagogia e estrutura
- Novo: "Como decidir" (fluxo), "Duas negativas diferentes", Reflexão + Resumo, associar, 2 abertas
  (ck4_1, ck8_1). `validar_topico()` vazio; 0 `None` (caderno-escolar); ids únicos.
- Imagens: 4 mantidas (capa, erro, trabalho, rotina — já no estilo; texto em inglês correto e intencional).

**Pendências: 0.** Áudio: 10 narrações em PT (1 reescrita na revisão + 1 por corte), 10/10 conferidos. 4 áudios regerados um por vez (corte entre blocos e um "E aí" que a voz inventou no fim).
