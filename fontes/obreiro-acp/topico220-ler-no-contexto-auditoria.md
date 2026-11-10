# Auditoria — T220 "Ler o texto no seu contexto" (Obreiro ACP)

Conteúdo: `backend/_criar_topico220_obreiro_acp.py` → `_topico220_obreiro_acp_final.json` (12 slides, 7 imagens, 3 checkpoints).
Dossiê: [topico220-ler-no-contexto.md](topico220-ler-no-contexto.md) · Data: 2026-11-10.

## 1. Citações bíblicas (ACF)
`_conferir_citacoes_220.py`: 22 trechos comparados letra por letra com `_textos_biblicos_topico220.json` (19 passagens baixadas da ACF). **Todas as citações em bloco passaram.**
As 6 "falhas" listadas são **falsos positivos** do detector (aspas em texto que não é versículo: enunciados, analogia, nomes gregos); conferidas à mão.

## 2. Afirmação → fonte → status
| Afirmação no texto | Fonte (dossiê #) | Status |
|---|---|---|
| Paulo e Silas em Tessalônica: três sábados na sinagoga, mostrando nas Escrituras que o Cristo tinha de sofrer e ressuscitar; inveja e alvoroço; enviados de noite a Bereia | 1 (At 17:1-3, 5, 10) | ✅ |
| Bereia = cidade da Macedônia; hoje lá está Véria, na Grécia | 8 | ✅ |
| Sinagoga = lugar onde os judeus se reuniam para ler as Escrituras e orar | Wikipédia "Sinagoga" (lida) | ✅ |
| At 17:11: "de bom grado", "examinando cada dia" | 1 | ✅ |
| "Examinando" = anakrínō: investigar, examinar, pesquisar com cuidado | 2 | ✅ |
| Matthew Henry (começo do séc. 18; comentário de 1708–1710): compararam com outras partes das Escrituras, sem preconceito | 4; Wikipédia "Matthew Henry" (lida) | ✅ paráfrase atribuída |
| Contexto = o que está em volta da frase + circunstâncias | 6 | ✅ |
| Camadas: trecho, capítulo, livro, Bíblia inteira; contexto da história | 7 | ✅ ("Bíblia inteira" = Henry: "other places of scripture") |
| Lc 15:1-3: Jesus contou a parábola a quem murmurava porque ele recebia pecadores | 1 | ✅ (o texto **não** diz quantas parábolas) |
| Publicanos = cobradores de impostos para o Império Romano, desprezados pelo povo; fariseus = grupo de judeus dedicados à lei; escribas = especialistas no estudo e na explicação da lei | Wikipédia "Publicano", "Fariseus", "Escriba" (lidas) | ✅ ("Publicano" é esboço; a definição básica bate com Lc 15:1 "publicanos e pecadores") |
| Parábola = história que traz uma verdade importante | Priberam (lido: "Narração alegórica que envolve… alguma verdade importante") | ✅ |
| Salmos = poesia; "pastor" é imagem do cuidado de Deus | 1; T218 (grupo poesia e sabedoria) | ✅ |
| Jó: três amigos (2:11); Elifaz fala primeiro (4:1) e diz que o inocente não perece (4:7-8); Deus: "não falastes de mim o que era reto" (42:7) | 1 | ✅ — o texto **não** diz que tudo o que os amigos disseram é errado; repete o que Deus disse |
| "Como se o sofrimento de Jó fosse castigo pelo que ele plantou" | 1 (Jó 4:8 "semeiam mal, segam o mesmo") | ✅ leitura direta do versículo |
| Jr 29: carta aos deportados por Nabucodonosor (29:1); casas, jardins, famílias, paz da cidade (29:5-7); 70 anos (29:10); 29:11 | 1, 9 | ✅ sem datas |
| Guzik: promessa feita aos judeus no cativeiro; mostra o coração de Deus pelo seu povo, que não muda | 5 | ✅ paráfrase atribuída |
| 2Tm 2:15: "maneja bem" = orthotoméō, "cortar reto", ensinar a verdade correta e diretamente | 1, 3 | ✅ |
| Ne 8: o povo que voltou do cativeiro (8:17) se reuniu na praça e pediu a Esdras, o escriba, o livro da lei (8:1); liam e explicavam o sentido (8:8) | 1 | ✅ |
| Filipe e o homem da Etiópia (costura com o T217) | T217 (At 8:30-35, conferido lá) | ✅ |

## 3. Erros que a auditoria pegou (e saíram do texto)
1. "Matthew Henry, do século 18" → conferido (1662–1714; comentário de 1708–1710) → "do começo do século 18".
2. "Publicanos eram… malvistos; fariseus e escribas eram religiosos que estudavam a lei" (escrito sem fonte) → definições trocadas pelas das fontes lidas.
3. "Parábola = uma história curta que ensina uma verdade" → "uma história que traz uma verdade importante" (Priberam).
4. "Cativeiro = viviam presos" → os exilados construíam casas e plantavam (Jr 29:5); virou "tinham sido levados à força e viviam numa terra estrangeira".
5. "Babilônia, um país distante" → "longe da sua terra" (Babilônia é cidade e império; o texto não precisa disso).
6. "Quando o povo voltou do cativeiro…" (Ne 8) estava sem base → Ne 8:1 e 8:17 baixados e lidos.
7. "Paulo e Silas pregavam de cidade em cidade" → "chegaram à cidade de Tessalônica" (At 17:1).
8. Datas do exílio **não entram**: as fontes divergem (598/597, 587/586, 605/609).

## 4. Rascunhos de IA (comparação)
- **Gemini** (`_conteudo_conteudo_topico220.json`): 9 slides de conteúdo, **0 blocos de citação literal**; usou **Fp 4:13** como exemplo (fica para o T222, ver a fronteira no dossiê) e um slide sobre "gêneros bíblicos" maior que o escopo. Acertou At 17:5 (inveja). **Nada aproveitado.**
- **Groq** (`segunda_opiniao`, gpt-oss-120b; terminou logo depois da publicação e foi comparado em seguida): 6 slides de conteúdo, só 1 bloco de citação, e ele **não é literal** (é paráfrase com um trecho de Ne 8:8 dentro); cita Filipenses (T222); **não** tem o caso de Jeremias 29. **Nada aproveitado**; o texto publicado não mudou.
- A versão final vem só do dossiê.

## 5. Continuidade e fronteira
- Costura: T219 terminou com "a próxima aula ensina a ler o texto no seu contexto"; o T220 abre com "na aula anterior você aprendeu a achar". At 17:11, que apareceu de passagem no T218, aqui é a passagem-base (decisão do Atila, NIA-T-020). Filipe (T217) é retomado como exemplo de ajuda.
- **Não** ensina o método observar/entender/aplicar (T221: só 1 frase de ponte no fim) e **não** faz lista de erros nem usa Fp 4:13 (T222). O caso de Jó é ensinado como a pergunta "quem está falando?", e não como lista de erros.

## 6. Regras do curso ACP
- Sem nota de neutralidade nem slide de tradições ✅.
- Termos explicados na mesma frase: sinagoga, examinar (anakrínō), contexto, parábola, publicano, fariseu, escriba, cativeiro, maneja bem (orthotoméō) ✅.
- Guzik e Henry só em paráfrase atribuída ✅.
- Sem "Orientação da ACP" (não há regra da casa neste tópico) ✅.
- **Para o pastor/Adriano (não trava):** a ênfase em Jr 29:11 (promessa dita aos exilados, que mostra o coração de Deus) está como o pastor ensina?

## 7. Estrutura (portão determinístico)
`validar_topico()` → `[]` · render `trigo-maduro`: 183 KB, 0 `None` · ids de pergunta e de item únicos · `fluxo` (não `diagrama`) · capa com `imagem_capa` · Reflexão + Resumo (6 bullets autônomos para o "Relembrando" do T221) ·
perguntas: mc 1, tf 2, lacuna 1, classify 1, associar 1, **open 2** ✅.

## 8. Publicação e áudio
- 7 imagens olhadas uma a uma; `t220-bereanos` refeita (pseudo-escrita no rolo do centro). JPG + `.otim.webp`, todas 200 na VM1.
- Áudio: as 29 narrações da IA foram **todas reescritas à mão** (ela pôs fatos a mais: "os dois apóstolos" para Silas, "futuro de esperança", "gravemente doente"; usou jargão como "gênero literário"; repetiu a abertura "Ao analisar o livro de Jó…"; trocou as perguntas da Reflexão por afirmações). `_conferir_audio`: 0 problemas. 5 blocos gerados um a um, porque o corte do lote não foi achado.
- Diagnóstico de produção: tudo ✓; 29 áudios + 14 imagens respondendo 200.

## Resultado
**0 pendências de fato.** Segue para imagens, publicação e áudio.
