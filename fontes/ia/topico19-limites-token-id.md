# Dossiê — "O problema e a virada — limites do Token ID"

Curso "Engenharia de Agentes LLM" (Course 5) · Módulo "Fundamentos de LLMs" (id 8) · Aula
"Transformers por dentro" (lesson 88) · `Topico.id=19` · 2026-10-12 · **revisão completa** (o
conteúdo anterior era o port do deck de estudo do Atila: validado por ele, mas sem dossiê, sem
imagens internas, sem áudio, sem Reflexão e com 2 blocos `diagrama`). A estrutura e as ideias do
deck foram mantidas; o que muda é a fonte de cada afirmação e o formato.
Todas as fontes acessadas em 2026-10-12; PDFs e arquivos baixados e lidos no texto.

**Costura:** primeiro tópico da Aula 2. Vem depois do T18 "Aplicação no agente" (Aula 1: o LLM faz
linguagem, fatos vêm de tools). Antes do T20 "Embeddings" — que abre com "No tópico anterior, a
mensagem 'Tenho dois gatos e pouca luz' virou [4821, 1359, 8274, 74, 5291, 3190]… o ID é como um
número de prontuário" (**manter essa frase, essa lista e essa comparação**). → **aqui só o
PROBLEMA**: por que os tokens precisam se relacionar, o que é o Token ID, de onde vem o número e
por que ele não serve pra comparar significado. Não explica embedding (T20) nem Attention (T22).

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Apostila (primária do curso) | `Estudo IA/aula 02.md`, Partes 1–2; deck `Estudo IA/exercicios/aula2-topico1-limites-do-token-id.html` | "O cliente tem dois gatos. Ele procura uma planta bonita para colocar na sala." — "Ele" precisa se relacionar com algo anterior; "planta" com cliente, sala, bonita, gatos; Garden: apartamento pequeno → espaço; pouca iluminação → ambiente; dois gatos → segurança; planta bonita → estética; "como fazer cada token acessar informações relevantes dos demais tokens?" → Attention; "antes de Attention precisamos transformar linguagem em matemática"; "Tenho dois gatos e pouca luz" → Tenho 4821, dois 1359, gatos 8274, e 74, pouca 5291, luz 3190; "8274 > 3190" não diz nada; "Token IDs são basicamente índices" |
| 2 | Paper original | Vaswani et al., *Attention Is All You Need* (2017), §1 e §2. https://arxiv.org/abs/1706.03762 | Mecanismos de atenção permitem "modeling of dependencies without regard to their distance in the input or output sequences"; nas arquiteturas anteriores citadas, relacionar duas posições custa mais quanto maior a distância, o que "makes it more difficult to learn dependencies between distant positions" |
| 3 | Livro-texto | Jurafsky & Martin, *Speech and Language Processing* 3ª ed. (rascunho de 19/ago/2026), cap. 2 (tokens e BPE), cap. 6 (índices do vocabulário), cap. 7 (contexto distante). https://web.stanford.edu/~jurafsky/slp3/ | Cap. 2: "the true output of the tokenizer is simply a sequence of unique token ids"; BPE: "The most frequent neighboring pair of characters is 'A B' so we merge those, add a new merged token 'AB' to the vocabulary…"; continua "until k merges have been done creating k novel tokens"; "The resulting vocabulary consists of the original set of characters plus k new symbols". Cap. 6: "we first convert the tokens into vocabulary indices (these were created when we first tokenized the input using BPE or SentencePiece)". Cap. 7: "I walked along the pond, and noticed one of the trees along the bank" — "bank" é a margem e não a instituição financeira "because of the context, including words like pond"; "these contextual words that help us compute the meaning of words in context can be quite far away in the sentence or paragraph" |
| 4 | Paper original | Sennrich, Haddow, Birch, *Neural Machine Translation of Rare Words with Subword Units* (BPE, 2016), §3.2. https://arxiv.org/abs/1508.07909 | "We iteratively count all symbol pairs and replace each occurrence of the most frequent pair ('A', 'B') with a new symbol 'AB'. Each merge operation produces a new symbol…" |
| 5 | Dado real (primário) | Vocabulário público do GPT-2: `vocab.json` em https://huggingface.co/openai-community/gpt2 (baixado e lido) | 50.257 entradas. IDs 0–255: símbolos básicos (0 = "!"). 256 = " t", 257 = " a", 262 = " the". Último: 50256 = "<\|endoftext\|>". " cat" = 3797, entre 3796 "rief" e 3798 "esc" (3795 " psych", 3799 " observ"). " dog" = 3290 (entre "inally" e "mitted"). " cats" = 11875 (entre " engines" e " buffer"). " happy" = 3772; " prison" = 3770; " glad" = 9675; " sad" = 6507. No GPT-2, o ID 8274 é " Bru" e o 3190 é " completely" → os IDs da apostila são ilustrativos |
| 6 | Doc oficial | Hugging Face Transformers — Glossário, "input IDs"; `GPT2Config.vocab_size`. https://huggingface.co/docs/transformers/glossary | "They are token indices, numerical representations of tokens building the sequences that will be used as input by the model."; "Each tokenizer works differently but the underlying mechanism remains the same." |
| 7 | Explicação de especialista | Andrej Karpathy, repositório `minbpe` (README e lecture.md). https://github.com/karpathy/minbpe | "minbpe always allocates the 256 individual bytes as tokens, and then merges bytes as needed from there… when (a,a) is merged to Z, Z will become 256. Likewise Y will become 257 and X 258"; "the integer 'plucks out' a row of this embedding table" |
| 8 | Caso que deu errado | RISKS Digest vol. 18, nº 7 (abril de 1996), "AOL censors British town's name!", repassando o Computer underground Digest e o *Scunthorpe Evening Telegraph* de 9/abr/1996. http://catless.ncl.ac.uk/Risks/18/07 | Um morador de Scunthorpe (Inglaterra) não conseguiu se registrar na AOL: o programa de cadastro, com filtro de indecência, não aceitava o nome da cidade; ele só conseguiu escrevendo "Sconthorpe", e a AOL anunciou que passaria a chamar a cidade assim |
| 9 | Paper original (apoio) | Mikolov et al., word2vec (2013), Introdução. https://arxiv.org/abs/1301.3781 | expectativa de que "similar words tend to be close to each other" numa representação vetorial (a citação longa sobre "índices num vocabulário" já está no T20 — aqui só paráfrase) |

Tipos cobertos: apostila/material didático, paper original (3), livro-texto, dado real, doc oficial,
especialista, caso que deu errado — **7 de 8**.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| Cada token precisa de informação de outros tokens, que podem estar longe | 1, 2, 3 (cap. 7) | ok |
| A resposta do Transformer é a Attention (não explicar aqui) | 1, 2 | ok |
| A saída do tokenizador é uma sequência de IDs; ID = índice do token no vocabulário | 3 (cap. 2 e 6), 6 | ok |
| O número vem da construção do vocabulário: símbolos básicos primeiro, depois um token novo a cada junção do par mais frequente | 3 (cap. 2), 4, 7, 5 | ok — o deck dizia "ordem de descoberta ou frequência"; agora preciso: ordem de criação no BPE, que é guiada por frequência |
| No GPT-2 real, vizinhos de ID não têm relação de sentido; palavras relacionadas ficam longe | 5 | ok — dado lido no arquivo |
| Diferença entre IDs não mede semelhança | 1, 5 | ok |
| Cada tokenizador tem os seus IDs | 3 (cap. 6), 6 | ok |
| Comparar texto literal ≠ comparar significado (caso Scunthorpe) | 8 | ok — o caso é de comparação de letras, não de IDs; apresentado como "o mesmo tipo de erro" |
| A saída: uma representação em que proximidade matemática = proximidade de uso (embedding) | 1, 9 | ok — só a pista; o T20 explica |

## Divergências / cuidados
- Os IDs 4821, 1359, 8274… são **ilustrativos** (apostila). No GPT-2, 8274 é " Bru". Dizer isso no texto.
- "IDs por frequência" é impreciso: a frequência decide a ORDEM das junções; o ID é a ordem de criação.
- Os exemplos reais são em inglês (o vocabulário do GPT-2 é de texto em inglês); o espaço antes da
  palavra faz parte do token — simplificar como "a palavra cat".
- Não dizer que o ID "não serve pra nada": ele serve pra achar a linha na tabela (T20).
- Scunthorpe: a fonte não detalha a regra do filtro; não afirmar qual palavra ele procurava.
  As fontes divergem sobre COMO o morador conseguiu se cadastrar (o RISKS diz "Sconthorpe"; o jornal
  local, citado em outros lugares, diz que ele trocou o endereço) → não afirmar; só o que todas dizem:
  o cadastro foi recusado e a AOL passou a usar "Sconthorpe".

## O que ficou de fora
- Como o BPE trata espaços, bytes e Unicode → Aula 1 (tokens) já cobriu o necessário.
- One-hot → além do nível. Embedding matrix, dimensão, proximidade → T20. Attention → T22.
- Do deck antigo: a lista de usos "RAG, deduplicação, moderação" virou exemplos mais concretos; os
  cards "geração de código (total e sum)" e "análise de sentimento" ficaram só como exemplos de pares.
