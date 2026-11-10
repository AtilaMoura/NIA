# Auditoria — T218 "Antigo e Novo Testamento: os 66 livros em um mapa" (Obreiro ACP)

Conteúdo: `backend/_criar_topico218_obreiro_acp.py` → `_topico218_obreiro_acp_final.json` (14 slides, 8 imagens, 4 checkpoints).
Dossiê: [topico218-66-livros-mapa.md](topico218-66-livros-mapa.md) · Data: 2026-11-10.

## 1. Mapa dos 66 livros
`backend/_conferir_mapa_218.py`: lista de 66 livros na **ordem do índice da ACF** (bibliaonline), 39 + 27 = 66; grupos do AT = 5 + 12 + 5 + 5 + 12 = 39 e do NT =
4 + 1 + 13 + 8 + 1 = 27; os 10 rótulos de grupo aparecem no texto com a quantidade certa. **MAPA OK.** A soma de capítulos dos profetas (183 e 67) vem da
contagem do mesmo índice. As 13 cartas de Paulo (Romanos a Filemom) foram conferidas uma a uma: todas começam o versículo 1 com "Paulo".

## 2. Citações bíblicas (ACF)
`_conferir_citacoes_218.py`: 27 trechos comparados letra por letra com o texto baixado (`_textos_biblicos_topico218.json`, 43 passagens). **Todas as citações em bloco
passaram.** O script lista 7 "falhas", **todas falsos positivos** do detector (aspas pareadas atravessando texto que não é versículo; conferidos à mão): "novo testamento"
e "aliança nova" são trechos curtos de Lc 22:20 e Jr 31:31, ambos lidos; o resto são enunciados de pergunta e explicação.

## 3. Afirmação → fonte → status
| Afirmação no texto | Fonte (dossiê #) | Status |
|---|---|---|
| 66 livros; 39 no AT (Gênesis a Malaquias) e 27 no NT (Mateus a Apocalipse) | 1 | ✅ índice da ACF lido |
| "Testamento" = também "aliança" (Strong G1242: *disposition… a testament or will; a compact, a covenant*); Lc 22:20; Jr 31:31 | 1, 2 | ✅ |
| Algumas igrejas, como a católica, têm livros a mais no AT; este curso usa 66 | 5 | ✅ uma frase, **sem número** (o "73" não foi lido em fonte) |
| Grupos do AT e do NT (nomes = "ajuda de estudo"; a ordem dos livros é a da Bíblia) | 1 | ✅ dito no texto |
| Pentateuco = "cinco partes" (Wikipédia "Pentateuco", lida) | — | ✅ |
| Salmos = livro com mais capítulos (150); Obadias tem 1 capítulo | 1 | ✅ do índice ("maior" trocado por "mais capítulos") |
| "Maiores"/"menores" = tamanho dos livros, não importância (183 x 67 capítulos) | 1 | ✅ contagem feita; a afirmação "não importância" é lógica a partir dos números e do dossiê |
| Jesus: "lei de Moisés, profetas e Salmos" (Lc 24:44); Hb 1:1-2 (falou pelos profetas, depois pelo Filho) | 1 | ✅ |
| Evangelho = "boa notícia" (G2098); Mc 1:1 | 3, 1 | ✅ |
| Apocalipse = "revelação" (G602); Ap 1:1 começa com a palavra | 4, 1 | ✅ |
| Atos "parece continuar" o 3º Evangelho; os dois dirigidos a Teófilo (Lc 1:1-4; At 1:1-2) | 1 | ✅ texto cauteloso: **não** diz quem escreveu |
| 13 cartas de Paulo começam com o nome dele; Tg, Pe, Jd se identificam; 2 e 3 Jo "o presbítero"; Hebreus sem nome | 1 | ✅ |
| 21 cartas (13 + 8) no NT | 1 | ✅ soma do mapa |
| Mt 22:23-29: saduceus (não acreditavam na ressurreição) perguntam; Jesus: "Errais, não conhecendo as Escrituras" | 1 | ✅ contexto lido (Mt 22:23-29) |
| Bereia: Paulo e Silas chegam; examinavam cada dia as Escrituras (At 17:10-11) | 1 | ✅ contexto lido |

## 4. Erros que a auditoria pegou (e saíram do texto)
1. "Salmos, o maior da Bíblia" → "o livro com mais capítulos (150)".
2. "Jesus avisou um grupo que estudava as Escrituras" → o texto não diz que estudavam: virou "alguns saduceus, que não acreditavam na ressurreição, fizeram uma pergunta" (contexto lido).
3. "Os mesmos grupos que você acabou de ver (Lei, profetas, Salmos)" → Jesus usa 3 partes e o mapa usa 5 grupos; o texto diz agora que os grupos do mapa são **ajuda para iniciante, não os nomes que Jesus usou**.
4. "A Bíblia chama de epístolas" → a palavra aparece em 2Pe 3:16; reescrito para "também se chamam epístolas (a segunda carta de Pedro usa essa palavra)".
5. "Atos é a continuação do 3º Evangelho" (afirmativo) → "parece continuar", com a base (dirigidos a Teófilo).
6. "Os cinco livros" como tradução de Pentateuco → "cinco partes" (Wikipédia).
7. "Na última ceia" → "depois da ceia" (é o que Lc 22:20 diz).
8. "Apocalipse não quer dizer fim do mundo, como muita gente pensa" → tirei a parte sobre o que "muita gente pensa" (sem fonte).
9. "Bíblia de 66 livros que você tem em mãos na maioria das Bíblias evangélicas" → "como na tradução que estamos lendo (ACF)".
10. "Presbítero é alguém mais velho que lidera" → "um líder da igreja" (a etimologia não foi lida; o Estatuto lista Presbítero como ministério).

## 4b. Rascunhos de IA (comparação)
- **Gemini** (`_conteudo_conteudo_topico218.json`): 7 slides, **0 blocos de citação literal**, 1 menção ao número "73" (livros da Bíblia católica), que **não foi lido em fonte** e
  por isso ficou fora do texto final. Nada aproveitado.
- **Groq** (`segunda_opiniao`, terminou depois da publicação; comparado em seguida): 10 slides, só 1 bloco de citação literal, 1 menção a "tradições" (o curso não faz comparação).
  **Nada foi aproveitado**; o texto publicado não mudou.
- A versão final vem só do dossiê.

## 5. Continuidade e fronteira
- Costura com o T217 ("biblioteca", "pessoas reais"); fecha com `proximo_topico_label` = T219 (achar versículo).
- Não ensina a citar referência (T219), não conta a história do cânon, não dá autoria detalhada nem resume cada livro.

## 6. Regras do curso ACP
- Sem nota de neutralidade nem slide de tradições ✅ (a diferença católica está em **uma frase**, e o texto volta à Bíblia de 66 livros).
- Termos explicados na mesma frase: Testamento, aliança, Pentateuco, profeta, evangelho, apocalipse, epístola, presbítero, tratado ✅.
- Sem "Orientação da ACP" (não há regra da igreja neste tópico) ✅.
- **Pendência para o pastor/Adriano (não trava):** confirmar se a ACP usa os mesmos nomes de grupo (Lei, História, Poesia e sabedoria, Profetas maiores/menores, Evangelhos, Cartas de Paulo, Outras cartas) e se quer a frase sobre a Bíblia católica.

## 7. Estrutura (portão determinístico)
`validar_topico()` → `[]` · render `trigo-maduro`: 189 KB, 0 `None` · ids únicos · `fluxo` (não `diagrama`) · capa com `imagem_capa` · Reflexão + Resumo (7 bullets autônomos para o "Relembrando" do T219) ·
perguntas: mc 2, tf 2, classify 2, lacuna 1, associar 1, **open 2** ✅.

## 8. Revisão de 2026-11-10 (auditoria pedida pelo Atila, tarefa NIA-T-019)
Erros que a 1ª auditoria deixou passar, corrigidos no texto e republicados:
1. **1 João omitida** em "de quem são as cartas": o aluno concluía que Hebreus era a única carta sem nome. Card virou "Primeira carta de João e Hebreus"; resumo e explicação do ck3_2 ajustados.
2. **"Testamento vem de uma palavra grega"** → "traduz uma palavra grega" (a palavra portuguesa vem do latim; Jeremias escreveu em hebraico). Resumo: "também quer dizer aliança" (o "também" tinha caído); explicação do ck3_3 igual.
3. **"A maior parte do NT são cartas"** → "a maioria dos livros do NT" (em volume de texto, Evangelhos + Atos passam da metade).
4. **Maiores/menores**: a explicação não tinha fonte; entrou Agostinho (*Cidade de Deus* XVIII, 29, lido no texto literal da tradução NPNF) e a nota de Lamentações (5 capítulos, mas no grupo dos maiores, logo depois de Jeremias).
5. Fontes: 2ª fonte independente para 39 / 27 / 21 cartas (Wikipédia pt e en); Pentateuco e Agostinho registrados no dossiê; Pró-Livro (não usado) saiu da lista.
6. Áudio: narrações dos blocos alterados reescritas à mão e regeradas; as do resumo e da reflexão também (a IA tinha virado pergunta aberta em afirmação e tirado "evangelho = boa notícia").
- **Fronteira (decisão do Atila):** At 17:11 (Bereia) é a passagem-base do 1º tópico da Aula 1.2; aqui aparece como exemplo curto. Mantido até decisão.

`validar_topico()` → `[]`; render 0 `None`; mapa OK; citações: as mesmas 7 falsas-positivas de aspas, nenhuma citação em bloco falhou.

## Resultado
**0 pendências de fato.** Segue para imagens, publicação e áudio.
