# Especificação — Engenharia de Agentes LLM / IA (Course 5)

Segue a [BASE](BASE.md). Plano geral e fases: `PLANO_CURSO_IA_EMAUS.md`.

- **Tema:** `azul-petroleo` (claro + escuro; escolhido 2026-10-03 no catálogo — antes `vinho-ouro`, `vidro-fume`)
- **Perfil de agente:** `PERFIL_TECH` (`backend/app/agents/perfis.py`) — bate com o curso
  (agente de vendas WhatsApp do Garden Center).
- **Referência de qualidade:** Tópicos 13-19 (portados dos decks) e 20 (Embeddings).

## Passo 1 — Fonte

- Fonte primária = **apostila própria do Atila**, fora do repo:
  `C:\Users\amand\OneDrive\Documentos\Estudo IA\aula NN.md` (grade em `Plano do curso.md`).
  Ex.: Positional Encoding = `aula 02.md`, Parte 6.
- Se o tópico já tem deck validado em `Estudo IA/exercicios/aulaN-topicoM-*.html`,
  **portar** com `scripts/portar_exercicio_para_schema.py` em vez de escrever do zero.
- Fato fora da apostila (número de dimensões de um modelo, fórmula, paper) →
  conferir em fonte primária (paper original, doc oficial) antes de escrever.
- **A apostila sozinha não basta (2026-10-01):** o dossiê soma papers originais, livros
  (Jurafsky & Martin, Raschka, Chip Huyen), explicação de especialista (Alammar, Weng,
  Karpathy) e **casos que deram errado** (Air Canada, concessionária Chevrolet,
  Mata v. Avianca). Lista no [FONTES_GUIA.md](FONTES_GUIA.md).

## Passo 2 — Escrita

- O Atila domina o assunto → **pode revisar**. Por isso aqui a IA pode ajudar:
  `backend/_gerar_<tema>_curso_ia.py {groq|gemini}` (script isolado — o endpoint HTTP
  morre no reload do uvicorn) → montagem híbrida com correção manual
  (`_montar_<tema>_final.py`) → `_criar_topico_<tema>.py`.
- Correções que SEMPRE precisam ser feitas na mão: Groq modo pro deixa avaliação toda
  `mc`; Gemini modo pro trunca JSON no QuizAgent.
- Sempre fechar o tópico com aplicação prática num agente real. Não precisa ser só o
  Garden Center: alternar com **empresa de segurança/portaria/câmeras/portões** (onde o
  Atila presta serviço) e outros (clínica, condomínio, atendimento de loja).
- Fórmula/mecanismo → `fluxo` (e, se precisar de conta, bloco de código).

## Passo 6 — Imagens

- **Estilos escolhidos (catálogo visual, 2026-10-01):** ★ `isometrico-claro` (principal,
  capas), `pop-art`, `line-art`, `sketchnote`, `blueprint`. Prompt-base de cada um em
  `docs/estilos/catalogo.json`. Sugestão de uso: isométrico para arquitetura/mecanismo,
  sketchnote para resumo e mapa de conceitos, line art para ilustração leve, pop art para
  situação/diálogo (agente conversando com cliente), blueprint para esquema físico.
- As 3 imagens antigas de Embeddings (estilo "diagrama brilhante", em
  `imagem/curso-ia/aula2/topico2-embeddings/`) **não** seguem o estilo escolhido e nunca
  foram aplicadas: regerar no estilo novo quando revisar o tópico 20.
- Pasta de destino: `backend/static/course-images/curso5/` (ainda não existe).

## Passo 7 — Áudio

- Só o TTS por slide da BASE.
