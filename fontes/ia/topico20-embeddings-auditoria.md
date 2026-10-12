# Auditoria — Tópico 20 "Embeddings" (revisão completa)

Curso de IA (Course 5) · `Topico.id=20` · 2026-10-12 · régua: `fontes/ia/topico20-embeddings.md`.
Conteúdo auditado: `backend/_criar_topico20_ia.py` → `_topico20_ia_final.json` (16 slides).
**Resultado: 0 pendências.**

## 1. Por que foi refeito

O conteúdo anterior (cópia em `backend/_topico20_backup_prod.json`) não tinha dossiê nem auditoria,
nem imagens internas, nem áudio, nem Reflexão, nem pergunta aberta, e usava um bloco `diagrama`.
Além disso trazia afirmações sem fonte, que **não** foram reaproveitadas:

| Afirmação antiga | Problema |
|---|---|
| "128 dimensões costumam ser suficientes para consultas de estoque"; "subir para 256" | número inventado; e confunde embedding com consulta de estoque |
| "1024 dimensões… pode fazer o modelo memorizar ruído" / "risco de overfitting" | sem fonte |
| "SLA de latência < 200 ms e recall > 90%"; "diferença de recall < 2%" | métricas inventadas |
| "Se o ID não existir, usa-se o vetor de token `<unk>`" | sem fonte; não é como o lookup de um LLM é descrito nas fontes |
| "Consulta é O(1)" | sem fonte, irrelevante pro nível |
| "ao receber 'Quero uma orquídea', o tokenizador gera IDs como [1023, 587, 2145]" | IDs inventados, diferentes dos da apostila |
| "a tool search_products usa esses vetores [do LLM] para buscar" | mistura a tabela interna do LLM com modelo de embedding de busca |
| "embedding contextualizado incorpora a intenção de compra" | exagero sem fonte |
| "vetor-store (ex.: FAISS)" | ferramenta fora do dossiê |

## 2. Afirmações do tópico → fonte

| Slide | Afirmação | Fonte (#) | Status |
|---|---|---|---|
| s1 | "Tenho dois gatos e pouca luz" → [4821, 1359, 8274, 74, 5291, 3190]; ID = número de prontuário | 1; T19 em produção (mesma lista, sem o ponto final) | ok |
| s1 | Citação Mikolov: palavras como "unidades atômicas", "índices num vocabulário", sem noção de similaridade | 4 (Introdução, lido no PDF) | ok — tradução livre marcada |
| s1 | Embedding = "vetor (lista) de números de ponto flutuante" | 8 | ok |
| s1 | Números reais, que podem ser negativos | 3 (cap. 5) | ok |
| s1 | gatos → [0.21, -0.72, 1.13, 0.08, …] | 1 | ok — dito no texto que são inventados pra ilustrar |
| s2 | Matriz com uma linha por token; formato V × d | 1, 3 (cap. 6 e 7) | ok |
| s2 | O ID só seleciona a linha (indexação) | 3 (cap. 6: "we use indexing to select the corresponding rows") | ok |
| s2 | GPT-2 padrão: 50.257 tokens, 768 números | 7 | ok — reconferido em busca independente |
| s2 | 50.257 × 768 = 38.597.376 | conta nossa, conferida | ok — texto diz "fazendo a conta" |
| s2 | Valores aprendidos no treino; "embeddings aprendidos" | 2 (§3.4) | ok |
| s4 | Transformer 2017: 512 (base) e 1024 (grande) | 2 (§3.1; Tabela 3, linha "big 6 1024 4096 16" lida no PDF) | ok |
| s4 | BERT: 768 base, 1024 grande, vocabulário de 30.000 tokens | 6 | ok |
| s4 | Embeddings de palavra antigos: de 50 a 1000 | 3 (cap. 5) | ok |
| s4 | Dimensões "não têm uma interpretação clara" | 3 (cap. 5) | ok |
| s5 | Cosseno: "de longe a medida mais comum"; 1 / 0 / −1 | 3 (cap. 5, §5.4) | ok |
| s5 | "a conta por trás dela volta no tópico de Self-Attention" | 3 (cosseno baseado no produto escalar); apostila Parte 10 | ok |
| s5 | rei − homem + mulher → mais perto de rainha | 4 | ok |
| s5 | Alammar: vetores de 50 números treinados na Wikipédia; "rainha" entre 400.000 | 9 | ok |
| s5 | Ressalvas: excluir as palavras de entrada; funciona com palavras frequentes e certas relações | 3 (cap. 5) | ok |
| s7 | word2vec = um embedding fixo por palavra (estático) | 3 (cap. 5) | ok |
| s7 | Contextual = vetor diferente em cada contexto | 3 (cap. 5) | ok |
| s7 | Citação ELMo (2018), polissemia | 5 (resumo, lido no PDF) | ok — tradução livre; o parêntese "(e.g., syntax and semantics)" foi omitido sem mudar o sentido |
| s7 | "muda de jiboia" × "o horário muda" | exemplo de língua, não é fato técnico | ok — não afirma nada sobre IDs |
| s8 | Linha da tabela é a mesma nas duas frases; as camadas constroem a representação contextualizada | 1 (Parte 4), 3 (cap. 7) | ok |
| s8 | Citação J&M cap. 7 | 3 (lido no PDF) | ok |
| s8 | Posição acrescentada antes das camadas | 3 (cap. 7); T21 | ok — só menciona |
| s8 | Gatos → gatos + planta → gatos + pouca luz + planta | 1 (Parte 5) | ok |
| s8 | "embedding = significado" é incompleto | 1 (Parte 4) | ok |
| s8 | Attention "daqui a dois tópicos" | grade: T21 posição, T22 Self-Attention | ok |
| s10 | 2016, Universidade de Boston e Microsoft Research | 10 (afiliações na 1ª página) | ok |
| s10 | word2vec do Google News: 3 milhões de palavras e termos, 300 dimensões | 10 | ok — reconferido em busca independente |
| s10 | programador/dona de casa; pai/médico, mãe/enfermeira | 10, 3 | ok |
| s10 | Citação "aplicação cega…" | 10 (1ª frase do resumo) | ok |
| s10 | Busca de candidatos pode rebaixar documentos com nome de mulher; embeddings amplificam o viés | 3 (§5.8) | ok |
| s11 | "Distâncias pequenas sugerem alta relação…" | 8 | ok |
| s11 | 1536 e 3072 por padrão | 8 | ok — reconferido em busca independente; texto data a consulta |
| s11 | Usos: busca, agrupamento, recomendações, classificação; cosseno recomendado | 8 | ok |
| s11 | Catálogo/ocorrências viram vetores; busca traz textos com outras palavras | 8 (busca por relação) + T19 | ok — escrito como "tende a"; exemplos são ilustrações |
| s11 | "tóxica para gatos" pode aparecer perto de "é segura para gatos?" | raciocínio a partir de 8 (a medida é de relação, não de acerto) | ok — escrito como "pode aparecer"; a conclusão (fato vem de tool) é a linha do curso |
| s13 | Resumo | repete só o que está acima | ok |

## 3. Fatos de alto risco — busca independente (2026-10-12)

- GPT-2: 50.257 × 768 = 38.597.376 → confirmado por tutoriais independentes da doc da HF.
- text-embedding-3-small 1536 / 3-large 3072 → confirmado (doc oficial + terceiros).
- word2vec Google News: ~3 milhões de palavras e frases, 300 dimensões → confirmado (página do projeto).

## 4. Rascunhos (Gemini 3.7 Flash e Groq) — o que NÃO entrou

Nenhum texto dos rascunhos entrou. Erros encontrados:

- **Gemini:** ID "38421 para orquídea" e lista [1843, 38421, 9122] inventados; "similaridade 0.84";
  preços e SKUs inventados; analogia inventada "Adubo Orquídea − Orquídea + Cacto ≈ Adubo Cacto";
  conta do viés escrita ao contrário ("homem − programador + mulher"); "espaço não-linear";
  "bilhões de textos da internet"; viés de gênero atribuído à busca do Garden Center sem fonte;
  distância euclidiana e banco vetorial fora do dossiê; "cada número representa uma característica"
  (contradiz a fonte 3 e o próprio slide seguinte).
- **Groq:** "Distância euclidiana = similaridade"; analogia do código de barras que põe preço e estoque
  dentro do vetor (o oposto do que o tópico ensina); fallback `<UNK>`; "versão feminina da Aloe vera";
  regra inventada de "filtrar stop-words" (a fonte diz o contrário: funciona com palavras frequentes);
  exemplo "engenheiro/enfermeira" que não está no artigo citado; vetores "reescritos milhares de vezes";
  afirmou que Espada-de-São-Jorge é segura para gatos (sem fonte); usou bloco `diagrama`.
- **Aproveitado (só a ideia, reescrita):** o exemplo de "muda" (muda de jiboia × o horário muda), do Gemini.

## 5. Pedagogia

- Ordem: problema (T19) → vetor → tabela → tamanho → proximidade → limite (polissemia) → como o
  Transformer resolve → risco (viés) → uso no agente. Exemplo antes da abstração em todo slide.
- Toda pergunta é respondível com o que foi ensinado (ck1: s2; ck2: s2, s4, s5; ck3: s7–s8;
  ck4: s11 e as três fontes citadas em s5, s7, s10; ck5: s8, s1–s2, s11).
- Tipos: 5 `mc`, 3 `tf`, 1 `classify`, 1 `associar`, 2 `open`. Ids únicos no tópico.

## 6. Continuidade

- Abre retomando o T19 (mesma frase, mesmos IDs, "número de prontuário") e cumpre o que ele prometeu
  (embedding matrix, dimensão, "banco").
- Não invade o T21 (posição só é citada num passo do fluxo) nem o T22 (não explica Q/K/V nem a conta).
- O T21 em produção resume o T20 como "token ID → vetor pela embedding matrix; dimensão; estático ×
  contextualizado" — continua verdadeiro.
- Fecha com `proximo_topico_label` = "Positional Encoding". O Resumo "📌" tem bullets que se
  sustentam sozinhos (viram o "↩ Relembrando" do T21).

## 7. Direito autoral

Citações curtas de papers e do livro, atribuídas e marcadas como tradução livre; nenhum bloco longo.

## 8. Estrutura

`validar_topico()` = `[]`; ids duplicados = nenhum; render local (tema azul-petroleo) com 0 `None`;
capa com `imagem_capa`; 2 `fluxo`, nenhum `diagrama`; Reflexão "💭" + Resumo "📌".

## 9. Imagens (8: capa + 7; 9 slides de conteúdo → densidade 0,78)

Estilo isométrico claro (o mesmo texto de estilo do T21; o catálogo no Artifact não abre nesta conta).
Todas olhadas uma a uma: sem letras nem números.

| Arquivo | Resultado |
|---|---|
| t20-capa-vetores | ok |
| t20-prontuario-mapa | ok |
| t20-tabela | ok |
| t20-dimensoes | ok |
| t20-vizinhos | ok |
| t20-banco | ok |
| t20-vies | **refeita** — a 1ª saiu escura, com painéis de gráfico e folhas riscadas; cena simplificada |
| t20-busca | ok — `alt` ajustado (a imagem destaca 4 pontos, não 3) |
