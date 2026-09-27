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

## Protótipos

| Nº | Arquivo | Página | Status |
|---|---|---|---|
| 01 | `prototipos-front/01-visitante.html` | `/` visitante | ✅ aprovado e aplicado (commit `b3a445c`) |
| 02 | `prototipos-front/02-entrar-criar-conta.html` | `/entrar` + `/criar-conta` | ✅ aprovado e aplicado |
| 03 | `prototipos-front/03-inicio.html` | `/inicio` | ✅ aprovado e aplicado |
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
| ⬜ | `/curso/[courseId]` | `app/curso/[courseId]/page.tsx` | Página do curso, módulos em accordion com o próximo tópico aberto |
| ⬜ | `/topico/[topicoId]` | `app/topico/[topicoId]/page.tsx` | Leitor do tópico em slides (iframe), aceita `?slide=N` |
| ⬜ | `/topico/[topicoId]/prova` | `app/topico/[topicoId]/prova/page.tsx` | Prova do tópico, com bloqueio quando não tem prova ou o curso não está publicado |
| ⬜ | `/progresso` | `app/progresso/page.tsx` | Progresso do aluno |
| ⬜ | `/perfil` | `app/perfil/page.tsx` | Perfil |
| ⬜ | `/preferencias` | `app/preferencias/page.tsx` | Preferências (tema) |

### Revisão (professor/admin)

| Status | Rota | Arquivo | O que é |
|---|---|---|---|
| ⬜ | `/revisao` | `app/revisao/page.tsx` | Fila de revisão com seletor de curso |
| ⬜ | `/revisao/curso/[courseId]` | `app/revisao/curso/[courseId]/page.tsx` | Revisão de um curso |
| ⬜ | `/revisao/topico/[topicoId]` | `app/revisao/topico/[topicoId]/page.tsx` | Revisão de um tópico |
| ⬜ | `/revisao/alunos` | `app/revisao/alunos/page.tsx` | Lista de alunos |
| ⬜ | `/revisao/aluno/[userId]` | `app/revisao/aluno/[userId]/page.tsx` | Detalhe de um aluno |

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
