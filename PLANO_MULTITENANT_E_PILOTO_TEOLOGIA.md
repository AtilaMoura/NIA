# Plano — Multi-tenant leve + piloto do domínio teológico

Contexto: o usuário vai validar o NIA com **duas frentes reais e simultâneas** — tecnologia/
IA/dados/programação (uso próprio) e teologia bíblica pra uma igreja (fidelidade ao texto,
vida de Jesus, obreiro, diácono, vida de Paulo). Isso substitui a visão anterior de "categoria/
nicho como tag num catálogo único" (`PLANO_IMPLEMENTACAO_FRONTEND.md`, backlog de nicho) —
os dois públicos são incompatíveis demais pra dividir catálogo.

Decisões travadas com o usuário em 2026-08-22 (ver memória `nia-multi-tenant-decisao`,
`nia-prompts-hardcoded-dominio`, `nia-piloto-filipenses`):

- Multi-tenant **leve**, não SaaS completo: entidade `Tenant`, sem billing/self-service —
  só o usuário administra as duas frentes.
- Isolamento total de catálogo por tenant.
- Roteamento por slug no MVP (`nia.app/tech`, `nia.app/igreja`), via função central de
  resolução de tenant (pra trocar por subdomínio depois sem reescrever telas).
- Papel novo `professor`: revisor humano escopado ao tenant, comenta por tópico, aprova.
- Domínio `teologia` exige aprovação humana obrigatória antes de publicar; `tech` mantém
  aprovação automática do Reviewer como já funciona hoje.

---

## Fase 0 — Achado bloqueante + correção (feito nesta sessão)
**Status: [OK]** — 2026-08-22.

Lendo o código (não suposição): `ContentAgent` (`specialists/ia_agent.py`), `ReviewerAgent`
e `TutorAgent` tinham o domínio "LLM aplicado a um agente de vendas via WhatsApp para um
Garden Center" **hardcoded na string do prompt**, independente do `assunto` pedido — bloqueava
literalmente gerar qualquer curso fora de tech. `EstruturaAgent` e `QuizAgent` já eram
genéricos, não precisaram mudar.

**Corrigido**: criado `backend/app/agents/perfis.py` — `PerfilDominio` (dataclass:
`contexto_curso`, `fio_condutor`, `exemplo_calibracao`) com dois perfis: `PERFIL_TECH`
(extraído do que já existia, sem reescrever nada do domínio tech) e `PERFIL_TEOLOGIA` (novo).
Os três agentes agora recebem `perfil: PerfilDominio = PERFIL_TECH` como parâmetro opcional —
comportamento do domínio tech não muda (perfil não é passado em lugar nenhum antigo, usa o
default). `routers/pipeline.py` ganhou um campo `perfil: str = "tech"` em `GerarLicaoRequest`
e `AvaliarResumoRequest`, resolvido por `resolver_perfil()`.

Isto é a versão MVP do `domain_profile` que a tabela `Tenant` vai carregar na Fase T0 do plano
multi-tenant (abaixo) — quando essa fase acontecer, os dois perfis migram de constante Python
pra linha de banco, não é retrabalho.

**Bônus (pedido do usuário)**: novo tipo de bloco `imagem_sugerida` no schema de conteúdo —
texto livre descrevendo uma imagem que ajudaria (ex: mapa de Filipos), **sem gerar imagem
nenhuma**. Instrução explícita pro agente: usar raramente, só quando fizer sentido de verdade,
nunca em todo slide. Renderiza como placeholder visível no HTML (reaproveita CSS `box-instr`
que já existia — nenhum estilo novo).

---

## Fase T0-T6 — Multi-tenant leve (schema, roteamento, login, admin, blocos, `LessonAsset`, polish)
**Status: [ ]** — planejado, não iniciado. Ver detalhe completo na conversa de 2026-08-22 e na
memória `nia-multi-tenant-decisao`. Fica pra depois do piloto abaixo confirmar que o
`PERFIL_TEOLOGIA` produz conteúdo de qualidade — não faz sentido investir em schema de tenant
antes de validar se a geração em si funciona bem pro domínio novo.

**Confirmado como escopo do MVP em 2026-08-26** (curso de obreiro é o segundo piloto do domínio
teologia, ver `curso de obreiro/anotação para IA.md`): T0 (schema `Tenant`) + T1 (roteamento por
slug) + T2 (login real, começando só e-mail/senha — Google fica pra depois, se fizer falta) fazem
parte do MVP pra colocar o curso de obreiro no ar pra igreja do usuário, com uma segunda frente
(igreja pagante) planejada como uma segunda linha `Tenant` no mesmo schema, não redesenho.
**Sequenciamento decidido**: como T0-T2 não bloqueiam gerar mais conteúdo, o usuário priorizou
deixar o backend de geração de conteúdo (ver `PLANO_IMPLEMENTACAO_ESTUDO_IA.md`, Fase 2c) rodando
100% primeiro — multi-tenant e frontend ficam pausados até isso funcionar de ponta a ponta.

**T3 — detalhe confirmado da tabela de comentário/anotação**: em vez do fluxo completo de
aprovação formal por `professor`, o MVP escopa só uma tabela nova e simples, `LessonComment`
(`lesson_id`, `autor`/`user_id`, `referencia_bloco` opcional, `texto`, `resolvido` bool) —
separada do `review_feedback` (que continua sendo só o parecer estruturado do `ReviewerAgent`).
Serve pro caso real do usuário: ele (tech) e um amigo formado em biologia/teologia revisando e
anotando cada tópico do curso de obreiro, com autoria distinguível entre os dois.

---

## Piloto — Curso "Filipenses" (domínio teológico)
**Status: [OK] — primeira lição gerada, aprovada e disponível no painel do aluno (2026-08-22).**

Objetivo: testar o `PERFIL_TEOLOGIA` com uma carta só (não as 13 cartas de Paulo de uma vez —
mais barato de calibrar, menos arriscado como primeiro teste). Escopo pedido pelo usuário:
nível intermediário, cobrindo contexto histórico-cultural de Filipos (por que Paulo esteve lá,
a cultura da época, motivo da carta) + exposição textual próxima, palavra por palavra, do que
Paulo escreveu — pode citar estudiosos como apoio, nunca equiparado ao texto bíblico. Linha
doutrinária: genérico evangélico, sem viés denominacional (decisão explícita do usuário).

**Demo pedida**: gerar a estrutura completa do curso (todos os módulos/tópicos), gerar conteúdo
só do primeiro tópico, e mostrar isso reaproveitando o painel do aluno que já existe (mesmo
fluxo do curso de teste da Fase 7 do backend) — os tópicos sem conteúdo aparecem como "Em
preparação" (estado que já existia, não é feature nova). O usuário vai usar isso pra mostrar
pro professor/revisor da igreja.

**Passos:**
1. [OK] Corrigir o bloqueio de domínio (Fase 0 acima).
2. [OK] Subir os containers (`db`, `backend`) e confirmar que a API responde.
3. [OK] `POST /pipeline/cursos` — curso 6, "Estudo Intermediário da Carta de Paulo aos
   Filipenses", 5 módulos gerados (contexto histórico → exegese caps. 1-2 → exegese
   caps. 3-4 → metodologia/estudiosos → aplicação), 14 lições no total, todas com
   `content=None` esperando geração.
4. [OK] `POST /pipeline/licoes/{id}/gerar` com `perfil="teologia"` — lição 24 (contextual,
   sem referência bíblica no título) e lição 27 (exegese, "Fil 1:1-11") geradas e
   **aprovadas** (score 9 e 10).
5. [OK] Frontend no ar, curso aparece em `/aluno/explorar`, lições 24/27 abrem e renderizam,
   as demais (sem conteúdo gerado ainda) aparecem como "Em preparação" — estado que já
   existia, não precisou de tela nova.

**Achados/bugs reais corrigidos no caminho** (nenhum deles specific do domínio teológico —
todos bloqueavam qualquer geração, inclusive tech):
- `GroqService` usava `llama-3.3-70b-versatile`, modelo **descontinuado** pela Groq — a
  conta não tem mais nenhum Llama 3.x disponível. Trocado pro maior disponível hoje,
  `openai/gpt-oss-120b`.
- Esse modelo é de "raciocínio" — sem `reasoning_effort: "low"` ele gasta parte do
  `max_tokens` "pensando" (campo `reasoning` separado) e pode devolver `content` vazio.
  Adicionado esse parâmetro.
- Tier gratuito da Groq tem teto de 8000 tokens/minuto **por requisição** (prompt +
  `max_tokens` reservado) — `max_tokens=8000` do `generate_json` estourava sozinho.
  Reduzido pra 6000.
- **Achado específico do domínio teológico**: pedir citação bíblica "exata" sem fornecer o
  texto de verdade não funciona — o modelo tenta citar de memória e erra (Reviewer pegou
  isso duas vezes, reprovou certo). Corrigido com grounding real: `backend/app/services/
  biblia_service.py` busca o texto verdadeiro (tradução Almeida, domínio público, via
  bible-api.com) quando o título da lição tem uma referência entre parênteses (ex.: "(Fil
  1:1-11)" — é assim que o `EstruturaAgent` nomeou as lições de exegese) e injeta no prompt
  do `ContentAgent`. Sem referência no título, o fio condutor proíbe citação literal
  (só paráfrase com referência) — mesmo princípio do "fatos vêm de tools, nunca de memória"
  que já existia no domínio tech.
- Frontend rodando em Docker: `page.tsx` (Server Component) roda DENTRO do container e não
  resolve `localhost:8100` (aponta pro próprio container, não pro backend) — precisa do
  hostname da rede Docker (`http://backend:8000`). Corrigido com `API_URL_INTERNAL` novo em
  `docker-compose.yml`, lido só server-side em `app/lib/api.ts`. Exceção: `lessonRenderUrl()`
  sempre usa a URL pública mesmo chamada server-side, porque o resultado vira `src` de um
  `<iframe>` que o NAVEGADOR carrega, não o container.
- **Pegadinha de ambiente pra lembrar em sessões futuras**: depois de mudar env var ou
  arquivo consumido só em runtime, `docker compose up -d frontend` sozinho não bastou —
  o volume anônimo `/app/.next` (cache do Turbopack) ficou servindo bundle antigo mesmo
  com o container "recriado". Só resolveu com `docker compose stop frontend && rm -f
  frontend && up -d frontend` (remove o container de verdade, o que também derruba o
  volume anônimo).

Pendência ainda não resolvida: o usuário mencionou fazer a implementação "com o opencode" e,
perguntado o que significa, respondeu descrevendo a demo em vez de esclarecer a ferramenta —
ainda não está claro se é a CLI OpenCode, outra coisa, ou um lapso de digitação.

**Acesso pra demo**: `http://localhost:4100/aluno/explorar` (curso "Estudo Intermediário da
Carta de Paulo aos Filipenses") ou direto `http://localhost:4100/aluno/licoes/24` (contexto
histórico) / `.../licoes/27` (exegese Fil 1:1-11, com citação bíblica real). Containers
`nia_db`, `nia_backend`, `nia_frontend` precisam estar de pé (`docker compose up -d`).
