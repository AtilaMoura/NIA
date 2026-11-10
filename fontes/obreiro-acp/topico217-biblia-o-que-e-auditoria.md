# Auditoria — T217 "O que é a Bíblia e quem a escreveu" (Obreiro ACP)

Conteúdo: `backend/_criar_topico217_obreiro_acp.py` → `_topico217_obreiro_acp_final.json` (15 slides, 9 imagens, 4 checkpoints).
Dossiê: [topico217-biblia-o-que-e.md](topico217-biblia-o-que-e.md) · Data: 2026-11-10.

## 1. Citações bíblicas (ACF)
`backend/_conferir_citacoes_217.py` compara cada trecho entre aspas contra o texto da ACF baixado
(`_textos_biblicos_topico217.json`): **30 trechos conferidos**. Todas as citações bíblicas passaram (blocos `quote`, cards e
trechos nos parágrafos). O script devolve 8 "falhas", **todas falsos positivos** do detector (aspas pareadas atravessando texto que
não é versículo: definição de "Bíblia", enunciados de pergunta, texto de Guzik, resposta-modelo). Conferidos à mão: nenhum é versículo.
Erro **real** que o conferidor achou e eu corrigi: "inspiradas pelo Espírito Santo" no resumo (a ACF diz "inspirados", 2Pe 1:21).

## 2. Afirmação → fonte → status
| Afirmação no texto | Fonte (dossiê #) | Status |
|---|---|---|
| Bíblia foi o livro mais citado, 485 vezes (Pró-Livro 2024) | 7 | ✅ lida na página |
| "Bíblia" ← grego *tà biblía*, "os livros"; plural de *biblíon*, de *býblos* (papiro) | 6 | ✅ Wikipédia (pt), referência geral. Ligação com a cidade de Biblos **ficou de fora** |
| Coleção de livros; hebraico, aramaico (alguns trechos) e grego; português é tradução | 6 | ✅ |
| 2Tm 3:14-17 (texto central); "sagradas Escrituras" de Timóteo = AT na época | 1 | ✅ texto; leitura direta |
| *theópneustos* = *theós* + soprar; "inspirada por Deus"; "soprada por Deus" ao pé da letra | 2 (Thayer/Strong) | ✅ lido |
| Guzik: inspiração alcança as próprias palavras; "toda" a Escritura | 3 | ✅ paráfrase atribuída; página lida |
| Imagem do sopro: Gn 2:7, Sl 33:6 | 1 | ✅ (paralelo de linguagem; o texto não faz argumento exegético a mais) |
| CGADB explicou ao Senado que a Bíblia "é" a Palavra de Deus e não só "contém" | 5 | ✅ PDF lido (p. 3). **É posição das Assembleias de Deus, e o texto diz isso; não atribui nada à ACP** |
| 2Pe 1:21; 2Sm 23:2; Jr 1:9 — Deus falou por pessoas | 1 | ✅ |
| Moisés escreveu (Dt 31:24); Jeremias ditou a Baruque (Jr 36:4); Lucas se informou (Lc 1:3); cartas de Paulo lidas nas igrejas (Cl 4:16) | 1 | ✅ |
| "Mais de mil anos" entre Moisés e os apóstolos; "dezenas de escritores" | — | ✅ sustentado só pelo texto bíblico e cronologia comum (Moisés séc. XV–XIII a.C.; apóstolos séc. I d.C.). **Sem "40 autores" nem "1.500 anos"** (fonte institucional não lida) |
| 4 usos (2Tm 3:16) e "toda a boa obra" (v.17) | 1, 3 | ✅ |
| Jo 20:31 (propósito do Evangelho) | 1 | ✅ |
| Diabo citou o Sl 91 (Mt 4:5-7); Jesus respondeu com "Também está escrito" | 1 | ✅ (Sl 91:11-12 conferido) |
| Homem etíope lendo Isaías; Filipe perguntou (At 8:27-35) | 1 | ✅ At 8:27-28 e 8:30-35 conferidos |
| Pedro avisa dos "pontos difíceis de entender… que os indoutos e inconstantes torcem" (2Pe 3:16); "indoutos" = sem instrução | 1 | ✅ |

## 3. Erros que a auditoria pegou (e saíram do texto)
1. "jovem Timóteo, seu ajudante" → o dossiê não sustenta "jovem" nem "ajudante": virou "Timóteo, que tinha aprendido com ele" (2Tm 3:14).
2. "Mais tarde, Pedro colocou…" → cronologia entre as cartas não está no dossiê: tirei "mais tarde".
3. "Filipe, um dos primeiros servos da igreja" → At 6 não foi lido neste dossiê: virou "um discípulo de Jesus".
4. "No deserto, o diabo…" (tentação do templo é em Jerusalém, não no deserto) → "Quando o diabo tentou Jesus".
5. Citações em cards com palavra faltando (Dt 31:24 sem a vírgula e a minúscula; Jr 36:4 sem "Baruque") → refeitas letra por letra.
6. "ministro da rainha" (Etiópia) → o texto diz "superintendente de todos os seus tesouros": virou "responsável pelos tesouros da rainha dos etíopes".
7. "inspiradas" → "inspirados" (ACF, 2Pe 1:21).
8. Número "485 vezes" confirmado na página (e não de memória, como no T66).
9. **Correção posterior (2026-11-10, publicada):** o card "Lucas pesquisou" e itens ligados atribuíam o 3º Evangelho a Lucas, mas o nome **não consta no texto lido** (é tradição). Agora: "o autor do Evangelho de Lucas" (card, associar, explicação, resposta-modelo) e a introdução do slide 7 diz "quatro exemplos de como escreveram" (antes "quatro deles", que chamava Lucas de escritor). Só o áudio desse bloco foi regenerado (s7 b0); os outros 28 ficaram como estavam.

## 3b. Rascunhos de IA (comparação)
- **Gemini** (`_conteudo_conteudo_topico217.json`): 8 slides, **0 blocos de citação literal** (nenhum versículo copiado da ACF), 1 menção a
  "66 livros" (invade o T218). Mesmos assuntos centrais do roteiro, sem o caso real (At 8), o caso que deu errado (Mt 4) nem as quatro pessoas
  escrevendo. **Nada foi aproveitado**; a versão final vem do dossiê.
- **Groq** (`segunda_opiniao`, qwen3.8-27b): 7 slides, **0 blocos de citação literal**, repete o número **"1.500"** (anos) duas vezes, que o dossiê
  deixou de fora por falta de fonte lida, e traz 1 menção a "tradições" (o curso não faz comparação). **Nada foi aproveitado.**
- Resultado da comparação: os dois rascunhos cobrem os mesmos assuntos centrais, mas nenhum copiou versículo da ACF; a versão final vem só do dossiê.

## 4. Continuidade e fronteira
- Não invade o T218 (não diz quantos livros nem lista), nem T219 (achar versículo), nem a aula 1.2 (só aponta para ela), nem T227 (línguas).
- Primeiro tópico do curso: não cita Obreiro I/II. Fecha com `proximo_topico_label` = título do T218.

## 5. Regras do curso ACP
- Sem nota de neutralidade e sem slide "O que as tradições dizem" ✅.
- Termos explicados na mesma frase: Escritura, inspirada, profeta, profecia, apóstolo, papiro, Antigo/Novo Testamento, indoutos, epístola evitada ("carta") ✅.
- Sem "Orientação da ACP" (não há regra da igreja neste tópico) ✅.
- **Posição da ACP sobre a Bíblia:** Declaração de Fé da ACP ainda pendente (decisão 1 da grade) → o texto só afirma o que a própria Bíblia diz e
  atribui a frase de fé às Assembleias de Deus. **Pastor e Adriano revisam depois de publicado.**

## 6. Estrutura (portão determinístico)
`validar_topico()` → `[]` · render com tema `trigo-maduro`: 187 KB, 0 ocorrências de `None` · ids de pergunta e de item únicos ·
`fluxo` (não `diagrama`) · capa com `imagem_capa` · Reflexão + Resumo (6 bullets autônomos para o "Relembrando" do T218) ·
perguntas: `mc`, `tf`, `associar`, `lacuna`, `classify`, **2 `open`** ✅.

## Resultado
**0 pendências de fato.** Pode seguir para imagens e publicação. Itens para o pastor/Adriano (revisão posterior, não travam):
(a) confirmar a posição da ACP sobre a Bíblia quando a Declaração de Fé chegar; (b) se querem o número "cerca de 40 autores" no texto (hoje fora, sem fonte lida).
