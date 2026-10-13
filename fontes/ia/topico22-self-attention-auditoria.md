# Auditoria — Tópico 22 "Self-Attention: Query, Key, Value"

Curso de IA (Course 5) · `Topico.id=22` · 2026-10-12 · régua: `fontes/ia/topico22-self-attention.md`.
Conteúdo auditado: `backend/_criar_topico22_ia.py` → `_topico22_ia_final.json` (17 slides).
**Resultado: 0 pendências.**

## 1. Afirmações do tópico → fonte

| Slide | Afirmação | Fonte (#) | Status |
|---|---|---|---|
| s1 | Cada token já tem vetor e posição, mas montados sem olhar os vizinhos | T20, T21; 3 | ok |
| s1 | Frase do cliente; ao processar "planta", "gatos" e "iluminação" pesam mais que "dois" | 1 (Parte 7) | ok — "provavelmente", como na apostila ("talvez") |
| s1 | Frase do animal e da rua; a self-attention permite associar "ele" a "animal" | 4 | ok — paráfrase atribuída a Alammar |
| s1 | Não existe tabela manual; a relação é aprendida | 1 (Parte 7) | ok |
| s2 | Citação da definição de atenção | 2 (§3.2, lido no PDF) | ok — tradução livre; "[…]" marca o trecho omitido |
| s2 | Bahdanau, Cho e Bengio (2014): "busca suave" em vez de um vetor de tamanho fixo | 5 (resumo, lido no PDF) | ok |
| s4 | Três papéis: elemento atual / comparado para definir peso / pesado e somado | 3 (§7.1) | ok — J&M falam em entradas "anteriores"; aqui "os outros", porque a máscara é do T23 (ver item 5) |
| s4 | Três matrizes aprendidas; vetor × matriz → Q, K, V | 1, 3, 4 | ok |
| s4 | Frases "precisa / oferece / passa adiante" + "não leve ao pé da letra" | 1 (Parte 8) | ok |
| s5 | Produto escalar; quanto maior, mais parecidos | 3 | ok |
| s5 | [1, 2]·[3, 1] = 5 | conta conferida no script | ok |
| s5 | Notas da Query de "planta" (3,2 / 32,0 / 26,4 / 30,4 / 24,0) | inventadas, dito no texto | ok |
| s5 | Notas não são probabilidades | 1 (Parte 9) | ok |
| s6 | d_k = 64 no paper de 2017 → divide por 8 | 2 (§3.2.2: "d_k = d_v = d_model/h = 64"), 4 | ok |
| s6 | Motivo da divisão, como suspeita dos autores | 2 ("We suspect…") | ok — "quase não consegue aprender" = gradientes extremamente pequenos |
| s6 | Softmax: pesos positivos que somam 1; mesma função da Aula 1 | 2, 4; T16 | ok |
| s6 | 0,4 / 4,0 / 3,3 / 3,8 / 3,0 → 1% / 37% / 18% / 30% / 14% | **conta conferida por `assert` no script** | ok |
| s6 | "gatos" e "luz" juntos = dois terços | 37 + 30 = 67 | ok |
| s8 | Multiplicar cada Value pelo peso e somar; irrelevantes "afogadas" | 4 (passos 5 e 6) | ok |
| s8 | Resultado = nova representação contextualizada | 1 (Parte 10) | ok |
| s8 | Fórmula Attention(Q,K,V) = softmax(QKᵀ/√d_k)V | 2 (eq. 1) | ok |
| s9 | "Self": Q, K, V da mesma sequência; definição do paper | 1 (Parte 12), 2 (§2) | ok |
| s9 | Todos os tokens fazem a conta ao mesmo tempo | 2 (matrizes Q, K, V empacotadas), 4 | ok |
| s9 | Três linhas do nanoGPT | 6 (linhas lidas no arquivo, literais) | ok |
| s9 | Há outras linhas no meio; uma é a máscara | 6 (`masked_fill`, e também `attn_dropout`) | ok — corrigido: a 1ª versão dizia "mais uma linha" |
| s11 | Atenção é conta; o comportamento vem das matrizes aprendidas | 1 (Parte 11) | ok |
| s11 | Jain & Wallace (2019): pesos pouco correlacionados com outras medidas; distribuições diferentes, mesma resposta; citação | 7 (resumo, lido no PDF) | ok |
| s11 | Wiegreffe & Pinter (2019): depende da definição; teste precisa do modelo inteiro | 8 (resumo) | ok |
| s11 | Os dois estudos usaram principalmente modelos anteriores aos LLMs de hoje | 7 (texto: 36 menções a LSTM, nenhuma a Transformer), 8 ("especially within RNN models") | ok |
| s12 | A ligação é calculada com pesos aprendidos, não garantida → restrição crítica em código | consequência de 1 (Parte 11) + linha do curso (T18) | ok — é recomendação de projeto, escrita como tal |
| s12 | Mapa de atenção = pista, não laudo | 7, 8 | ok |

## 2. Fatos de alto risco — conferência refeita

- Fórmula e d_k = 64: lidos no PDF do paper (§3.2.1 e §3.2.2).
- Código do nanoGPT: lido no arquivo `model.py` baixado; as três linhas citadas são literais.
- Exemplo numérico: o script recalcula (÷ √64, softmax, arredondamento) e só grava o JSON se bater.

## 3. Rascunhos (Gemini 3.7 Flash e Groq) — o que NÃO entrou

Nenhum texto dos rascunhos entrou. Erros encontrados:

- **Groq:** apresentou como "código do nanoGPT" três linhas que não estão no arquivo (`self.scale`,
  `attn_weights.softmax`); afirmou que "o peso máximo de atenção dispara a tool" de estoque/preço
  (isso não existe — tool é chamada pelo texto que o modelo gera, não por peso de atenção); mandou
  "substituir o Value por dados da tool"; exemplo numérico com d_k = 2 fora do dossiê; blocos
  inválidos (`vocab`, `badges`).
- **Gemini:** código genérico apresentado como real; dimensão 768 e histórico de RNNs fora do
  dossiê; um CEP real de São Paulo num exemplo; preços inventados; afirmações de certeza sobre
  quais tokens "geram alta compatibilidade".
- A analogia da estante/biblioteca apareceu nos dois e na versão final — é a leitura natural de
  query/key/value; a versão final foi escrita antes de ler os rascunhos.

## 4. Pedagogia

- Ordem: problema → definição em palavras → analogia → os três papéis → a conta em 4 passos com um
  único exemplo que atravessa os slides → fórmula só depois dos passos → código → cuidado → agente.
- Toda pergunta respondível com o ensinado (ck1: s2, s1; ck2: s4, s5, s6; ck3: s5–s9; ck4: s11,
  s12; ck5: s4, s5–s8, s12).
- Tipos: 4 `mc`, 4 `tf`, 1 `classify`, 1 `associar`, 2 `open`. Ids únicos.

## 5. Continuidade

- Retoma T20 (embedding; "a conta por trás volta no tópico de Self-Attention"; o "banco" na
  Reflexão) e T21 (posição).
- **Não invade o T23:** uma cabeça só, sem máscara. A máscara é citada uma vez (a linha omitida do
  código) e remetida ao próximo tópico. Por isso os papéis de J&M foram escritos com "os outros
  tokens" em vez de "os anteriores".
- `proximo_topico_label` = "Causal Masking + Multi-Head Attention". O "📌 Resumo" se sustenta
  sozinho (vira o "↩ Relembrando" do T23).

## 6. Direito autoral

Duas citações curtas (Vaswani; Jain & Wallace), atribuídas e marcadas como tradução livre; três
linhas de código de projeto aberto, atribuídas.

## 7. Estrutura

`validar_topico()` = `[]`; ids duplicados = nenhum; render local (azul-petroleo) com 0 `None`; capa
com `imagem_capa`; 1 `fluxo`, nenhum `diagrama`; Reflexão "💭" + Resumo "📌".

## 8. Imagens (8: capa + 7; 10 slides de conteúdo → densidade 0,70)

Isométrico claro, todas aprovadas na 1ª geração, olhadas uma a uma (sem letras nem números em
destaque). Ajuste: o `alt` da capa foi reescrito pra bater com a imagem (bloco central com seis ao redor).

## 9. Áudio (35 blocos, MP3)

- Narrações: 17 das 35 reescritas antes da voz. Erros: 1ª narração cortada no meio da frase; o motivo
  da divisão por √d_k dito como certeza (o paper diz "suspeitamos"); termos trocados ("autoatenção",
  "consulta, chave e valor") num tópico que usa Query/Key/Value; colchetes, decimais e "d_k" que
  seriam mal lidos; lista de pesos fora de ordem; título em inglês de artigo (risco de a voz trocar
  de idioma); acréscimos sem base ("processa de forma muito eficiente"); "eu deixei uma linha de
  fora" (o texto diz que há outras linhas). A narração do slide do agente ganhou o conteúdo dos
  dois blocos de duas colunas, que não são narrados. Registro em `backend/_revisar_narracao_topico22.py`.
- Voz: `gemini-3.8-flash-tts` em 5 lotes e `gemini-3.8-flash-lite-tts` em 2 (a cadeia trocou sozinha
  num 503 e quando a cota do dia do primeiro acabou).
- `_conferir_audio.py 22 5`: 0 com problema; fim de cada transcrição lido um a um, sem sobra de fala.
- Produção: 43 mídias (35 MP3 + 8 imagens) respondendo 200; diagnóstico sem ✗.
