# Revisão do front — página por página

Criado em 2026-09-26. Objetivo: revisar cada página do front, anotar problemas e melhorias,
e só depois montar o plano de execução (aprovar antes de mexer).

## Fluxo combinado (2026-09-26)

1. Revisar a página atual (desktop, tablet e mobile) e anotar aqui.
2. Montar o **protótipo em HTML separado** em `prototipos-front/NN-nome.html`, sem Next e com os mesmos tokens e imagens do `emaus-web`.
3. O usuário aprova o protótipo.
4. Só então replicar no `emaus-web`.

## Decisões

- **Estudos pessoais** (Inglês, Engenharia de Agentes LLM, Redes e Câmeras) **saem da vitrine**. Vão pra uma página própria que só o Master vê (ex.: `/estudos`), que entra na fila de protótipos.
- **`/` para visitante sem login**: página curta e direta que apresenta a plataforma e mostra só 3 cursos em destaque (Obreiro I aberto, Panorama da Bíblia e Como Estudar a Bíblia em breve) + "e mais N em preparação". Não mostra a grade completa. CTA principal: **Criar conta grátis**.
- **`/` com login**: redireciona pra `/inicio`.
- **"Esqueceu a senha?"** (2026-09-26): por enquanto só um aviso "peça pra quem administra o Emaús na sua igreja". Recuperação por e-mail fica pra depois (precisa de backend + envio de e-mail).

## Pendências levantadas pelo usuário (2026-09-27)

Anotadas ao aprovar a `/inicio`. Nenhuma foi feita ainda.

### P1. Cadastro simples demais — senha com confirmação ✅ FEITO (2026-09-27)
Hoje `/criar-conta` só pede nome, e-mail e senha (mín. 6). Pedido: **campo "confirmar senha"**
(e revisar o que mais falta no cadastro). Só front: comparar os dois campos antes de enviar e
mostrar erro "as senhas não conferem". Avaliar junto: regra de senha mais forte e mostrar a força.

### P2. "Esqueci minha senha" de verdade
Hoje o link só mostra o aviso "peça pro administrador" (decisão provisória de 2026-09-26).
Pedido: fluxo real de recuperação. Precisa de **backend novo**:
- token de redefinição com validade curta (tabela nova ou campo no `User`), uso único;
- envio de e-mail (escolher serviço — ex.: Resend/Brevo/SMTP; ver custo do tier grátis na hora);
- telas: "informe seu e-mail" → e-mail com link → "crie uma nova senha";
- resposta igual pra e-mail existente e inexistente (não revelar quem tem conta).
Alternativa intermediária, sem e-mail: admin gera um link de redefinição na área de revisão.

### P3. Matrícula: o curso só é "do aluno" quando ele decide fazer
Hoje, na `/inicio`, **todo curso publicado já aparece em "Seus cursos"** pra qualquer aluno.
Pedido: o aluno escolhe o curso ("quero fazer este curso") e só então ele vira dele.
Proposta:
- **Backend:** tabela `Matricula` (`user_id`, `course_id`, `criada_em`, `status`), endpoints
  pra matricular e listar as matrículas do usuário. Soft delete (nunca apagar) ao desistir.
- **`/inicio`:** "Seus cursos" = só os matriculados. Abaixo, "Cursos disponíveis" com o botão
  **"Quero fazer este curso"**. Aluno novo sem matrícula vê direto os disponíveis.
- **`/curso/{id}`:** sem matrícula → página de apresentação do curso com o botão de matrícula;
  com matrícula → a trilha de hoje.
- Liga com a ideia já registrada de liberar curso por usuário / assinatura (memória
  `nia-emaus-pagamento-acesso-curso`): a matrícula é o mesmo registro que um dia pode exigir
  pagamento ou liberação manual.

## Protótipos

| Nº | Arquivo | Página | Status |
|---|---|---|---|
| 01 | `prototipos-front/01-visitante.html` | `/` visitante | ✅ aprovado e aplicado (commit `b3a445c`) |
| 02 | `prototipos-front/02-entrar-criar-conta.html` | `/entrar` + `/criar-conta` | ✅ aprovado e aplicado |
| 03 | `prototipos-front/03-inicio.html` | `/inicio` | ✅ aprovado e aplicado |
| 04 | `prototipos-front/04-curso.html` | `/curso/{id}` | ✅ aprovado e aplicado |
| 05 | `prototipos-front/05-topico.html` | `/topico/{id}` (moldura + slides) | ✅ aprovado e aplicado (vale também pra prova) |
| 06 | `prototipos-front/06-prova.html` | `/topico/{id}/prova` | ✅ aprovado e aplicado |
| 07 | `prototipos-front/07-progresso.html` | `/progresso` | ✅ aprovado e aplicado |
| 08 | `prototipos-front/08-perfil.html` | `/perfil` | ✅ aprovado e aplicado |
| 09 | `prototipos-front/09-preferencias.html` | `/preferencias` | ✅ aprovado e aplicado |
| 10 | `prototipos-front/10-pessoas.html` | `/revisao/pessoas` (+ rodapé logado) | ✅ aprovado e aplicado |
| — | — | `/estudos` (Master) | versão funcional aplicada (mesmos cartões da /inicio); protótipo próprio a fazer |

**Legenda de status:** ⬜ não revisada · 🔍 revisando · 📝 revisada (melhorias anotadas) · ✅ melhorias aplicadas

**O que olhar em cada página:** visual/consistência · mobile (360px) · navegação/fluxo · textos · estados (vazio, carregando, erro) · desempenho

> ⚠️ Antes de começar: há mudanças **não commitadas** em `emaus-web/app/_ui/CartaoContinuar.tsx`,
> `PosterCurso.tsx` e `Prateleira.tsx` (componentes da `/inicio`) — decidir se commita ou descarta.
>
> Pendências da FASE 6 que afetam várias páginas: **escolha do logo** (`/dev/marca`) e **spec da página inicial**.

---

## 🟢 Emaús (`emaus-web/`, dev :4200) — em produção

### Pública / entrada

| Status | Rota | Arquivo | O que é |
|---|---|---|---|
| ✅ | `/` | `app/page.tsx` | Landing pública: hero em carrossel + catálogo de cursos |
| ✅ | `/entrar` | `app/entrar/page.tsx` | Login |
| ✅ | `/criar-conta` | `app/criar-conta/page.tsx` | Cadastro |

### Aluno

| Status | Rota | Arquivo | O que é |
|---|---|---|---|
| ✅ | `/inicio` | `app/inicio/page.tsx` | Home multi-curso estilo streaming (prateleiras, "Continuar estudando") |
| ✅ | `/curso/[courseId]` | `app/curso/[courseId]/page.tsx` | Página do curso, módulos em accordion com o próximo tópico aberto |
| ✅ | `/topico/[topicoId]` | `app/topico/[topicoId]/page.tsx` | Leitor do tópico em slides (iframe), aceita `?slide=N` |
| ✅ | `/topico/[topicoId]/prova` | `app/topico/[topicoId]/prova/page.tsx` | Prova do tópico, com bloqueio quando não tem prova ou o curso não está publicado |
| ✅ | `/progresso` | `app/progresso/page.tsx` | Progresso do aluno |
| ✅ | `/perfil` | `app/perfil/page.tsx` | Perfil |
| ✅ | `/preferencias` | `app/preferencias/page.tsx` | Preferências (tema) |

### Revisão (professor/admin)

| Status | Rota | Arquivo | O que é |
|---|---|---|---|
| ⬜ | `/revisao` | `app/revisao/page.tsx` | Fila de revisão com seletor de curso |
| ⬜ | `/revisao/curso/[courseId]` | `app/revisao/curso/[courseId]/page.tsx` | Revisão de um curso |
| ⬜ | `/revisao/topico/[topicoId]` | `app/revisao/topico/[topicoId]/page.tsx` | Revisão de um tópico |
| ⬜ | `/revisao/alunos` | `app/revisao/alunos/page.tsx` | Lista de alunos |
| ⬜ | `/revisao/aluno/[userId]` | `app/revisao/aluno/[userId]/page.tsx` | Detalhe de um aluno |
| ✅ | `/revisao/pessoas` | `app/revisao/pessoas/page.tsx` | Pessoas (só Master): todo mundo, login, atividade, tempo |
| ✅ | `/revisao/pessoas/[userId]` | `app/revisao/pessoas/[userId]/page.tsx` | Detalhe de uma pessoa (só Master) |

### Dev (fora da navegação)

| Status | Rota | Arquivo | O que é |
|---|---|---|---|
| — | `/dev` | `app/dev/page.tsx` | Vitrine dos componentes de UI |
| — | `/dev/marca` | `app/dev/marca/page.tsx` | 16 conceitos de logo v3 (escolha pendente) |

---

## ⚪ NIA (`frontend/`, dev :4100) — front antigo, parado

| Status | Rota | Observação |
|---|---|---|
| — | `/` | Ainda é a página padrão do Next ("To get started…") |
| — | `/aluno` | Painel do aluno (layouts Retomar/Biblioteca/Trilha) |
| — | `/aluno/explorar` | Catálogo de todos os cursos |
| — | `/aluno/licoes/[lessonId]` | Página da lição (render HTML) |
| — | `/aluno/progresso` | Progresso |
| — | `/aluno/perfil` | Perfil |
| — | `/aluno/preferencias` | Preferências |
| — | `/dev/design-system` | Verificação da Fase 1 |

> Decidir: revisar também ou deixar congelado?

---

## Anotações por página

### `/` — Landing — 2026-09-26

Revisada logada como Master e também sem login (via curl). Larguras testadas: desktop 1370px,
tablet 804px e mobile 375px (iframe, porque a janela do Chrome não fica menor que 500px).
Altura da página: ~5.000px no desktop e **~10.800px no mobile** (umas 18 telas).

**O que já está bom**
- Hero forte: título, subtítulo, ilustração em aquarela e carrossel.
- Tablet: grid de 2 colunas, nav cabe inteira, sem scroll horizontal.
- Mobile: sem scroll horizontal, menu hambúrguer funciona (Início/Cursos/Progresso/Revisão + Perfil/Preferências/Sair).
- Nenhuma imagem quebrada.

**Problemas — conteúdo / posicionamento**
1. 🔴 **O CTA principal é `Começar por "Inglês"`** num site de formação bíblica. Ele pega o *primeiro* curso publicado de `CATALOGO` (`page.tsx:153`), e o primeiro é Inglês. O mesmo CTA aparece de novo no fim da página.
2. 🔴 **Cursos pessoais na vitrine pública**: Inglês, Engenharia de Agentes LLM e Redes e Câmeras aparecem em "Os cursos" como se fossem do Emaús. Isso quebra a promessa "Cursos de Bíblia, doutrina e vida cristã". Precisa decidir: esconder, ou separar numa área "Estudos pessoais" que só o Master vê.
3. 🟠 **"Espiar um tópico →" sem login leva pra `/entrar`**: promete uma prévia e pede login. Ou abre um tópico de amostra público, ou o texto muda.
4. 🟠 **Sem login não existe CTA de "Criar conta"** no hero. O botão manda pro curso, que redireciona pra `/entrar?next=/curso/9`. O "Como funciona" diz "Crie sua conta", mas nenhum botão leva pra `/criar-conta`.
5. 🟠 **Com login, a landing continua falando com visitante**: "Comece hoje. É de graça. Crie a conta…" aparece mesmo pra quem já tem conta. Opções: redirecionar logado pra `/inicio`, ou trocar os textos quando houver sessão.
6. 🟡 **"4 disponíveis · 12 em preparação"**: mais "em breve" que cursos de verdade, o que passa sensação de site vazio. Avaliar mostrar só 3–4 "em breve" com um "ver todos".
7. 🟡 **Obreiro II sem capa**: aparece o placeholder verde "FO".
8. 🟡 **Redes e Câmeras sem capa** (fundo azul liso) e **capa do Engenharia LLM com o título escrito na imagem**, fora do padrão das outras.

**Problemas — visual / componentes**
9. 🔴 **Avatar mostra "M("**: `Avatar.tsx:5` pega a 1ª letra da 1ª e da última palavra de "Master (Atila)". Precisa ignorar pontuação/parênteses.
10. 🟡 No menu mobile os ícones são **emojis coloridos**, enquanto o resto do site usa ícones de traço (SVG). Fica inconsistente.
11. 🟡 Nav ativa marca "Cursos" quando se está em `/` (topo da landing). Pequeno, mas confunde.

**Problemas — mobile**
12. 🟠 **Página longa demais no celular** (~10.800px): "Como funciona" (4 passos) + "Diferenciais" (3) empilhados em uma coluna ocupam ~2.000px antes de chegar nos cursos, e os 16 cards grandes em coluna única ocupam ~7.000px. Sugestões: passos em grid 2×2 compacto ou carrossel horizontal; cards "em breve" menores (lista ou carrossel horizontal).
13. 🟡 No mobile a ilustração do hero fica abaixo da dobra; dá pra reduzir ou encurtar o respiro do hero.

**Problemas — desempenho / acessibilidade**
14. 🔴 **Os 4 ícones do "Como funciona" pesam 2,3 MB** (PNG 479–701 KB cada) e são exibidos a **44px**. Converter pra WebP pequeno (~5–10 KB) ou SVG. Eles ainda recebem preload (`:HL`) no topo.
15. 🟠 **22 imagens, nenhuma com `loading="lazy"`**, e não se usa `next/image`. Total de imagens: ~4,5 MB na primeira carga. As capas em "em preparação" poderiam carregar sob demanda.
16. 🟡 21 de 22 imagens com `alt=""`. Nas decorativas está certo, mas as **capas dos cursos** deveriam ter alt descritivo (ou `aria-hidden` explícito, se o título já descreve).

**Prioridade sugerida**
- **Alta:** 1, 2, 9, 14 (rápidas e visíveis)
- **Média:** 3, 4, 5, 12, 15
- **Baixa:** 6, 7, 8, 10, 11, 13, 16

<!-- Preencher conforme revisa. Modelo:

### /rota — AAAA-MM-DD
**Problemas:**
- ...
**Melhorias propostas:**
- ...
**Prioridade:** alta / média / baixa
-->

### `/entrar` e `/criar-conta` — 2026-09-26

Revisadas no desktop (1366px), tablet (560px) e mobile (375px). Não há scroll horizontal
em nenhuma largura, e o layout em coluna única funciona no celular.

**Problemas**
1. 🔴 **O cadastro vem preenchido com o login salvo no navegador.** Nenhum campo tem `autocomplete`,
   então o Chrome preenche e-mail e senha salvos em `/criar-conta`. Faltam `autocomplete="email"`,
   `current-password` / `new-password` e `name`, que também ajudam o gerenciador de senhas a salvar a conta nova.
2. 🟠 **Sem saída**: nenhum cabeçalho, e o logo não é link. Quem chegou pelo "Criar conta grátis" não
   tem como voltar pra página inicial.
3. 🟠 **Desktop vazio**: um form de 320px no meio de uma tela creme. Não reforça o que a pessoa ganha
   ao criar a conta, e a página de visitante promete "grátis · sem cartão · leva um minuto".
4. 🟠 **Sem "Esqueci minha senha"**: o backend não tem fluxo de recuperação (`routers/auth.py`).
   Precisa decidir: fluxo por e-mail (backend novo) ou, por enquanto, "fale com o administrador".
5. 🟡 **Senha**: sem botão de mostrar/ocultar; no cadastro, a regra de "mínimo 6 caracteres" só aparece
   no erro do navegador.
6. 🟡 **Quem já está logado** consegue abrir `/entrar` e `/criar-conta`; deveria ir pra `/inicio`.
7. 🟡 **`/criar-conta` ignora `?next=`**: quem veio de um curso específico cai sempre em `/inicio`.
8. 🟡 **Autofill** pinta o campo de azul claro (padrão do Chrome), fora da paleta.
9. 🟡 **Mensagem de erro** sem `aria-live`: leitor de tela não anuncia.

**Prioridade sugerida**
- **Alta:** 1, 2
- **Média:** 3, 4, 5, 6
- **Baixa:** 7, 8, 9

### `/inicio` — 2026-09-27

Revisada logada como Master, no desktop (1366px), tablet (768px) e mobile (375px).

> Antes da revisão: `CartaoContinuar.tsx`, `PosterCurso.tsx` e `Prateleira.tsx` tinham alterações
> nunca commitadas (22/09 00:24) que quebravam a página (ex.: um "0" solto embaixo do pôster).
> Com a aprovação do usuário, elas foram salvas em `backups/wip-inicio-2026-09-22.patch` e os
> arquivos voltaram pra versão do commit.

**O que já está bom**
- Sem scroll horizontal da página em nenhuma largura; as prateleiras deslizam de lado como esperado.
- Nav, cabeçalho e rodapé já com o logo novo.

**Problemas**
1. 🔴 **Estudos pessoais visíveis e acessíveis pra qualquer aluno.** A prateleira "Estudos pessoais"
   aparece pra todo mundo logado e, como Inglês, Engenharia LLM e Redes estão publicados, o aluno
   consegue abrir e fazer esses cursos. Decisão já tomada: vão pra uma página só do Master (`/estudos`).
   Precisa bloquear também o acesso direto em `/curso/{id}` pra quem não é Master.
2. 🔴 **"Continuar estudando" quebrado (também em produção).** A capa ocupa o cartão inteiro e o
   texto fica com 0px: `CapaCurso` já traz `w-full`, que vence o `w-16` passado pelo `CartaoContinuar`
   (o mesmo conflito de classe que o comentário do `CapaCurso.tsx` avisa).
3. 🟠 **Prateleira "Formação bíblica" com 13 cursos, 11 "Em breve"**: mais cadeado do que curso;
   o que dá pra estudar se perde no meio.
4. 🟠 **Títulos cortados**: "Formação do Obreiro: Do C…" nos dois obreiros, e fica impossível
   distinguir o I do II.
5. 🟡 **Saudação "Bom te ver de volta, Master"** pega a 1ª palavra de "Master (Atila)"; o avatar
   continua "M(" (achado 9 da `/`).
6. 🟡 **Obreiro II "Em breve" até pro revisor**, sem capa (placeholder "FO"); Redes sem capa ("RC").
7. 🟡 **Barra de rolagem aparente** embaixo da prateleira no desktop.

**Prioridade sugerida**
- **Alta:** 1, 2
- **Média:** 3, 4
- **Baixa:** 5, 6, 7

### `/curso/{id}` — 2026-09-27

Revisada logada como Master, com o curso 8 (Obreiro I), no desktop (1366px), tablet (768px) e
mobile (375px). O banco local ainda tem o curso 8 **antes da divisão** (7 módulos, 5 tópicos
com conteúdo).

**O que já está bom**
- Sem scroll horizontal da página; o accordion de módulos funciona e abre o módulo do próximo tópico.
- Estado de cada tópico legível (✓ concluído, anel no atual, "…" em preparação) e chip da prova
  travado até concluir (link irmão, não aninhado — correto).

**Problemas**
1. 🔴 **Capa do curso ocupa a primeira tela inteira** (16:9 na largura toda ≈ 1116×628 no desktop):
   o aluno abre o curso e não vê progresso, nem "continuar", nem módulos sem rolar.
2. 🔴 **Imagens pesadas**: capas em PNG servidas pelo backend — capa do curso 1,3 MB, módulo 1
   1,9 MB, módulo 2 1,1 MB… ≈ 8 MB só de capas numa página. Converter pra WebP/JPG ~150 KB e
   carregar as dos módulos sob demanda (`loading="lazy"`).
3. 🟠 **Título escrito dentro da imagem e diferente do catálogo**: a capa diz "Formação Geral do
   Novo Obreiro Cristão" (título antigo no banco), a vitrine diz "Formação do Obreiro: Do Chamado ao
   Serviço I". O `<h1>` real fica escondido (`sr-only`).
4. 🟠 **Capa de cada módulo corta o texto desenhado nela** (faixa de 144px de altura mostra
   "E FUNDAMENTO BÍBLICO" pela metade). Todas as 7 faixas aparecem, uma por módulo, deixando a
   página com ~3.400px.
5. 🟠 **"Continuar em …" é um link pequeno de texto**, não um botão — a ação principal da página
   some no meio.
6. 🟡 Módulos "em preparação" ocupam o mesmo espaço dos que têm conteúdo (com capa grande).
7. 🟡 **Nav no tablet (768px) quebra em 2 linhas** ("Meu progresso", "Estudos pessoais") desde que
   o item "Estudos pessoais" entrou — afeta todas as páginas logadas.
8. 🟡 **Tema herdado entre contas no mesmo navegador**: depois de entrar como Aluno (tema escuro),
   o Master voltou em tema escuro — o cookie `tm_theme` não é refeito no login.

**Prioridade sugerida**
- **Alta:** 1, 2, 5
- **Média:** 3, 4, 7
- **Baixa:** 6, 8

### `/topico/{id}` — moldura + slides — 2026-09-27

Escopo **B** (decisão do usuário): a moldura do `emaus-web` **e** os slides renderizados pelo
backend (`backend/app/renderer/templates/topico.html.j2`, 2.567 linhas; temas em
`docs/schema/temas.json`). Revisado com o Tópico 1 (Sacerdócio, tema `trigo-maduro`, 15 slides:
capa, 10 de conteúdo, 3 checkpoints, resultado). O dev do Next caiu por falta de memória
(0,9 GB livres), então os slides foram revisados direto pelo backend (`:8100/topicos/1/render`).

**Problemas**
1. 🔴 **Os slides nunca usaram a fonte do tema (bug, também em produção).** O Jinja escapa as
   aspas dos nomes de fonte dentro do `<style>` (`&#39;Fraunces&#39;`), o CSS fica inválido e o
   navegador cai em **Times New Roman / Arial**. Afeta todos os temas com nome de fonte entre aspas.
   Correção: `| safe` nos 4 pontos do template (linhas 256, 257, 261, 714) — valores vêm do
   `temas.json`, que é nosso.
2. 🔴 **Imagens pesadíssimas**: ~11 MB só de imagens no Tópico 1 (`pedras-vivas.jpg` 3,8 MB em
   4032×3024, direto da câmera; capa 2,5 MB; outras 1,2–1,3 MB). Converter pra WebP/JPG ~1600px
   (~150–250 KB) e `loading="lazy"` depois do 1º slide.
3. 🟠 **Três faixas de cabeçalho empilhadas**: barra do Emaús ("Voltar ao curso · aula · Tópico X de Y ·
   Recomeçar · logo") + barra do slide ("Tópico 1 · título · Corrido · Claro · 1/15 · ⛶") + rótulo da
   seção. No celular, as barras fixas somam ~200px de 560 → sobra ~360px pra ler.
4. 🟠 **Rótulo da seção mostra o código interno** ("PEDRAS-VIVAS", "TEXTO-CENTRAL") em vez do
   título ("Pedras Vivas, Casa Espiritual").
5. 🟠 **Botões flutuantes (❓ dúvida, ✍️ anotação) ficam por cima do conteúdo** — sobre o texto e a
   imagem.
6. 🟠 **Capa corta o título desenhado na imagem** ("SACERDÓCIO" some) — mesmo problema das capas
   com texto embutido.
7. 🟡 **No celular o título do tópico quebra em 3 linhas** na barra do slide.
8. 🟡 **Imagem "grudada" (sticky) de 223px** no conteúdo do desktop: ocupa boa parte da tela baixa.
9. 🟡 **"↺ Recomeçar" usa `window.confirm()`** (caixa nativa do navegador), fora do visual.
10. 🟡 **Mensagens do iframe sem checar origem** (`topico-ui.tsx` aceita `postMessage` de qualquer
    janela); risco baixo, mas o certo é aceitar só do backend.

**Prioridade sugerida**
- **Alta:** 1 (correção de 4 linhas), 2, 3
- **Média:** 4, 5, 6
- **Baixa:** 7, 8, 9, 10

**Aplicado em 2026-09-27**
- Template `topico.html.j2`: fontes com `| safe` (Fraunces/Source Sans voltaram); barra de cima
  única (voltar · onde · título · menu ⋯ com corrido/tema/tela cheia/PDF/Recomeçar); progresso
  segmentado com losango nos checkpoints; rótulo de seção com código interno escondido; ✍️/❓ na
  barra de baixo; imagem sem "sticky" e com teto de 42% da tela; letras A/B/C nas opções;
  "Recomeçar" com diálogo da página (tópico e prova); setas não trocam slide enquanto digita;
  só aceita mensagem do próprio pai.
- Imagens: `backend/scripts/otimizar_imagens.py` gera cópias `.otim.webp` (1600px, q80) ao lado
  das originais; filtro `imagem_web` no `render.py` usa a cópia se existir. 110 imagens:
  **61,3 MB → 6,6 MB**. Originais intactas. **Em produção: rodar o script no servidor.**
- `emaus-web`: tópico e prova sem a barra própria (passam `?onde=`); removidos os 2 botões
  "Recomeçar" com `window.confirm`; prova trata o "Recomeçar" do menu; tópico e prova só aceitam
  `postMessage` da origem do backend.
- Testado: tópico, prova e modo revisão (render direto + página de teste temporária no backend,
  já apagada); voltar e Recomeçar pelo Emaús; celular 375px (barras 139px, sem scroll lateral).

### `/topico/{id}/prova` — 2026-09-27

Já herdou a barra única do render (commit `2ed9426`). Revisada com a prova 17 (7 slides:
intro, 3 objetivas, 2 abertas, resultado) direto pelo backend, e a tela de bloqueio como Aluno.

**Problemas**
1. 🔴 **Texto errado na introdução de 16 das 18 provas**: "a avaliação final de verdade acontece
   quando você levar o resumo desta tela pro chat com o Claude" — da época em que o tutor era
   externo. Vem fixo do gerador (`backend/app/agents/montar_topico.py`), então toda prova nova
   nasce com ele. Corrigir o gerador + script de dados (com backup) pras provas existentes
   (local e produção).
2. 🔴 **A ação principal do resultado está escondida**: o slide diz "Clique em 'Fim', embaixo, pra
   enviar sua avaliação" — o envio pro tutor depende de um botão pequeno na barra de baixo.
3. 🟠 **Resposta certa aparece em laranja (cor de destaque), não verde**, e certo/errado só por cor
   (sem ✓/✗ escrito) — confunde com "selecionada" e não funciona pra daltônico.
4. 🟠 **Progresso da prova embolado**: com 5 de 7 slides sendo pergunta, os losangos se amontoam no
   meio e intro/resultado ocupam metade da barra cada.
5. 🟠 **Tela "Termine o tópico primeiro"** usa a barra antiga do Emaús (diferente da nova), botão
   fantasma "Voltar ao tópico" e muito vazio. Mesmo visual antigo em "Curso em preparação" e
   "Tópico em preparação".
6. 🟡 Pergunta sem "Questão X de 5"; só o tipo ("Múltipla escolha").
7. 🟡 Rótulos técnicos no resultado: "Acertos automáticos", "Respostas com alta confiança e erro".
8. 🟡 Caixa da resposta aberta com 2 linhas (pequena pra resposta de 2 partes).

**Prioridade sugerida**
- **Alta:** 1, 2
- **Média:** 3, 4, 5
- **Baixa:** 6, 7, 8

**Aplicado em 2026-09-27**
- Template: verde de acerto (`--good`, os temas não tinham) com "✓ Correta" / "✗ Sua resposta"
  escritos — vale também pros checkpoints do tópico; "Questão X de N"; intro com números contados
  das perguntas (questões · abertas · ~minutos); caixa da aberta maior; resultado com rótulos
  simples e botão grande **"Enviar pro tutor corrigir →"** no slide (o "Fim" da barra some
  quando embutido); estado "O tutor está corrigindo…" com animação; progresso sem losangos
  quando a maioria dos slides é pergunta.
- Gerador (`montar_topico.py`): intro nova. Dados: `backend/scripts/corrigir_intro_provas.py`
  corrigiu 16 provas locais (backup `backend/_backup_intro_provas_2026-09-27_2009.json`).
  **Em produção: rodar `docker exec nia_backend python scripts/corrigir_intro_provas.py --aplicar`.**
- `emaus-web`: `_ui/TelaAviso.tsx` (barra igual à do render + ícone + passos + botão principal)
  em "a prova abre quando concluir o tópico", "tópico em preparação" e "curso em preparação".

### `/progresso` — 2026-09-27

Revisada logada como Master (desktop). Página simples: título, barra do curso, aviso e a lista de
tópicos agrupada por aula (`_ui/LinhaDoTempoTopicos.tsx`, também usada em `/revisao/aluno/[id]`).

**Problemas**
1. 🔴 **Um curso só, fixo no código** (`TEOLOGIA_COURSE_IDS[0]` = Obreiro I). Quem faz outro curso
   não vê o próprio progresso. E usa o título antigo do banco ("Formação Geral do Novo Obreiro
   Cristão").
2. 🟠 **Mensagens que se contradizem**: "Você ainda não concluiu nenhum tópico. Comece pelo
   primeiro" + botão "Começar: …" enquanto a lista mostra o 1º tópico "Continuar · Em andamento
   desde 6 de set".
3. 🟠 **"Disponível" com "Em andamento desde 5 de set"**: o selo usa o estado da árvore (só o 1º
   não concluído é "atual"), mas a data vem do progresso real — tópico começado aparece como
   "Disponível".
4. 🟠 **As provas não aparecem** (nem feita, nem veredito), apesar de o dado existir
   (`listAvaliacaoProgress`).
5. 🟡 **Cada tópico é um cartão alto** (selo + título + data + link "Abrir tópico" em 3 linhas):
   com 50+ tópicos por curso a página fica enorme.
6. 🟡 Tempo de estudo só aparece se > 0 e fica escondido numa linha pequena.

**Prioridade sugerida**
- **Alta:** 1
- **Média:** 2, 3, 4
- **Baixa:** 5, 6

**Aplicado em 2026-09-27**
- `_lib/progresso.ts`: junta todos os cursos em que o aluno já estudou (estudos pessoais só pro
  Master) + progresso das provas + resumo geral.
- `/progresso`: resumo (concluídos · dominados · provas · tempo), um bloco por curso com
  Continuar, estado vazio "Você ainda não começou nenhum curso".
- `_ui/LinhaDoTempoTopicos.tsx` compacto, por módulo (abre onde o aluno está), linha inteira é
  link, "Em andamento" pra tópico começado, chips de tutor e prova. Também muda o visual de
  `/revisao/aluno/[id]` (cartão em volta) — o cabeçalho dessa página ainda é de 1 curso só e com
  título antigo: fica pra revisão das páginas de revisão.
- Testado: Master com 3 cursos (Inglês, Engenharia, Obreiro I), celular 375px sem scroll lateral,
  aluno sem progresso vê o estado vazio e não vê curso pessoal.

### `/perfil` — 2026-09-27

Revisada logada como Master (desktop).

**Problemas**
1. 🟠 **"Estudo" fixo num curso só** (`TEOLOGIA_COURSE_IDS[0]`), com o título antigo do banco e
   0% — e repete, pior, o que a `/progresso` já mostra.
2. 🟠 **Não dá pra trocar a senha.** Só o nome é editável; o backend também não tem esse
   recurso (só `/auth/register` e `/auth/login`). Liga com as pendências P1 (senha no cadastro) e
   P2 (esqueci a senha).
3. 🟡 **Sem "Sair" nem atalho pra Preferências** na página — só no menu do avatar.
4. 🟡 **Página quase vazia** (avatar, nome e uma barra); sem "membro desde".

**Prioridade sugerida**
- **Média:** 1, 2
- **Baixa:** 3, 4

**Aplicado em 2026-09-27**
- Backend: `POST /auth/trocar-senha` (schema `TrocarSenha`, mínimo 6, exige a senha atual, recusa
  nova igual à atual; o token atual continua valendo). Testado: atual errada, nova curta, troca
  ok, login com a antiga falha, volta ao original.
- `emaus-web`: `/api/senha` (proxy com o token httpOnly); `/perfil` com conta (nome editável,
  papel, e-mail, "no Emaús desde"), "Seu estudo" com dados reais de todos os cursos + "Ver meu
  progresso", trocar senha (atual + nova + confirmar), atalho Preferências e Sair.
- **Pendência P1 feita**: "Confirme a senha" no `/criar-conta` (aviso ao digitar + bloqueia envio).

### `/preferencias` — 2026-09-27

Revisada logada como Master (desktop). Tema (claro/escuro) + tamanho do texto (P/M/G), salvos
na conta e no cookie.

**Problemas**
1. 🟠 **Não vale pros slides** — onde o aluno passa quase todo o tempo. O render dos slides tem o
   próprio botão de tema (guardado à parte, `localStorage` do backend) e não tem tamanho de
   texto; a URL do render só recebe o tema do curso, não o modo claro/escuro nem a fonte.
2. 🟡 **Sem "Automático"** (seguir o tema do aparelho).
3. 🟡 **Os 3 tamanhos quebram em 2 linhas** ("Grande" cai pra baixo) e não há prévia do efeito.

**Prioridade sugerida**
- **Média:** 1
- **Baixa:** 2, 3

**Aplicado em 2026-09-27**
- Tema **"Automático"**: backend aceita `auto` (CHECK recriada em `main.py`, roda sozinha no
  start — **em produção entra no deploy**); CSS usa as cores escuras quando o aparelho está no
  escuro; botão ☾/☀ do cabeçalho troca pro oposto do que está na tela.
- `/preferencias`: Aparência (Claro · Escuro · Automático com amostras), Tamanho do texto numa
  linha, prévia ao vivo.
- **Valem nos slides**: o Emaús passa `?modo=&fonte=` pro render (tópico e prova); o render
  aplica o tema pedido (vale mais que o botão salvo no navegador) e o tamanho via `zoom` no
  slide. Testado: site escuro + grande → slides escuros e maiores; celular 375px sem estourar.

### `/revisao/pessoas` + rodapé logado — 2026-09-28

**Pedido:** o Master precisa ver se os admins entram e leem o curso, ver todo mundo (alunos
e equipe) e quando/quanto tempo cada um estuda. O rodapé logado de produção estava estranho
(logo, links em coluna, linha embaixo).

**Aplicado**
- **Rodapé** numa linha só (logo + assinatura à esquerda, links à direita), logado e visitante.
- **Pessoas** (só Master; admin/professor continuam em `/revisao/alunos`): resumo (cadastrados,
  estudaram em 7 dias, concluídos, admins/professores sem concluir nada), filtro por papel,
  busca, ordenação; tabela no desktop, cartões no celular. Detalhe: números + tópicos por curso
  com datas, slide onde parou, tempo, tutor e prova. Sub-nav da revisão: Master vê "Pessoas".
- **Backend:** `GET /pessoas/` e `/pessoas/{id}` (router → `services/pessoas_service.py`, 403 pra
  quem não é master). Login e cadastro gravam `users.last_login` (antes nunca era gravado).
- **Tempo de estudo:** o render manda `POST /{topico|avaliacao}-progress/{id}/tempo` a cada minuto
  se a aba está visível e houve interação nos últimos 10 min; o backend soma 60s e ignora sinal
  com menos de 50s do anterior (coluna nova `ultimo_sinal_em`, migration em `main.py`). Revisão
  (`?contexto=revisao`) não conta.
- **Histórico:** login e tempo só existem a partir do deploy — a página avisa.
- Testado: 375/800/1280 sem estourar; aluno recebe 403; sinal repetido não soma; sinal real do
  render chegou e somou 60s (minuto de teste desfeito no banco local).

