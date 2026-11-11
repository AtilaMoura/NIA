# Auditoria — T221 "Observar, entender, aplicar" (Obreiro ACP)

Conteúdo: `backend/_criar_topico221_obreiro_acp.py` → `_topico221_obreiro_acp_final.json` (13 slides, 7 imagens, 3 checkpoints).
Dossiê: [topico221-observar-entender-aplicar.md](topico221-observar-entender-aplicar.md) · Data: 2026-11-11.

## 1. Citações bíblicas (ACF)
`_conferir_citacoes_221.py`: 20 trechos comparados letra por letra com `_textos_biblicos_topico221.json` (14 passagens baixadas da ACF). **Todas as citações em bloco passaram.**
As 6 "falhas" listadas são **falsos positivos** (aspas em frases de Matthew Henry traduzidas, enunciados e lacuna); conferidas à mão.

## 2. Afirmação → fonte → status
| Afirmação no texto | Fonte (dossiê #) | Status |
|---|---|---|
| Tiago escreveu uma das cartas do NT | 1 (Tg 1:1) | ✅ |
| Tg 1:22-25 (espelho; cumpridor; bem-aventurado) | 1 | ✅ |
| "Cumpridores" = poiētḗs, quem faz; "atenta bem" = parakýptō, abaixar-se para olhar de perto | 4, 2 | ✅ |
| "Bem-aventurado" = feliz, abençoado | — | ✅ termo explicado (uso comum; já usado no curso) |
| Matthew Henry (começo do séc. 18): "ouvir é para fazer"; "não é falar, mas andar" | 7 | ✅ citação curta de clássico, traduzida e atribuída |
| Esdras: sacerdote (7:11) e "escriba hábil na lei de Moisés" (7:6); buscar, cumprir, ensinar (7:10) | 1 | ✅ |
| Henry sobre Esdras: "primeiro aprendeu e depois ensinou"; "primeiro fez e depois ensinou" | 7 | ✅ |
| Três passos (observar, entender, aplicar) = forma **comum**; há quem divida em mais etapas | 5, 6 | ✅ (Navigators: "Commonly… three parts"; um autor deles usa sete passos) |
| Observar = olhar com atenção; perguntas quem, o quê, onde, quando, o que se repete | 9, 5 | ✅ |
| Sl 119:18 como oração antes de ler | 1 | ✅ |
| Entender usa as 4 perguntas do T220 e compara com outras partes (At 17:11) | T220; 1 | ✅ |
| Mt 7:24-27 encerra o ensino que Jesus deu num monte (Mt 5:1 "subiu a um monte"; 7:28 "concluindo Jesus este discurso") | 1 | ✅ — o nome "Sermão do Monte" **não** é usado (não li fonte para o nome) |
| Lc 6:46; Jo 13:17 | 1 | ✅ |
| Mc 1:32-38: à tarde a cidade à porta; curas; de madrugada, lugar deserto, orava; "Todos te buscam"; "Vamos às aldeias vizinhas… porque para isso vim" | 1 | ✅ |
| Guzik: menos sono e mais oração depois de um dia longo; a pressão deve levar à oração | 8 | ✅ paráfrase atribuída |
| Aplicação sai do sentido do texto | 5 ("application of the principles") | ✅ 1 frase, aponta para o T222 |

## 3. Erros que a auditoria pegou (e saíram do texto)
1. "Esdras foi sacerdote e escriba… que ensinou o povo" (sem fonte) → Ed 7:6 e 7:11 baixados; texto agora cita "escriba hábil na lei de Moisés (Ed 7:6)".
2. "Sermão do Monte (Mateus 5 a 7)" → o nome não foi lido em fonte; virou "o longo ensino que deu num monte (Mateus 5 a 7)", com Mt 5:1 e 7:28 lidos.
3. "Jesus orou **a sós**… e da oração **saiu decidido**" (inferência de causa) → "foi orar num lugar deserto; quando o acharam, disse que ia às aldeias vizinhas, 'porque para isso vim'" (o que o texto diz).
4. Citação de Mc 1:32-34 cortada no meio do versículo 34 → versículo completo.
5. Nomes de quem popularizou o método → fora (Wikipédia e Precept deram 404).

## 4. Rascunhos de IA (comparação)
- **Gemini** (`_conteudo_conteudo_topico221.json`): 6 slides de conteúdo, **0 blocos de citação literal**; traz um quadro mandando "apresentar as diferentes leituras" de "tradições cristãs" (contra a regra do curso confessional). **Nada aproveitado.**
- **Groq** (`segunda_opiniao`, terminou logo depois da publicação): 6 slides de conteúdo, 2 citações (Tg 1:22 e 1:25), **literais e certas**, que o texto final já tem; usa Mc 1 como o final. **Nada novo aproveitado**; o texto publicado não mudou.
- A versão final vem só do dossiê.

## 5. Continuidade e fronteira
- Costura: o T220 prometeu "observar, entender e aplicar"; o T221 abre com "no tópico anterior você aprendeu a ler no contexto" e põe as 4 perguntas do T220 **dentro** do passo "entender" (box curto, sem reensinar).
- **Não** usa Fp 4:13 nem faz lista de erros (T222: só 1 frase de cuidado que aponta para ele); **não** usa At 6 (M2).

## 6. Regras do curso ACP
- Sem nota de neutralidade nem slide de tradições ✅.
- Termos explicados na mesma frase: cumpridor (poiētḗs), atenta bem (parakýptō), bem-aventurado, escriba, observar, entender, aplicar ✅.
- Henry citado curto (clássico); Guzik só em paráfrase ✅.
- Sem "Orientação da ACP" (não há regra da casa neste tópico) ✅.

## 7. Estrutura (portão determinístico)
`validar_topico()` → `[]` · render `trigo-maduro`: 181 KB, 0 `None` · ids de pergunta e de item únicos · `fluxo` (não `diagrama`) · capa com `imagem_capa` · Reflexão + Resumo (6 bullets autônomos para o "Relembrando" do T222) ·
perguntas: mc 1, lacuna 1, tf 2, classify 1, associar 1, **open 2** ✅.

## 8. Publicação e áudio
- 7 imagens olhadas uma a uma: todas aprovadas (sem escrita em destaque). JPG + `.otim.webp`, 14 respondendo 200.
- **Correção depois do 1º PUT:** ficou no texto "Num lugar deserto, *isto é, sem gente*" (glosa sem fonte que a auditoria mandou tirar) → tirada e republicada antes do áudio.
- Áudio: as 30 narrações da IA foram **reescritas à mão** (ela acrescentou "daquele que serviu perfeitamente", leu a sigla "Ed 7:6" e mudou o texto). `_conferir_audio`: 2 com problema (repetição e palavras a mais em s2b0 e s8b0) → regerados um a um → **0 problemas**.
- Diagnóstico de produção: tudo ✓; 30 áudios + 14 imagens respondendo 200.

## Resultado
**0 pendências de fato.** Segue para imagens, publicação e áudio.
