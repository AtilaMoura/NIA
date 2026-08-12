# Plano de Implementação — NIA no padrão "Estudo IA"

Objetivo: fazer o NIA gerar cursos no mesmo nível do que construímos manualmente em `Estudo IA/exercicios/` — slide deck interativo, com checkpoints com gate, diagramas SVG, áudio com velocidade, tema visual escolhível, e avaliação/reforço personalizado — mas de forma automatizada, escalável pra qualquer assunto, com estrutura de curso variável (não fixa em 6 tópicos).

Cada fase tem: o que já existe no NIA hoje, o que precisa ser construído, e um teste concreto pra marcar `[OK]`. Não passar pra próxima fase sem marcar a anterior.

Referência viva do padrão de conteúdo: `../Estudo IA/exercicios/aula1-topico4-geracao-resposta.html` (o mais completo) e `../Estudo IA/CLAUDE.md` (convenções).

---

## Fase 0 — Schema estruturado + catálogo de temas
**Status: [OK]** — 2026-08-11. Artefatos: `docs/schema/schema-conteudo-topico.md`, `docs/schema/schema-conteudo-topico.example.json` (Tópico 4 completo, 19 slides, 8 gates, 2 diagramas — validado), `docs/schema/temas.json` (4 temas), campo `User.preferred_theme` adicionado em `models.py`.
Pendência conhecida (não bloqueia): schema ainda não tem um tipo de bloco pra "mini-check" sem gate (usado no reforço visual) — registrado na seção de checagem de genericidade do `.md`. `preferred_theme` só entra no banco quando as tabelas forem (re)criadas — não há Alembic neste projeto, só `Base.metadata.create_all()`, que não altera tabela já existente.

O que já existe: `Course.structure` (JSONB) e `Lesson.content` (Text/Markdown) no banco.
O que falta: um schema JSON que descreva um tópico inteiro em partes reaproveitáveis (não texto solto) — slides, tipo de cada slide (definição/analogia/checkpoint/diagrama/aplicação), boxes semânticas, perguntas com gabarito, descrição textual de cada diagrama a gerar.

**Construir:**
- `docs/schema-conteudo-topico.json` (ou `.md` com exemplo) — schema formal.
- Catálogo dos 4 temas (Vidro Fumê, Estufa Noturna, Console Verde, Aurora Botânica) como dados: paleta (hex), tipografia, radius, motion — não CSS solto.
- Novo campo `theme` (`Course.theme` ou `User.preferred_theme`) no banco — hoje não existe nenhum campo de tema.

**Teste [OK quando]:** converter manualmente o Tópico 4 já existente (`aula1-topico4-geracao-resposta.html`) pro novo schema JSON, sem perder nenhuma seção/pergunta/diagrama, e validar que o schema é genérico o bastante pra descrever também o Tópico 5 (Alucinação, com 3 diagramas e cards de tipologia).

---

## Fase 1 — Renderizador (JSON estruturado → HTML interativo)
**Status: [OK]** — 2026-08-11. Artefatos: `backend/app/renderer/render.py`, `backend/app/renderer/templates/topico.html.j2`, `backend/app/renderer/__init__.py`. Adicionado `jinja2==3.1.2` ao `requirements.txt` (arquivo também corrigido de UTF-16 pra UTF-8 nesse processo — o original tinha uma codificação incomum que poderia dar problema no `pip install`).

Melhoria em relação ao processo manual: `buildSummary()` agora é 100% genérico — não existe mais `order`/`labels` escritos à mão por tópico. `render.py` varre os slides e monta `QUESTION_ORDER` automaticamente (achatando os itens de `classify`), incluindo o `open_total` calculado, não mais hardcoded.

**Teste realizado:** renderizado `schema-conteudo-topico.example.json` (Tópico 4) nos 4 temas. Confirmado por inspeção do HTML gerado: 19 slides (contagem exata via regex, batendo com o original), os 8 `data-gate` presentes (`ck1`,`ck2`,`ck3`,`ef1`-`ef5`), os 2 diagramas SVG embutidos, botões de classificação renderizando com valor+rótulo corretos, zero sobra de sintaxe Jinja (`{{`/`{%`) no output, variáveis de cor/tipografia trocando corretamente entre temas (conferido no Console Verde). Abri o Vidro Fumê e o Console Verde no navegador pra conferência visual/funcional (navegação, gate, áudio).

**Bugs encontrados e corrigidos durante o teste** (não escondidos): (1) botões de classify estavam sendo gerados com só 1 botão e valor errado — faltava estruturar `rotulos_opcoes` como `{valor, rotulo}` em vez de string solta; corrigido no schema e no exemplo. (2) `PROXIMO_TOPICO_LABEL` tinha uma expressão Jinja com um `if false else` sobrando de uma tentativa anterior — simplificado. (3) JS tinha um trecho morto (`buildClassifyButtons`, `window.__classifyRotulos`) de uma abordagem abandonada — removido.

O que já existe: nada — hoje o conteúdo é servido como Markdown puro.
O que falta: código determinístico (sem IA) que pega o JSON da Fase 0 + o tema escolhido e monta o HTML completo — topbar, progresso, slides, gate (`checkGate()`), navbar com áudio+velocidade, tela cheia, e os `<svg>` a partir da descrição textual do diagrama.

**Construir:**
- Módulo `renderer/` no backend (ou serviço separado) que gera o HTML final.
- Reaproveitar o esqueleto de CSS/JS já validado nos arquivos de `exercicios/` — é a mesma engenharia, só parametrizada por tema.

**Teste [OK quando]:** rodar o renderizador com o JSON do Tópico 4 (convertido na Fase 0) nos 4 temas, e o resultado precisa funcionar igual ao HTML original — slides navegando, gate bloqueando até responder, áudio lendo, resumo final montando corretamente.

---

## Fase 2 — Especialista de IA estruturado, por área
**Status: [OK, com ressalva documentada]** — 2026-08-11. Artefatos: `backend/app/agents/specialists/ia_agent.py`, `backend/app/renderer/validate.py` (checagem determinística, nasceu direto de um problema real encontrado aqui), `backend/_test_gerar_topico6.py` (script de teste ponta a ponta).

**Teste real, ao vivo, via Groq (llama-3.3-70b-versatile)** — gerou o Tópico 6 (Aplicação no agente, que não existia em `Estudo IA/`) 3 vezes, revisando e ajustando o prompt entre cada rodada:
- **Rodada 1**: estrutura válida, mas conteúdo genérico e circular ("o agente usa IA pra responder mensagens" repetido), ignorou o foco pedido, sem analogia, diagrama vazio, `ck3`/`ef4` com enunciado idêntico, e inventou um "Tópico 7" que não existe.
- **Rodada 2** (prompt com exemplo de calibração + regra de não-duplicar + próximo tópico travado por código, não pela IA): nomeou tool concreta (`check_stock`), referenciou Tópicos 4 e 5 de verdade, diagrama virou fluxo de 3 passos — mas `ck1`/`ef1` duplicaram (a mesma pergunta que eu tinha "consertado" em outro par reapareceu duplicada num par diferente).
- **Rodada 3** (regra de duplicidade generalizada pra qualquer par, não só ck3/ef4): `ck1`/`ef1` pararam de duplicar, mas `ck2`/`ef4` duplicaram — **o mesmo problema, deslocado, não eliminado**.

**Conclusão honesta**: um prompt sozinho, por melhor que seja, não evita de forma confiável que o modelo repita uma pergunta em rodadas diferentes — é uma limitação real de geração em uma única passada, não falta de instrução. A solução correta não é continuar ajustando o prompt indefinidamente — é ter uma checagem determinística depois da geração. Por isso criei `validate.py` agora (não esperei a Fase 5): ele varre o JSON e pega enunciados duplicados, `gate_id`/`id` repetidos, diagrama sem narrativa de fluxo, e checkpoint sem pergunta. Rodado contra a Rodada 3, pegou a duplicata `ck2`/`ef4` corretamente.

**Decisão inicial**: Fase 2 marcada OK porque a capacidade central (especialista gera o schema válido, com voz e profundidade adequadas, nomeando mecanismos reais) está comprovada. A ressalva — duplicidade ocasional — fica formalmente delegada à Fase 5: o Reviewer Agent deve rodar `validate.py` e, se pegar problema, mandar de volta pro Specialist com o problema apontado (loop gerar → validar → regenerar se necessário), não confiar em uma geração única.

### Revisão da Fase 2 — separação em ContentAgent + QuizAgent (mesmo dia, a pedido do usuário)

O usuário questionou o design de agente único (fazer conteúdo + perguntas numa chamada só) e propôs a separação que o próprio README do NIA já sugeria: um agente por responsabilidade. Reestruturado:

- **`ContentAgent`** (`specialists/ia_agent.py`, renomeado de `IASpecialistAgent`) — escreve só os slides de ensino, sem nenhuma pergunta. Marca `checkpoint_apos` (o quê testar, não a pergunta em si) e `avaliacao_conceitos` (5 itens, o que cada um deve verificar).
- **`QuizAgent`** (`quiz_agent.py`, reescrito do zero — a versão antiga gerava texto solto sem gabarito) — lê o JSON de conteúdo pronto e escreve as perguntas de verdade em cima dele.
- **`montar_topico.py`** (novo, código puro sem IA) — junta os dois JSONs no tópico final. Aqui, e não pedindo pra IA, ficam: o texto padrão da intro de avaliação, o título do slide de resultado, e o cálculo do número de checkpoints pro badge (o bug de contagem errada da rodada 2 fica estruturalmente impossível agora — é `len()`, não a IA "lembrando" de contar certo).

**Bug novo encontrado nesta rodada**: o QuizAgent (ambos os serviços, mesmo com exemplo explícito no prompt) esqueceu o campo `"tipo"` em toda pergunta gerada — o dado categorizador tava implícito nas chaves do dict (`checkpoints.ck1`), então a IA claramente inferiu que já tinha "dito" o tipo e não repetiu dentro do objeto. Corrigido em duas camadas: prompt mais explícito ("tipo" é uma chave de verdade dentro do objeto) + `_inferir_tipo_pergunta()` em `montar_topico.py`, que deduz o tipo pelos campos presentes se a IA esquecer de novo — rede de segurança em código, não só instrução.

**Resultado da rodada com os dois agentes separados** (Tópico 6, mesmo tema/nível/foco de antes): `validate.py` passou limpo (zero problemas, incluindo zero duplicidade — a melhora que motivou a separação funcionou). Também achei e corrigi, nesta rodada, um **bug no próprio `validate.py`**: a checagem de diagrama contava "quantos tipos de conector existem no texto" em vez de "quantas setas de fluxo existem" — um diagrama genuinamente bom com 3 setas (`cliente → orquestrador → tool → resposta`) tomava só 1 ponto e era sinalizado como fraco por engano. Corrigido pra contar ocorrências de verdade.

**O que ainda não está perfeito** (fica pro Fase 5, que precisa de julgamento semântico, não só estrutural — string-matching não pega isso):
- Uma referência de continuidade errada: o conteúdo disse "lembra do Tópico 3, onde aprendemos sobre tokenização" — tokenização foi Tópico 2, Tópico 3 foi Context Window. Erro factual sobre o próprio curso.
- `ck3` e `ef4` (ambas abertas) pedem essencialmente a mesma coisa ("descreva a visão de arquitetura...") com palavras diferentes — não é uma duplicata literal (por isso `validate.py` não pegou), é uma duplicata de *ideia*. Só um revisor com juízo semântico (IA) pega isso, não checagem de string.
- A analogia do "vendedor lido" foi reciclada do Tópico 1, mas aplicada de forma rasa — não conecta com o ponto específico deste tópico (como o agente compensa a limitação do vendedor).

**Decisão final**: Fase 2 permanece **[OK]**, arquitetura corrigida pra 2 agentes especializados (confirmadamente melhor — zero duplicidade estrutural nesta rodada, vs. 3 rodadas seguidas com duplicidade no agente único). As 3 lacunas acima são qualidade semântica, não estrutura — é exatamente o escopo que a Fase 5 (Reviewer com IA) existe pra cobrir.

O que já existe: `specialist_agent.py` — mas devolve Markdown solto e é genérico pra qualquer assunto (bug identificado: `generate_lesson_content` tem um `if/else` nas linhas 138-145 que faz a mesma coisa nos dois ramos).
O que falta: agentes por área (começando por IA/LLM), com o fio condutor da área embutido no prompt, devolvendo o schema da Fase 0 (não Markdown).

**Construir:**
- `backend/app/agents/specialists/ia_agent.py` — prompt carrega o fio condutor (LLM é só camada de linguagem, fatos vêm de tools/grounding) e o padrão de seções.
- Corrigir o bug do `generate_lesson_content` original ou substituir de vez por este.

**Teste [OK quando]:** gerar o Tópico 6 (Aplicação no agente — ainda não existe em `Estudo IA/`) com esse agente, revisar manualmente o JSON gerado, e confirmar que segue o mesmo padrão pedagógico dos Tópicos 1-5 feitos à mão.

---

## Fase 3 — Estrutura de curso variável por assunto e por nível
**Status: [ ]**

**Observação registrada (2026-08-11):** o curso não pode ficar preso a sempre seguir o mesmo padrão de slides (capa → definição → analogia → checkpoint → ... → avaliação). Duas variações precisam ser possíveis, não só a quantidade de tópicos:
- **Por assunto**: já coberto pela ideia original desta fase.
- **Por nível** (`básico` / `intermediário` / `avançado` / `especialista`): um curso básico pode não precisar de 3 checkpoints + 5 perguntas de avaliação por tópico; um "especialista" pode precisar de mais profundidade ou menos guia passo a passo. Isso não é só volume de conteúdo — pode mudar quais tipos de bloco/slide fazem sentido usar.
- O schema da Fase 0 já não obriga um padrão fixo (`slides` é uma lista aberta) — isso ajuda, mas a lógica de **quando usar o quê** por nível ainda não existe em nenhum agente.
- **Confirmado com o usuário: não precisa estar pronto na primeira versão, mas precisa estar no escopo** — não pode ser esquecido nem exigir redesenho do schema depois.

**Status: [OK]** — 2026-08-11. Artefato: `backend/app/agents/estrutura_agent.py` (`EstruturaAgent.gerar_estrutura(assunto, nivel, objetivo)`), testado com `backend/_test_estrutura.py`.

**Teste real**: gerei a estrutura de 3 cursos — mesmo assunto (LLM aplicado ao Garden Center) em nível básico vs. especialista, e um assunto totalmente diferente (marketing digital) em nível básico. Nenhum número travado no prompt desta vez (removi o `Gere {3} módulos com {3} aulas cada` hardcoded do agente antigo). Resultado:

| Curso | Módulos | Tópicos |
|---|---|---|
| LLM · básico | 4 | 9 |
| LLM · especialista (mesmo assunto, nível diferente) | 3 | 6 |
| Marketing digital · básico (assunto diferente) | 4 | 11 |

Confirma as duas dimensões pedidas: nível muda a quantidade (especialista teve menos módulos/tópicos que básico, mesmo assunto) e assunto muda a quantidade (marketing teve mais tópicos que LLM, mesmo nível). Rodei o caso "LLM básico" duas vezes (um rate limit da Groq forçou repetir) e os números saíram diferentes entre as rodadas (12 tópicos numa, 9 na outra) — não é bug, é a IA decidindo de verdade a cada geração, não repetindo um valor decorado.

Ainda não implementado (fica pra Fase 7): tela/endpoint pra revisar a lista de tópicos propostos antes de mandar gerar o conteúdo de cada um — hoje o teste só gera e imprime, não tem esse passo de revisão humana no meio.

O que já existe: `generate_course_structure` já gera módulos/aulas dinamicamente por `topic`/`level`/`goal`; o banco (`Module.lessons_count`, `Course.structure` JSONB) já aceita qualquer número. Não tem nada fixo em "6 tópicos" hoje.
O que falta: o prompt de estrutura ainda pede um número fixo de módulos/aulas (`Gere {3} módulos com {3} aulas cada` — hardcoded). Precisa decidir a quantidade certa baseado na complexidade do assunto, e permitir o usuário revisar/editar a lista antes de gerar conteúdo.

**Construir:**
- Tirar o hardcode `{3}`/`{3}` do prompt — deixar a IA propor a quantidade adequada ao assunto/nível, com um mínimo/máximo razoável.
- Tela ou endpoint simples pra revisar a lista de tópicos propostos antes de disparar a geração de conteúdo de cada um.

**Teste [OK quando]:** gerar a estrutura de dois cursos bem diferentes (ex: "Fundamentos de LLM" e outro assunto qualquer) e confirmar que o número de tópicos muda de forma sensata pra cada um, não fica travado em 6.

---

## Fase 4 — Seletor de tema integrado
**Status: [OK]** — 2026-08-11.

Depende da Fase 0 (catálogo de temas) e Fase 1 (renderizador aceitar tema como parâmetro).

**Construído:**
- `backend/app/routers/lessons.py` (novo router, registrado em `main.py`) — CRUD de `Lesson` (guarda o JSON estruturado como texto) + `GET /lessons/{id}/render?theme=...&user_id=...` (tema explícito > `User.preferred_theme` > `"vidro-fume"` padrão) + `GET /lessons/temas/catalogo` (pro frontend montar o seletor a partir de `temas.json`, sem duplicar a lista).
- Gravar a escolha: **não precisou de endpoint novo** — `PUT /users/{id}` já aceita qualquer campo (incluindo `preferred_theme`, adicionado na Fase 0) porque os endpoints existentes do NIA já são genéricos (`setattr` em cima de um dict).

**Teste realizado** (`backend/_test_seletor_tema.py`, roda sem precisar do servidor de pé): carreguei o JSON do Tópico 6 **uma única vez** e chamei `render_topico()` 4 vezes trocando só o `theme_id`, com `assert id(content) == content_id_antes` confirmando que é o mesmo objeto Python o tempo todo — nenhuma regeneração. As 4 saídas têm `--bg` diferente (confirma que o tema realmente mudou o resultado) com tamanho de HTML muito próximo entre si (confirma que é o mesmo conteúdo, só a casca visual muda).

**Descoberta importante nesta fase**: o stack Docker do NIA (`nia_backend` + `nia_db`) já estava **rodando de verdade** (25h up) quando cheguei nesta fase — não é só um projeto parado. `docker-compose.yml` monta `./backend:/app` como volume, então os arquivos novos já estão visíveis dentro do container sem rebuild. Duas coisas, porém, **não** foram aplicadas no container ao vivo (decisão consciente — não mexi num serviço já rodando sem confirmar antes):
1. `jinja2` (adicionado ao `requirements.txt` na Fase 1) provavelmente não está instalado no ambiente Python *dentro* do container, só no meu venv de teste local — precisaria reinstalar dependências ou reconstruir a imagem.
2. `User.preferred_theme` existe no `models.py`, mas como não há Alembic (só `create_all()`, que não altera tabela já existente), a coluna não existe de fato no Postgres que já está rodando há 25h — precisaria de um `ALTER TABLE` manual ou recriar o banco.

Preferi confirmar com o usuário antes de reiniciar/alterar um serviço que já está no ar em vez de fazer isso sem avisar.

---

## Fase 5 — Reviewer com checklist de cobertura
**Status: [OK]**

O que existia antes: `reviewer_agent.py` só reescrevia texto "mais didático" — não verificava cobertura nem corretude, e nunca reprovava nada.

**O que foi construído:** `ReviewerAgent.revisar_topico()` reescrito do zero, em duas camadas:
1. **Estrutural (sem IA)** — roda `validate.py` primeiro. Se achar qualquer problema estrutural, reprova na hora (`score: 0.0, aprovado: false, camada: "estrutural (validate.py, sem IA)"`) sem gastar nenhuma chamada de IA.
2. **Semântica (IA)** — só roda se a camada 1 passou limpo. Prompt (`SCHEMA_REVISAO`) pede JSON com `score`, `aprovado`, `pontos_fortes`, `problemas` (cada um com `gravidade`: bloqueante/leve, `onde`, `descricao`). Verifica 6 pontos que checagem de string não pega: fio condutor da área, continuidade com tópicos anteriores, cobertura do foco obrigatório, duplicidade semântica entre perguntas (ideia repetida, não string igual), conteúdo genérico demais, gabarito ambíguo/questionável. `aprovado` só pode ser `true` com `score >= 7` E zero problemas bloqueantes.
3. `_resumir_para_revisao()` remove `svg_raw` do JSON antes de mandar pra IA — reduz tokens sem perder nada relevante pro julgamento semântico.

**Teste realizado (mockado, `_test_reviewer.py`, sem chamar API — quota diária da Groq ainda esgotada no momento do teste):**
- Cenário 1: tópico com checkpoint sem perguntas + sem diagrama → reprovado na camada estrutural, confirmado que a IA (`FakeServiceQuebraSeChamado`, que derruba o teste se `generate_json` for chamado) **nunca foi acionada** — prova que o curto-circuito economiza quota de verdade.
- Cenário 2: tópico estruturalmente limpo mas semanticamente fraco (sem aplicação prática + gabarito questionável, exatamente o critério do teste original) → IA mockada reprova com `score: 4.5` e os 2 problemas bloqueantes aparecem corretos no resultado.
- Cenário 3: tópico bom → aprovado com `score: 8.5`.

Todos os 3 cenários passaram. Nenhum bug encontrado nesta fase — a única correção foi de processo (`py_compile` rodado antes do teste, sem erro).

**Pendente (não bloqueia o [OK]):** reverificação com IA real assim que a quota da Groq resetar, pra confirmar que o modelo de fato segue o formato `SCHEMA_REVISAO` na prática (o mock prova que o *código* lida certo com qualquer resposta bem-formada; não prova que o Groq sempre devolve bem-formado — mesmo tipo de risco já visto e mitigado no Modo Pro).

**Atualização (teste real na Fase 7):** verificado com Gemini real (Groq seguia esgotada) — o Reviewer pegou, na prática, exatamente os 2 tipos de problema que a checagem semântica foi desenhada pra achar: uma alucinação de continuidade (referência a um tópico que não existe) e duplicidade semântica entre perguntas com palavras diferentes. Formato `SCHEMA_REVISAO` seguido corretamente pelo Gemini. Reteste específico com Groq (o provider usado em todo o resto do desenvolvimento) segue pendente.

---

## Fase 6 — Tutor Agent (avaliação + reforço personalizado)
**Status: [OK]**

O que existia antes: campo `Progress.tutor_analysis` (JSONB) no banco, pronto pra receber isso — mas `tutor_agent.py` não existia no código.

**O que foi construído:** `backend/app/agents/tutor_agent.py` — `TutorAgent.avaliar_resumo(resumo_texto, contexto_topico="", historico_reforcos="")`. Entrada é o texto CRU do "=== RESUMO ===" que o template já monta (`buildSummary()` em `topico.html.j2`) — a IA lê exatamente como leria colado no chat, sem o front precisar parsear nada antes. Saída (`SCHEMA_AVALIACAO`): `veredito` (dominado/reforco), `resumo_diagnostico`, `pontos_fortes`, `lacunas` (cada uma com `tema`, `evidencia` citando o item exato do resumo, `gravidade` superficial/real), `reforco_sugerido` (`necessario`, `foco`, `instrucao_para_gerar` — uma instrução pra quem for gerar o material de reforço, nunca o material em si, e proibida de pedir repetição da explicação original). Critério de veredito: só "dominado" sem nenhuma lacuna "real"; erro isolado com confiança baixa/média conta como "superficial" e não bloqueia. Reusa `FIO_CONDUTOR_IA` de `specialists/shared.py`.

**Teste realizado (mockado, `_test_tutor.py`, sem chamar API — quota diária da Groq ainda esgotada):**
- Cenário 1: resumo reconstruído a partir do que está documentado em `Estudo IA/progresso.md` pro Tópico 4 ANTES do reforço (2 erros de classificação temperatura baixa/alta com confiança alta + confusão repetida na resposta aberta + exemplo emprestado do Tópico 2) → IA mockada com o veredito que uma avaliação honesta deveria dar → `veredito: "reforco"`, bate com a decisão manual real registrada no histórico.
- Cenário 2: resumo da reaplicação PÓS-reforço (5/5, exemplos já usando o critério certo) → `veredito: "dominado"`, bate com "Liberado como dominado" registrado no histórico.
- Confirmado por asserção que o resumo colado e o contexto/histórico passados realmente chegam no prompt enviado à IA.

**Ressalva importante (mesma da Fase 5):** o mock prova que o *código* monta o prompt certo e repassa o veredito estruturado sem alterar nada — não prova que o Groq de fato raciocina certo sobre um resumo real. Não havia um resumo colado literal da sessão original salvo em lugar nenhum (só o registro estruturado do que aconteceu em `progresso.md`), então o texto de teste é uma reconstrução fiel aos fatos documentados, não uma cópia do original. Reteste com IA real fica pendente pra quando a quota resetar.

**Fora de escopo aqui (mantido assim de propósito):** o agente não gera o material de reforço em si (o HTML/SVG do slide deck de reforço) — só decide se precisa e dá a instrução de foco. Geração do material visual continua um passo separado, consistente com o fluxo documentado no CLAUDE.md de Estudo IA.

**Atualização (teste real na Fase 7):** verificado com Gemini real — dado um resumo bem respondido (6/6 objetiva, 3/3 abertas coerentes usando o critério certo), devolveu `veredito: "dominado"` com diagnóstico específico citando os itens certos (`ck3_1`, `ef4_1`, `ef5_1`), sem elogio genérico. `Progress.can_advance` virou `true` no banco corretamente. Reteste com resumo fraco (pra ver reprovação com IA real, não só mockada) e reteste específico com Groq seguem pendentes.

---

## Fase 7 — Integração ponta a ponta
**Status: [OK] — testado mockado E com container/Postgres/IA reais (ver detalhes abaixo)**

**O que foi construído:**
- `backend/app/agents/pipeline.py` — orquestração pura (sem banco, sem HTTP), liga as Fases 0-6:
  - `gerar_estrutura_curso()`: chama o `EstruturaAgent` (Fase 3).
  - `gerar_e_revisar_topico()`: gera 1 tópico (`ContentAgent`, modo comum ou pro — Fase 2/2b) → `QuizAgent` → `montar_topico()` → `ReviewerAgent.revisar_topico()` (Fase 5), tudo num só passo. Sobrescreve `topico_id`/`aula`/`numero` depois da geração — mesma trava determinística já usada pra `proximo_topico_label`, não confia na IA pra identificadores que o banco já sabe.
- `backend/app/routers/pipeline.py` — glue de banco/HTTP em cima disso, nas duas frentes combinadas:
  - **Admin**: `POST /pipeline/cursos` (estrutura variável → salva Course+Module+Lesson, todas as lições com `is_approved=False`); `POST /pipeline/licoes/{id}/gerar` (gera+revisa 1 lição por vez — `modo: "comum"|"pro"` escolhido por request; só marca `is_approved=True` se o Reviewer aprovar; se reprovar, guarda o feedback em `Lesson.review_feedback` e devolve os problemas, sem tentar de novo sozinho — evita gastar chamada de IA numa causa que pode precisar ajuste manual de foco).
  - **Aluno**: `POST /pipeline/licoes/{id}/avaliar` (cola o resumo → `TutorAgent` decide → `Progress.tutor_analysis` guarda o histórico completo de avaliações, `Progress.can_advance` só fica `True` com veredito "dominado"). Estudo em si continua em `GET /lessons/{id}/render` (Fase 4, já existia).
  - Contexto de continuidade entre tópicos (`contexto_topicos_anteriores`) é montado a partir das lições já **aprovadas** no curso, não das geradas — o aluno vê o que já foi validado, e a IA só referencia tópicos que realmente passaram pela revisão.
  - `foco` de cada lição vem de `Course.structure` (JSON já salvo na Fase 3) — não criou coluna nova só pra isso.
  - Registrado em `main.py` (`app.include_router(pipeline.router)`).

**Teste realizado (mockado, `_test_pipeline_e2e.py`, sem banco e sem API real):** curso pequeno de 1 módulo / 2 tópicos, ponta a ponta:
1. `EstruturaAgent` gera a estrutura (2 tópicos).
2. Tópico 1 gerado (modo comum) + revisado → aprovado; confirmado que `topico_id`/`aula`/`numero` saem sobrescritos com os valores do banco, não os que a IA escreveu.
3. Tutor avalia um resumo bom do Tópico 1 → "dominado".
4. Tópico 2 gerado passando o Tópico 1 como `contexto_topicos_anteriores` → aprovado; **confirmado por asserção que o texto de continuidade chegou tanto no prompt do ContentAgent quanto no do Reviewer**.
5. Tutor avalia o resumo do Tópico 2 → "dominado" → ciclo dos 2 tópicos completo, zero passo manual.
6. Cenário extra: tópico sem diagrama → Reviewer reprova na camada estrutural, confirmado por asserção que a chamada semântica de IA (3ª chamada) **nunca foi feita** — a rota fica pronta pra devolver o feedback pro admin sem desperdiçar quota.

Todos os 6 passos/asserções passaram. Nenhum bug encontrado na orquestração.

**Atualização — verificação real feita (container + Postgres + IA de verdade, não mockada):**

Container atualizado: `jinja2` instalado (rebuild da imagem, já vem de `requirements.txt` agora), `docker-compose.yml` ganhou o volume `./docs:/docs` (o renderizador lê `docs/schema/temas.json` fora de `backend/`, e só `./backend:/app` estava montado — sem isso o container não achava os temas), coluna `users.preferred_theme` aplicada via `ALTER TABLE` (sem Alembic, como já era o padrão do projeto). `nia_db` foi recriado junto pelo `docker compose up --build`, mas os dados sobreviveram porque `pgdata` é volume nomeado, não bind mount — confirmado com `\dt` antes/depois.

**3 bugs reais encontrados e corrigidos** (nenhum deles aparecia nos testes mockados — só apareceram rodando contra API/DB de verdade, exatamente o motivo de fazer esse teste):
1. `backend/requirements.txt` ainda estava UTF-16 no disco (o registro de uma sessão anterior dizia que isso já tinha sido corrigido, mas a correção não persistiu) — build da imagem quebrava com `UnicodeDecodeError` no `pip install`. Reescrito limpo em UTF-8.
2. `Course.level` tinha `CHECK` constraint travado em inglês (`'basic','intermediate','advanced'`, resquício do fluxo antigo/`specialist_agent.py`), mas o `EstruturaAgent` (Fase 3) — a fonte de verdade agora — produz `"básico"|"intermediário"|"avançado"|"especialista"`. Toda tentativa de criar curso pelo pipeline novo quebrava com `CheckViolation`. Corrigido o `CheckConstraint` em `models.py` e recriada a constraint no banco (1 curso legado com `level='basic'` foi normalizado pra `'básico'`, não apagado).
3. `GeminiService.generate_json()`/`GroqService.generate_json()` usavam `max_tokens=4000` fixo, sem repassar de fora. Um tópico completo em modo "comum" (schema inteiro numa chamada só) fica perto de 3000-3500 tokens de saída — com o Gemini, isso cortou o JSON no meio (`"Resposta não é JSON válido"` era na real JSON truncado, não markdown sobrando). Subido o default pra 8000 nos dois services.

**Teste real executado** (curso pequeno, assunto "Grounding: por que o preço nunca pode vir do modelo", nível básico, `course_id=4`), via HTTP contra o container e o Postgres de verdade:
- `POST /pipeline/cursos` → `EstruturaAgent` real (Groq) gerou 3 módulos / 6 tópicos, salvos no banco.
- `POST /pipeline/licoes/10/gerar` (modo comum): a Groq bateu no limite diário de novo no meio do teste (rate limit real, esperado) → trocado pra `modelo:"gemini"` no meio do teste, sem mudar nada no código (confirma que o parâmetro `modelo` da rota funciona de verdade). 3 tentativas reais, todas informativas:
  - Tentativa 1: reprovado na **camada estrutural** — `QuizAgent` esqueceu de escrever pergunta pro `ck3` que o `ContentAgent` tinha marcado. `montar_topico.py` não quebrou (usa `.get(gate_id, [])`), `validate.py` pegou ("Checkpoint 'ck3' sem perguntas"), `is_approved` ficou `False`, feedback salvo em `Lesson.review_feedback` — comportamento exatamente como desenhado.
  - Tentativa 2: passou pela estrutura, reprovado na **camada semântica** — o `ContentAgent` alucinou uma referência a um "Tópico 4 de Fundamentos" que não existe (era o primeiro tópico do curso). O `Reviewer` pegou exatamente esse tipo de erro (checagem "Continuidade", desenhada na Fase 5 pra isso) + 2 duplicidades semânticas leves entre perguntas. Prova real de que a camada semântica funciona pro que foi construída pra pegar.
  - Tentativa 3: aprovado (score 9, 1 problema leve não-bloqueante) → `Lesson.is_approved=True`, `Lesson.content` salvo, `Lesson.estimated_read_time_minutes=14`.
- `GET /lessons/10/render?theme=vidro-fume` → 200 OK, HTML de ~51KB, renderizou o conteúdo real gerado (não um fixture) sem erro.
- `POST /pipeline/licoes/10/avaliar` (usuário de teste criado, `user_id=1`) com um resumo bem respondido → Tutor (Gemini) devolveu `veredito: "dominado"` → `Progress` criado no banco com `can_advance=true`, `current_lesson_index=2`, `status='in_progress'`.

Ciclo completo confirmado ponta a ponta com infraestrutura real: estrutura → conteúdo → revisão (nos 2 modos de reprovação E aprovação) → renderização → avaliação do tutor → progresso salvo. `course_id=4` e `user_id=1` ficam no banco como dados de teste (não apagados, é dev).

**Ainda pendente (não bloqueia o [OK], baixo risco):** o modo "pro" e o fluxo com Groq não foram reverificados com IA real nesta rodada (Groq voltou a bater o limite diário durante o teste); a lógica é idêntica à do modo comum já testada mockada e realmente pela Fase 2b, e o parâmetro `modelo` já provou funcionar trocando pra Gemini no meio do teste.

---

## Fase 2b — Modo "Pro" (geração assunto por assunto)
**Status: [OK]** — 2026-08-11. A pedido do usuário: admin poder escolher entre modo **Comum** (1 chamada de IA gera o tópico inteiro — `ContentAgent.generate_conteudo`, já existia) e modo **Pro** (uma chamada de IA por assunto dentro do tópico — `ContentAgent.generate_conteudo_pro`, novo). As duas saídas têm exatamente o mesmo formato, então `QuizAgent`/`montar_topico`/`validate`/`render_topico` não sabem nem precisam saber qual modo gerou o conteúdo.

Como funciona o modo Pro: `gerar_esqueleto_assuntos()` (1 chamada — decide títulos/foco dos assuntos e onde entram checkpoints, sem escrever conteúdo) → `gerar_assunto()` (1 chamada por assunto, cada uma vendo um resumo dos assuntos já escritos nesse mesmo tópico, pra manter costura e não repetir) → mesma montagem de sempre.

**Efeito colateral real e necessário**: mais chamadas de IA por tópico bateu direto no limite de tokens/minuto do tier grátis da Groq (12000 TPM) — aconteceu de novo aqui, não foi só na Fase 3. Resolvido criando `BaseAgent.run_json_com_retry()` (novo, em `base_agent.py`, usado por todos os agentes agora): captura erro 429, lê quantos segundos a própria API pede pra esperar, e tenta de novo (até 3x). Isso não é só pro modo Pro — deixa qualquer agente mais resistente a rate limit, geral.

**Comparação real, mesmo Tópico 6, mesmo foco pedido:**

| | Comum (1 chamada) | Pro (5 chamadas, 1 por assunto) |
|---|---|---|
| Analogia | reciclou "vendedor lido" de forma rasa, sem conectar ao ponto do tópico | analogia **nova e melhor** ("orquestrador = maestro regendo orquestra") |
| Blocos por assunto | tipicamente 2 (parágrafo + 1 box) | tipicamente 4-5 (parágrafo + def + analogia/app + cols2 + timeline) |
| `validate.py` | limpo | limpo (depois da correção abaixo) |
| Duração estimada | 15 min (razoável) | **60 min — exagerado**, a IA não recebeu faixa de referência nesse modo |
| Diagrama | presente | **nenhum assunto usou diagrama** — o modo Pro não força isso como o modo Comum força |
| Tipos de pergunta nos checkpoints | mix de mc/tf/classify/open | **as 3 perguntas de checkpoint saíram todas "open"** — desbalanceado, mais digitação pro aluno que o padrão dos Tópicos 1-5 |

**Bug novo encontrado e corrigido**: os itens de `timeline` saíram com `"cor": "azul"/"verde"/"amarelo"` (palavras, não hex) — `style="background:azul"` é CSS inválido, a cor simplesmente não aparece. `validate.py` não pegava isso antes (JSON estruturalmente válido, só visualmente quebrado). Corrigido em duas camadas, de novo: prompt explícito ("cor" tem que ser hex tipo `#2c7fb8`, nunca nome) + checagem nova em `validate.py` que rejeita qualquer `cor` fora do padrão hex.

**Conclusão honesta**: modo Pro entrega conteúdo visivelmente mais rico (confirma a hipótese), mas tinha 3 lacunas de calibração que o modo Comum não tinha (duração, ausência de diagrama, perguntas de checkpoint todas abertas) — nenhuma era bug estrutural, eram faltas de instrução no prompt do esqueleto/assunto.

**As 3 correções foram feitas em duas camadas** (prompt + código, não só prompt — mesmo padrão do resto do projeto):
- Prompt: `duracao_estimada_min` travado em 10-20 na instrução; `precisa_diagrama` (exatamente 1 assunto marcado true) propagado até `gerar_assunto`, que exige o bloco quando marcado; `checkpoint_apos` ganhou um campo `"tipo"` que o `QuizAgent` agora é instruído a respeitar, não escolher livremente.
- Código (rede de segurança, pro caso a IA ignore a instrução de novo): `montar_topico.py` agora tem `duracao = max(10, min(20, ...))` (clamp determinístico) e carrega `tipo_esperado` no slide de checkpoint; `validate.py` ganhou 2 checagens novas — tipo da pergunta bate com `tipo_esperado`, e existe pelo menos 1 bloco `diagrama` em algum lugar do tópico.

**Verificado sem chamar API nenhuma** (`backend/_test_mock_pipeline.py`, um `FakeService` devolve respostas pré-escritas simulando o pipeline inteiro): cenário com IA "bem-comportada" passa limpo; cenário simulando a IA repetindo os 3 bugs originais de propósito confirma que a duração é corrigida sozinha (60→20, nem vira "problema") e que `validate.py` pega os outros 2 (diagrama ausente, tipo de pergunta divergente). Reteste com a API de verdade (Groq) fica pendente até o limite diário liberar — o teste mockado cobre a lógica, não substitui confirmar a qualidade real do texto gerado.

## Ordem recomendada

0 → 1 → 2 seguem em sequência (cada uma depende da anterior). 3 e 4 podem ser feitas em paralelo depois da 2. 5 e 6 podem ser feitas em paralelo depois da 0. 7 é sempre por último.

---

## Backlog (fora do escopo atual — só registrado, não implementar ainda)

- **Geração de imagens de exemplo via API**: quem está criando o curso escreve uma descrição e escolhe entre imagens geradas por IA pra ilustrar o tópico (diferente dos diagramas SVG da Fase 1, que são sempre gerados por código). Precisa decidir qual API de geração de imagem usar e como isso entra no schema da Fase 0.
- **Vídeos**: duas direções possíveis, nenhuma decidida — (a) puxar vídeos existentes da internet, mas esbarra em direito de imagem/uso; (b) gerar vídeo via IA. Nenhuma das duas está madura o bastante pra entrar nas fases atuais — fica registrado pra revisitar depois que o pipeline de texto+diagrama (Fases 0-7) estiver funcionando ponta a ponta.
