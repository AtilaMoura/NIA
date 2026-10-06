# Especificação — Inglês (Course 9)

Segue a [BASE](BASE.md). É o curso **mais diferente**: foco em vocabulário/escuta, não
em explicação de conceito. Histórico: `estudo-ingles/PASSO_A_PASSO.md`, `estudo-ingles/PLANO.md`.

- **Tema:** `caderno-escolar` (claro + escuro; escolhido 2026-10-01, antes `papel-latao`)
- **Perfil de agente:** `PERFIL_INGLES` (`backend/app/agents/perfis.py`)
- **Estrutura:** uma aula POR FONTE (música, vídeo…), dividida por PARTE da fonte
  (trecho do vídeo / movimento da música), não por skill.
- **Nível do Atila:** básico — explicação em português, exemplos em inglês.

## Passo 1 — Fonte

- **Prioridade nova (2026-10-01):** montar a base do **básico ao intermediário** antes das
  músicas, com fonte de instituição: descritores CEFR, Oxford 3000, English Vocabulary
  Profile, British Council, BBC Learning English, Cambridge Dictionary (IPA), YouGlish.
  Lista completa no [FONTES_GUIA.md](FONTES_GUIA.md). Músicas e vídeos vêm depois, como
  prática da base.
- Fonte das aulas de música/vídeo = o material real: transcrição do vídeo (`estudo-ingles/unidades/<nn>/_transcricao.md`,
  com timestamps) ou pesquisa da música (`_pesquisa.md`).
- **Nunca reproduzir letra de música** ou trecho longo com copyright — parafrasear o
  sentido e mandar acompanhar a letra oficial (YouTube/Genius). Exemplos são frases próprias.
- História/contexto: pesquisa web com fonte citada, nada "de cabeça".

## Passo 2 — Escrita (substitui a BASE)

- **Híbrido a partir do dossiê** (BASE, Passo 2). Cuidado conhecido: o `ContentAgent`
  (Groq e Gemini) **não respeita lista fechada** de palavras quando escreve de memória —
  inventou vocabulário e testou palavra nunca ensinada. Por isso: a lista de palavras do
  tópico vem pronta do dossiê, a IA só organiza explicação/exemplo, e a auditoria confere
  palavra por palavra (nenhuma a mais, nenhuma a menos, toda pergunta só com palavra ensinada).
- Formato pedido pelo Atila: **"palavra por palavra"** — toda palavra/expressão de
  conteúdo do trecho vira bloco `vocab` (termo, classe, tradução, `exemplo_en`, cuidado);
  palavra de função só aparece na frase traduzida.
- Checkpoint logo depois de cada parte (só avança dominando a parte).
- Tipos de pergunta próprios: `lacuna`, `associar`, `open` com `resposta_modelo`.
- Bloco `audio_video` pra trecho do vídeo/música (placeholder sem `url` se não houver).
- Regras de perfil: nomear o tempo verbal, contrastar armadilha do português.
- Entregável de revisão (opcional, usado na Aula 2): `topicoN-...-completo.html` antes do banco.

## Passo 6 — Imagens

- Estilos (catálogo visual, 2026-10-01): ★ `flat-escuro-latao` (principal: flat colorido,
  fundo escuro, luz latão, sem rosto, sem texto; lote de referência
  `scripts/imagens_ingles_aula2_topico1.json`), `pop-art` (diálogos), `line-art`,
  `sketchnote` (resumo de vocabulário).
- "Bastante imagens" (pedido do Atila) — idealmente 1 por parte/movimento.
- Pasta: `backend/static/course-images/curso9/`.

## Passo 7 — Áudio (substitui a BASE)

- **Não gerar arquivo.** O template já tem, pra todo bloco `vocab`: 🔊 do termo, 🔊 do
  `exemplo_en` e "🔊 Ouvir vocabulário desta seção" (Web Speech `en-US`). Basta o
  `exemplo_en` estar bem escrito.
- Pendência: shadowing com voz gerada (Gemini TTS inglês) ainda não decidido.

## Revisão

- Atila aprova pelo `/revisao/topico/{id}`; não seguir pro próximo tópico antes disso
  (evita retrabalho em série, lição do T1).

## Revisar tópico antigo no padrão novo (roteiro aprovado pelo Atila em 2026-10-06)

Vale pra T9, T10, T11, T27 (Aula 1 "To be & verbos normais") e qualquer tópico de Inglês feito
antes do processo novo. **Um tópico por vez, com revisão do Atila entre eles.** Mesmo id/URL.

1. **Backup** do conteúdo atual: `backend/_backup_topico<N>_<data>.json` (nunca apagar).
2. **Dossiê** `fontes/ingles/topico<N>-<slug>.md`: fontes de instituição (Cambridge Dictionary
   Grammar, British Council LearnEnglish, English Grammar Profile — nível A1/A2, Cambridge IPA pra
   pronúncia); **lista FECHADA** de formas/palavras do tópico; armadilhas reais do português com
   fonte (ex.: ser×estar, idade com "be", o erro "I am work" do diagnóstico).
3. **Conteúdo** `backend/_criar_topico<N>_ingles.py`: mantém o que já funciona; acrescenta o que o
   padrão novo pede (Reflexão "💭 Pra pensar" + Resumo, `imagem_capa`, `fluxo`, ≥1 tf/classify/
   associar + 2 abertas). **Não invadir** o tópico seguinte (ex.: T9 não ensina verbo normal/don't
   — é do T10; nem he/she/it + s — Aula 2). **Manter os ids de pergunta** que continuam iguais (as
   respostas salvas do Atila ficam ligadas ao id — `TopicoResposta`).
4. **Auditoria palavra por palavra**: nenhuma palavra fora da lista; toda pergunta só com o que já
   foi ensinado ATÉ aquele ponto do curso (lição do T4/T27: "she plays" antes do "-s").
5. **Imagens novas** no estilo `flat-escuro-latao` (catálogo): `scripts/imagens_ingles_topico<N>.json`.
6. **Publicar** local + produção (PUT com `is_approved=true`), conferir 200.
7. **Áudio: narração em PORTUGUÊS por bloco** (decisão 2026-10-06 — igual Redes/Obreiro/IA). Os
   exemplos em inglês continuam na voz en-US dos cards (`vocab`/`ditado`), não na narração.
   Revisar cada narração: pronúncia de palavra inglesa no meio do português, nenhuma frase longa
   em inglês (a voz pt-BR lê errado), nada de abreviação.
8. FILA + memória + commit local.
