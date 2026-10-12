# Dossiê — "Embeddings"

Curso "Engenharia de Agentes LLM" (Course 5) · Módulo "Fundamentos de LLMs" (id 8) · Aula
"Transformers por dentro" (lesson 88) · `Topico.id=20` · 2026-10-12 · **revisão completa** (o
conteúdo anterior saiu do Groq com correção manual, sem dossiê, sem imagens internas e sem áudio).
Formato: `docs/processo-topico/FONTES_GUIA.md` + `docs/processo-topico/ia.md`. Todas as fontes
acessadas em 2026-10-12; os PDFs foram baixados e as frases lidas no texto extraído.

**Costura:** vem depois do T19 "Limites do Token ID" (ID é índice, "número de prontuário"; 8274 >
3190 não diz nada; falta uma representação em que proximidade matemática = proximidade de
significado; promete "embedding matrix, dimensão e o banco financeiro × banco de sentar"). Antes do
T21 "Positional Encoding" (posição somada ao embedding) e do T22 "Self-Attention". → **aqui só o
VETOR**: o que é, de onde sai (tabela), tamanho, proximidade, estático × contextual, viés, e o uso
de modelos de embedding num agente. Não explica posição (T21) nem como a atenção mistura o contexto
(T22) — só diz que as camadas fazem isso.

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Apostila (primária do curso) | `Estudo IA/aula 02.md`, Partes 2–5 | "Tenho dois gatos e pouca luz." → [4821, 1359, 8274, 74, 5291, 3190, 13]; "gatos → [0.21, -0.72, 1.13, 0.08, ...]" ("simplificando absurdamente"); "Em modelos reais, esse vetor pode possuir milhares de dimensões"; E ∈ R^(V×d), V = vocabulário, d = dimensão; "embedding = E[8274]"; "um lookup extremamente grande"; "Embeddings são vetores que representam o significado das palavras" = útil mas incompleto; "O banco aprovou meu financiamento" × "Sentei no banco da praça": parte de representação semelhante e, depois das camadas, incorpora o contexto; Parte 5: "Tenho gatos" → "Tenho gatos e quero uma planta" (toxicidade, pet-safe) → "Tenho gatos, pouca luz e quero uma planta" |
| 2 | Paper original | Vaswani et al., *Attention Is All You Need* (2017), §3.1 e §3.4, Tabela 3. https://arxiv.org/abs/1706.03762 | §3.4: "Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model."; §3.1: todas as subcamadas "as well as the embedding layers, produce outputs of dimension d_model = 512"; Tabela 3: modelo "big" com d_model = 1024 |
| 3 | Livro-texto | Jurafsky & Martin, *Speech and Language Processing* 3ª ed. (rascunho de 19/ago/2026), cap. 5 "Embeddings", cap. 6 §"embedding matrix", cap. 7 "Transformers and Pretraining". https://web.stanford.edu/~jurafsky/slp3/ | Cap. 5: "embeddings, short dense vectors… with number of dimensions d ranging from 50-1000, rather than the much larger vocabulary size \|V\|. These d dimensions don't have a clear interpretation… the values will be real-valued numbers that can be negative"; "By far the most common similarity metric is the cosine of the angle between the vectors"; "The cosine value ranges from 1 for vectors pointing in the same direction, through 0 for orthogonal vectors, to -1 for vectors pointing in opposite directions"; "Word2vec embeddings are static embeddings, meaning that the method learns one fixed embedding for each word in the vocabulary… contextual embeddings like the popular family of BERT representations, in which the vector for each word is different in different contexts"; analogia: o resultado costuma ser uma das palavras de entrada, "so these must be explicitly excluded", e funciona bem com "frequent words, small distances, and certain relations"; §5.8: "embeddings, alas, also reproduce the implicit biases and stereotypes that were latent in the text"; "algorithms that use embeddings as part of a search for hiring potential programmers or doctors might thus incorrectly downweight documents with women's names"; "embeddings don't just reflect the statistics of their input, but also amplify bias". Cap. 6: "Each row of the embedding matrix represents each token of the vocabulary V as a (row) vector of dimensionality d… E has shape [\|V\| × d]"; "we use indexing to select the corresponding rows from E". Cap. 7: "Each token is first converted to an embedding from the embedding matrix E"; "In a transformer, layer by layer, we build up richer and richer contextualized representations of the meanings of input tokens" |
| 4 | Paper original | Mikolov, Chen, Corrado, Dean, *Efficient Estimation of Word Representations in Vector Space* (word2vec, 2013). https://arxiv.org/abs/1301.3781 | "vector("King") - vector("Man") + vector("Woman") results in a vector that is closest to the vector representation of the word Queen"; palavras antes eram "represented as indices in a vocabulary", sem "notion of similarity between words"; "less than a day to learn high quality word vectors from a 1.6 billion words data set" |
| 5 | Paper original | Peters et al., *Deep contextualized word representations* (ELMo, 2018). https://arxiv.org/abs/1802.05365 | "a new type of deep contextualized word representation that models both (1) complex characteristics of word use (e.g., syntax and semantics), and (2) how these uses vary across linguistic contexts (i.e., to model polysemy)" |
| 6 | Paper original | Devlin et al., *BERT* (2018), §3. https://arxiv.org/abs/1810.04805 | "WordPiece embeddings… with a 30,000 token vocabulary"; BERT-base H=768, BERT-large H=1024 |
| 7 | Doc oficial | Hugging Face Transformers — GPT-2 (`GPT2Config`). https://huggingface.co/docs/transformers/model_doc/gpt2 | `vocab_size` padrão 50257: "Vocabulary size of the model"; `n_embd` padrão 768: "Dimensionality of the embeddings and hidden states" → tabela de 50.257 × 768 = 38.597.376 números (conta nossa) |
| 8 | Doc oficial (modelo de embedding como produto) | OpenAI, guia "Vector embeddings". https://developers.openai.com/api/docs/guides/embeddings | "An embedding is a vector (list) of floating point numbers."; "Small distances suggest high relatedness and large distances suggest low relatedness."; tamanho padrão 1536 (`text-embedding-3-small`) e 3072 (`text-embedding-3-large`); usos listados: busca, agrupamento, recomendações, detecção de anomalia, medida de diversidade, classificação; "We recommend cosine similarity." |
| 9 | Explicação de especialista | Jay Alammar, *The Illustrated Word2vec*. https://jalammar.github.io/illustrated-word2vec/ | vetor GloVe de "king" treinado na Wikipédia: "It's a list of 50 numbers."; "king" − "man" + "woman": "queen" é a palavra mais próxima entre 400.000; similaridade de cosseno como jeito comum de medir |
| 10 | Caso que deu errado (pesquisa) | Bolukbasi, Chang, Zou, Saligrama, Kalai, *Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings* (2016). https://arxiv.org/abs/1607.06520 | "even word embeddings trained on Google News articles exhibit female/male gender stereotypes to a disturbing extent"; o mesmo sistema das analogias responde "man is to computer programmer as woman is to x" com x = homemaker, e "father is to a doctor as a mother is to a nurse"; embedding word2vec do Google News: 3 milhões de palavras e termos, 300 dimensões; "The blind application of machine learning runs the risk of amplifying biases present in data." |

Tipos cobertos: apostila (material didático), paper original (4), livro-texto, doc oficial (2),
especialista, caso que deu errado, caso real em produção (GPT-2, BERT, API de embeddings) — **7 de 8**.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| Embedding = vetor (lista de números reais, podem ser negativos) que representa o token | 1, 3, 8 | ok |
| Sai de uma tabela: matriz E com uma linha por token do vocabulário, formato V × d; o ID só escolhe a linha | 1, 3 (cap. 6 e 7) | ok |
| Os valores são aprendidos no treino, ninguém os escreve | 2 ("learned embeddings"), 3 | ok |
| GPT-2: vocabulário 50.257, dimensão 768 | 7 | ok — produto 38.597.376 é conta nossa, dita como tal |
| Dimensão: 512 (Transformer base 2017), 1024 (big); 768/1024 (BERT base/large); estáticos de 50 a 1000 | 2, 6, 3 | ok |
| As dimensões não têm interpretação clara | 3 | ok — não dizer "uma dimensão = uma característica" |
| Proximidade: cosseno, de 1 (mesma direção) a −1 (opostas), 0 = ortogonais | 3, 8, 9 | ok — sem fórmula (produto escalar aparece no T22) |
| rei − homem + mulher ≈ rainha | 4, 9, 3 | ok — com a ressalva do J&M (palavras de entrada excluídas; funciona pra palavras frequentes e certas relações) |
| Estático = um vetor fixo por palavra (word2vec); contextual = vetor diferente em cada contexto | 3, 5 | ok |
| No Transformer, o embedding inicial é o mesmo e as camadas constroem a representação contextualizada | 1, 3 (cap. 7) | ok — "como" é o T22 |
| Embeddings reproduzem (e amplificam) vieses do texto de treino | 10, 3 | ok |
| Modelos de embedding (API) devolvem um vetor por texto; distância pequena = alta relação; servem pra busca | 8 | ok — relação ≠ fato; fato de negócio vem de tool (linha do curso desde a Aula 1) |

## Casos reais / caso que deu errado
- **Real:** GPT-2 (50.257 × 768), BERT (30.000 tokens, 768/1024), API de embeddings (1536/3072).
- **Deu errado:** Bolukbasi et al. (2016) — embedding público treinado em notícias responde
  "programador − homem + mulher = dona de casa". J&M: usado numa busca de currículos, isso pode
  rebaixar documentos com nome de mulher.

## Divergências / cuidados
- "Embedding = significado" é a simplificação que a apostila chama de incompleta: dizer
  "representação aprendida a partir do uso"; o sentido em contexto vem depois das camadas.
- A analogia rei/rainha não é mágica: J&M avisam das condições. Não dizer que "sempre funciona".
- Não confundir os dois usos da palavra: (a) a tabela de entrada do LLM (um vetor por token);
  (b) modelo de embedding vendido por API (um vetor por texto inteiro). O conteúdo antigo misturava.
- O exemplo de vetor [0.21, -0.72, 1.13, 0.08, …] é inventado pela apostila pra ilustrar — dizer isso.
- Os IDs 4821, 1359, 8274… são ilustrativos (apostila), não de um tokenizador real.
- Dimensão e nome de modelos de API mudam rápido: citar com "na documentação consultada em out/2026".

## O que ficou de fora
- Como o word2vec é treinado (skip-gram, amostragem negativa) → além do nível; só "aprendido do uso".
- Posição → T21. Q/K/V, produto escalar e a conta da atenção → T22.
- Matriz de saída/unembedding e compartilhamento de pesos (Vaswani §3.4) → Parte 24 da apostila.
- Banco vetorial, chunking, RAG completo → aulas de Retrieval (aqui só a ideia de buscar por proximidade).
- Números do conteúdo antigo ("128 dimensões bastam pra estoque", "latência < 200 ms", "recall > 90%",
  fallback `<unk>`, FAISS) → sem fonte; removidos.
