- Tópico 1: Sacerdócio de Todos os Crentes — 1Pe 2:9
- Tópico 2: Dons Espirituais — Rm 12:6-8 (lista os dons de verdade, referência diferente da atual)
- Tópico 3: Vocação e Ofícios — Ef 4:11-12
- Tópico 4: Função no Corpo de Cristo — 1Co 12:12-27 (passagem mais longa, "o corpo tem muitos membros")
- Tópico 5: Integração dos Três — síntese, sem referência nova obrigatória

Quantas vezes cada agente chama a IA (1 tópico, modo pro)

Agente: ContentAgent
Método: gerar_esqueleto_assuntos()
Chamadas: 1
Por quê: Decide em quantos "assuntos" o tópico se divide (título, foco, quem leva diagrama/checkpoint) —
ainda sem escrever conteúdo
────────────────────────────────────────
Agente: ContentAgent
Método: gerar_assunto() (loop)
Chamadas: N (normalmente 5-9)
Por quê: 1 chamada por assunto — cada uma inclui fio_condutor + exemplo_calibracao do perfil + o texto
bíblico real (texto_biblico_base) + resumo dos assuntos já escritos, pra não repetir
────────────────────────────────────────
Agente: QuizAgent
Método: generate_perguntas()
Chamadas: 1
Por quê: Vê o conteúdo inteiro já pronto (todos os assuntos juntos) e escreve todas as perguntas (checkpoints

- avaliação) numa passada só
  ────────────────────────────────────────
  Agente: ReviewerAgent
  Método: validate.py
  Chamadas: 0
  Por quê: Checagem estrutural determinística (sem IA), roda sempre primeiro
  ────────────────────────────────────────
  Agente: ReviewerAgent
  Método: validate.py
  Chamadas: 0
  Por quê: Checagem estrutural determinística (sem IA), roda sempre primeiro
  ────────────────────────────────────────
  Agente: ReviewerAgent
  Método: revisão semântica
  Chamadas: 1 (só se o estrutural passar)
  Por quê: Julga fio condutor, continuidade, duplicidade, gabarito
  ────────────────────────────────────────
  Agente: ReviewerAgent
  Método: revisão semântica
  Chamadas: 1 (só se o estrutural passar)
  Por quê: Julga fio condutor, continuidade, duplicidade, gabarito
  ────────────────────────────────────────
  Agente: Total num sucesso
  Método:
  Chamadas: ~8-12
  Por quê: 1 esqueleto + 5-9 assuntos + 1 quiz + 1 revisão
  ────────────────────────────────────────
  Agente: Total num sucesso
  Método:
  Chamadas: ~8-12
  Por quê: 1 esqueleto + 5-9 assuntos + 1 quiz + 1 revisão

O que sabemos que aconteceu hoje de verdade

Tentativa: Groq
Chamadas confirmadas: não sei precisar — ver abaixo
Onde travou: 20 min de silêncio total é compatível com travar já na 1ª chamada (gerar_esqueleto_assuntos): o
retry aninhado (4× do GroqService dentro de 3× do BaseAgent) sozinho pode consumir até ~30 min numa única
chamada lógica se cada tentativa bate rate limit
────────────────────────────────────────
Tentativa: Gemini
Chamadas confirmadas: exatamente 1 (confirmado no código: BaseAgent só re-tenta em erro 429/rate_limit; um
504 propaga na hora, sem retry)
Onde travou: 1ª chamada (gerar_esqueleto_assuntos), timeout do lado do Google
