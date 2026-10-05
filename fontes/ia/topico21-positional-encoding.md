# Dossiê — "Positional Encoding"

Curso "Engenharia de Agentes LLM" (Course 5) · Módulo "Fundamentos de LLMs" (id 8) · Aula
"Transformers por dentro" (lesson 88) · `Topico.id=21` · 2026-10-05 · gerado pelo `/criar-topico`.
Formato: `docs/processo-topico/FONTES_GUIA.md` + `docs/processo-topico/ia.md`.

**Costura:** vem depois do T19 "Limites do Token ID" e do T20 "Embeddings" (token ID → vetor pela
embedding matrix; dimensão; estático × contextualizado). Antes do T22 "Self-Attention: Query, Key,
Value" e do T23 "Causal Masking + Multi-Head". → **aqui só POSIÇÃO**: por que o modelo precisa dela,
como ela entra (somada ao embedding / dentro da atenção) e as três famílias (aprendida, senoidal,
RoPE). Não explica Q/K/V nem a conta da atenção (T22) — só diz que o RoPE age "na atenção".

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Apostila (primária do curso) | `Estudo IA/aula 02.md`, Parte 6 "O problema da posição" | "O gato derrubou a planta" × "A planta derrubou o gato": mesmos tokens, ordem muda o sentido; "token representation + informação de posição"; exemplo "Tenho dois gatos e pouca luz" com posições 1-6; cita embeddings posicionais aprendidos e RoPE; no pipeline: Token IDs → Embedding lookup → **Positional information** → blocos |
| 2 | Paper original | Vaswani et al., *Attention Is All You Need* (2017), §3.5. https://arxiv.org/abs/1706.03762 | "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence."; "The positional encodings have the same dimension d_model as the embeddings, so that the two can be summed." (d_model = 512 no modelo base); fórmulas PE(pos,2i)=sin(pos/10000^(2i/d_model)), PE(pos,2i+1)=cos(…); "The wavelengths form a geometric progression from 2π to 10000·2π."; "We also experimented with using learned positional embeddings instead, and found that the two versions produced nearly identical results."; "We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training." |
| 3 | Livro-texto | Jurafsky & Martin, *Speech and Language Processing* 3ª ed., cap. 7 "Transformers and Pretraining" (rascunho de ago/2026), §7.4. https://web.stanford.edu/~jurafsky/slp3/7.pdf | "These token embeddings are not position-dependent."; absoluta = embeddings iniciados aleatórios "corresponding to each possible input position up to some maximum length", aprendidos no treino, e **somados** ao embedding do token (mesma dimensão); problema: "plenty of training examples for the initial positions… fewer at the outer length limits. These latter embeddings may be poorly trained and may not generalize well"; senoidal usada no Transformer original e pode capturar que "position 4… is more closely related to position 5 than it is to position 17"; posição relativa "often implemented in the attention mechanism at each layer rather than being added once at the initial input. The most popular such… is the Rotary Position Embedding (RoPE)" |
| 4 | Paper original | Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding* (2021). https://arxiv.org/abs/2104.09864 | RoPE "encodes the absolute position with a rotation matrix and meanwhile incorporates the explicit relative position dependency in self-attention formulation"; propriedades: "flexibility of sequence length", "decaying inter-token dependency with increasing relative distances" |
| 5 | Caso real (modelo em produção) | Touvron et al., *LLaMA: Open and Efficient Foundation Language Models* (2023), §2.2. https://arxiv.org/abs/2302.13971 | "We remove the absolute positional embeddings, and instead, add rotary positional embeddings (RoPE), introduced by Su et al. (2021), at each layer of the network." |
| 6 | Doc oficial | Hugging Face Transformers — GPT-2. https://huggingface.co/docs/transformers/model_doc/gpt2 | `n_positions` (padrão 1024): "The maximum sequence length that this model might ever be used with."; "Pad inputs on the right because GPT-2 uses absolute position embeddings."; `n_embd` 768 |
| 7 | Explicação de especialista | Jay Alammar, *The Illustrated Transformer*. https://jalammar.github.io/illustrated-transformer/ | (paráfrase) vetores de posição somados aos embeddings pra o modelo saber a posição de cada palavra ou a distância entre elas; ilustração de 20 palavras × 512 dimensões; nota de 2020: o paper intercala seno/cosseno, a implementação Tensor2Tensor concatena — mesma informação |
| 8 | Caso que deu errado (pesquisa) | Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (TACL, 2023). https://arxiv.org/abs/2307.03172 | "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts." — mesmo modelos de contexto longo |

Tipos cobertos: apostila, paper original (2), livro-texto, caso real em produção, doc oficial,
especialista, caso que deu errado — **7 de 8**.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| Mesmos tokens em outra ordem mudam o sentido → o modelo precisa de posição | 1, 2 | ok |
| O embedding do token sozinho não carrega posição | 3 ("not position-dependent") | ok |
| O Transformer não tem recorrência nem convolução, por isso precisa "injetar" posição | 2 | ok — **não** explicar aqui por que a atenção ignora ordem (T22) |
| Posição somada ao embedding, mesma dimensão | 2, 3, 7 | ok |
| Aprendida (absoluta): uma linha por posição até um máximo; ex. GPT-2 até 1024 | 3, 6 | ok |
| Problema da aprendida: posições do fim pouco treinadas, não generalizam além do máximo | 3, 6 | ok |
| Senoidal: fórmula fixa (seno/cosseno, frequências diferentes); Vaswani: aprendida deu "quase idêntico"; escolheram senoidal pela possível extrapolação | 2, 3 | ok — "may allow" = PODE permitir (não garantir) |
| RoPE: rotação; absoluta + dependência relativa; aplicada na atenção, em cada camada; mais popular hoje | 3, 4 | ok |
| LLaMA trocou posição absoluta por RoPE em cada camada | 5 | ok |
| "Lost in the middle": informação no meio de contexto longo é menos usada | 8 | ok — estudo de 2023 com os modelos da época; não generalizar pra "todo modelo hoje" |

## Divergências / cuidados
- Vaswani diz que aprendida × senoidal deram resultados "nearly identical" — não dizer que a senoidal é "melhor".
- A extrapolação da senoidal é hipótese do paper ("may allow"), não resultado garantido.
- "Lost in the middle" é um efeito medido, não a causa provada (o paper não atribui só ao positional encoding) → apresentar como "a posição na janela importa na prática", sem dizer que o RoPE causa isso.
- Números de modelos atuais (contexto de X mil tokens) mudam rápido e não foram conferidos → não citar.
- A fórmula vai como curiosidade (bloco de código/fluxo), não como coisa a decorar.

## O que ficou de fora
- Q/K/V e a conta da atenção → T22. Máscara causal → T23.
- Matemática da rotação do RoPE (matrizes 2×2, pares de dimensões) → além do nível.
- ALiBi, extensões de contexto (interpolação, YaRN) → sem fonte conferida aqui; fora do nível.
