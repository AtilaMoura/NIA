# FASE 6 — Landing, menu, logo e imagens (polish visual)

Planejamento (2026-09-05). Nada implementado ainda. Imagens vão pelo **script**
(`scripts/gerar_imagem_gemini.py`, o usuário roda no Gemini logado), NUNCA pela API.

---

## 1. Análise de mercado — o que plataformas de curso profissionais têm

Referências: Coursera, Udemy, Domestika, MasterClass, Skillshare · e de fé:
**BibleProject** (referência de ouro pro tom), RightNow Media, Ligonier Connect,
Zondervan Academic.

O que quase toda landing de curso profissional tem e o Emaús **não tem** ainda:

| Elemento | Por que importa | Estado no Emaús |
|---|---|---|
| **Prova social** (nº de alunos, depoimentos, "usado por X igrejas", quem fez o conteúdo) | é o que faz confiar | zero — precisa ao menos de espaço reservado + selo de metodologia |
| **"Como funciona"** (3-4 passos) | tira a fricção "o que é isso e como uso" | não tem |
| **Amostra grátis** ("espie um tópico") | maior alavanca de conversão em educação | não tem |
| **Metadados no card** (nível · nº tópicos · duração · "com tutor") | deixa o curso tangível | card só tem título + descrição |
| **Visual de herói forte** (ilustração/foto/vídeo) | espaço mais valioso da página | hoje é um contorno de livro quase invisível |
| **CTA final** (faixa antes do rodapé) | recaptura quem rolou até o fim | não tem |
| **FAQ** ("preciso pagar? saber teologia? funciona no celular? o que é o tutor?") | responde a objeção na hora | não tem |
| **Rodapé completo** (navegação, contato) | fecho profissional | hoje só a citação de Lc 24 |

O que **combina com o tom** de Emaús (formação bíblica, calmo, não é venda agressiva):
- BibleProject: ilustração linda, muito respiro, **uma mensagem por seção**, zero urgência.
- **Nada** de "vagas limitadas", countdown, "últimas unidades". Calor e profundidade > hype.
- Prova social discreta ("junte-se a quem está estudando") > "10.000 ALUNOS!!!".

## 2. Diagnóstico da landing atual

- **Herói**: headline boa (Fraunces, forte). Lado direito é um vazio com um livro
  fantasma quase invisível — desperdício do espaço mais nobre.
- **Logo no menu**: o símbolo é uma **aquarela de ~34px que vira um borrão ilegível**
  (aquarela não funciona pequena). "Emaús" em serif está ok, mas símbolo+texto está
  **desequilibrado**: símbolo apagado, espaço demais entre eles, o "ú" puxa o olho.
- **Menu**: "Cursos · Continuar estudando" à esquerda competem entre si; sem hierarquia.
- **Catálogo**: cards bonitos com as capas em aquarela, mas sem metadado; label
  "Em preparação/breve/revisão" pequeno demais.
- **Pilares**: os 3 ícones SVG são finos e genéricos, quase somem.
- **Rodapé**: só a citação. Falta navegação e fôlego.

## 3. Proposta — nova estrutura da Landing

1. **Menu** redesenhado (ver §4)
2. **Herói** — headline + subhead + **2 CTAs** (Começar · Espiar um tópico) +
   **carrossel de ilustrações** à direita (3-4 aquarelas rotativas, fade suave, pausa no
   hover, respeita `prefers-reduced-motion`) + 1 linha discreta de prova social.
3. **Como funciona** — 4 passos (ícone + número): criar conta grátis → escolher um curso
   → estudar tópico a tópico no seu ritmo → progresso + tutor acompanham.
4. **3 diferenciais** — os pilares atuais repaginados (número grande + título + texto,
   ícone maior/ilustrado).
5. **Amostra** — "Espie um tópico" com preview do render de um tópico aprovado + CTA.
6. **Catálogo** — cards com metadado (nível · N tópicos · com tutor); o disponível em
   destaque, os "em breve" em grade menor.
7. **Depoimento** — 1 card placeholder (ativa quando tiver real).
8. **FAQ** — accordion, 4-5 perguntas.
9. **CTA final** — faixa "Comece hoje. É de graça." + botão.
10. **Rodapé** — logo + navegação (Cursos, Entrar/Meu estudo, Área de revisão se
    aplicável) + citação de Lc 24.32 + assinatura.

## 4. Proposta — Menu (todas as telas)

- Logo à esquerda: **símbolo SVG limpo** (não a aquarela) + "Emaús", conjunto mais junto
  e equilibrado (mesmo peso visual).
- Nav enxuta: "Cursos" | (logado) "Meu estudo".
- Direita: toggle tema → avatar com papel.
- Sticky com blur (já tem) + borda/sombra que aparece só ao rolar.

## 5. Proposta — Logo (várias versões pra escolher)

**Símbolo** (gero 5 variações pelo script — foco: **ler bem pequeno**):
livro+brasa minimalista · selo circular · só-brasa · só-livro · traço único.

**Lockup / wordmark** (código, não imagem — mostro 4-5 arranjos):
horizontal (menu) · empilhado (herói/rodapé) · brasa no lugar do acento do "ú" · dentro
de um selo · só texto com kerning/peso melhor.

Depois: **favicon** novo do símbolo escolhido + og-image.

## 6. Imagens a gerar (pelo script, o usuário roda)

1. `scripts/marca_emaus_v2.json` — 5 variações de símbolo (legível pequeno).
2. `scripts/heroi_emaus.json` — 4 ilustrações pro carrossel do herói (ex.: dois
   caminhantes numa estrada ao entardecer · lâmpada + livro aberto · mãos folheando as
   Escrituras · pequeno grupo estudando à luz de vela). Composição com respiro à
   esquerda pro texto não brigar.
3. (opcional) `scripts/como-funciona_emaus.json` — 4 mini-ilustrações pros passos, OU
   ícones desenhados à mão em SVG (mais leve, decido depois).

Fluxo: escrevo os JSON → usuário roda `python scripts/gerar_imagem_gemini.py
scripts/<arquivo>.json` → `python scripts/preparar_imagens_emaus.py ...` → escolhemos as
melhores no navegador (Claude-in-Chrome agora conecta).

## 7. Ordem de execução

1. **Agora**: usuário aprova/ajusta este plano.
2. Escrevo os JSONs de imagem → usuário gera o lote → escolhemos.
3. Em paralelo: faço **menu + logo (lockups em código)** e a **estrutura nova da
   landing** com placeholders.
4. Troco placeholders pelas imagens escolhidas.
5. Polish: espaçamento, tipografia, hover, responsivo 360→ultrawide, claro/escuro, a11y.
6. Conferência no navegador (prints via Claude-in-Chrome).

## Decisões (usuário, 2026-09-05)

**FICAM ANOTADAS — NÃO implementar agora:**
1. **Amostra grátis** (liberar 1 tópico sem login) — decidir depois; hoje o middleware
   bloqueia tudo menos `/`, `/entrar`, `/criar-conta`. Na landing, o botão "Espiar um
   tópico" por ora leva pro `/entrar` (ou pro tópico já logado).
2. **Depoimentos e FAQ** — as seções NÃO entram nesta rodada. Ficam como TODO pra quando
   houver depoimento real e as perguntas definidas.

**DECIDIDO — implementar:**
- **Carrossel**: rotação automática **com pausa no hover** (+ respeita
  `prefers-reduced-motion`: sem auto-rotação, só setas).
- **Ilustração gerada é a regra em tudo** — herói (carrossel), "como funciona", e o
  símbolo do logo. Nada de ícone SVG genérico onde couber ilustração.
- **Script de recorte de fundo** — estender `preparar_imagens_emaus.py` com um modo
  genérico `recortar <arquivo> <destino>` (pro símbolo do logo e spots de "como
  funciona" que precisam de fundo transparente). O herói mantém o fundo pergaminho
  (faz parte do estilo; entra com máscara/overlay no tema escuro).
- **Menu** organizado de verdade pra navegação — desktop (barra limpa) e mobile (drawer /
  menu que abre), sem a nav espremida de hoje.
- **Aproveitar a largura da tela** — herói e seções usam a largura toda (bleed onde fizer
  sentido), 360px → ultrawide, bonito e profissional.

## Imagens — JSONs pro script (§6 detalhado)

- `scripts/heroi_emaus.json` — 4 ilustrações pro carrossel (estrada de Emaús ao
  entardecer · livro + lamparina · mãos folheando · grupo estudando à luz de vela).
  Composição quadrada/retrato, respiro pro texto.
- `scripts/marca_emaus_v2.json` — 5 símbolos (foco: ler a 24px). Livro+brasa minimal ·
  selo circular · só-brasa · só-livro · traço único.
- `scripts/como_funciona_emaus.json` — 4 spots pequenos e consistentes pros passos.

## Estado

**Rodada 1 (2026-09-05) — código + pipeline de imagem, testado no navegador:**
- **Bug de CSS corrigido**: `globals.css` tinha `img { height: auto }` solto (fora de
  `@layer`), que vencia os utilitários do Tailwind v4 → todo `object-cover` renderizava
  na altura natural da imagem, não na do container. Movido pra `@layer base`. Isso
  quebrava carrossel E capas de curso.
- **Menu novo** (`CabecalhoApp` + `Logo` + `MenuMobile` + `_lib/nav.ts`): barra única no
  desktop, hambúrguer + drawer no mobile. Logo agora usa o **símbolo SVG** (não a
  aquarela borrada), lockup mais equilibrado, variante `empilhado`. `MenuUsuario`
  simplificado (só desktop) usando a lista compartilhada `itensUsuario(papel)`.
- **Landing nova** (`page.tsx`): herói 2 colunas (texto + `Carrossel`), "Como funciona"
  (4 passos numerados), 3 diferenciais repaginados, catálogo separando
  disponível/em-breve + metadado (nível · com tutor), CTA final, rodapé completo.
  Depoimentos e FAQ ficaram de fora (anotados). Botão "Espiar um tópico" leva pro tópico
  se logado, senão `/entrar` (amostra sem login continua anotada).
- **`_ui/Carrossel.tsx`**: rotação automática (5s, confirmada funcionando no navegador),
  pausa no hover/foco, respeita `prefers-reduced-motion`, bolinhas de navegação.
- **`_lib/imagens.ts`**: `slidesHeroi()` usa `/heroi/*.jpg` quando existir, senão cai nas
  capas como placeholder. `imagemExiste()` genérico.
- **Prompts de imagem reescritos bem detalhados** (a pedido do usuário) —
  `scripts/{heroi_emaus,marca_emaus_v2,como_funciona_emaus}.json`.
- **`scripts/preparar_imagens_emaus.py` estendido**: modos `heroi`, `simbolos`,
  `como-funciona`, e `recortar <origem> <destino>` genérico. `recortar_fundo()` virou
  função reusável.

**Rodada 2 (2026-09-05) — imagens geradas (13, via Gemini web / script):**
- Fix no `gerar_imagem_gemini.py`: `insert_text` no lugar de `type(delay=8)` — o editor
  Quill do Gemini novo estourava o timeout com prompt longo (commitado separado).
- `imagem/marca/emaus/v2/` — 5 símbolos → `preparar_imagens_emaus.py simbolos` →
  `emaus-web/public/marca/v2/*.png` (fundo recortado). Página de comparação em
  `emaus-web/app/dev/marca/page.tsx` (`/dev/marca`) — mostra cada um em 6 tamanhos
  (18→140px) sobre claro/escuro + mockup "Emaús".
  - Leitura do Claude (falta o usuário escolher): **`simbolo-traco-unico`** segura melhor
    pequeno e é o mais "logo"; `simbolo-livro-brasa` é o mais bonito grande mas some no
    favicon; `simbolo-selo` só serve grande; `simbolo-brasa`/`simbolo-livro` perdem
    metade do significado (só fogo / só livro).
- `imagem/heroi/emaus/v1/` — 4 ilustrações → `preparar_imagens_emaus.py heroi` →
  `emaus-web/public/heroi/{estrada,lamparina,folhear,grupo}.jpg` (crop quadrado central,
  1200px). **`slidesHeroi()` já pega elas automaticamente** — carrossel do herói agora
  usa as reais (não mais as capas placeholder). Todas no estilo certo (aquarela+tinta,
  pergaminho). Melhores: `estrada` (estrada de Emaús) e `folhear` (mãos no livro).
- `imagem/como-funciona/emaus/v1/` — 4 spots → `preparar_imagens_emaus.py como-funciona`
  → `emaus-web/public/como-funciona/passo-{1..4}-*.png` (fundo recortado). A landing já
  troca o número pelo spot quando o arquivo existe.

**Falta (rodada 3):**
- **Usuário escolher o símbolo do logo** em `/dev/marca` → aplicar no `Logo.tsx`
  (`LogoSimbolo` volta a poder usar `<img>` do escolhido, ou refaço o SVG à mão baseado
  nele) + favicon (`app/icon.svg` ou `.png`) + og-image novos.
- Conferir a landing com as imagens reais no navegador (carrossel + como-funciona) e
  ajustar enquadramento/moldura (o herói tem margem de pergaminho; no tema escuro pode
  precisar de um frame/inner-shadow).
- Curso 9 (Inglês) sem capa — degradê liso. Decidir com a sessão do Inglês.
- Conferência no mobile de verdade.
- Polish: espaçamento fino, hover, claro/escuro, a11y.
- Depoimentos + FAQ (quando o usuário liberar — seguem anotados, fora de escopo).

**Como regerar/reprocessar imagens:**
```
python scripts/gerar_imagem_gemini.py scripts/<marca_emaus_v2|heroi_emaus|como_funciona_emaus>.json
python scripts/preparar_imagens_emaus.py <simbolos|heroi|como-funciona>
```
(dirige o Gemini web num perfil Chrome isolado `~/.nia-playwright-profile`, ~1min/img.)
