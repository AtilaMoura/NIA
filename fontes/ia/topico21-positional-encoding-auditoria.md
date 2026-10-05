# Auditoria — T21 "Positional Encoding"

Conteúdo final: `backend/_criar_topico21_ia.py` → `_topico21_ia_final.json` (16 slides, 8 imagens,
1 fluxo, 5 checkpoints). Dossiê: `topico21-positional-encoding.md`. 2026-10-05.

## 1. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | "O gato derrubou a planta" × "A planta derrubou o gato": mesmos tokens, sentido diferente | 1 (apostila Parte 6) | ✔ |
| s1 | Exemplo samambaia/jiboia | didático (criado pro curso, sem fato técnico) | ✔ |
| s2 | Citação J&M "embeddings de token não dependem da posição" (tradução livre) | 3 | ✔ |
| s2 | Citação Vaswani §3.5 "sem recorrência nem convolução… injetar posição" (tradução livre) | 2 | ✔ |
| s2 | "O Transformer não lê palavra por palavra, em fila, como modelos mais antigos" | 2 ("no recurrence") | ✔ — sem entrar no porquê da atenção (T22) |
| s4 | Vetor de posição com a mesma dimensão, somado ao embedding; d_model = 512 no modelo base | 2, 3, 7 | ✔ |
| s4 | "Tenho dois gatos e pouca luz" com posições 1-6 | 1 | ✔ |
| s5 | Aprendida: vetores iniciados aleatórios, um por posição até um máximo, treinados junto | 3 | ✔ |
| s5 | GPT-2 `n_positions` = 1024 ("comprimento máximo…"); padding à direita por usar posição absoluta | 6 (doc HF) | ✔ |
| s5 | Ponto fraco: poucas amostras nas posições do fim; podem generalizar mal; sem vetor além do limite | 3 (+ dedução direta da tabela finita, 6) | ✔ |
| s7 | Fórmulas PE(pos,2i)=sin, PE(pos,2i+1)=cos, 10000^(2i/d_model) | 2 | ✔ (conferidas no paper) |
| s7 | Comprimentos de onda em progressão geométrica de 2π a 10000·2π | 2 | ✔ |
| s7 | Citação "quase idênticos… pode permitir extrapolar" (tradução livre) | 2 | ✔ |
| s7 | Analogia do relógio (ponteiros em velocidades diferentes) | didática, coerente com "frequências diferentes" (2, 3) | ✔ |
| s8 | Citação RoFormer "matriz de rotação… dependência relativa" (tradução livre) | 4 | ✔ |
| s8 | Propriedades: flexibilidade de comprimento; dependência que decai com a distância | 4 | ✔ |
| s8 | J&M: RoPE é o mais popular; age na atenção em cada camada | 3 | ✔ |
| s8 | LLaMA: removeu posição absoluta e pôs RoPE "em cada camada da rede" | 5 | ✔ (corrigido: "a Meta escreveu" → "os autores escrevem", a fonte não fala da empresa) |
| s10 | Citação Lost in the Middle (tradução livre); vale até pra modelos de contexto longo | 8 | ✔ |
| s10 | "Sem exagero": efeito medido em 2023, não causa provada | cuidado do dossiê | ✔ |
| s11 | Aplicações Garden Center e portaria (onde pôr regras, tool e cadastro) | aplicação de 8 + ia.md (fechar com agente real) | ✔ — recomendação prática, não fato novo |
| s13 | Resumo = só o que foi dito | — | ✔ |

## 2. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-3.5-flash`) e Groq (`qwen3.8-27b`). Arquivos
`backend/_conteudo_{conteudo,segunda_opiniao}_topico21.json`. Os dois seguiram a ordem do roteiro,
mas trouxeram afirmações fora do dossiê:

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| Gemini | "modelos modernos (como o LLaMA 3) aceitam contextos de até 128k tokens" graças ao RoPE | número de modelo atual não conferido + relação causal sem fonte (o dossiê proíbe) |
| Gemini | "concatenar aumentaria o tamanho do vetor a cada palavra" | raciocínio errado (concatenar acrescenta um número fixo de dimensões, não "a cada palavra") |
| Gemini | "o RoPE entende perfeitamente a distância" | exagero; a fonte fala em "dependência relativa" |
| ambos | detalhe de Query/Key, produto escalar, "preserva a magnitude" | é do T22 (e fora do dossiê) |
| Groq | PE "adicionado (ou concatenado)" | as fontes (Vaswani, J&M, Alammar) dizem SOMADO |
| Groq | "modelos da família Transformer utilizam senoidal… BERT opta diferente" | sugere que a senoidal é a regra; sem fonte |
| Groq | "o encoding garante…" (2x); "janelas deslizantes" | exagero / fora do dossiê |
| Groq | analogia do "maestro pintando cadeiras" | confusa (mistura aprendida e senoidal) |
| Gemini | bloco `diagrama` (2x) | proibido (usar `fluxo`) |

Aproveitado: só a ordem geral (bate com o roteiro) e a ideia de fechar com "Lost in the Middle" no
agente de vendas (já planejada). Nenhum texto copiado.

## 2b. Imagens
8 geradas (isométrico claro, paleta do catálogo). Aceitas com observação: a capa tem um "09"
pequeno numa engrenagem do fundo (periférico, não em destaque); `t21-rope` mostra uma seta só (não
duas) → legenda e alt ajustados pro que a imagem mostra ("girado num ângulo que depende da posição").

## 3. Pedagogia
- Abre retomando o T20 (embedding = o que o token é) e fecha com ponte pro T22 (Self-Attention).
- Três famílias em ordem histórica, cada uma com a fonte primária.
- Checkpoints: tf, mc, classify (6 itens), associar, mc com cenário + **2 abertas** (ck5_2, ck5_3) ✔.
- Reflexão "💭 Pra pensar" + Resumo ✔. Caso que deu errado (Lost in the Middle) ✔.
  Aplicação em agente real: Garden Center **e** portaria (alternância pedida no ia.md) ✔.

## 4. Continuidade
- Não explica Q/K/V nem a conta da atenção (T22) — só diz que o RoPE age "dentro da atenção".
- Não repete o T20 (dimensão/estático×contextual) além da retomada.
- Nenhum número de contexto de modelo atual (mudam rápido, não conferidos).

## 5. Estrutura
- `validar_topico()` vazio; 0 `None` no render (azul-petroleo); ids de pergunta e item únicos;
  `fluxo` (nenhum `diagrama`); capa com `imagem_capa`. O schema não tem bloco de código → fórmula
  num `box` de itens, marcada como curiosidade.

**Pendências: 0.**
