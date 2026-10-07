# Auditoria — Prova do T66 "Inspiração: a Escritura soprada por Deus"

Curso Obreiro I (8) · `Topico.id=66` · 2026-10-07 · `/criar-provas-topicos` (2ª prova do padrão novo).
Banco: `backend/_prova_topico66.json` (gerado por `backend/_montar_prova_topico66.py`).
Regra do curso (PROVA.md §3): banco 18, rodada 6, nota 60%, `tipos_minimos {"open": 1}`.
Fontes: conteúdo publicado do tópico 66 (slides s1–s13) + `fontes/obreiro/topico66-inspiracao.md`.

## Perguntas

| id | assunto | tipo | o que cobra | sustentação | status |
|---|---|---|---|---|---|
| p66_01 | A | mc | 2Tm 3:15: sábio "para a salvação" | s2 quote 2Tm 3:14-17 | ok |
| p66_02 | A | tf (F) | theopneustos só aparece uma vez no NT | s4 box "A palavra no original" | ok |
| p66_03 | A | mc | theos + pneō | s4 box | ok — distratores sem palavra grega nova |
| p66_04 | A | tf (V) | inspiração está no que foi escrito (Guzik) | s4 box analogia (paráfrase atribuída) | ok |
| p66_05 | A | associar | Gn 2:7, Sl 33:6, 2Tm 3:16 → imagem do sopro | s4 quotes + s2 | ok |
| p66_06 | A | open | por que "TODA Escritura" importa pra quem ensina | s2 box "Repare em duas coisas" + s8 | ok |
| p66_07 | B | mc | 2Pe 1:21: movidos pelo Espírito | s5 quote | ok |
| p66_08 | B | tf (V) | Hb 1:1-2 | s5 quote | ok |
| p66_09 | B | lacuna | Mt 5:18 "um só til" | s6 quote | ok — resposta única "til" |
| p66_10 | B | tf (F) | escrita por pessoas reais | s5 parágrafo + fluxo | ok |
| p66_11 | B | mc | 1Ts 2:13: a palavra "opera" em quem crê | s6 quote + box "Pro obreiro" | ok |
| p66_12 | B | open | pessoas escreveram × Palavra de Deus | s5 inteiro | ok |
| p66_13 | C | tf (F) | os quatro usos juntos (ilustração da obra) | s8 box analogia | ok |
| p66_14 | C | mc | alvo de 2Tm 3:17 | s2 quote + s8 parágrafo + box "Ligando com o Módulo 1" | ok |
| p66_15 | C | mc | o curso não toma partido (nota de neutralidade) | s9 box neutralidade, item 3 | ok |
| p66_16 | C | mc | Declaração de Chicago (1978), 200+ líderes | s9 box neutralidade, item 2 | ok |
| p66_17 | C | tf (F) | inspiração não garante leitura certa | s10 quote 2Pe 3:15-16 + box | ok |
| p66_18 | C | open | um uso da Escritura aplicado sem "torcer" | s8 cards + s10 | ok |

## Checagens gerais

| Checagem | Resultado |
|---|---|
| **Citações bíblicas idênticas às do tópico** (regra do Obreiro) | ok — 12 trechos conferidos por script contra os blocos `quote` publicados (2Tm 3:15, 3:16, 3:17; Gn 2:7; Sl 33:6; 2Pe 1:21; Hb 1:1-2; Mt 5:18; 1Ts 2:13; 2Sm 23:2; Jr 1:9; 2Pe 3:16). O texto do tópico já tinha sido conferido na ACF na auditoria do T66 |
| Neutralidade doutrinária | ok — p66_15 e p66_16 cobram o que o tópico APRESENTA, sem tomar partido; nenhuma pergunta pede pra escolher entre Chicago e infalibilidade em fé e prática, nem entre Calvino e Dei Verbum |
| Gabarito conferido / mc com uma só certa | ok (18/18) |
| Nada além do tópico | ok — sem cânon (T70), sem confiabilidade/suficiência (T67/T68) |
| Cópia de checkpoint | nenhuma (comparado com ck1_1…ck4_3). Evitados de propósito: classificar situações pelos 4 usos (= ck4_1), "inspiração de artista" (= ck4_2), associar textos a ideias com "anulada/recebida" (= ck2_1) |
| Ids únicos | ok — `p66_NN` e `p66_NN_x` |
| Abertas com resposta-modelo | 3 (uma por assunto) |
| `_publicar_prova.py --checar` | ✅ |

## Erros pegos durante a escrita

- Rascunho de classificar situações pelos 4 usos repetia o ck4_1 → virou tf da ilustração da obra (p66_13).
- Rascunho do p66_11 era associar textos a ideias, igual ao ck2_1 → virou mc sobre "opera em vós que credes".
- Rascunho do p66_03 tinha distratores com palavras gregas que o tópico não ensina (logos, graphē) → trocados por descrições em português.

**Pendências: 0.** Liberado pra publicar.
