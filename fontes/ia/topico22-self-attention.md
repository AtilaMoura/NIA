# Dossiê — "Self-Attention: Query, Key, Value"

Curso "Engenharia de Agentes LLM" (Course 5) · Módulo "Fundamentos de LLMs" (id 8) · Aula
"Transformers por dentro" (lesson 88) · `Topico.id=22` · 2026-10-12 · gerado pelo `/criar-topico`.
Formato: `docs/processo-topico/FONTES_GUIA.md` + `docs/processo-topico/ia.md`. Todas as fontes
acessadas em 2026-10-12; PDFs, páginas e código baixados e lidos no texto.

**Costura:** 4º tópico da aula. Já vistos: T19 (cada token precisa dos outros; ID é só índice),
T20 (embedding: vetor por token; cosseno; "a conta por trás volta no tópico de Self-Attention"; as
camadas constroem a representação contextual), T21 (posição somada ao embedding; RoPE age "dentro
da atenção"). Depois: T23 "Causal Masking + Multi-Head Attention", T24 "Dentro do bloco
Transformer". → **aqui UMA cabeça de atenção, sem máscara**: o problema, a definição, Q/K/V, os
quatro passos da conta (produto escalar → escala → softmax → soma dos Values), por que "self", e o
cuidado de não ler peso de atenção como explicação. **Não** explica máscara causal, várias cabeças,
MLP, residual nem KV cache.

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Apostila (primária do curso) | `Estudo IA/aula 02.md`, Partes 7–12 | "Tenho dois gatos, pouca iluminação e quero uma planta bonita" — ao processar "planta", quais tokens importam; "não existe uma tabela manual… Essa relação é aprendida"; Q = XW_Q, K = XW_K, V = XW_V, matrizes aprendidas; Query = "que tipo de informação este token precisa?", Key = "que tipo de informação este token pode oferecer?", Value = "qual informação será transferida…"; "Não tome essas frases literalmente"; scores "não são probabilidades ainda"; Attention(Q,K,V) = softmax(QKᵀ/√d_k)V em 4 passos; pesos de exemplo somando 1,00; soma ponderada dos Values → "nova representação contextualizada"; Parte 11: "Attention não significa: 'o modelo descobriu conscientemente que gatos são importantes'. Attention é uma operação matemática"; Parte 12: "Por que self? Porque Q, K e V são derivados da própria sequência" |
| 2 | Paper original | Vaswani et al., *Attention Is All You Need* (2017), §2, §3.2, §3.2.1. https://arxiv.org/abs/1706.03762 | "An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors. The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key."; "We compute the dot products of the query with all keys, divide each by √d_k, and apply a softmax function to obtain the weights on the values."; Attention(Q,K,V) = softmax(QKᵀ/√d_k)V; "We suspect that for large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients. To counteract this effect, we scale the dot products by 1/√d_k."; "Self-attention, sometimes called intra-attention is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence." |
| 3 | Livro-texto | Jurafsky & Martin, *Speech and Language Processing* 3ª ed. (rascunho de 19/ago/2026), cap. 7, §7.1. https://web.stanford.edu/~jurafsky/slp3/7.pdf | três papéis de cada vetor de entrada: *query* = "the current element being compared to the preceding inputs"; *key* = "a preceding input that is being compared to the current element to determine a similarity weight"; *value* = "a preceding element that gets weighted and summed up to compute the output"; "transformers introduce weight matrices W^Q, W^K, and W^V"; produto escalar: "The larger the score, the more similar the vectors that are being compared"; "We'll normalize these scores with a softmax"; "Attention is the mechanism in the transformer that weighs and combines the representations from appropriate other tokens in the context"; a rede feedforward opera em cada posição separadamente, em contraste com a atenção, "whose job is to mix information from different token positions" |
| 4 | Explicação de especialista | Jay Alammar, *The Illustrated Transformer*. https://jalammar.github.io/illustrated-transformer/ | frase "The animal didn't cross the street because it was too tired" — a self-attention permite associar "it" a "animal"; seis passos: criar Query, Key e Value "by multiplying the embedding by three matrices that we trained"; score = produto escalar da query com a key; dividir por 8 ("the square root of the dimension of the key vectors used in the paper – 64"), o que leva a gradientes mais estáveis; softmax "normalizes the scores so they're all positive and add up to 1"; multiplicar cada value pelo peso e somar; palavras irrelevantes são "afogadas" por números minúsculos |
| 5 | Paper original (origem da ideia) | Bahdanau, Cho, Bengio, *Neural Machine Translation by Jointly Learning to Align and Translate* (2014; ICLR 2015). https://arxiv.org/abs/1409.0473 | o vetor de tamanho fixo é "a bottleneck"; propõem "allowing a model to automatically (soft-)search for parts of a source sentence that are relevant to predicting a target word" |
| 6 | Projeto real (código) | Andrej Karpathy, `nanoGPT`, arquivo `model.py`, classe da atenção. https://github.com/karpathy/nanoGPT | `q, k, v = self.c_attn(x).split(...)`; `att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))`; `att = F.softmax(att, dim=-1)`; depois `att @ v`. (Entre a 1ª e a 2ª linha há uma linha de máscara — assunto do T23.) |
| 7 | Caso que deu errado / pesquisa | Jain & Wallace, *Attention is not Explanation* (2019). https://arxiv.org/abs/1902.10186 | pesos de atenção são apresentados como indicando a importância das entradas, mas: "learned attention weights are frequently uncorrelated with gradient-based measures of feature importance, and one can identify very different attention distributions that nonetheless yield equivalent predictions"; "standard attention modules do not provide meaningful explanations and should not be treated as though they do" |
| 8 | Pesquisa (o contraponto) | Wiegreffe & Pinter, *Attention is not not Explanation* (2019). https://arxiv.org/abs/1908.04626 | "We challenge many of the assumptions underlying this work, arguing that such a claim depends on one's definition of explanation, and that testing it needs to take into account all elements of the model." |

Tipos cobertos: apostila/material didático, paper original (2), livro-texto, especialista, projeto
real, caso que deu errado, artigo de pesquisa — **7 de 8**.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| A atenção deixa a representação de um token incorporar informação de outros tokens relevantes; a relação é aprendida, não programada | 1, 3, 4 | ok |
| Definição: query + pares key-value → saída = soma ponderada dos values; peso = compatibilidade query × key | 2 | ok |
| A ideia de "busca suave" vem da tradução automática (2014) | 5 | ok |
| Cada vetor é projetado em Q, K e V por três matrizes aprendidas | 1, 3, 4 | ok |
| As frases "precisa / oferece / transfere" são interpretação, não objetos guardados | 1 | ok |
| Passo 1: produto escalar query·key; quanto maior, mais compatível | 2, 3, 4 | ok |
| Passo 2: dividir por √d_k (no paper d_k = 64 → divide por 8); motivo: produtos grandes empurram a softmax para regiões de gradiente minúsculo | 2, 4 | ok — o paper diz "suspeitamos": escrever como hipótese dos autores |
| Passo 3: softmax → pesos positivos que somam 1 | 2, 3, 4 | ok |
| Passo 4: soma dos Values com esses pesos = nova representação contextualizada | 1, 2, 4 | ok |
| "Self": Q, K e V saem da mesma sequência; relaciona posições de uma única sequência | 1, 2 | ok |
| No código real são três linhas | 6 | ok — avisar que a linha de máscara é do T23 |
| Peso de atenção não é, por si, explicação da decisão do modelo | 1 (Parte 11), 7 | ok — com o contraponto (8) |

## Divergências entre fontes
- **Atenção explica ou não?** Jain & Wallace (2019): não deve ser tratada como explicação.
  Wiegreffe & Pinter (2019): depende da definição de explicação e do teste. → o tópico **mostra a
  divergência** e tira a lição prática comum às duas: peso de atenção não é prova do motivo.
  Os dois estudos usaram principalmente modelos anteriores aos LLMs atuais (redes recorrentes com
  atenção) — dizer isso, não generalizar.
- J&M descrevem a atenção já olhando só para os tokens anteriores (modelo de linguagem causal);
  Vaswani/Alammar descrevem sem essa restrição. Aqui vai a versão sem máscara; o T23 acrescenta.

## Cuidados
- Os números do exemplo (scores e pesos) são **inventados para ilustrar**; a conta entre eles tem
  que fechar. A linha de pesos da apostila (0,01 / 0,37 / 0,18 / 0,31 / 0,13) não sai da linha de
  scores que ela mostra antes (são exemplos separados). Para o aluno poder refazer a conta, o
  tópico usa scores escalados 0,4 / 4,0 / 3,3 / 3,8 / 3,0, cuja softmax dá 1% / 37% / 18% / 30% /
  14% (soma 100%) — quase a mesma distribuição da apostila.
- Não dizer que o modelo "decide" ou "percebe": é conta com matrizes aprendidas (apostila, Parte 11).
- d_k = 64 é do modelo do paper de 2017; não é regra geral.

## O que ficou de fora
- Máscara causal e várias cabeças → T23. MLP, residual, layer norm → T24. KV cache → T25.
- Atenção aditiva × multiplicativa (Vaswani §3.2.1), complexidade O(n²) → além do nível.
- Ferramentas de visualização de atenção → sem fonte conferida aqui.
