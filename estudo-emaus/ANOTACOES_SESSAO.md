# Estudo "O Caminho de Emaús" — anotações de sessão

Sessão de 2026-09-02. Material de **estudo pessoal do Atila**, separado do curso de obreiro.
Muito visual, sem quiz e sem avaliação. Duas entregas do mesmo conteúdo: **página completa**
(leitura corrida) + **slides**, cada uma com seu link (Artifact no claude.ai).

---

## Plano aprovado (2026-09-02)

Roteiro em 4 partes + extras, ~14 ilustrações coloridas, entrega como 2 Artifacts.
Bíblia: **Almeida domínio público** (via bible-api.com), a mesma do resto do projeto.
Estilo de imagem: **livro ilustrado de Bíblia, aquarela/guache colorido**, luz quente,
paisagem da Judeia, sem texto na imagem, sem símbolos denominacionais.

Fases: (1) pesquisa + texto bíblico real · (2) roteiro detalhado — **aprovação** ·
(3) versão página → 1º link · (4) ilustrações · (5) versão slides → 2º link ·
(6) conferência final de citações.

---

## O que já foi feito nesta sessão

### 1. Verificação de material anterior — CONCLUÍDO
- Procurei no repositório todo por "Emaús / Lucas 24 / Cléopas / caminho de Emaús".
- **Não existe nenhuma aula de Emaús começada.** O nome "Emaús" no projeto é só o nome
  da *plataforma* de frontend (`emaus-web/`, `PLANO_FRONT_OBREIRO.md`). O estudo do relato
  bíblico nunca foi iniciado. Começamos do zero.

### 2. Pasta criada
- `estudo-emaus/` na raiz (irmã de `curso de obreiro/`).
- `estudo-emaus/_raw/` — respostas cruas da bible-api e do comentário (não descartar).
- `imagem/emaus/` criada para as ilustrações.

### 3. Pesquisa — texto bíblico real — CONCLUÍDO
Buscado o texto real (Almeida, bible-api.com) e salvo em `_raw/*.json` + consolidado em
`_textos_biblicos.md`. Passagens capturadas:

| Grupo | Passagens |
|---|---|
| Núcleo | Lc 24:13-35 (relato de Emaús) |
| Contexto do mesmo dia | Lc 24:1-12 (túmulo vazio, mulheres, Pedro), Lc 24:36-49 (aparição aos Onze à noite), Lc 24:44-48, Lc 24:50-53 (ascensão) |
| Paralelo | Mc 16:12-13 ("manifestou-se sob outra forma a dois deles") |
| Jesus previu a paixão | Lc 9:22, Lc 18:31-34 ("eles não entenderam nada disso") |
| Mesa / testemunho | Jo 20:19-20, At 10:40-41 ("comemos e bebemos com ele depois que ressurgiu") |
| "O Cristo nas Escrituras" (o que Jesus pôde usar no v.27) | Gn 3:15, Gn 22:8, Nm 21:8-9, Dt 18:15, Sl 16:8-11, Sl 22:1-2, Sl 22:16-18, Sl 118:22-24, Is 50:6, Is 53:3-7, Os 6:2, Jonas 1:17 |
| O "partir do pão" na igreja | At 2:42, 1Co 11:23-26 |
| Testemunho da ressurreição | 1Co 15:3-8, 1Pe 1:10-12 |

> Nota técnica: o texto Almeida da bible-api tem pequenos artefatos de OCR em alguns
> versículos (ex.: Lc 24:20 sai "...as nossas autoridades e entregaram..." faltando o "o").
> Corrigir pontualmente contra a Almeida padrão ao montar o HTML, sem mudar a tradução.

### 4. Pesquisa — comentário de apoio — CONCLUÍDO
- Scraped `enduringword.com/bible-commentary/luke-24/` (David Guzik) via Firecrawl.
- Seção de Emaús salva em `_raw/guzik_emaus.md`. Vai entrar como **paráfrase atribuída**
  ("Guzik observa que…"), nunca citação longa (comentário sob copyright).
- Pontos úteis já levantados: "sessenta estádios" ≈ 11 km (Josefo cita uma Emaús a
  30 estádios — pode ser ida-e-volta); os dois eram discípulos comuns, não apóstolos
  famosos; "tardos de coração" = problema no coração, não na cabeça; *diermeneuo*
  ("expôs") = ficar colado ao texto, sem alegoria; a refeição **não** era sacramental
  (eles nem estiveram na Última Ceia) — era ceia simples de aldeia; Spurgeon sobre
  "constrangeram-no"; a mudança do sábado para o domingo como evidência da ressurreição.

---

## O que FALTA (retomar daqui)

1. ~~**Fase 2 — roteiro detalhado**~~ — **CONCLUÍDO** (2026-09-02). Roteiro completo seção
   a seção, com prosa de verdade, textos bíblicos, glossário, extras, lista de 14 imagens e
   4 diagramas, em `ROTEIRO_EMAUS.md`. **Aguardando aprovação do Atila** antes da Fase 3.
2. ~~**Fase 3** — versão página~~ — **CONCLUÍDO** (2026-09-02).
   `caminho-de-emaus-completo.html` publicado como Artifact:
   **https://claude.ai/code/artifact/201c6984-8a35-482c-9a3d-62c0eccc2da1**
   - Sistema visual próprio (NÃO o sépia do obreiro): paleta colorida —
     indigo-dusk `#4a3e6b` (primária), oliva, terracota, âmbar, brasa; tema claro+escuro.
   - Fontes: Young Serif (títulos) + Spectral (corpo/versículos) + Archivo (rótulos).
   - Layout "estrada": trilha vertical com estações numeradas; cor de acento muda por
     Parte acompanhando a hora do dia (tarde→conversa→anoitecer→volta).
   - 10 seções + extras; 8 ilustrações SVG coloridas originais + 2 placeholders (IMG-3,
     IMG-10) marcados "arte final na próxima etapa"; 4 diagramas
     (linha do tempo, mapa Jerusalém→Emaús, quadro "O Cristo nas Escrituras", padrão de Emaús).
   - Glossário com tooltip no hover/focus + seção de glossário visível.
   - **Não consegui revisar visualmente** — extensão do Chrome não conectou nesta sessão.
     Revisão estática do HTML feita; publicado. Se algo estiver quebrado no link, ajustar e republicar.

3. ~~**Fase 4** — ilustrações~~ — **CONCLUÍDO** (2026-09-02).
   - API do Gemini NÃO gera imagem no free tier destas chaves (cota 0) — confirmado.
     Caminho: `scripts/gerar_imagem_gemini.py` (Gemini web, grátis, perfil isolado já
     existia e estava logado).
   - `estudo-emaus/imagens_emaus.json` — 10 cenas, estilo "livro ilustrado, aquarela
     colorida", personagens consistentes (Cléopas=terracota, companheiro=verde-oliva,
     Jesus=azul-índigo). Geradas em ~10 min, salvas em `imagem/emaus/cenas/v1/`.
   - Todas as 10 saíram boas (revisadas uma a uma).
   - Otimizadas p/ JPEG 1024px q80 (~1.3 MB total) e embutidas como data URI no HTML via
     `_template_completo.html` + substituição (script inline). HTML final 1.76 MB.
   - Os 8 SVGs toscos que eu tinha desenhado à mão foram REMOVIDOS. Os 4 diagramas
     (linha do tempo, mapa, quadro "O Cristo nas Escrituras", padrão de Emaús) continuam
     em SVG — esses ficaram bons.
   - Artifact republicado no MESMO link:
     **https://claude.ai/code/artifact/201c6984-8a35-482c-9a3d-62c0eccc2da1**
   - Regerar cena: apagar o PNG em `imagem/emaus/cenas/v1/` e rodar
     `python scripts/gerar_imagem_gemini.py estudo-emaus/imagens_emaus.json`, depois
     re-embutir (`_raw/_img_datauris.json` + template).

4. ~~**Fase 5** — slides~~ — **CONCLUÍDO** (2026-09-02).
   `caminho-de-emaus-slides.html` — 53 slides, navegação teclado (← → espaço Home/End) +
   toque (tap lateral / swipe) + índice (☰) + barra de progresso + deep-link `#n` +
   retomada via localStorage (try/catch). Mesmo sistema visual e as 10 imagens embutidas.
   Publicado como Artifact NOVO (2º link):
   **https://claude.ai/code/artifact/f37f7b6f-a8f8-4070-a88c-57aec1420f4e**
   Template: `_template_slides.html` (+ mesmo passo de injeção de data URI).

5. ~~**Fase 6** — conferência de citações~~ — **FEITO** (spot-check, 2026-09-02).
   Conferidos contra `_textos_biblicos.md` todos os blocos `verse` das duas versões:
   Lc 24:13-14, 15-17, 19+21, 27, 28-29, 30-31, 32, 33+35, 45 e Mc 16:12-13 — batem com o
   texto Almeida da bible-api. A tabela "O Cristo nas Escrituras" são paráfrases curtas
   assumidas como reconstrução (nota de honestidade no próprio material).
   Guzik entra sempre como paráfrase atribuída, nunca citação longa.

## Estado final (2026-09-02)

**As duas entregas estão no ar:**
- Página completa: https://claude.ai/code/artifact/201c6984-8a35-482c-9a3d-62c0eccc2da1
- Slides (53): https://claude.ai/code/artifact/f37f7b6f-a8f8-4070-a88c-57aec1420f4e

Não consegui abrir nenhuma das duas para revisão visual (extensão do Chrome não conecta
nesta sessão). Revisão estática feita. Se o Atila achar algo torto, corrigir e republicar
(mesmo file path → mesmo link).

Pendências reais que sobraram:
- Revisão visual das duas páginas pelo Atila.
- Eventual regeração de alguma cena que ele não goste (apagar PNG + rerodar script + re-injetar).
- Fase 6 "linha a linha" completa (só foi spot-check dos blocos de citação).

---

## Fase 7 — vídeos narrados (iniciada 2026-09-02/03)

Ideia do Atila: vídeos curtos por parte/seção, com narração TTS + as ilustrações.

**Descobertas de infra:**
- **Sem GPU NVIDIA** → XTTS v2 / F5-TTS / Fish Speech fora (precisam 6-8 GB VRAM).
- **Gemini TTS FUNCIONA no free tier destas chaves** (≠ imagem, que é cota 0). Modelos
  `gemini-2.5-flash-preview-tts` / `gemini-3.1-flash-tts-preview`, PT-BR, ~30 vozes,
  estilo controlável por instrução. Rate limit ocasional (retry com espera resolve).
- `ffmpeg` não estava instalado → `pip install imageio-ffmpeg` (binário embutido, sem admin).
- `pip install google-genai` no host (antes só no container).

**Pipeline construído:** `estudo-emaus/video/montar_video.py` — lê um JSON de roteiro
(`{titulo, subtitulo, voz, estilo, formato, segmentos:[{imagem, narracao, legenda}]}`),
gera 1 WAV por segmento (Gemini TTS, com cache), monta cada cena (fundo borrado + ilustração
centrada com Ken Burns/zoom lento + legenda em PNG via Pillow com a tipografia do estudo),
card de título, e concatena. Saída MP4. `_work/` guarda intermediários (WAV cacheado).

**Piloto feito:** `estudo-emaus/video/piloto_partir_do_pao.json` → `.mp4` (71s, 9:16, voz
Achernar, §7 "O partir do pão", 5 segmentos). Enviado ao Atila (cópia 720p — upload de
11 MB falhou, 2.4 MB passou).

**Decisões ainda abertas (perguntadas ao Atila):** formato (9:16 x 16:9 x 4:5),
granularidade (~10 curtos por seção x ~4 por parte), voz definitiva, manter legenda queimada.

**Polish possível depois:** fundo menos escuro / imagem maior; crossfade entre cenas;
música de fundo suave; versão 16:9 pro YouTube.

### Fase 7b (2026-09-03) — imagens verticais + piloto v2 com movimento

- **10 imagens verticais 9:16** geradas (`imagens_emaus_vertical.json` →
  `imagem/emaus/cenas/v1v/`). Estilo saiu mais "aquarela solta" que a leva horizontal
  (menos traço de nanquim), mas mesma paleta e personagens. Servem pro vídeo vertical sem
  faixa preta. (As horizontais `v1/` ficam pro 16:9 / páginas.)
- **`montar_video.py` ganhou movimento:** `_kenburns()` com modos (in/out/left/right/up),
  vinheta radial estática (PNG via Pillow), grão de filme (`noise` leve), poeira flutuante
  (loop `_assets/dust_*.mp4` pré-renderizado 1x), e tremular quente (`eq` com `sin(t)`) nos
  segmentos com `"luz":"quente"`. Config: `"movimento": true` + por segmento `"mov"`/`"luz"`.
- **Lição de performance:** filtros por-pixel-por-frame são caríssimos nesta máquina (sem
  GPU). `boxblur=46:5` **por frame** e `vignette` com **expressão** levavam ~165 s/segmento.
  Solução: **placa de fundo borrada estática** (`_bg_plate`, 1 PNG por imagem) + **vinheta
  PNG estática** + dust como **loop pré-renderizado**. Caiu pra ~15‑30 s/segmento. Preset
  `veryfast`. Estimativa série completa: ~20 min por formato, em lote no fundo.
- Piloto v2: `video/piloto_partir_do_pao_v2.json` → `.mp4` (71 s, 9:16). Enviado (720p).
- Voz: **fica Achernar nos testes**; usuário quer outra pra série final (mandar amostras).

---

## Estrutura de conteúdo pretendida (resumo — detalhar na Fase 2)

**Parte 1 – A cena:** (1) o terceiro dia e o desânimo; (2) a caminhada triste (v.13-17);
(3) o desconhecido que se aproxima, "olhos impedidos" (v.15-16).
**Parte 2 – A conversa:** (4) "só tu és peregrino?" — o relato deles, "nós esperávamos"
(v.18-24); (5) "ó néscios e tardos de coração" — Moisés e os Profetas, o Cristo que
*precisava* padecer (v.25-27).
**Parte 3 – A mesa:** (6) "fica connosco" (v.28-29); (7) o partir do pão, "abriram-se-lhes
os olhos", ele desaparece (v.30-31); (8) "não se nos abrasava o coração?" (v.32).
**Parte 4 – A missão:** (9) a volta imediata a Jerusalém, "ressurgiu verdadeiramente"
(v.33-35); (10) temas e aplicação + o "padrão de Emaús".
**Extras:** mapa Jerusalém→Emaús; linha do tempo do domingo da ressurreição; quadro
"O Cristo nas Escrituras"; paralelo Emaús ↔ encontro cristão (Palavra + pão); glossário
visual (Emaús, Cléopas, "partir do pão", "néscios", "estádios"); Mc 16:12-13.

**Neutralidade:** onde tradições cristãs divergem (natureza do "partir do pão" —
eucaristia x ceia comum), apresentar as leituras sem tomar partido. Guzik/Morrison já
argumentam que ali era ceia comum; registrar isso como uma leitura, não como a única.

---

## Arquivos desta sessão

- `estudo-emaus/ANOTACOES_SESSAO.md` (este arquivo)
- `estudo-emaus/_textos_biblicos.md` — todos os textos bíblicos consolidados
- `estudo-emaus/_raw/*.json` — respostas cruas da bible-api (26 passagens)
- `estudo-emaus/_raw/guzik_emaus.md` — comentário de Guzik (Lucas 24), seção Emaús
- `imagem/emaus/` — vazia ainda

Nenhum arquivo fora de `estudo-emaus/` e `imagem/emaus/` foi tocado. Nada publicado ainda.
