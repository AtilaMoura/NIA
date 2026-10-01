# Guia de fontes — o que buscar antes de escrever qualquer tópico

Criado em 2026-10-01 a pedido do Atila: "enriquecer a fonte com livros, artigos, projetos
reais, estudos, pesquisadores, PDFs, especialistas e até exemplos que não deram certo —
deixar a nossa base o mais rica possível de qualquer curso". **A fonte é o diferencial
do curso.** Vale pra todo curso; a lista concreta de cada um fica no fim deste arquivo e
na especificação do curso.

---

## 1. Os 8 tipos de fonte (buscar o máximo de tipos diferentes por tópico)

| Tipo | O que é | Pra que serve no tópico |
|---|---|---|
| **Primária / oficial** | Texto bíblico, RFC, especificação, documentação oficial, paper original | Base de toda afirmação verificável. Sem ela, não escreve |
| **Livro-texto / referência** | Livro usado em curso de graduação ou formação, dicionário, enciclopédia | Explicação didática e ordem lógica do assunto |
| **Artigo / pesquisa** | Artigo acadêmico, estudo, pesquisa com dados | Profundidade e números reais |
| **Especialista** | Pesquisador, professor, autor reconhecido, comentarista | Interpretação, nuance, "como um especialista pensa" |
| **Projeto / caso real** | Projeto, empresa, igreja, implantação que aconteceu de verdade | Exemplo concreto que o aluno reconhece |
| **Caso que deu errado** | Incidente, postmortem, processo judicial, erro histórico documentado | Ensina pelo contraste: o que evitar e por quê |
| **Material didático de instituição** | Apostila, PDF, curso aberto de escola/universidade reconhecida | Sequência pedagógica testada, exercícios |
| **Dado / estatística** | Pesquisa, censo, relatório com número | Dimensão do problema, "quanto", "quão comum" |

**Meta por tópico:** pelo menos 5 dos 8 tipos; toda afirmação central com **1 fonte
primária + 1 independente**; pelo menos 1 caso real e 1 caso que deu errado quando o
assunto permitir.

## 2. Hierarquia de confiança (quando as fontes discordam)

1. Primária/oficial (RFC, spec, texto bíblico, paper original, doc do fabricante)
2. Livro-texto e material de instituição reconhecida
3. Artigo revisado por pares / pesquisa com metodologia
4. Especialista reconhecido (blog, palestra, comentário)
5. Fórum, vídeo, post — **só como pista** pra achar fonte melhor, nunca como base

Divergência real entre fontes de nível alto → o tópico **mostra a divergência** (igual à
nota de neutralidade do obreiro), não escolhe um lado em silêncio.

## 3. Direito autoral

- Domínio público (autor morto há mais de 70 anos, texto antigo): pode citar trecho.
- Material moderno (livro, comentário, letra de música, apostila): **paráfrase atribuída**
  ("Kurose e Ross explicam assim: …"), nunca bloco longo copiado.
- Imagem de terceiro: nunca. Imagem é sempre gerada (ver catálogo visual).

## 4. Dossiê do tópico (entregável do Passo 1)

Um arquivo por tópico: `fontes/<curso>/topicoN-<slug>.md` (pasta na raiz do repo).

```markdown
# Dossiê — <título do tópico>
## Fontes
| # | Tipo | Referência (autor, título, ano, link) | Acesso em | O que usei |
## Afirmações centrais
| Afirmação | Fontes (#) | Status |
## Casos reais / casos que deram errado
## Divergências entre fontes
## O que ficou de fora (e por quê)
```

O dossiê é a matéria-prima do Passo 2 (geração) e a régua da auditoria (Passo 5).

## 5. Como buscar

- `WebSearch` pra descobrir; `WebFetch`/`firecrawl scrape` pra ler a página inteira.
- PDF de instituição: baixar e ler as páginas relevantes (Read com `pages`).
- Sempre anotar link + data de acesso no dossiê.
- Conferir se a fonte é **atual** quando o assunto muda rápido (IA, segurança, preços de nuvem).

---

## 6. Fontes por curso (ponto de partida, ampliar sempre)

### Obreiro (teologia)
- **Texto bíblico:** `biblia_service` (obrigatório, nunca de memória).
- **Comentaristas em domínio público (pode citar):** Matthew Henry, C. H. Spurgeon, João
  Calvino, John Gill, Adam Clarke.
- **Comentaristas modernos (só paráfrase):** David Guzik (Enduring Word), John Stott, Warren
  Wiersbe, F. F. Bruce, D. A. Carson.
- **Léxico/dicionário:** Strong e Vine (via Blue Letter Bible) pra palavra no original.
- **Documentos históricos:** Credo Apostólico, Didaquê, confissões históricas (citar a
  tradição de cada uma, mantendo a neutralidade entre denominações).
- **Casos reais:** história da igreja, biografias missionárias; **casos que deram errado:**
  escândalos e quedas de liderança documentados publicamente (sem expor pessoa comum).

### Inglês
- Base do básico ao intermediário **antes** de músicas (decisão do Atila, 2026-10-01).
- **Nível/vocabulário:** descritores CEFR (Council of Europe), Oxford 3000/5000, English
  Vocabulary Profile (Cambridge).
- **Material didático aberto:** British Council LearnEnglish, BBC Learning English.
- **Pronúncia e uso real:** Cambridge Dictionary (IPA + áudio), YouGlish (a palavra em
  vídeos reais), corpus COCA pra frequência.
- **Gramática:** gramáticas de referência (ex.: Murphy, *English Grammar in Use*) só em paráfrase.
- **Casos que deram errado:** falsos cognatos e erros típicos de brasileiro (listas de
  instituições, não de fórum).

### Redes e Câmeras
- **Primárias:** RFCs (`estudo-redes-cameras/FONTES.md`), especificações ONVIF, docs
  oficiais (MediaMTX, Tailscale, AWS/Backblaze), manuais de fabricante (Intelbras, Hikvision).
- **Livros:** Kurose & Ross (*Redes de Computadores e a Internet*), Tanenbaum (*Redes de
  Computadores*), material da Cisco Networking Academy (CCNA).
- **Segurança:** OWASP IoT Top 10, guias do NIST, avisos da CISA.
- **Casos que deram errado:** botnet Mirai (2016, câmeras e DVRs com senha padrão),
  câmeras expostas na internet sem senha, vazamentos de NVR — sempre com fonte jornalística
  ou técnica séria.
- **Projetos reais:** o NVR de Piazza Fontana (192.168.1.19), mais cenários variados:
  condomínio, pequena empresa, residência, comércio.

### IA / Agentes LLM
- **Papers originais:** *Attention Is All You Need* (2017), BERT, GPT-3, RAG (Lewis et
  al., 2020), Chain-of-Thought, ReAct.
- **Livros:** Jurafsky & Martin, *Speech and Language Processing* (rascunho aberto);
  Sebastian Raschka, *Build a Large Language Model (From Scratch)*; Chip Huyen, *AI Engineering*.
- **Explicação de especialista:** Jay Alammar (*The Illustrated Transformer*), Lilian Weng,
  Andrej Karpathy (aulas abertas).
- **Docs oficiais:** Anthropic, OpenAI, Google (comportamento atual de modelo/API).
- **Casos que deram errado:** chatbot da Air Canada (tribunal mandou honrar promessa
  inventada, 2024), chatbot de concessionária Chevrolet "vendendo carro por US$ 1" (2023),
  advogados multados por citar processos inventados por IA (Mata v. Avianca, 2023).
- **Projetos/exemplos de domínio:** agente do Garden Center (loja de plantas no WhatsApp),
  **empresa de segurança/portaria/câmeras/portões** (onde o Atila presta serviço) e outros
  (clínica, condomínio, atendimento de loja).

---

## 7. Fluxo de autoria com as fontes (vale pra todo curso)

1. **Dossiê** (Passo 1) — eu monto, com as fontes acima.
2. **Geração híbrida** — Groq e Gemini, separados, recebem o dossiê com a instrução
   "organize ESTE material em aula" (nunca "escreva sobre X" de memória). Pedir "não invente"
   não funciona; dar o material e pedir pra organizar funciona melhor.
3. **Comparação e complemento** — eu comparo as duas versões, junto o melhor de cada uma
   e acrescento o que as duas deixaram passar do dossiê.
4. **Auditoria IA** (Passo 5 da BASE) — confiro cada afirmação contra o dossiê.

Se o Groq/Gemini estiver fora do ar ou gerar algo pior que o dossiê, escrevo direto a
partir do dossiê (já aconteceu no Obreiro T4 e no Inglês) — a etapa 4 continua obrigatória.
