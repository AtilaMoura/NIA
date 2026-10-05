# Auditoria — T67 "Confiabilidade da Palavra" (Sl 19:7-11)

Conteúdo final: `backend/_criar_topico67_obreiro.py` → `_topico67_obreiro_final.json` (17 slides,
8 imagens, 1 fluxo, 5 checkpoints). Dossiê: `topico67-confiabilidade.md`. 2026-10-05.

## 1. Citações bíblicas (conferência automática, letra por letra)

Script de checagem (mesmo método do T66): cada `quote` "(Almeida)" e cada trecho curto entre aspas
foi comparado com o texto da bible-api normalizado + correções da auditoria.
**10/10 blocos `quote` ✓ e 21/21 trechos curtos ✓.**

Erros da FONTE corrigidos (bible-api, "João Ferreira de Almeida", domínio público):
| Ref. | Fonte trazia | Corrigido | Conferência |
|---|---|---|---|
| Sl 19:4 | "consfins" | "confins" | typo óbvio; ACF v.4 "até ao fim do mundo" (mesmo sentido) — não citado no tópico, só no rascunho |
| Hb 6:18 | "impossivel" | "impossível" | acento |
| Lc 1:3 | "haver **investido** tudo" | "haver **investigado** tudo" | Tradução Brasileira (Wikisource) "investigado"; ACF "havendo-me já informado minuciosamente" |
| Lc 1:3-4 | "em ordem. para que" (ponto no meio da frase) | "em ordem, para que" | pontuação |

## 2. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | 2Tm 3:16 retomado do T66; Jo 17:17 | 1 | ✔ |
| s2 | Três movimentos do Sl 19 (1-6 criação, 7-11 Palavra, 12-14 oração) | 1, 6 (Guzik, paráfrase) | ✔ |
| s2 | Citação Matthew Henry "dois livros excelentes…" (tradução livre) | 5 | ✔ (domínio público) |
| s4 | 6 nomes, 6 qualidades, "quase todos com um efeito" (5 efeitos) | 1 — contado no texto | ✔ (evitado "seis efeitos") |
| s4 | C. S. Lewis: Sl 19 o maior poema do Saltério, uma das maiores letras do mundo | 7 (paráfrase atribuída) | ✔ |
| s5 | "Perfeita" = *tamim* (inteiro, completo, íntegro, sem defeito) | 2 (BLB H8549) | ✔ |
| s5 | "Fiel" da raiz *'aman* (sustentar, confirmar, ser firme), raiz de "amém" | 3 (BLB H539) | ✔ |
| s5 | Numeração hebraica: Sl 19:8 = nosso 19:7 | 3 (o BLB lista como 19:8) | ✔ |
| s5 | Citação Spurgeon "testemunho… tão seguro… consolo sólido" (tradução livre) | 4 | ✔ (domínio público) |
| s7 | Nm 23:19; Js 23:14; Is 40:8; Mt 24:35; 1Pe 1:25; Hb 6:18 | 1 | ✔ |
| s8 | Lc 1:3-4; 2Pe 1:16 | 1 | ✔ |
| s8 | Rolo de Isaías: achado 1946-47 por pastores em Qumran; ~125-100 a.C.; ~mil anos mais antigo que os manuscritos conhecidos (Códice de Alepo); 66 capítulos na mesma ordem; "geralmente consistente"; >2.600 variantes, maioria pequenas; Santuário do Livro | 11 (Wikipedia + Museu de Israel) | ✔ — data como faixa (as duas fontes: ~125 e ~100 a.C.) |
| s8 | "Sem exagero": não prova tudo, não é idêntico | cuidado do dossiê | ✔ |
| s10 | Gn 3:1 (dúvida sobre a palavra); Mt 4:6 citado fora do contexto, Mt 4:7 resposta | 1, 12 | ✔ |
| s11 | Westminster I.5 (literal) | 8 | ✔ |
| s11 | Dei Verbum 11 (literal) | 9 | ✔ |
| s11 | Chicago "infalibilidade e inerrância podem ser distinguidas, mas não separadas" | 10 (dossiê T66) | ✔ |
| s11 | Nota de neutralidade: todas afirmam verdade; diferença no alcance; não toma partido; remete ao pastor | 8, 9, 10 | ✔ |
| s13 | Sl 19:10-11, 12, 14 — advertência e recompensa | 1, 6 | ✔ |
| s14 | Resumo = só o que foi dito | — | ✔ |

## 3. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-2.5-flash` — o 3.5 e o 3.7 deram 503) e Groq (`gpt-oss-120b`).
Arquivos `backend/_conteudo_{conteudo,segunda_opiniao}_topico67.json`. Os dois seguiram a
estrutura do dossiê, mas acrescentaram afirmações sem fonte:

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| **Groq** | Declaração de Chicago "distingue 'verdade revelada' (doutrina, moral, salvação) de 'informação factual', permitindo que questões científicas…" | **ERRADO e perigoso** — inverte a posição de Chicago (que defende a inerrância também em história e ciência); justamente o tipo de erro que quebraria a neutralidade |
| Groq | "o conteúdo essencial permanece idêntico"; "não alteram o sentido das passagens" | as fontes dizem "geralmente consistente", não "idêntico"; "não alteram o sentido" não está no dossiê |
| Groq | linha do tempo "1960-1970 – análise comparativa"; "1947 e 1956"; "um pastor beduíno encontra um fragmento" | datas e detalhes sem fonte (as fontes: três pastores, 1946-47) |
| Gemini | "variantes pequenas que não alteram as doutrinas centrais" | afirmação teológica sem fonte no dossiê |
| Gemini | "a inerrância se aplica estritamente aos manuscritos originais (autógrafos)" | não está no dossiê (fica fora do nível) |
| Gemini | Westminster "imediatamente inspiradas"; manuscritos "do século X d.C." | não estão no dossiê (não conferidos) |
| Gemini | analogia "variantes = português arcaico × moderno" | imprecisa (as variantes não são só de época) |
| ambos | pergunta "seis efeitos" como resposta errada/tf | ok — confirma o cuidado do dossiê; no final virou a contagem certa (5 efeitos) |
| Gemini | Pv 30:5-6, Sl 18:30, Dt 18:22 usados | corretos (estão no dossiê), mas ficaram de fora por foco/tamanho |

Aproveitado: a ordem geral (que bate com o roteiro) e a ideia de uma pergunta "fato × exagero"
sobre o Rolo de Isaías (virou o ck3_2). Nenhum texto copiado.

Erro da fonte que o gerador deixou passar: a correção "ordem. para" não pegava porque a bible-api
quebra linha no meio do Lc 1:3 — o gerador agora normaliza os espaços antes de corrigir (os
rascunhos já tinham saído com o ponto final no meio da frase; o final está correto).

## 4. Pedagogia
- Abre retomando o T66 (inspiração → confiança); fecha com ponte pro T68 (suficiência).
- Ilustração própria (cadeira: confiar é sentar), ligada à raiz de "amém".
- Checkpoints: tf, mc, associar, lacuna, mc com cenário, classify (6 itens) + **2 abertas** (ck5_2, ck5_3) ✔.
- Reflexão "💭 Pra pensar" + Resumo ✔. Caso real (Rolo de Isaías) e caso que deu errado (Gn 3; Mt 4) ✔.

## 5. Continuidade
- Não invade T68 (2Pe 1:19-21 — só o v.16 foi usado), nem T69 (tradição), nem a Aula 58 (cânon).
- Reusa do T66 só Chicago e a ideia de 2Pe 3:16 (sem repetir a citação).

## 6. Estrutura
- `validar_topico()` vazio (duração ajustada 22→20 min); 0 `None` no render (trigo-maduro);
  ids de pergunta e item únicos; `fluxo` (nenhum `diagrama`); capa com `imagem_capa`.

## 7. Revisão humana
- `is_approved=true` = só estrutural. O professor teólogo e o pastor leem a versão
  `curso de obreiro/topico67-confiabilidade-completo.html` depois (não é pré-requisito pra publicar).

## 8. Imagens
8 geradas (estilo editorial do obreiro). Rejeitada e regerada: `t67-erva-e-palavra` — a lombada
do livro trazia a palavra "BIBLE" legível (texto em destaque); prompt ajustado pra capa lisa.

**Pendências: 0.**
