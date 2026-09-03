# Processo real de criação de um Tópico — curso de obreiro

Documento de referência, escrito em 2026-08-30 depois de criar os Tópicos 1 e 2 na mão. Objetivo: registrar o passo a passo de verdade (não o ideal, o que realmente funcionou) pra (a) repetir nos Tópicos 3-27 sem reinventar cada vez, e (b) servir de base quando isso virar automação de verdade no `EstruturaAgent`/pipeline do NIA (ver `PLANO_IMPLEMENTACAO_ESTUDO_IA.md`, Fase 2c).

**Hoje é tudo manual, orquestrado por mim (Claude) chamando os agentes/serviços do NIA um a um.** Nenhum endpoint único faz isso de ponta a ponta ainda.

---

## Passo 1 — Pesquisa

- Fontes reais: comentários bíblicos confiáveis (ex: David Guzik/Enduring Word), artigos teológicos (ex: CPAJ/Mackenzie), pesquisa via Firecrawl quando necessário.
- Buscar o **texto bíblico real** de toda referência que vai ser citada, via `biblia_service.buscar_todos_textos("Rm 12:6-8")` — nunca aceitar citação de memória da IA.
- Guardar essa pesquisa (não descartar depois de usar uma vez — é a base pra Estágio de auditoria no Passo 8).

## Passo 2 — Gerar o conteúdo em 2 provedores, separado

- Chamar `ContentAgent.gerar_esqueleto_assuntos()` (decide em quantos assuntos o tópico se divide) e depois `gerar_assunto()` em loop, **uma vez com Groq, uma vez com Gemini** — perfil `obreiro`, com `texto_biblico_base` da pesquisa real do Passo 1.
- **Cuidado real de infra**: Groq tem teto de 8000 tokens/min por requisição; Gemini (SDK `google-genai`) tem teto de 20 requisições/dia grátis. Rodar via script isolado, não pelo endpoint `/pipeline/topicos/{id}/gerar` ainda (ele não separa por provedor pra comparação — só gera com 1 provedor de cada vez, e chama Quiz/Reviewer junto, gastando cota à toa se for só pra comparar).

## Passo 3 — Comparar os dois, decidir o que usar

- Ler o conteúdo dos dois de verdade (não só contar blocos). Critérios: riqueza, clareza pro formato slide, fidelidade bíblica, continuidade com tópicos anteriores, variedade de tipo de pergunta nos checkpoints/avaliação, bugs técnicos (ex: `icone` em inglês em vez de emoji, `tipo: "diagram"` em vez de `"diagrama"`).
- Montar uma tabela de comparação (documentada em `anotação para IA.md` pros Tópicos 1 e 2).
- **Achado real (Tópico 2)**: nenhum dos dois provedores sozinho é "o melhor" — Gemini teve prosa mais rica e continuidade melhor, Groq seguiu a regra de variedade de tipo de pergunta com mais disciplina. O padrão que funcionou foi montar um híbrido.

## Passo 4 — Montar o conteúdo final (híbrido, corrigindo bugs)

- Escolher a base mais rica (normalmente a prosa, não o esqueleto de perguntas).
- Corrigir bugs pontuais achados no Passo 3 na mão (ícone, variedade de `avaliacao_conceitos` — pelo menos 1 `tf`/`classify` e 2 `open`, nunca só `mc`).
- Redistribuir `checkpoint_apos` pelos assuntos com tipos variados (mc/tf/open), não deixar tudo concentrado em 1-2 assuntos.

## Passo 5 — Gerar as perguntas de verdade (QuizAgent)

- Chamar `QuizAgent.generate_perguntas()` no conteúdo final montado.
- **Achado real de infra**: em tópicos ricos (40+ blocos), o QuizAgent estourava o teto do Groq (`_resumir_blocos_para_quiz()` corta o texto mandado pra IA — não o conteúdo salvo — e `max_tokens` do Quiz foi reduzido pra 2800, já corrigido no código).
- **Achado real de comportamento**: pedindo muitas perguntas numa chamada só (3 checkpoints + 5 avaliação = 8), o Groq às vezes esquece 1 — sem correção de código ainda, checar sempre (Passo 7) e preencher na mão se precisar.

## Passo 6 — Montar o tópico final (determinístico, sem IA)

- `montar_topico(conteudo, perguntas, proximo_topico_label=...)` — monta os slides de checkpoint/avaliação/resultado, calcula duração e badges.

## Passo 7 — Checagem estrutural automática antes de salvar

- Nenhum checkpoint com `perguntas: []` (achado real: acontece, ver Passo 5).
- `imagem_capa` presente no resultado (achado real: `montar_topico()` não repassava esse campo — corrigido no código, mas vale conferir sempre).
- Depois de renderizar: `grep -n "None"` no HTML de verdade (não só na versão que você mesmo escreve por fora) — pega bloco de diagrama com `svg_raw: null` que passou despercebido.

## Passo 8 — Auditoria de conteúdo (Estágio D, manual por enquanto)

Comparar o conteúdo final contra a pesquisa do Passo 1, e contra o padrão já estabelecido no Tópico 1:
- Tem slide de **Reflexão** (perguntas abertas, sem gate, conectando com o tópico anterior)?
- Tem slide de **Resumo do Tópico** (bullets consolidados) antes da avaliação final?
- Referências bíblicas citadas de passagem (só entre parênteses) viraram **citação real** (bloco `quote`), ou continuam só mencionadas?
- Se o tema tem divergência entre tradições cristãs (ex: dons de cura/línguas, cessacionismo x continuísmo), tem uma **nota de neutralidade doutrinária** explícita, sem tomar partido?
- Todo bloco `diagrama` tem `svg_raw` de verdade (SVG desenhado à mão, cores do tema) — não só descrição em texto.

## Passo 9 — Imagens

- Hoje: manual. Buscar no Pexels (licença livre) OU gerar via `ImageService` (OpenAI `gpt-image-1`) usando a **base de estilo do curso** (documentada em `anotação para IA.md`, seção "Guia de estilo de imagem do curso") + um prompt específico por imagem.
- Padrão: 1 imagem de capa (`imagem_capa`) + 1-2 imagens inline (`imagem_sugerida`) só onde fizer sentido de verdade — não forçar em todo assunto.
- **Pendência registrada pra detalhar depois**: o fluxo ideal busca da internet E gera a descrição pro usuário criar a dele, as duas opções sempre juntas — formato ainda não definido no schema.

## Passo 10 — Salvar e renderizar

- `PUT /topicos/{id}` com o conteúdo final.
- `GET /topicos/{id}/render?theme=trigo-maduro` → versão slides (com exercícios).
- Renderizador próprio (script local, reaproveita a mesma paleta CSS) → versão leitura corrida (artigo único, sem exercícios) — **as duas versões sempre devem existir pro mesmo tópico**, geradas a partir do mesmo JSON salvo, nunca reescritas separadamente.

## Passo 11 — Revisão humana (ainda não construída como fluxo real)

- `is_approved=true` no banco hoje só significa "passou a checagem estrutural" — **não é aprovação de conteúdo/doutrina**.
- Falta a tabela `LessonComment` (planejada, ver `PLANO_MULTITENANT_E_PILOTO_TEOLOGIA.md`, Fase T3) pra você e o professor/teólogo anotarem por tópico.

---

## O que já está em código vs. o que ainda é manual

| Etapa | Hoje |
|---|---|
| Pesquisa + texto bíblico real | Manual (Firecrawl + `biblia_service`, chamados por mim) |
| Gerar conteúdo (2 provedores) | Código existe (`ContentAgent`), mas rodar nos 2 e comparar é manual |
| Montar híbrido + corrigir bugs | 100% manual |
| QuizAgent | Código existe e funciona, chamado manualmente no conteúdo final |
| `montar_topico()` | Código, determinístico, funciona |
| Checagem estrutural | Parcialmente automática (script confere checkpoints/imagem_capa), o resto é eu conferindo o HTML renderizado |
| Auditoria de conteúdo (Passo 8) | 100% manual |
| Imagens | 100% manual (Pexels ou `ImageService`, escolhido caso a caso) |
| Salvar + renderizar (2 versões) | Código existe pros slides; a leitura corrida é um script separado meu, fora do NIA |
| Revisão humana | Sem tabela/fluxo ainda |

**Pra virar automação de verdade** precisa, na ordem que já foi decidida antes (ver análise estratégica, D3): `EstruturaAgent` ganhar `PerfilDominio` (hoje só monta grade genérica), um `AuditorAgent` pro Passo 8, e a tabela `LessonComment` pro Passo 11. Nenhum desses 3 existe ainda.

---

## Atualização 2026-09-01 — refinamentos aprendidos gerando o Tópico 3 (Vocação e Ofícios)

O fluxo dos 11 passos continua valendo. O que mudou/ficou mais nítido:

**Passo 1 (Pesquisa) — três acréscimos:**
1. **Re-conferir as citações dos tópicos ANTERIORES** se o novo tópico reusa algum
   versículo. Gerando o T3, conferi contra `biblia_service` 3 citações que eu (Claude)
   tinha escrito **de memória** no T2 na sessão anterior — as 3 estavam erradas (1Co 12:11
   "distribuindo" ≠ "repartindo"; 1Co 12:12 reescrito; Ef 4:11-12 "deu uns como… pastores e
   mestres, tendo em vista" ≠ "para… doutores, querendo"). Regra reforçada: **nunca**
   confiar na memória do modelo pra texto bíblico, nem pra versículo "curto e conhecido".
2. **Firecrawl pra comentário real** (Guzik/Enduring Word): `firecrawl scrape` das páginas
   de `enduringword.com/bible-commentary/<livro-cap>/`. Usar como APOIO e entrar como
   **paráfrase atribuída** ("Guzik resume assim: …"), nunca citação em bloco longa —
   comentário é material sob copyright.
3. Buscar bem mais referências do que a IA vai usar — no T3 foram ~18 passagens
   (`biblia_service.buscar_texto` uma a uma), várias entraram como bloco `quote` que a
   geração da IA não tinha pensado (ex: 1Pe 5:1-4, At 20:17+28, 1Tm 4:14).

**Passo 2 — script padrão:** `backend/_gerar_topicoN_obreiro.py` (ver `_gerar_topico3_obreiro.py`
de modelo). Faz `generate_conteudo_pro()` UMA VEZ com `GroqService()` e UMA VEZ com
`GeminiService()`, os dois com `perfil=PERFIL_OBREIRO` e o `texto_biblico_base` real, e
salva `_conteudo_groq_topicoN.json` / `_conteudo_gemini_topicoN.json` (bind mount → aparecem
no host em `backend/`). Rodar com `docker exec nia_backend python _gerar_topicoN_obreiro.py`
em background (leva minutos). Cota: Gemini ~6-10 chamadas por rodada (teto 20/dia).

**Passo 3 — exemplo real (T3):** nenhum provedor ganha sozinho. Gemini foi mais rico,
costurou melhor com T1/T2 e tratou a neutralidade doutrinária com mais equilíbrio; Groq
teve mais disciplina na variedade de tipo de pergunta e **pegou um bug do Gemini** (os 5
itens de `avaliacao_conceitos` todos `"tipo":"mc"`). Decisão: base = Gemini, corrigindo as
perguntas na mão. Tabela completa fica em `anotação para IA.md`.

**Passo 4 vira o entregável de validação:** o `topicoN-<slug>-completo.html` (versão de
leitura corrida, no sistema visual dos T1/T2, com `.takeaway` no fim de cada seção) é
escrito PRIMEIRO e é o que vai pra revisão humana. Só **depois de validado** é que vira
JSON do schema + QuizAgent + `montar_topico()` + slides + `PUT /topicos/{id}`. Isso segue o
fluxo que o Atila definiu em `anotação para IA.md` ("primeiro sai rico de conteúdo, você/
professor valida, aí sim geramos a aula e rodamos a quiz").

**Passo 8 (auditoria) — fazer junto do Passo 4**, não depois: ao escrever o `completo.html`
já garantir seção de Reflexão, Resumo do Tópico, toda referência de passagem virando bloco
`quote` real, e nota de neutralidade explícita onde tradições divergem.
