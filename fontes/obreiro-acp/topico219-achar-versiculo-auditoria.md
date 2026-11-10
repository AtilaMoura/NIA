# Auditoria — T219 "Como achar qualquer versículo (livro, capítulo, versículo)" (Obreiro ACP)

Conteúdo: `backend/_criar_topico219_obreiro_acp.py` → `_topico219_obreiro_acp_final.json` (11 slides, 6 imagens, 3 checkpoints).
Dossiê: [topico219-achar-versiculo.md](topico219-achar-versiculo.md) · Data: 2026-11-10.

## 1. Citações bíblicas (ACF)
`_conferir_citacoes_219.py`: 13 trechos comparados letra por letra com o texto baixado (`_textos_biblicos_topico219.json`, 20 passagens). **Todas as citações em bloco passaram.**
O script lista 5 "falhas", **todas falsos positivos** (aspas pareadas atravessando enunciados e explicações; conferidos à mão: nenhum é versículo).

## 2. Afirmação → fonte → status
| Afirmação no texto | Fonte (dossiê #) | Status |
|---|---|---|
| Referência = livro + capítulo + versículo (Jo 3:16); João é o 4º livro do NT | 1, 2 | ✅ (ordem do índice da ACF) |
| Capítulo ≈ uma ou duas páginas; versículo = trecho de algumas linhas ou frases curtas | 4 | ✅ Wikipédia (pt), lida |
| Os textos originais não tinham capítulos e versículos numerados | 3, 4 | ✅ Wikipédia (en), lida |
| Capítulos nas cópias desde o início do séc. 13; versículos desde meados do séc. 16 | 3 | ✅ Wikipédia (en), lida |
| Lc 4:16-17: Jesus "achou o lugar em que estava escrito" (rolo de Isaías) | 1 | ✅ |
| Abreviaturas Gn, Sl, Is, Mt, Jo, At, Rm, Ap; Jo = João, Jn = Jonas, Jó = Jó; variam entre Bíblias/editoras | 2 | ✅ tabela do Bibliaon, lida (o próprio site lista variantes) |
| "Mt 5:3-4" = versículos 3 e 4; "Sl 23" = capítulo inteiro | — | ✅ convenção explicada no texto (não é fato externo); o "-" aparece nas fontes lidas ("1 Crônicas 5:27-41") |
| Jo 3:16 ≠ 1Jo 3:16 (textos diferentes) | 1 | ✅ os dois versículos foram lidos na ACF; **dito no texto como exemplo montado** |
| Obadias, Filemom, 2 e 3 João e Judas têm 1 capítulo; "às vezes" se cita só o versículo ("Judas 3") | 1 | ✅ índice da ACF; a parte de "às vezes se cita só o versículo" é hedge, não afirmação forte |
| Uma frase pode atravessar dois versículos: Lc 4:17-18 (o v.17 termina em dois-pontos e continua no v.18) | 1 | ✅ conferido na ACF |
| A divisão judaica difere da cristã: 1Cr 5:27-41 (hebraico) = 1Cr 6:1-15 (Bíblias cristãs); os Salmos têm 116 versículos a mais nas versões judaicas (tratam os títulos dos salmos de outro jeito) | 3, 4 | ✅ duas fontes lidas, independentes entre si |
| Mt 28:19, At 1:8, Pv 3:5-6 (exercício) | 1 | ✅ ACF |

## 3. Erros que a auditoria pegou (e saíram do texto)
1. **Ef 2:8-9 como "frase que atravessa dois versículos"** — o exemplo vem da fonte em inglês (tradução KJV, com dois-pontos). **Na ACF o versículo 8 termina com ponto final**, então a frase não atravessa. Troquei por Lc 4:17-18, conferido na ACF. (O rascunho do Gemini repetia o exemplo de Efésios.)
2. **Gn 1:2 como "versículo com mais de uma frase"** — também da fonte em inglês; na ACF o versículo é uma frase só, com ponto e vírgula. Saiu do texto.
3. "É por isso que, no tempo de Jesus, as pessoas achavam o texto de outro jeito" → generalização que o versículo não sustenta; virou "Veja como foi no tempo de Jesus. Quando ele foi à sinagoga…".
4. "Uma tabela brasileira muito usada" → "muito usada" sem fonte; virou "uma tabela brasileira de abreviaturas".
5. "A primeira carta de Paulo" (Romanos) → ambíguo (cronológico × ordem da Bíblia); virou "na ordem da Bíblia".
6. Badge "4 checkpoints" → o tópico tem 3.
7. Nomes (Langton, Estienne) **não entram no texto do aluno**: a fonte os cita, mas eles não ajudam quem está começando.

## 3b. Rascunhos de IA (comparação)
- **Gemini** (`_conteudo_conteudo_topico219.json`): 6 slides, **0 blocos de citação literal**, repete o exemplo de Ef 2:8-9 (inválido na ACF) e cita Langton. Nada aproveitado.
- **Groq** (`segunda_opiniao`, terminou depois da publicação; comparado em seguida): 6 slides, só 1 bloco de citação literal, cita Langton. **Nada aproveitado**; o texto publicado não mudou.

## 3c. Áudio
- Conferência (`_conferir_audio.py`): 21 mp3, idioma português, semelhança de 0,91 a 1,00. **Um áudio** (`s5-b2`) passou no limite mas repetia a última frase ("…só continua no versículo 18. E só continua no versículo 18"): narração reescrita e gerada de novo. Varredura automática de frase final repetida nos áudios dos T217, T218 e T219: nenhuma outra.
- Narrações corrigidas antes da voz: a [3] dizia que Jesus achou o lugar "com essa mesma lógica de localização" (falso: o rolo não tinha números); a [6] abria com "Preste muita atenção" (abertura proibida); siglas (Jo 3:16, Sl 23:1, Mt 5:3-4…) faladas por extenso.

## 4. Continuidade e fronteira
- Costura com T217 ("endereço", "biblioteca") e com o mapa do T218 (usa os grupos só para localizar); fecha com `proximo_topico_label` = "Ler o texto no seu contexto" (aula 1.2).
- Não ensina a ler no contexto nem a interpretar (aula 1.2); não usa vírgula/ponto e vírgula entre referências (**não verificado em fonte lida**).

## 5. Regras do curso ACP
- Sem nota de neutralidade nem slide de tradições ✅ (a diferença hebraica × cristã de numeração está em **um** quadro, como fato de numeração, sem tomar partido).
- Termos explicados na mesma frase: capítulo, versículo, referência, abreviatura ✅.
- Sem "Orientação da ACP" ✅. **Pendência para pastor/Adriano (não trava):** confirmar a tabela de abreviaturas a usar no curso (a adotada é a do Bibliaon; algumas Bíblias usam outras).

## 6. Estrutura (portão determinístico)
`validar_topico()` → `[]` · render `trigo-maduro`: 178 KB, 0 `None` · ids únicos · `fluxo` (não `diagrama`) · capa com `imagem_capa` · Reflexão + Resumo (6 bullets autônomos para o "Relembrando" do próximo tópico) ·
perguntas: associar 1, mc 1, tf 2, classify 1, lacuna 1, **open 2** ✅.

## Resultado
**0 pendências de fato.** Segue para publicação e áudio.

## Revisão de 2026-11-10 (auditoria pedida pelo Atila, tarefa NIA-T-021)
1. **"Capítulo tem cerca de uma ou duas páginas"** saiu porque não tinha fonte e não vale para todos (o Sl 117 tem 2 versículos e o Sl 119 tem 176). A narração do quadro (s1b3) foi refeita.
2. **Fica para o pastor/Adriano (não trava):** se entra 1 frase sobre a numeração diferente dos Salmos em Bíblias católicas. Só entra com fonte lida.

`validar_topico()` → `[]`; render 0 `None`; áudio conferido (0 problemas).
