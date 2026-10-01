# Auditoria IA — T66 "Inspiração: a Escritura soprada por Deus" (2Tm 3:16-17)

Obreiro I · Módulo 2 · Aula 60 · `Topico.id=66` · auditado em 2026-10-01 por Claude.
Dossiê: [topico66-inspiracao.md](topico66-inspiracao.md). Conteúdo: `backend/_criar_topico66_obreiro.py`
→ `_topico66_obreiro_final.json`. Revisão humana (professor teólogo e pastor) prevista, mas
não é pré-requisito pra publicar (decisão do Atila, 2026-10-01).

## 1. Texto bíblico (conferência automática letra por letra)

12 citações em bloco, todas comparadas com o texto da fonte (Almeida, bible-api) já corrigido:
**12 ok, 0 erro.**

| Correção feita NA FONTE antes de citar | Como foi conferido |
|---|---|
| 2Tm 3:15 — a fonte veio "pela **que** há em Cristo Jesus" (sem "fé") | ACF (bibliaonline.com.br/acf/2tm/3): "pela fé que há em Cristo Jesus" |
| 2Pe 3:16 — a fonte trazia "**mas** quais há pontos" | erro de digitação evidente → "nas quais" |
| Jr 1:9 — "disse- me" | espaço da fonte removido |

Rótulo usado: "(Almeida)" — o texto da bible-api não bate com a ARC (ex.: "desde a infância"
× "desde a tua meninice"). **Pendência registrada:** T1–T5 rotulam como "(ARC)"; conferir.

## 2. Fato (afirmação → fonte)

| # | Afirmação | Fonte | Status |
|---|---|---|---|
| 1 | Bíblia = livro mais citado, 485 menções (Retratos da Leitura 2024) | 9 | ok (página oficial do Instituto Pró-Livro) |
| 2 | "Sagradas letras" de Timóteo = Escrituras do AT, na época | 1 (2Tm 3:15) | ok — leitura direta |
| 3 | Pedro põe as cartas de Paulo junto das "outras Escrituras" | 1 (2Pe 3:16) | ok |
| 4 | theopneustos = theos + pneō, "soprada por Deus"; única ocorrência no NT | 2 | ok |
| 5 | Imagem do sopro em Gn 2:7 e Sl 33:6 | 1 | ok — apresentada como paralelo de linguagem |
| 6 | Guzik: a inspiração está no que foi escrito (Deus soprou "para fora") | 5 | ok — paráfrase atribuída |
| 7 | Os 4 usos e o v.17 | 1 | ok — sem nomes gregos (o rascunho do gpt-oss errou esses nomes) |
| 8 | Citação de Matthew Henry | 4 | ok — domínio público, tradução livre identificada |
| 9 | Westminster cap. I, II: "todos dados por inspiração de Deus para serem a regra de fé e prática" | 6 | ok |
| 10 | Dei Verbum nº 11: "têm Deus por autor"; "verdadeiros autores" | 7 | ok — **nº 11** (o rascunho do gpt-oss dizia nº 10) |
| 11 | Calvino: Lei e Profetas "ditada pelo Espírito Santo" | 3 | ok — domínio público |
| 12 | Declaração de Chicago (1978), +200 líderes evangélicos, inerrância total | 8 | ok |
| 13 | "outras correntes preferem infalibilidade em matéria de fé e prática" | 8 (a própria Declaração rejeita limitar a temas de fé — o que mostra que a posição existe) | ok, formulação cautelosa |

## 3. Comparação dos rascunhos (processo híbrido)

| Fonte do rascunho | Resultado |
|---|---|
| API Gemini (cadeia "conteudo") | 503/504 em TODOS os modelos, 2 tentativas — nada gerado |
| Groq qwen3.8-27b | recusou: pedido maior que o limite de tokens/min |
| Groq gpt-oss-120b (reserva) | **5 erros**: Westminster "instrumento passivo" (inventado), Dei Verbum nº 10, 2Pe 1:20 no lugar de 1:21, nomes gregos errados dos 4 usos, bloco de outro curso (vocab). Aproveitadas só 2 ilustrações (construtor; "não é inspiração de artista") |
| **Gemini web (navegador)** | **0 erro de fato**; 1 typo ("com las outras"), 1 detalhe fora do dossiê ("manuscritos originais"). **Aproveitado:** citação de 1Co 2:13, ligação "livro mais citado → responsabilidade de manusear bem", 1 pergunta de reflexão |

## 4. Pedagogia, neutralidade, continuidade, estrutura
- [x] Ponte com o Módulo 1 (s1, s8) e com o próximo (resultado → "Confiabilidade da Palavra")
- [x] Não invade T67–T69 (confiabilidade, suficiência, tradição) nem a Aula 58 (cânon)
- [x] **Nota de neutralidade explícita** (s9): terreno comum + 2 divergências, sem tomar partido, remete ao pastor
- [x] Caso que deu errado (2Pe 3:16) e caso real/dado (Retratos da Leitura)
- [x] Reflexão (4 perguntas) + Resumo (6 itens)
- [x] Perguntas: mc ×2, tf ×2, associar, lacuna, classify, open ×2 — todas respondíveis com o conteúdo
- [x] `validar_topico()` sem problemas; 0 `None` no render
- [ ] Imagens (7) — em geração
- [ ] Áudio — depois de publicado

**Resultado:** conteúdo APROVADO — 12 citações e 13 afirmações conferidas, 0 pendências de fato.
