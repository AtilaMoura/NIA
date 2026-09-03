# Estudo "O Caminho de Emaús" — passo a passo do que foi feito

Material de **estudo pessoal do Atila** sobre Lucas 24:13‑35. **Separado** do curso de
obreiro e da plataforma (`emaus-web/` é a plataforma, outra coisa). Tudo vive em
`estudo-emaus/` + as imagens em `imagem/emaus/`.

Datas: 2026‑09‑02 e 2026‑09‑03.

---

## 1. Entregas prontas (links)

| O quê | Link | Arquivo fonte |
|---|---|---|
| **Página completa** (leitura corrida) | https://claude.ai/code/artifact/201c6984-8a35-482c-9a3d-62c0eccc2da1 | `caminho-de-emaus-completo.html` |
| **Slides** (53 telas, teclado/toque/índice) | https://claude.ai/code/artifact/f37f7b6f-a8f8-4070-a88c-57aec1420f4e | `caminho-de-emaus-slides.html` |
| **Vídeo piloto** (§7, 9:16, 71s) | entregue no chat (cópia 720p) | `video/piloto_partir_do_pao.mp4` |

Republicar mantendo o mesmo link: reeditar o arquivo e publicar de novo pelo mesmo caminho.

---

## 2. Passo a passo do que foi feito

### Passo 1 — Verificação
Procurei "Emaús / Lucas 24 / Cléopas" no repositório inteiro. **Não havia nada começado** —
o `emaus-web/` é só o nome da plataforma. Começamos do zero.

### Passo 2 — Pesquisa (texto bíblico real)
- Buscadas **26 passagens** na `bible-api.com` (tradução **Almeida, domínio público**) —
  núcleo Lc 24:13‑35 + contexto do domingo + paralelo Mc 16 + as passagens do AT que Jesus
  pôde ter usado (Gn 3:15, Is 53, Sl 22, etc.) + At 2:42 / 1Co 11.
- Salvo cru em `_raw/*.json` e consolidado em `_textos_biblicos.md`.
- Comentário de apoio: **David Guzik / Enduring Word** (Lucas 24), via Firecrawl, salvo em
  `_raw/guzik_emaus.md`. Entra sempre como **paráfrase atribuída**, nunca citação longa
  (copyright).
- Regra: nenhum versículo vem "de cabeça" — sempre do texto buscado.

### Passo 3 — Roteiro
`ROTEIRO_EMAUS.md` — conteúdo de verdade, seção a seção: 4 partes (A cena / A conversa / A
mesa / A missão), 10 seções + extras (mapa, linha do tempo, quadro "O Cristo nas
Escrituras", glossário, Mc 16). Marca onde entra cada imagem e cada diagrama.
**Aprovado por você antes de virar HTML.**
Neutralidade explícita onde tradições divergem (o "partir do pão": eucaristia × ceia comum).

### Passo 4 — Página completa (HTML)
`caminho-de-emaus-completo.html`. Sistema visual **próprio** (não o sépia do obreiro):
- Paleta: indigo‑anoitecer (primária), oliva, terracota, âmbar, brasa. Tema claro **e** escuro.
- Fontes: Young Serif (títulos) + Spectral (corpo/versículos) + Archivo (rótulos).
- Layout "estrada": trilha vertical com estações numeradas; a cor de destaque muda por
  Parte acompanhando a hora do dia da história.
- 4 diagramas em SVG desenhados à mão (linha do tempo, mapa, quadro do Cristo, padrão de Emaús).
- Glossário com dica ao passar o mouse + seção visível.
- **Primeira versão tinha 8 SVGs de cena feitos por mim — ficaram toscos, foram removidos**
  e trocados pelas ilustrações de verdade (passo 5).

### Passo 5 — Ilustrações (aquarela colorida)
- A **API do Gemini não gera imagem** nestas chaves (free tier = cota 0). Caminho usado:
  `scripts/gerar_imagem_gemini.py` (Gemini web, perfil de Chrome isolado já logado, grátis).
- `imagens_emaus.json` — **10 cenas**, estilo "livro ilustrado, aquarela/guache colorido",
  personagens consistentes: **Cléopas = terracota, companheiro = verde‑oliva, Jesus =
  azul‑índigo**.
- Geradas em ~10 min, salvas em `imagem/emaus/cenas/v1/` (PNG ~1024 px).
- Otimizadas para JPEG e **embutidas nos HTML como data URI** (a página fica ~1,8 MB,
  carrega rápido, funciona offline).
- Descrições em `DESCRICOES_IMAGENS_EMAUS.md`.
- **Decisão:** esse estilo colorido passa a valer também para o **curso de obreiro**
  (anotado em `curso de obreiro/anotação para IA.md` e no topo de `DESCRICOES_IMAGENS.md`).

### Passo 6 — Slides (HTML)
`caminho-de-emaus-slides.html` — **53 telas**. Mesmo conteúdo e imagens.
Navegação: setas `←` `→` / espaço / Home / End · no celular toque nas laterais ou deslize ·
botão **☰ índice** · barra de progresso · deep‑link `#n` · lembra onde parou (localStorage).

### Passo 7 — Conferência de citações
Todos os blocos de versículo das duas versões conferidos contra `_textos_biblicos.md`
(spot‑check): Lc 24:13‑14, 15‑17, 19+21, 27, 28‑29, 30‑31, 32, 33+35, 45 e Mc 16:12‑13 —
batem. A tabela "O Cristo nas Escrituras" são paráfrases curtas assumidas como
reconstrução (tem nota de honestidade no próprio material).

### Passo 8 — Vídeo (piloto)
Ideia sua: vídeos curtos por parte/seção, narração + as ilustrações.
- **Sem GPU NVIDIA** na máquina → modelos locais bons de voz (XTTS, F5, Fish) estão fora.
- **Gemini TTS FUNCIONA no free tier** (≠ imagem!). `gemini-2.5-flash-preview-tts`, PT‑BR,
  ~30 vozes, estilo controlável por instrução. Devolve PCM → viramos WAV.
- **Veo (texto/imagem → vídeo) do Gemini: cota 0** também. Fora por enquanto.
- `ffmpeg` não estava instalado → `pip install imageio-ffmpeg` (binário embutido, sem admin).
- Pipeline: **`video/montar_video.py`** — lê um JSON de roteiro, gera 1 WAV por segmento
  (Gemini TTS, com cache em `_work/`), monta cada cena (fundo borrado + ilustração centrada
  com zoom lento Ken Burns + legenda em PNG na tipografia do estudo), card de título,
  concatena. Saída MP4.
- Piloto: `video/piloto_partir_do_pao.json` → `.mp4` — §7 "O partir do pão", 5 segmentos,
  71 s, vertical 9:16, voz **Achernar**.

---

## 3. Como refazer / atualizar cada parte

| Tarefa | Comando |
|---|---|
| Rebuscar um versículo | `curl "https://bible-api.com/luke+24:13-35?translation=almeida"` |
| Regerar uma ilustração | apagar o PNG em `imagem/emaus/cenas/v1/`, editar `imagens_emaus.json`, `python scripts/gerar_imagem_gemini.py estudo-emaus/imagens_emaus.json` (pula as que já existem) |
| Re‑embutir imagens no HTML | otimizar PNG→JPEG→data URI, atualizar `_raw/_img_datauris.json`, rodar a substituição de `__IMG_xx__` em `_template_completo.html` / `_template_slides.html` → gera os `caminho-de-emaus-*.html` |
| Republicar (mesmo link) | reeditar o `.html` e publicar pelo mesmo caminho |
| Gerar um vídeo | `python estudo-emaus/video/montar_video.py estudo-emaus/video/<roteiro>.json` |
| Trocar formato do vídeo | mudar `"formato"` no JSON (`"9:16"` / `"16:9"`) e rodar de novo — **não regera áudio** (WAV fica em cache) |

---

## 4. Ajustes que ainda vamos fazer (pendências)

### 4.1 Imagens para desktop **e** celular
Hoje as 10 ilustrações são **paisagem ~1,83:1** (boas para 16:9 / leitura). Para vídeo
vertical (9:16) elas ficam com faixa preta/borrada em cima e embaixo.
**Plano:** gerar cada cena em **dois enquadramentos**:
- **Wide 16:9** — desktop, YouTube, a página de leitura.
- **Vertical 9:16 (ou 4:5)** — celular, Reels/Shorts/status, o vídeo vertical.
Custa pouco (mesmo script, dois prompts por cena, com "wide 16:9 composition" / "vertical
9:16 composition" no texto). Fica em `imagem/emaus/cenas/v1/` e `.../v1-vertical/`.

### 4.2 Voz
Para **os testes atuais fica a Achernar**. Para a série final você quer **outra voz** —
vou te mandar 3‑4 amostras PT‑BR (ex.: Sadaltager, Sulafat, Vindemiatrix, Achird) para
escolher antes de gerar o lote.

### 4.3 Movimento nas imagens — **sim, dá para fazer** (sem GPU, sem custo)
Além do zoom lento que já tem, dá para somar:
- **Ken Burns melhor:** direções variadas de pan, aceleração suave no começo/fim, leve rotação.
- **Camadas atmosféricas** (o que mais dá "vida"): poeira flutuando na estrada, raios de
  luz, grão de filme sutil, vinheta que "respira", e nas cenas de lamparina um **tremular
  quente** da luz. Tudo composto no ffmpeg, sem GPU.
- **Parallax 2.5D** (efeito "foto viva"): separar a imagem em camadas de profundidade e
  mover cada uma num ritmo → dá sensação de 3D. Dá para fazer sem GPU, é esforço médio
  (uma vez por imagem).
- **Animação de verdade** (roupa balançando, fogo mexendo): só com image‑to‑video pago
  (Kling / Luma / Runway / Veo) — fica para depois, se valer a pena.
Recomendo testar **atmosféricas + Ken Burns melhor** já no próximo piloto.

### 4.4 Outras decisões abertas
- **Granularidade:** ~10 vídeos curtos (1 por seção) ou ~4 maiores (1 por Parte).
- **Formatos a entregar:** 9:16 sempre; 16:9 também? (re‑render barato)
- **Legenda queimada:** manter (recomendo sim).
- Música de fundo suave? Transição com fade entre cenas?
- Revisão visual das duas páginas por você (a extensão do Chrome não conectou nas sessões,
  então eu não abri para conferir — código revisado, mas o olho é seu).

---

## 5. Infra descoberta (resumo, para não retestar)

| Item | Situação |
|---|---|
| GPU NVIDIA | **Não tem** |
| Gemini API — **imagem** | cota 0 no free tier (as duas chaves) — usar o script de navegador |
| Gemini API — **TTS/áudio** | **funciona** no free tier · PT‑BR · ~30 vozes |
| Gemini API — **Veo (vídeo)** | cota 0 no free tier |
| ffmpeg | instalado via `pip install imageio-ffmpeg` |
| `google-genai` | instalado no host e no container `nia_backend` |
| Chaves | `backend/.env` → `GEMINI_API_KEY`, `GEMINI_API_KEYflash` |

---

## 6. Estrutura de arquivos

```
estudo-emaus/
  PASSO_A_PASSO.md          <- este arquivo
  ANOTACOES_SESSAO.md       <- log cronológico detalhado
  ROTEIRO_EMAUS.md          <- roteiro do conteúdo (aprovado)
  PESQUISA / _textos_biblicos.md  <- 26 passagens (Almeida)
  DESCRICOES_IMAGENS_EMAUS.md
  imagens_emaus.json        <- prompts das 10 cenas
  _template_completo.html / _template_slides.html   <- fontes com tokens __IMG_xx__
  caminho-de-emaus-completo.html / caminho-de-emaus-slides.html  <- publicados
  _raw/                     <- respostas cruas (bible-api, guzik, data URIs, amostras TTS)
  video/
    montar_video.py         <- pipeline de vídeo
    piloto_partir_do_pao.json / .mp4
    _work/                  <- intermediários (WAV cacheado, segmentos)
imagem/emaus/cenas/v1/      <- as 10 ilustrações (PNG)
scripts/gerar_imagem_gemini.py   <- gerador de imagem (Gemini web)
```
