# Especificação — Curso de Obreiro (Course 8 = I, Course 12 = II)

Segue a [BASE](BASE.md). Aqui só o que o obreiro acrescenta/substitui.
Histórico detalhado (T1-T5, tabelas Groq×Gemini): `curso de obreiro/PROCESSO_CRIACAO_TOPICO.md`
e `curso de obreiro/anotação para IA.md`.

- **Tema:** `trigo-maduro`
- **Perfil de agente:** `PERFIL_OBREIRO` (`backend/app/agents/perfis.py`)
- **Referência de qualidade:** T5 "Integração dos Três" (`Topico.id=5`) — padrão novo.

## Passo 1 — Fonte

- Texto bíblico **sempre** por `biblia_service.buscar_todos_textos("Rm 12:6-8")` /
  `buscar_texto` — nunca de memória, nem versículo "curto e conhecido" (3 citações
  erradas de memória já foram achadas no T2).
- Re-conferir citações de tópicos ANTERIORES que o novo reusa.
- Buscar bem mais passagens do que a IA usaria (~15-20).
- Mais nomes além do Guzik (2026-10-01): clássicos em domínio público (Matthew Henry,
  Spurgeon, Calvino, John Gill, Adam Clarke) podem ser citados; modernos (Stott, Wiersbe,
  F. F. Bruce, Carson) só em paráfrase. Léxico Strong/Vine pra palavra no original. Lista
  completa no [FONTES_GUIA.md](FONTES_GUIA.md).
- Comentário: Guzik/Enduring Word via Firecrawl
  (`enduringword.com/bible-commentary/<livro-cap>/`) — **só paráfrase atribuída**
  ("Guzik resume assim: …"), nunca citação longa (copyright).
- A própria API bíblica pode vir corrompida (1Pe 4:11 "ma quem") — ler o texto.

## Passo 2 — Escrita (substitui a BASE)

1. `backend/_gerar_topicoN_obreiro.py`: `generate_conteudo_pro()` **1× Groq e 1× Gemini**,
   `perfil=PERFIL_OBREIRO` + `texto_biblico_base` real. Rodar em background via
   `docker exec nia_backend python ...`. Cota Gemini ~6-10 chamadas/rodada (teto 20/dia);
   Gemini às vezes cai com 503 "high demand" (instabilidade, não cota).
2. Comparar os dois de verdade (riqueza, fidelidade, continuidade, variedade de pergunta,
   bugs) → tabela em `anotação para IA.md`. Nenhum ganha sozinho: montar **híbrido**.
3. Se os dois vierem ruins/indisponíveis → escrever à mão grounded no Passo 1 (já
   aconteceu no T4).
4. **Entregável de validação = `curso de obreiro/topicoN-<slug>-completo.html`**
   (leitura corrida, `.takeaway` por seção). O Atila/professor valida ESTE arquivo;
   só depois vira JSON + QuizAgent + slides.

## Passo 5 — Auditoria (fazer junto do Passo 2)

- [ ] Toda referência citada de passagem virou bloco `quote` real
- [ ] Tema com divergência entre tradições (dons, cessacionismo…) tem **nota de
      neutralidade doutrinária** explícita
- [ ] Reflexão + Resumo presentes (faltaram no T3 original)
- [ ] `is_approved=true` = só estrutural; revisão doutrinária humana é à parte

## Slides "O que as tradições cristãs dizem" (formato novo, 2026-10-07)

> Status: **piloto no T66 aguardando aprovação do Atila** (rascunho em
> `backend/_topico66_tradicoes_rascunho.json`). Depois de aprovado, vale pra T67, T68, T69 e
> todo tópico novo que tiver divergência entre tradições.

O formato antigo (parágrafo + citações soltas + uma "nota de neutralidade" com tudo junto)
ficou confuso: as citações (`quote`) não têm áudio, então a narração pulava direto pra
divergência; os nomes dos documentos apareciam sem explicação; cada item juntava várias ideias.

**São dois slides, um depois do outro:**

1. **"O que as tradições cristãs dizem"** — apresenta quem fala.
   - `paragrafo` de abertura (1-3 frases): a pergunta do tópico e o que todas têm em comum.
   - Um `box` `def` **por tradição**, com `itens` nesta ordem:
     `Quem é:` (1 linha — que igreja, que documento, ano) · `O que diz:` (em palavras simples) ·
     `Nas palavras dela:` (citação **curta, até ~25 palavras**, com a referência).
     Rótulo: `📜 <Tradição> — <Documento> (<ano>)`. Nunca usar `quote` aqui (fica sem áudio).
2. **"Onde concordam e onde divergem"**
   - `box` `app` `✅ Onde concordam` — só o que as fontes citadas sustentam.
   - Um `box` `def` **por divergência** (`⚖️ Diferença N — <pergunta simples>`), com `itens`:
     um item por posição + um último `Em resumo:`. **Uma ideia por item.**
   - `box` `summary` `🤝 Este curso não toma partido` (conhecer as posições + conversar com o pastor).

**Regras de texto:** todo nome de documento, pessoa ou termo técnico (inerrância, magistério,
cessacionista…) é explicado **na mesma frase** em que aparece. Nada de citação nova de memória:
só o que está no dossiê do tópico (`fontes/obreiro/`) — o formato muda, as fontes não.

**Regras de áudio (narração):** explica como professor — quem está falando, o que quis dizer,
por que importa — em vez de ler o texto. Não lê o rótulo da caixa. Até ~30 s (~75 palavras)
por bloco. Números e anos por extenso. Cada narração tem que fazer sentido sozinha.

## Passo 6 — Imagens

- Estilo: **ilustração editorial bíblica contemporânea, semi-realista, cinematográfica**
  (substitui a aquarela simples desde 2026-09-15). Prompt-base e paleta em
  `curso de obreiro/DESCRICOES_IMAGENS.md` e na memória `nia-estilo-editorial-obreiro`.
- Imagens internas **sem texto**; a CAPA pode ter o título pintado na cena.
- Se a geração não agradar, perguntar se o Atila quer gerar ele mesmo (ChatGPT/Gemini)
  antes de insistir em rodadas.
- Pasta: `backend/static/course-images/curso8/`.

## Passo 7 — Áudio (exclusivo daqui)

- Narração por bloco `paragrafo`/`box`: `backend/_gerar_audio_bloco_obreiro.py <topico_id>`
  (Groq escreve a narração → Gemini TTS gera `.wav` em `static/audio/curso8/` →
  `_audio_blocos_topicoN.json` pra revisão → `_aplicar_audio_bloco_obreiro.py` grava
  `audio_url` no bloco). Retry: `_retry_audio_bloco_obreiro.py`.
- Gargalo: Gemini TTS **10 chamadas/dia** (1 por bloco). Pendente testar juntar vários
  blocos numa chamada e cortar por pausa. TTS local descartado (sem GPU).
