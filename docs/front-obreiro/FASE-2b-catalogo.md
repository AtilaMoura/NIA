# Extra — Catálogo público + landing do Emaús

Adiantado da FASE 6 a pedido do usuário (2026-09-03): dar cara de plataforma —
catálogo com vários cursos "em breve" (cadeado) + capas + landing.

Decisões travadas nesta rodada:
- Cursos "em breve" ficam **hardcoded no `emaus-web`** (`_lib/catalogo.ts`), não no banco do
  NIA (que é compartilhado com o front de tecnologia; rows fake vazariam pro `/aluno/explorar`).
- Capas geradas pelo **script do Gemini web** (`scripts/gerar_imagem_gemini.py`), estilo
  aquarela colorida + tinta sobre pergaminho.
- Lista de 12 cursos proposta pelo Claude (o usuário edita `catalogo.ts` quando quiser).

## Arquivos

| Arquivo | O quê |
|---|---|
| `emaus-web/app/_lib/catalogo.ts` | `CATALOGO: CursoCatalogo[]` (12), `GRADIENTE_TOM`, `caminhoCapa(slug)`. 1 disponível (`courseId 8`), 11 `disponivel:false`. |
| `emaus-web/app/_lib/capas.ts` | `capaExiste(slug)` — server, checa `public/capas/{slug}.jpg`. |
| `emaus-web/app/_ui/CapaCurso.tsx` | capa 3:2: `<img>` se existe, senão degradê do tom + monograma. Vinheta pra profundidade. |
| `emaus-web/app/page.tsx` | landing: `CabecalhoApp` + hero + grade de `CardCurso` (`sm:2 / lg:3` colunas). Card disponível → `Link /curso/{id}`; "em breve" → `🔒 Em breve`, sem link, opacidade 75%. |
| `emaus-web/app/_ui/AlternarTema.tsx` | toggle ☾/☀ no cabeçalho (grava cookie `tm_theme`). Provisório até `/preferencias`. |
| `emaus-web/app/_ui/CabecalhoApp.tsx` | +import do `AlternarTema` no bloco da direita. |
| `emaus-web/app/topico/[topicoId]/page.tsx` | fix: `<iframe>` ganhou `allow="fullscreen"` + `allowFullScreen`, tirou `sandbox` (conteúdo é do nosso backend). |
| `scripts/capas_emaus.json` | 12 prompts em inglês pro script do Gemini. |

## Gerar as capas (passo manual do usuário)

```bash
# pré-requisito, 1x: python scripts/configurar_perfil_gemini.py  (logar no Google no perfil isolado)
python scripts/gerar_imagem_gemini.py scripts/capas_emaus.json
```

Saída: `imagem/capas/emaus/v1/{slug}.png` (pula os que já existem).
Depois, converter/copiar pra `emaus-web/public/capas/{slug}.jpg` (mesmo nome de slug, extensão `.jpg`).
Assim que o arquivo existe, o card troca o degradê pela foto automaticamente (sem deploy).

Slugs: `formacao-novo-obreiro, panorama-da-biblia, como-estudar-a-biblia, evangelho-de-joao,
romanos, antigo-testamento-panorama, vida-de-oracao, doutrinas-essenciais,
discipulado-primeiros-passos, salmos, carater-cristao, missoes-e-evangelismo`.

## Aceite

1. `cd emaus-web && npx tsc --noEmit` → 0 erros. ✓
2. `GET localhost:4200/` → 200, landing com hero + 12 cards (1 "Começar", 11 "Em breve"). ✓
3. Card "Formação Geral do Novo Obreiro" → `/curso/8`. ✓
4. Sem nenhuma capa em `public/capas/`, todos os cards mostram o degradê do tom + monograma
   (não quebram). ✓
5. `/topico/1` → botão `⛶` do render entra em tela cheia. (conferir no navegador)

## Rodada 2 — identidade + polish (mesma sessão, 2026-09-03)

- **Logo** `_ui/Logo.tsx` (`Logo` = símbolo + wordmark "Emaús" em Fraunces; `LogoSimbolo` só o
  símbolo). Direção escolhida: **livro aberto + brasa**. Hoje é **SVG placeholder**; a versão
  ilustrada (aquarela/tinta) sai do script — ver abaixo. Flag `MARCA_ILUSTRADA_PRONTA` em
  `Logo.tsx` faz a troca (SVG → `/marca/emaus-simbolo.png`) numa linha.
- **Favicon** `app/icon.svg` (símbolo geométrico em âmbar sobre pergaminho, funciona em aba
  clara e escura).
- **Landing** (`app/page.tsx`) reescrita: hero com textura `.grao` + marca d'água do símbolo,
  faixa de 3 pilares ("Para entender de verdade" / "No seu ritmo" / "Sem viés de denominação"),
  grade de cursos, rodapé próprio com Lc 24.32.
- **globals.css**: `.grao` (grão SVG a 4%), `::selection` âmbar, scrollbar discreta,
  `scroll-behavior: smooth` (respeitando `prefers-reduced-motion`).
- **Estados**: `app/not-found.tsx` (404 amigável), `app/error.tsx` (client — detecta "API fora
  do ar" vs erro genérico, botão "tentar de novo"), `app/loading.tsx` (símbolo pulsando).
- **Metadata**: `layout.tsx` com `metadataBase` + `title.template "%s · Emaús"` + `openGraph`;
  `generateMetadata` em `/curso/[id]` (título do curso) e `/topico/[id]` (título do tópico);
  `/inicio` = "Meu estudo"; landing com título absoluto.
- **Shell**: `CabecalhoApp` usa o `Logo` (prop `hrefMarca`), `Rodape` idem; `/inicio` ganhou
  hero com textura + saudação pelo primeiro nome; barra do `/topico` com o símbolo.
- **Bug conhecido (menor)**: `/curso/{id fora do catálogo}` mostra a página "não encontrado"
  certinha, mas com HTTP 200 em vez de 404 (quirk do `notFound()` no dev do Next 16). UX ok.

### Marca ilustrada — FEITO (2026-09-03)

- `gerar_imagem_gemini.py scripts/marca_emaus.json` → `emaus-simbolo-a.png` (aquarela detalhada)
  e `emaus-simbolo-b.png` (minimalista) em `imagem/marca/emaus/v1/`. Variante `c` o script pulou.
- **Escolhida B.** `preparar_imagens_emaus.py marca emaus-simbolo-b.png` recorta o fundo por
  saturação → `emaus-web/public/marca/emaus-simbolo.png` (transparente 731×661, ok claro+escuro).
  `MARCA_ILUSTRADA_PRONTA = true` em `_ui/Logo.tsx`. Tamanhos: cabeçalho 34px, rodapé/tópico 28px.
- Favicon segue SVG. Opção A guardada como ilustração decorativa reserva.

### Capas — FEITO (2026-09-03)

- `gerar_imagem_gemini.py scripts/capas_emaus.json` → 12 PNGs em `imagem/capas/emaus/v1/`.
- `preparar_imagens_emaus.py capas` → 12 JPGs (~1024px, q82, 75–150KB) em
  `emaus-web/public/capas/{slug}.jpg`. Enquadramento 3:2 pelo `object-cover`.
- Estilo coerente (aquarela+tinta, paleta quente). Nit: `doutrinas-essenciais` tem uma letrinha
  fraca na pedra angular (prompt pedia "no text") — regerar 1 se incomodar.

## Estado

- [~] Catálogo + identidade + polish + **todas as imagens (marca + 12 capas)** feitos e ligados,
  testado via curl/tsc 2026-09-03. Site em `:4200` mostra as capas reais.
  **Pendência:** conferência visual nos 2 modos (extensão Chrome não conecta aqui).
