# Auditoria — Tópico 19 "O problema e a virada — limites do Token ID" (revisão completa)

Curso de IA (Course 5) · `Topico.id=19` · 2026-10-12 · régua: `fontes/ia/topico19-limites-token-id.md`.
Conteúdo auditado: `backend/_criar_topico19_ia.py` → `_topico19_ia_final.json` (15 slides).
**Resultado: 0 pendências.**

## 1. O que mudou em relação ao conteúdo antigo

O antigo (cópia em `backend/_topico19_backup_prod.json`) era o port do deck de estudo do Atila. A
linha de raciocínio foi mantida (caixa-preta → tokens precisam se relacionar → Token ID → por que
não basta → mesmo problema em outros domínios → pista da solução), assim como a frase de exemplo,
os IDs ilustrativos, a analogia do prontuário, a do detetive e a pergunta aberta do colega.

| Ponto do conteúdo antigo | O que foi feito |
|---|---|
| "IDs atribuídos geralmente por ordem de descoberta… ou por frequência" | **corrigido/precisado**: o ID é a ordem de criação do token no vocabulário; no BPE, a frequência decide a ordem das fusões (fontes 3, 4, 7) |
| "dois [tokens] totalmente diferentes podem ter IDs próximos, por pura coincidência de quando foram vistos pela primeira vez no corpus" | **reescrito**: não é "quando foram vistos", é a ordem das fusões; agora mostrado com dados reais do GPT-2 |
| "'Incrível' e 'sensacional' têm Token IDs distantes" | **removido**: afirmação sobre IDs reais sem conferência; trocado por pares conferidos no vocabulário do GPT-2 |
| "bank vira banco ou margem" | mantido, agora com a fonte (J&M cap. 7) |
| 2 blocos `diagrama` (SVG) | trocados por `cols2` + imagem |
| Sem Reflexão, 1 pergunta aberta, sem imagens internas, sem áudio | corrigido |
| Resumo com rótulo "🧠" (não gerava o "↩ Relembrando" do T20) | agora "📌 Resumo do tópico" |

## 2. Afirmações do tópico → fonte

| Slide | Afirmação | Fonte (#) | Status |
|---|---|---|---|
| s1 | Caminho entrada → tokens → … → resposta; caixa-preta entre tokens e logits | 1 (deck), Aula 1 | ok |
| s1 | Exemplo do cliente com dois gatos e pouca iluminação | 1 | ok |
| s2 | "O cliente tem dois gatos. Ele procura…": "Ele" e "planta" dependem de tokens anteriores | 1 (Parte 1) | ok |
| s2 | Exemplo do lago e da margem ("bank"); contexto pode estar bem longe | 3 (cap. 7, ex. 7.5) | ok — paráfrase atribuída |
| s2 | Citação Vaswani: dependências sem levar em conta a distância | 2 (§1, lido no PDF) | ok — tradução livre |
| s2 | Attention no Tópico 4 da aula | grade: T19, T20, T21, T22 | ok |
| s4 | Tabela de IDs de exemplo; "ilustrativos" | 1; 5 (no GPT-2, 8274 é outro token) | ok — texto avisa |
| s4 | Saída do tokenizador = sequência de ids | 3 (cap. 2) | ok |
| s4 | ids de entrada = índices de token, representações numéricas | 6 | ok |
| s5 | BPE: símbolos básicos → contar pares → fundir o mais frequente → token novo → repetir | 3 (cap. 2), 4 (§3.2) | ok |
| s5 | 256 primeiros para símbolos básicos; fusões recebem 256, 257, 258 | 7 | ok — dito como "tokenizador didático" do Karpathy |
| s5 | GPT-2: 50.257 entradas; 0–255 básicos, 0 = "!"; 256 " t", 257 " a", 262 " the"; 50256 = fim de texto | 5 (arquivo lido) | ok |
| s5 | "ID baixo sugere pedaço frequente" | inferência de 3/4 + 5 | ok — escrito como "sugere" |
| s6 | "cat" 3797; vizinhos 3795 "psych", 3796 "rief", 3798 "esc", 3799 "observ" | 5 | ok |
| s6 | "happy" 3772 e "prison" 3770; "dog" 3290; "cats" 11875 entre "engines" e "buffer"; "glad" 9675 | 5 | ok |
| s6 | ID é índice; embedding é vetor num espaço com geometria | 1 (deck), T20 | ok |
| s8 | Scunthorpe, 1996: cadastro recusado pelo filtro de indecência da AOL; AOL passou a usar "Sconthorpe" | 8 | ok — ver item 3 |
| s8 | Busca, tradução, recomendação, agente de vendas | 1 (deck) | ok — exemplos, sem afirmar IDs |
| s9 | Expectativa de que palavras parecidas fiquem próximas (word2vec, 2013) | 9 | ok — paráfrase |
| s9 | O ID serve pra achar o vetor na tabela | 3 (cap. 6), 7 | ok |
| s10 | Cada tokenizador funciona de um jeito | 6 | ok |
| s10 | Exemplos do Garden Center e da portaria | ilustrações coerentes com o T20 | ok |
| s12 | Resumo | repete só o que está acima | ok |

## 3. Fatos de alto risco — busca independente (2026-10-12)

- " dog" = 3290 e " the" = 262 no GPT-2 → confirmados em fonte independente (post de Simon Willison).
  " cat" = 3797 não apareceu na busca; vale o arquivo `vocab.json` lido diretamente (fonte primária).
- Scunthorpe/AOL, abril de 1996 → confirmado. **Divergência achada:** o RISKS Digest diz que o morador
  se cadastrou escrevendo "Sconthorpe"; o jornal local, citado por outras fontes, diz que ele trocou o
  endereço. **Corrigido no texto:** saiu a frase sobre como ele conseguiu; ficou só o que todas as
  fontes dizem (cadastro recusado; a AOL passou a usar "Sconthorpe"). A regra exata do filtro não é
  afirmada.

## 4. Rascunhos (Gemini 3.7 Flash e Groq) — o que NÃO entrou

Nenhum texto dos rascunhos entrou. Erros encontrados:

- **Gemini:** IDs "reais" inventados (" plant" = 3605, " active" = 3604, "water" 1660, "sun" 4299…
  — no arquivo, " plant" é 4618); "gatos foi a 8.274ª fusão"; "vocabulário de cerca de 100.000
  tokens"; IDs inventados pra "adubo", "orquídea", "flor"; citação de J. R. Firth (1957) fora do
  dossiê; detalhes do filtro de Scunthorpe que a fonte não dá; preços e nomes de tools inventados.
- **Groq:** "no GPT-2, o ID 0 é `<|endoftext|>` e o ID 1 é '!'" (errado: 0 é "!", o fim de texto é
  50256); "filtro que bloqueava qualquer e-mail" (era o cadastro); "regar, sol e vaso provavelmente
  têm IDs baixos" (chute); blocos `timeline` e tipos inválidos.

## 5. Pedagogia

- Ordem: o que já se sabe → o problema grande (relacionar tokens) → o problema básico (números) → de
  onde vem o número → prova com dado real → o mesmo erro fora dos LLMs → pista → uso no agente.
- Perguntas respondíveis com o ensinado (ck1: s2; ck2: s4–s6; ck3: s8, s10 e as fontes citadas em
  s2, s5, s8; ck4: s10, s6, s10).
- Tipos: 3 `mc`, 2 `tf`, 1 `classify`, 1 `associar`, 2 `open`. Ids únicos.

## 6. Continuidade

- Retoma a Aula 1 (caminho completo, "LLM faz linguagem, fatos vêm de tools" na Reflexão).
- Entrega ao T20 exatamente o que ele usa na abertura: a frase "Tenho dois gatos e pouca luz", a
  lista [4821, 1359, 8274, 74, 5291, 3190] e o "número de prontuário".
- Não explica embedding nem Attention; só nomeia. `proximo_topico_label` = "Embeddings".
- O "📌 Resumo" tem bullets que se sustentam sozinhos (viram o "↩ Relembrando" do T20).

## 7. Direito autoral

Uma citação curta (Vaswani), atribuída; o resto é paráfrase atribuída. Dados do vocabulário são fatos.

## 8. Estrutura

`validar_topico()` = `[]`; ids duplicados = nenhum; render local (azul-petroleo) com 0 `None`; capa
com `imagem_capa`; 1 `fluxo`, nenhum `diagrama`; Reflexão "💭" + Resumo "📌".

## 9. Imagens (capa mantida + 7 novas; 9 slides de conteúdo → densidade 0,78)

A capa `t19-capa-limites-token-id.jpg` já estava no isométrico claro e foi mantida. Novas, todas
olhadas uma a uma:

| Arquivo | Resultado |
|---|---|
| t19-caixa-preta | ok — `alt` ajustado à imagem |
| t19-pistas | ok |
| t19-prontuario | ok |
| t19-vizinhos | ok |
| t19-filtro | **refeita** — a 1ª saiu com a palavra "REJECT" carimbada |
| t19-fila-mapa | **refeita** — a 1ª saiu escura, com mapa-múndi e traços imitando texto |
| t19-agente | ok |

## 10. Áudio (30 blocos, MP3)

- Narrações: 9 das 30 reescritas antes da voz. O erro mais sério estava no caso Scunthorpe: a
  narração gerada afirmava que o nome da cidade "continha um termo considerado impróprio" e que a
  AOL "teve que fingir" — detalhes que o texto evita de propósito (as fontes não dão a regra do
  filtro). Outras: tokens entre aspas e números grandes que seriam mal lidos, frase que anunciava
  a citação sem dizê-la, resumo com referência errada ("fazer isso causou erros", ligando o caso
  Scunthorpe a contas com IDs). A narração do slide dos vizinhos de "cat" ganhou os dados que
  estão no bloco de duas colunas, que não é narrado. Registro em `backend/_revisar_narracao_topico19.py`.
- Voz: `gemini-3.8-flash-tts`, 30/30.
- Corte corrigido sem gastar voz: o começo de "Jurafsky" tinha ficado no fim do s2-b0, e o s2-b1
  vinha com a transcrição vazia. "Cat." no fim do s6-b0 é invenção do Whisper (medido: silêncio).
- `_conferir_audio.py 19 5`: 0 com problema.
- Produção: 38 mídias (30 MP3 + 8 imagens) respondendo 200; diagnóstico sem ✗.
