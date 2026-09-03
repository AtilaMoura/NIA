# Prompt — pedido de sugestão de UX/mapa de páginas pro lado do aluno do NIA

> Cole isso numa conversa nova com outra IA. O pedido é só pra **mapear e sugerir**, não pra gerar código — isso eu já resolvo depois com a Claude Code, que já conhece a base inteira.

---

## O que é o NIA

O NIA é uma plataforma que gera cursos completos usando IA — não é um CMS onde alguém escreve aula manualmente. O fluxo é: um admin (só eu, por enquanto) pede um curso sobre um assunto, nível e objetivo; um pipeline de agentes de IA gera a estrutura (módulos e tópicos), depois gera o conteúdo de cada tópico, um revisor de IA aprova ou reprova cada lição antes dela ficar disponível pro aluno, e um "tutor" de IA avalia o que o aluno aprendeu ao final de cada lição. A venda do curso em si (pagamento, checkout) fica **fora** do NIA — plataforma externa tipo Hotmart/Kiwify. O NIA só precisa organizar o conteúdo e entregar a experiência de estudo.

Stack: backend FastAPI + SQLAlchemy + PostgreSQL (Docker); frontend Next.js 16 (App Router) + TypeScript + Tailwind v4.

## Como o conteúdo de uma lição é estruturado (isso já está pronto e funcionando)

Cada lição vira um JSON estruturado (não é texto livre nem Markdown) com uma sequência de **slides**: capa, slides de conteúdo (blocos reutilizáveis — definição, analogia, aplicação, comparação antes/depois, timeline, cards, diagrama), **checkpoints** (perguntas de múltipla escolha, verdadeiro/falso, classificação ou resposta aberta, que **bloqueiam** o avanço até serem respondidas), e um slide final de avaliação com resumo automático pra colar num chat. Um renderizador determinístico transforma esse JSON em HTML interativo — com narração por voz (TTS do navegador), tela cheia, 4 temas visuais de lição já prontos (Vidro Fumê, Estufa Noturna, Console Verde, Aurora Botânica). O aluno responde as perguntas objetivas na hora (correção automática) e as abertas ficam registradas; no fim ele cola um resumo estruturado e uma IA "Tutor" decide se ele **dominou** o tópico ou precisa de reforço — só então ele pode avançar pro próximo.

Isso funciona bem pra conteúdo **conceitual** (explicar um assunto, checar entendimento). A gente já identificou uma limitação real: pra assuntos que pedem prática intensiva e repetitiva (ex.: exercícios de idioma), esse modelo de "slide com checkpoint que aparece uma vez só" não é suficiente — não tem fila de exercícios, não tem repetição do que errou. Isso já está registrado como uma frente futura (um tipo de conteúdo irmão, tipo "prática", com mecânica de fila/repetição em vez de slide linear) — ainda não implementado.

## Sistema de identidade visual (já implementado)

5 "humores" de cor, cada um pensado pra uma família de assunto — a ideia é que a categoria do curso no futuro determine o humor automaticamente (não é escolha solta):

- **Musgo** (verde) — Bem-estar & Natureza
- **Âmbar** (dourado) — Negócios & Carreira
- **Maré** (azul-petróleo) — Tecnologia & Dados
- **Framboesa** (rosa/vermelho) — Criativo & Comunicação
- **Lavanda** (roxo) — Humanas & Idiomas

Cada humor tem variante clara/escura. Isso é a "moldura" do app (painel, navegação) — diferente do sistema de 4 temas de lição mencionado acima, que é só o conteúdo do slide.

## O que já existe no lado do aluno hoje (mapa atual de páginas)

1. **Painel** (`/aluno`) — com **3 variantes de layout** que o aluno escolhe: "Retomar" (hero de continuar + grade de cursos, padrão de fábrica), "Biblioteca" (sidebar + grade filtrável por status), "Trilha" (caminho vertical mostrando cada lição do curso atual como concluída/atual/bloqueada). Mostra os cursos com card clicável, badge de status (em andamento/concluído/sugerido) e barra de progresso.
2. **Página da lição** (`/aluno/licoes/[id]`) — o conteúdo interativo em tela cheia (iframe do renderizador), com botão de expandir de verdade pra fullscreen do navegador.
3. **Avaliação** — painel abaixo da lição onde o aluno cola o resumo gerado no fim do estudo e recebe o veredito do Tutor (dominado / precisa reforçar) com diagnóstico em texto.
4. **Preferências** (`/aluno/preferencias`) — escolher humor, modo claro/escuro e layout do painel, persistido de verdade no banco (não é só front).
5. **Progresso** (`/aluno/progresso`) — histórico de todas as avaliações do Tutor, agrupado por curso, com veredito e diagnóstico de cada lição avaliada.

**O que ainda não existe**: login/cadastro de verdade (autenticação ainda não implementada — hoje tudo roda com um usuário fixo de teste), qualquer coisa do lado do admin (a fila de aprovação e o assistente de criação de curso existem só via API/scripts de teste, sem UI).

## Dados do usuário que já existem no banco mas **não aparecem em nenhuma tela**

O model `User` já tem campos de gamificação prontos, sem nenhuma UI usando eles ainda: `total_points` (pontos), `level` (nível 1-100), `badges` (lista de conquistas), `streak_days` (sequência de dias de estudo), `preferred_topics`, `learning_style`. Isso é um sinal de que o produto foi pensado pra ter uma camada de engajamento/gamificação que nunca chegou a virar tela.

## Onde a gente sente que está "cru"

- O painel é puramente funcional — lista curso, mostra progresso, não tem nenhum elemento de motivação, celebração ou identidade (sem uso da gamificação que já existe no banco).
- Não existe uma tela de "Explorar" (catálogo completo de cursos disponíveis, só o que o aluno já começou aparece).
- Não existe tela de "Perfil" (conta, estatísticas, conquistas).
- Não existe nenhum tipo de notificação, lembrete, ou incentivo pra voltar a estudar.
- Um curso hoje é uma "ilha" — a visão de categorizar cursos por nicho (ex.: "Programação", "Jardinagem", cada um com identidade visual própria ligada ao humor de cor) já foi decidida como direção, mas ainda não implementada; não sabemos ainda como isso deveria aparecer na navegação do aluno.
- Tudo foi construído em ordem de dependência técnica (design system → fluxo → preferências → progresso), não em ordem de "o que faz o produto parecer profissional" — por isso o resultado parece funcional mas amador.

## O que eu peço

Considerando tudo isso — o tipo de conteúdo (estudo ativo estruturado, não vídeo-aula), o sistema visual que já existe, os dados de gamificação parados no banco, e as 5 páginas que já existem — **mapeie o conjunto completo de páginas que o lado do aluno de uma plataforma de cursos séria e profissional deveria ter**, e pra cada página nova ou já existente, descreva:

- o propósito dela (por que ela precisa existir, que problema resolve pro aluno);
- os elementos-chave que deveria ter pra parecer um produto maduro (não uma lista genérica de "seção A, seção B" — pensando no que citei de gamificação/motivação/identidade);
- como ela se conecta com as páginas que já existem.

Não preciso de código nem de wireframe visual — preciso do mapa de páginas com essa descrição de conteúdo/propósito por página, pra eu levar de volta pra implementação.
gemini pro:
Aqui está o mapeamento completo e definitivo do lado do aluno, estruturado para você entregar direto à ferramenta de código. Assumindo a Trilha como a fundação de engajamento principal, o ecossistema passa a ter 6 rotas interconectadas que ativam toda a gamificação e o sistema de humores que já existiam no seu banco.1. Painel Principal (/aluno) — O Motor de FocoPropósito: Ditar o ritmo de estudo e remover a fricção de decidir o que estudar a seguir, mantendo o aluno focado no curso atual.Estrutura & UI:HUD Superior (Gamificação): Barra fixada exibindo o level atual (1-100), total_points e um contador com ícone indicando os streak_days (dias seguidos de estudo). A Trilha Principal (Layout ativo): Uma visualização vertical mostrando o caminho do curso em andamento. Os nós anteriores aparecem como concluídos, o nó atual fica em destaque (pulsando ou com botão de ação primária), e os próximos aparecem bloqueados. Imersão Visual: O fundo ou os acentos da interface adotam automaticamente a cor correspondente ao humor do curso em andamento (ex: azul-petróleo para Tecnologia/Maré). Conexões: O nó ativo da trilha joga o usuário direto para /aluno/licoes/[id]. Um clique no HUD de nível leva para /aluno/progresso. 2. Meus Cursos / Biblioteca (/aluno/cursos) — A Visão PanorâmicaPropósito: Como a página inicial agora é ultra-focada em um único curso (a Trilha), o aluno precisa de um local secundário para gerenciar tudo o que já começou, pausou ou concluiu.Estrutura & UI:Layout em Grade Filtrável: Organização clássica com abas ou filtros para "Em andamento", "Concluídos" e "Sugeridos". Cards Enriquecidos: Cada card mostra a barra de progresso percentual, o humor de cor do nicho, e uma badge clara indicando o último veredito do Tutor de IA (se ele precisa reforçar algo ou se dominou o assunto). Conexões: Clicar em um curso inativo o define como a nova Trilha principal em /aluno.3. Explorar (/aluno/explorar) — O Catálogo de DescobertaPropósito: Quebrar o efeito de "ilha" dos cursos, mostrando ao aluno a vastidão do conteúdo gerado pela IA e incentivando novas matrículas.Estrutura & UI:Vitrine Dinâmica: Uma seção de recomendações gerada a partir do campo preferred_topics do aluno. Navegação por Humores: Trilhos de conteúdo divididos explicitamente pelo sistema visual implementado: Musgo (Bem-estar), Âmbar (Negócios), Maré (Tecnologia), Framboesa (Criativo) e Lavanda (Humanas). Preview do Curso: Ao clicar em um card, um modal ou drawer exibe a estrutura gerada pelo pipeline de agentes de IA (módulos, tópicos e objetivos) antes do aluno iniciar. Conexões: Confirmar o início de um curso leva o usuário diretamente para a primeira lição.4. O Ambiente de Estudo (/aluno/licoes/[id]) — Imersão & AvaliaçãoPropósito: Entregar o conteúdo conceitual ativo através do renderizador de JSON, sem distrações do resto da plataforma. Estrutura & UI:Tela Cheia Obrigatória: O renderizador determinístico ocupa o navegador utilizando os temas visuais específicos da lição (Vidro Fumê, Estufa Noturna, Console Verde, Aurora Botânica). Avanço Bloqueado: A navegação através dos blocos (analogias, diagramas) pausa nos checkpoints (perguntas de múltipla escolha, verdadeiro/falso). O sistema corrige automaticamente as respostas fechadas e registra as abertas. Console do Tutor (Pós-Lição): No slide final, um painel estruturado aparece para o aluno colar o seu resumo. Feedback & Recompensa: Se o veredito da IA Tutor for "dominado", uma animação dispara atualizando os total_points do aluno, o botão de avanço é liberado e o sistema avalia se alguma nova badge foi conquistada. Conexões: O botão de retorno volta para /aluno. O botão de avanço puxa o próximo ID de lição. 5. Meu Desempenho (/aluno/progresso) — Reputação & HistóricoPropósito: Dar utilidade visual aos dados de gamificação parados no banco e manter um registro claro da evolução do aprendizado.Estrutura & UI:Histórico de Diagnósticos: O registro atual agrupado por curso, detalhando os textos onde o Tutor apontou o que precisa de reforço e o que foi dominado. Mural de Conquistas (Sala de Troféus): Uma nova interface utilizando a lista de badges do usuário. Mostra ícones coloridos para conquistas desbloqueadas (ex: "5 Dias Seguidos") e silhuetas cinzas para objetivos ainda não alcançados. Status de Nível: Um gráfico mostrando a distância em pontos (total_points) para o próximo level. 6. Perfil & Preferências (/aluno/preferencias) — Controle & IdentidadePropósito: Gestão técnica da conta e flexibilidade na interface.Estrutura & UI:Motor Visual: Opções para persistir no banco de dados a escolha de modo claro/escuro e o layout alternativo do painel (caso o aluno prefira o estilo "Retomar" ou "Biblioteca" no lugar da "Trilha"). Setup de Aprendizado: Formulários simples vinculados aos campos preferred_topics e learning_style para direcionar a experiência da plataforma. Gestão de Conta: Espaço reservado para a futura integração de autenticação de verdade, onde ficarão e-mail, senha e logout.

gamini fash:
Mapeamento Geral da Estrutura de Navegação
A plataforma passa a se organizar em 5 seções principais no menu/sidebar do aluno, além da tela imersiva da lição:

Início (Painel) — Foco: Momento presente, consistência e impulso rápido.

Meus Cursos (Biblioteca / Trilha) — Foco: Gestão do aprendizado em andamento.

Explorar (Catálogo & Categorias) — Foco: Descoberta, valor percebido e expansão.

Meu Desempenho (Progresso & Conquistas) — Foco: Gamificação, histórico e diagnostico da IA.

Perfil & Ajustes — Foco: Identidade, dados pessoais e preferências.

1. Início (/aluno) — Painel de Bordo & Motivação
   Propósito: Deixar de ser um mero "gerenciador de links" para virar um hub diário de motivação. Ele responde instantaneamente a três perguntas do aluno: "Onde eu parei?", "Qual meu ritmo esta semana?" e "O que devo fazer agora?".

Elementos-Chave para Maturidade:

Header Dinâmico de Identidade & Sequência (Streak): Exibição clara do nível atual do aluno (ex: Nível 12 • Aprendiz Constante), total de pontos e o contador de streak_days em destaque (com micro-animação/fogo ou indicador visual dos dias da semana marcados).

Hero "Continuar de Onde Parou" (Ação Primária): O card do curso mais recente em destaque absoluto, mostrando o tópico exato onde o aluno parou (ex: "Módulo 2, Lição 3: Anatomia das Variáveis"), estimativa de tempo e botão direto para abrir a lição em tela cheia.

Widget de Ritmo Semanal / Gamificação Leve: Um resumo compacto do progresso recente: número de lições concluídas na semana, pontos acumulados nos últimos dias e a próxima badge que está perto de ser destravada (com barra de progresso visual).

Grade Secundária ("Seus Cursos Recentes"): Os outros 2 ou 3 cursos em andamento com barras de progresso percentuais compactas.

Banner Adaptativo por Humor: O topo do painel reage em tempo real usando o "Humor de Cor" da categoria do curso atual (ex: tom Âmbar se o curso ativo for de Negócios; Maré se for Tecnologia), conectando a moldura do app ao tema de estudo.

Conexão com o fluxo: É a porta de entrada. Direciona para a Página da Lição (/aluno/licoes/[id]), para a aba Meus Cursos ou para o detalhe de uma badge em Meu Desempenho.

2. Meus Cursos (/aluno/cursos) — Gestão da Trilha de Aprendizado
   Propósito: Consolidar a visualização dos cursos já matriculados ou iniciados, permitindo que o aluno alterne a forma como prefere enxergar a sua jornada de estudo sem poluir a tela inicial.

Elementos-Chave para Maturidade:

Seletor de Visão (Manutenção das 3 variantes já criadas):

Visão Trilha: Linha do tempo vertical estilo "mapa de saga", mostrando o caminho linear de lições (concluídas com veredito do Tutor, atual e bloqueadas).

Visão Grade/Biblioteca: Cards clássicos organizados por status (Em Andamento, Concluídos, A Reforçar).

Visão Retomar: Foco visual nos cursos com pendências urgentes.

Filtro por Categorias / Humores: Filtrar os cursos ativos por área temática (Tecnologia, Criativo, etc.), aplicando visualmente o Humor de cor correspondente nos badges ou bordas dos cards.

Sinalização de Veredito do Tutor no Card: Indicador direto se a última lição daquele curso foi classificada como "Dominado" (badge verde/sucesso) ou "Precisa de Reforço" (alerta visual incentivando a refazer antes de avançar).

Conexão com o fluxo: Alimentado pelo Início, direciona diretamente para o visualizador de lição (/aluno/licoes/[id]).

3. Explorar (/aluno/explorar) — Catálogo & Categorização por Nichos [NOVA]
   Propósito: Resolver o problema das "ilhas de conteúdo". Esta tela dá ao aluno a dimensão real do ecossistema do NIA, gerando percepção de valor e desejo de continuar aprendendo novos assuntos na plataforma.

Elementos-Chave para Maturidade:

Navegação por "Humores" (Categorias Temáticas): Em vez de tags genéricas, o catálogo se divide nos 5 eixos do sistema visual:

Maré (Tecnologia & Dados)

Âmbar (Negócios & Carreira)

Framboesa (Criativo & Comunicação)

Lavanda (Humanas & Idiomas)

Musgo (Bem-estar & Natureza)

Hero da Categoria Dynamic-Themed: Ao pairar ou selecionar uma categoria, a moldura e os destaques da tela transicionam suavemente para o Humor correspondente.

Card de Curso Enriquecido: Exibe o título, nível de dificuldade, quantidade de módulos/lições, tempo estimado total e um rótulo do formato de avaliação do Tutor.

Modal/Página de Detalhes do Curso (/aluno/explorar/[curso-slug]): Visão completa da ementa gerada pela IA antes de iniciar:

Módulos e tópicos detalhados.

Objetivos de aprendizado.

Botão claro de "Iniciar Curso" ou "Matricular-se".

Conexão com o fluxo: Acessível pelo menu principal. Ao clicar em "Iniciar Curso", insere o curso em /aluno/cursos e redireciona o aluno direto para a primeira lição.

4. Meu Desempenho (/aluno/progresso) — Gamificação & Diagnóstico da IA [EVOLUÇÃO]
   Propósito: Evoluir a tela de progresso atual de um mero "log de notas" para um centro de reputação e autoavaliação. Aqui o aluno vê a comprovação de que está evoluindo e entende seus pontos fracos.

Elementos-Chave para Maturidade:

Aba 1: Diagnósticos do Tutor (O que já existe hoje, reformulado):

Histórico de avaliações do Tutor, filtrável por curso.

Destaque para as lições marcadas como "Precisa Reforçar" com o texto exato do diagnóstico do Tutor e um botão rápido de "Tentar Novamente".

Aba 2: Sala de Conquistas & Nível (Ativação de badges, level e total_points):

Card de Level & XP: Visualização do nível atual (1-100), barra de progresso até o próximo nível e total de pontos acumulados.

Mural de Badges (Conquistas): Grade com todas as conquistas do sistema (ex: "Semana de Ferro" por 7 dias de streak, "Mestre Maré" por concluir 3 cursos de tecnologia, "Primeiro Domínio" na primeira nota máxima do Tutor).

Badges bloqueadas aparecem em tom fosco com dica de como desbloqueá-las; badges conquistadas aparecem coloridas com data de conquista.

Aba 3: Estatísticas de Aprendizado: Métricas como total de horas estudadas, número de checkpoints respondidos corretamente de primeira e taxa de aproveitamento com o Tutor.

Conexão com o fluxo: Pode ser acessada via menu principal ou clicando nos widgets de XP/Streak do Painel de Bordo.

5. Página da Lição (/aluno/licoes/[id]) & Painel do Tutor — Experiência Imersiva de Estudo [EVOLUÇÃO]
   Propósito: O ambiente sagrado de estudo. Precisa garantir foco absoluto no conteúdo estruturado (slides) e uma transição fluida para a etapa de veredito do Tutor.

Elementos-Chave para Maturidade:

Barra de Suporte Superior (Top Bar Minimalista):

Botão de voltar (retorna ao curso mantendo a visualização anterior).

Título do curso e módulo.

Indicador de progresso nos slides (ex: Slide 4 de 12).

Botão de tela cheia (para expandir o iframe/renderizador).

Área Central Imersiva: O renderizador determinístico em JSON rodando o tema escolhido para aquela lição (Vidro Fumê, Aurora Botânica, etc.).

Painel de Avaliação do Tutor (Drawer/Seção Inferior Enriquecida):

Fluxo de Cópia & Cole: Área amigável de transição ao chegar no slide final.

Feedback Visual do Veredito: Quando a IA responde, a interface reage com celebração visual se o veredito for Dominado (animação de pontos subindo +150 XP, destravamento de badge se houver) ou tom construtivo se for Precisa de Reforço.

Botão de Próximo Passo Claro: Botão "Avançar para Próxima Lição" só é liberado em estado ativo se o veredito for positivo.

Conexão com o fluxo: É o destino principal de todas as chamadas de estudo do app.

6. Perfil & Preferências (/aluno/perfil) — Identidade & Configurações [EVOLUÇÃO]
   Propósito: Unificar a gestão da conta, personalização do sistema visual e parâmetros de aprendizado do aluno em um só local.

Elementos-Chave para Maturidade:

Bloco 1: Cartão de Identidade: Foto/Avatar, nome, e-mail, data de início na plataforma e bio curta.

Bloco 2: Estilo de Aprendizado & Interesses (Ativação de learning_style e preferred_topics):

Seleção dos temas de maior interesse (usado futuramente para priorizar recomendações na aba Explorar).

Definição do estilo de aprendizado (ex: preferências de ritmo ou foco de feedback).

Bloco 3: Aparência & Tema (O que já existe em /aluno/preferencias):

Seletor do Humor de cor padrão do app (Musgo, Âmbar, Maré, Framboesa, Lavanda).

Alternância Dark/Light mode.

Escolha da variante de layout padrão do painel (Retomar, Biblioteca, Trilha).

Bloco 4: Conta & Autenticação (Pronto para quando a Auth entrar): Alterar senha, e-mail e sessões ativas.

Conexão com o fluxo: Acessível pelo menu lateral ou pelo avatar no canto superior da tela.

Resumo do Fluxo de Valor para o Aluno
Entrada (/aluno): Vê seu streak do dia, ganha tração visual e clica no botão "Continuar de onde parou".

Estudo (/aluno/licoes/[id]): Interage com os slides, responde checkpoints, gera o resumo final e submete ao Tutor.

Recompensa (Feedback do Tutor): Recebe o diagnóstico, ganha XP/Pontos, atualiza seu Nível e libera a próxima lição.

Exploração (/aluno/explorar): Ao concluir ou querer pausar um tema, navega pelas categorias por Humor de Cor para descobrir o próximo assunto gerado pela IA.

deepseek:

Camada 1 — Núcleo Existente (Refinamento)

1. Painel (/aluno)
   Propósito: Ser a central de comando do aluno — o lugar onde ele retoma de onde parou, vê seu progresso geral e sente que está avançando. Hoje é funcional, mas não motiva.

Elementos-chave para amadurecer:

Header de saudação contextual: "Boa noite, [nome]" + mensagem motivacional baseada no streak (ex.: "Você estudou 3 dias seguidos. Continue assim!")

Card de streak em destaque: chama visual com dias consecutivos, usando o humor de cor ativo (ex.: chama em gradiente para streak alto)

Atalho "Continuar de onde parou": hero card do curso ativo com CTA direto para a próxima lição não concluída, mostrando tempo estimado

Resumo semanal de atividade: mini gráfico ou barras mostrando lições concluídas nos últimos 7 dias (usa dados que já existem de progresso)

Widget de conquistas recentes: as 3 badges mais recentes desbloqueadas, com micro-animação

Seção "Sugeridos para você": cursos recomendados baseados em preferred_topics e learning_style (mesmo que seja mock inicialmente)

Conexões: linka para lição atual, perfil, explorar e progresso.

2. Página da Lição (/aluno/licoes/[id])
   Propósito: O coração do produto — a experiência de estudo ativo. Já funciona bem tecnicamente, mas precisa de "acabamento" que a faça parecer profissional.

Elementos-chave para amadurecer:

Barra de progresso da lição visível (não apenas dentro do iframe, mas no chrome ao redor)

Indicador de checkpoint respondido (bolinhas que preenchem conforme o aluno avança)

Modal de celebração ao concluir lição: confete + pontos ganhos + streak atualizado + botão "Avaliar com Tutor"

Feedback de narração: indicador visual de que o TTS está ativo, com controle de velocidade

Botão de "Preciso de ajuda": abre painel lateral com dica contextual ou link para reforço

Conexões: ao concluir, leva para avaliação; ao reprovar no Tutor, oferece "Refazer lição" ou "Estudar reforço".

3. Avaliação (painel abaixo da lição)
   Propósito: Fechar o ciclo de aprendizado — garantir que o aluno não apenas completou, mas dominou o conteúdo.

Elementos-chave para amadurecer:

Veredito com identidade visual forte: "Dominado" em verde com selo de aprovação; "Precisa Reforçar" em âmbar com ícone de reciclagem

Pontos ganhos na avaliação: mostrar quantos pontos aquela avaliação rendeu (e por quê)

Histórico de tentativas: se o aluno reprovou e tentou de novo, mostrar evolução

CTA contextual: se reprovado, "Gerar exercícios de reforço" (mesmo que ainda não exista, prepara para a frente futura de prática)

Conexões: alimenta progresso, painel e perfil.

4. Preferências (/aluno/preferencias)
   Propósito: Dar controle ao aluno sobre sua experiência — não só visual, mas de identidade.

Elementos-chave para amadurecer:

Preview em tempo real de como o painel ficará com cada layout (mini-mockup interativo)

Seleção de humor com descrição: "Âmbar — para negócios e carreira" (não só cores, mas contexto)

Opção de "Modo foco": desativar elementos de gamificação para quem prefere minimalismo

Preferência de narração: voz, velocidade, idioma do TTS

Conexões: persiste no banco e reflete imediatamente em todo o app.

5. Progresso (/aluno/progresso)
   Propósito: Dar visibilidade tangível do aprendizado — não só "o que fiz", mas "o que sei agora".

Elementos-chave para amadurecer:

Visão por curso com barra de domínio (não só progresso de conclusão, mas % de avaliações "dominado")

Gráfico de evolução temporal: pontos e nível ao longo do tempo

Lista de habilidades adquiridas: extraídas dos tópicos que o aluno dominou (ex.: "Consegue explicar fotossíntese")

Exportação de relatório: botão "Baixar relatório de progresso" (PDF simples)

Conexões: alimenta perfil e painel.

Camada 2 — Novas Páginas Essenciais 6. Explorar (/aluno/explorar)
Propósito: Resolver a descoberta de conteúdo — hoje o aluno só vê o que já comprou, não o que poderia aprender. Essencial para plataforma séria.

Elementos-chave:

Catálogo completo de cursos com cards ricos: capa, descrição, nível, duração estimada, badges de categoria

Filtros por humor/categoria (Musgo, Âmbar, Maré...) e por nível (iniciante, intermediário, avançado)

Busca com autocomplete

Seção "Recomendados para você" baseada em preferred_topics e histórico de estudo

Curso em destaque (curadoria manual ou algoritmo simples)

CTA para cursos não comprados: "Adquirir na Hotmart/Kiwify" (link externo, deixando claro que a compra é fora do NIA)

Conexões: linka para painel (ao comprar, curso aparece lá), perfil e preferências.

7. Perfil (/aluno/perfil)
   Propósito: Dar identidade ao aluno — o lugar onde ele se vê como estudante, com suas conquistas e estatísticas. É o "cartão de visita" do aprendizado.

Elementos-chave:

Avatar com moldura personalizada baseada no nível (bronze, prata, ouro...)

Nome, bio curta e tópicos de interesse (usa preferred_topics)

Nível com barra de progresso para o próximo nível (1-100, usando level e total_points)

Galeria de badges desbloqueadas com tooltips explicando como foram ganhas

Streak atual e recorde pessoal

Estatísticas gerais: total de lições concluídas, avaliações dominadas, tempo estimado de estudo, cursos completados

Gráfico de atividade (contribuição style, como GitHub)

Botão "Compartilhar perfil" (gera link público ou imagem)

Conexões: alimenta painel e progresso; dados vêm de avaliações e conclusões.

8. Conquistas (/aluno/conquistas)
   Propósito: Centralizar a gamificação — dar um lugar onde o aluno vê tudo que pode desbloquear e se motiva a continuar. Os dados já existem no banco (badges), mas nunca viraram tela.

Elementos-chave:

Grade de todas as badges possíveis, com as desbloqueadas em cor e as bloqueadas em cinza com descrição de como ganhar

Categorias de badges: consistência (streaks), domínio (avaliações), exploração (cursos variados), velocidade (lições em tempo recorde)

Badge em destaque (a mais recente desbloqueada, com animação de celebração)

Progresso para badges parcialmente completas (ex.: "5 de 7 dias de streak para badge semanal")

Notificação de nova badge desbloqueada (sino com badge no header)

Conexões: alimenta perfil e painel; dados vêm de avaliações e atividade.

Camada 3 — Páginas de Engajamento (Diferenciais) 9. Trilha de Aprendizado (/aluno/trilha/[cursoId])
Propósito: Dar visão de longo prazo — o aluno vê o curso como uma jornada, não como uma lista de lições. Diferente do layout "Trilha" do painel, esta é uma página dedicada.

Elementos-chave:

Mapa visual do curso: linha do tempo com marcos (módulos), cada lição como um nó (concluída/atual/bloqueada)

Checkpoints de domínio: a cada módulo, um "portão" que só abre quando todas as lições do módulo foram avaliadas como dominadas

Recompensas por módulo: badge ou pontos extras ao completar um módulo inteiro

Tempo estimado para conclusão baseado no ritmo do aluno

Botão "Continuar jornada" que leva para a próxima lição não dominada

Conexões: linka para lições, progresso e perfil.

10. Revisão Inteligente (/aluno/revisao)
    Propósito: Resolver a retenção de longo prazo — o aluno revisita conceitos que está prestes a esquecer. Usa o histórico de avaliações para gerar revisões personalizadas.

Elementos-chave:

Fila de revisão diária: tópicos que o aluno dominou mas que precisam de reforço espaçado (baseado em data da última avaliação)

Cards de revisão rápida: pergunta + resposta com botão "Lembrei" / "Esqueci" (spaced repetition simples)

Progresso da revisão do dia

Streak de revisão (diferente do streak de estudo)

Notificação diária: "Você tem 5 itens para revisar hoje"

Conexões: alimenta progresso e perfil; usa dados de avaliações passadas.

11. Notificações (/aluno/notificacoes)
    Propósito: Trazer o aluno de volta — lembretes inteligentes baseados em atividade. Hoje não existe nenhum mecanismo de retorno.

Elementos-chave:

Central de notificações com categorias:

Lembretes de estudo: "Você não estuda há 2 dias. Que tal 10 minutinhos?"

Conquistas desbloqueadas

Novos cursos disponíveis na sua área de interesse

Revisões pendentes

Preferências de notificação: quais tipos receber, em qual canal (in-app, email, push)

Notificações agrupadas por dia

Badge no sino com contagem de não lidas

Conexões: alimenta painel e perfil; dados vêm de atividade e gamificação.

12. Certificados (/aluno/certificados)
    Propósito: Dar prova tangível de conclusão — o aluno pode mostrar que dominou um curso. Profissionaliza a plataforma.

Elementos-chave:

Lista de certificados para cursos concluídos com avaliação "dominado" em todas as lições

Visual do certificado com identidade do humor do curso (ex.: certificado verde para curso de bem-estar)

Download em PDF com dados do aluno, curso, data de conclusão e carga horária estimada

Link público para verificação (URL única que qualquer pessoa pode acessar)

Botão "Compartilhar no LinkedIn" (integração futura)

Conexões: alimenta perfil; dados vêm de progresso e avaliações.

Camada 4 — Páginas de Suporte 13. Ajuda & Suporte (/aluno/ajuda)
Propósito: Reduzir fricção e ansiedade — o aluno sabe onde pedir ajuda se algo der errado.

Elementos-chave:

FAQ com busca

Tutoriais rápidos de como usar cada funcionalidade (vídeos curtos ou GIFs)

Formulário de contato para bugs ou sugestões

Status do sistema (se houver instabilidade)

Conexões: acessível de qualquer página via menu.

14. Configurações da Conta (/aluno/configuracoes)
    Propósito: Separar preferências de identidade (preferências) de configurações de conta (email, senha, privacidade). Profissionaliza a experiência.

Elementos-chave:

Dados da conta: nome, email, senha

Privacidade: quem pode ver perfil e certificados

Exportação de dados: botão "Baixar meus dados" (GDPR)

Exclusão de conta

Conexões: alimenta perfil e preferências.

Mapa de Navegação Consolidado
Header (presente em todas as páginas):

Logo NIA → Painel

Explorar

Progresso

Sino (notificações)

Avatar → Perfil, Conquistas, Certificados, Preferências, Configurações

Sidebar (opcional, layout Biblioteca):

Painel

Explorar

Trilha do curso atual

Revisão

Progresso

Conquistas

Certificados

Preferências

Resumo de Prioridades (o que implementar primeiro)
Perfil — usa dados que já existem no banco, dá identidade imediata

Conquistas — gamificação que já está pronta no backend, só falta UI

Explorar — resolve a descoberta de conteúdo, essencial para plataforma

Notificações — traz o aluno de volta, aumenta retenção

Trilha de Aprendizado — dá visão de jornada, diferencia o produto

As demais (Revisão, Certificados, Ajuda, Configurações) podem vir em seguida, quando o núcleo estiver sólido.

Esse mapa transforma o NIA de "funcional mas amador" para "profissional e engajador", usando tudo que já existe (gamificação no banco, sistema de humores, renderizador de lições) e adicionando apenas o que falta para fechar a experiência completa do aluno.

chatgpt:
Mapa recomendado do lado do aluno

Eu organizaria a experiência em 6 áreas principais:

Início · Explorar · Meus cursos · Progresso · Perfil · Preferências

E algumas telas funcionariam como partes desses fluxos, sem necessariamente aparecerem na navegação principal.

1. Início — /aluno

Status: já existe, mas precisa evoluir bastante

Propósito

Ser o lugar que responde imediatamente:

“O que eu deveria fazer agora?”

Hoje o painel é essencialmente uma lista de cursos com progresso. Isso é funcional, mas o próprio briefing identifica que ele não tem motivação, celebração ou identidade.

O que deveria aparecer

Bloco principal: Continuar estudando

Em vez de simplesmente mostrar um curso, mostrar a ação concreta:

Introdução a Python
Módulo 2 · Variáveis e tipos
68% concluído
Continuar lição →

Esse deve ser o elemento dominante da tela.

Progresso do dia

Uma pequena área orientada para comportamento:

Hoje: 1 lição concluída
+40 XP
🔥 7 dias seguidos

Não precisa virar um dashboard cheio de números.

Meta de sequência

O streak existente no banco finalmente ganha função real.

Exemplo:

🔥 7 dias de sequência
Estude hoje para chegar a 8.

Cursos em andamento

Cards mais editoriais, usando a identidade de cada nicho.

Aqui entra uma decisão importante do briefing: o humor de cor não deveria ser uma preferência arbitrária, mas uma consequência da categoria do curso.

Então um curso de Programação poderia assumir Maré, enquanto um curso de Jardinagem poderia assumir Musgo.

Conquistas recentes

Somente quando houver novidade:

🏆 Nova conquista
“Primeiro curso concluído”

Isso cria um momento de celebração sem transformar a home numa página de gamificação.

Sugestão de próximo estudo

Depois que o histórico ficar mais rico:

Você está estudando tecnologia
Continue com “Fundamentos de SQL”.

Isso pode futuramente usar preferred_topics e histórico de estudo, mas essa utilização é uma inferência de produto a partir dos campos existentes no usuário, não algo já especificado no funcionamento atual.

Conexões

Início → Curso → Lição → Avaliação → Início

E:

Início → Explorar → Curso

2. Explorar — /aluno/explorar

Status: nova

Essa é uma das maiores lacunas do produto hoje. O briefing explicitamente identifica a ausência de um catálogo completo.

Propósito

Responder:

“O que eu posso aprender aqui?”

O painel deve mostrar o que o aluno já está fazendo. Explorar deve mostrar o universo disponível.

Estrutura

Hero discreto

Explore novos assuntos

Não faria um marketplace agressivo.

Categorias

Aqui aparece pela primeira vez a taxonomia visual do NIA:

Tecnologia & Dados
Maré

Negócios & Carreira
Âmbar

Criativo & Comunicação
Framboesa

Humanas & Idiomas
Lavanda

Bem-estar & Natureza
Musgo

Isso transforma o sistema de identidade visual existente em uma estrutura de produto, e não apenas em decoração.

Lista de cursos

Cada card deveria mostrar:

categoria;
título;
nível;
objetivo;
quantidade de lições;
progresso, caso já iniciado;
status;
identidade visual da categoria.

Evitaria estrelas e avaliações no estilo marketplace. O NIA não é apresentado no briefing como uma plataforma de cursos aberta com conteúdo produzido por vários professores; o conteúdo é gerado pelo próprio sistema.

Conexões

Explorar → Categoria → Curso

ou diretamente:

Explorar → Curso

3. Categoria — /aluno/explorar/[categoria]

Status: nova, recomendada

Essa página não precisa existir necessariamente como uma grande seção independente, mas eu recomendo que exista conceitualmente.

Propósito

Dar identidade temática à biblioteca.

Exemplo:

Maré
Tecnologia & Dados
Aprenda ferramentas, conceitos e fundamentos para trabalhar melhor com tecnologia.

Depois:

Cursos de tecnologia

Isso permite que a decisão de usar humores por categoria deixe de ser apenas um sistema cromático e passe a ser parte da navegação.

Elementos

Cursos relacionados, filtros por:

nível;
duração;
status;
objetivo.

E uma entrada clara:

Ver curso

Conexão

Explorar → Categoria → Curso

4. Página do curso — /aluno/cursos/[id]

Status: nova — provavelmente uma das telas mais importantes

Esta é, na minha opinião, a maior página que falta entre o catálogo e a lição.

Hoje o curso parece uma “ilha”, e o próprio briefing identifica essa sensação.

Propósito

Ser a home daquele curso.

Antes de entrar numa lição, o aluno deveria entender:

O que vou aprender?
Onde estou?
Quanto já avancei?
O que vem depois?

Estrutura ideal

Cabeçalho do curso

Título
Categoria
Nível
Objetivo

Progresso geral

62% concluído
8 de 13 lições

Continuar

Um CTA dominante:

Continuar estudando

Trilha do curso

Aqui fica a versão mais madura da “Trilha” que hoje existe como uma das variantes do painel.

Cada módulo:

✓ concluído
→ atual
🔒 bloqueado

Cada lição pode mostrar:

duração;
estado;
avaliação;
eventualmente uma indicação de domínio.

Resumo de aprendizagem

Algo como:

Você já dominou 5 de 8 tópicos.

Isso começa a conectar progresso acadêmico com gamificação.

Conexões

Curso → Lição

Curso → Progresso

Curso → Explorar

Curso → Início

5. Lição — /aluno/licoes/[id]

Status: já existe

Essa página não precisa ser reinventada. O renderizador, checkpoints, avaliação e fullscreen já são justamente uma das partes mais fortes do produto.

O que eu adicionaria ao redor do conteúdo

Sem interferir no renderizador:

Contexto

Curso X · Módulo 2 · Lição 4

Progresso da trilha

4 de 12

Sinal de conclusão

Depois da avaliação aprovada:

✓ Tópico dominado

Recompensa discreta

Exemplo:

+40 XP

Isso faz a atividade parecer parte de um sistema maior.

Importante

Não colocaria leaderboard, feed social ou pop-ups de recompensa dentro da lição.

O modo de estudo já é deliberadamente focado em conteúdo + checkpoints + tutor.

A gamificação deve envolver o estudo, não interrompê-lo.

6. Resultado da avaliação — dentro da experiência da lição ou /aluno/licoes/[id]/resultado

Status: hoje existe como painel; eu daria mais importância a ele

Esse é um ponto extremamente importante do NIA.

A avaliação não é simplesmente “nota”. O Tutor decide se o aluno dominou o tópico ou precisa reforçar.

Tela/estado deveria responder

Você dominou este tópico.

ou

Ainda vale reforçar este tópico.

Mostrar

Resultado

Domínio / Reforço

Diagnóstico

O texto que hoje já existe.

O que fazer agora

Se dominou:

Próxima lição →

Se precisa reforçar:

Revisar este tópico

Isso é crucial.

Hoje o fluxo termina no veredito. Um produto maduro transforma o veredito em próxima ação.

Conexões

Lição → Resultado → Próxima lição

ou

Lição → Resultado → Curso

7. Progresso — /aluno/progresso

Status: já existe

Hoje a página mostra o histórico das avaliações do Tutor agrupado por curso.

Isso deveria evoluir de histórico para visão de aprendizagem.

Hierarquia

Resumo geral

3 cursos em andamento
27 tópicos dominados
86% de domínio médio

Essas métricas são exemplos de produto; os dados exatos precisam ser definidos de acordo com o que o backend realmente consegue calcular.

Atividade recente

Linha do tempo:

Hoje — SQL básico — Dominado
Ontem — Joins — Reforçar
11 ago — SELECT — Dominado

Progresso por curso

Cada curso com:

8/13 lições
61%

Áreas para reforçar

Esse poderia ser o elemento mais valioso da página:

Você teve dificuldade recentemente em:
JOINs · normalização · índices

Isso conecta diretamente a página com o Tutor.

Conexões

Progresso → Curso

Progresso → Lição

Progresso → Perfil

8. Perfil — /aluno/perfil

Status: nova

O briefing explicitamente aponta a ausência de uma tela de perfil.

Propósito

Não deveria ser apenas:

Nome / e-mail / editar.

Deve ser a identidade do aluno dentro do NIA.

Estrutura

Cabeçalho

Nome
Nível atual

Nível 12 · Aprendiz constante

Resumo

Pontos totais
Cursos concluídos
Tópicos dominados
Sequência atual

Os campos total_points, level e streak_days já existem.

Conquistas

Badges conquistadas.

Interesses

Temas preferidos.

Aqui preferred_topics pode eventualmente virar uma representação visível do perfil de aprendizagem. Novamente, isso é uma sugestão de uso baseada no modelo existente, não uma funcionalidade já descrita.

9. Conquistas — /aluno/perfil/conquistas

Status: nova

Eu não colocaria todos os badges no dashboard.

Propósito

Criar um lugar para o aluno perceber:

“Eu estou evoluindo.”

Organização

Conquistadas

Badges coloridas e comemorativas.

Em progresso

Exemplo:

🔒 8/10 lições concluídas
“Constância”

Isso aproveita diretamente o campo badges.

Regra importante

As conquistas precisam estar ligadas principalmente a comportamento de aprendizagem, não a ações artificiais.

Bom:

Primeiro curso concluído
7 dias estudando
10 tópicos dominados

Ruim:

Abriu o app 5 vezes
Clicou em 20 páginas

10. Notificações — /aluno/notificacoes

Status: nova

O briefing aponta explicitamente que hoje não existe qualquer sistema de notificação ou incentivo de retorno.

Propósito

Criar continuidade entre sessões.

Tipos realmente úteis

Progresso

Você concluiu 3 lições esta semana.

Conquista

Nova conquista desbloqueada.

Sequência

Sua sequência de 6 dias termina hoje.

Curso

Você está pronto para continuar “Python básico”.

Eu evitaria notificações promocionais. O NIA precisa parecer um ambiente de aprendizagem, não uma plataforma tentando trazer o usuário de volta a qualquer custo.

11. Preferências — /aluno/preferencias

Status: já existe

Hoje já permite:

humor;
modo claro/escuro;
layout do painel;
persistência no banco.
Eu manteria essa página enxuta

Separaria claramente:

Aparência

Humor
Tema claro/escuro

Experiência

Layout da home

Aprendizagem

Preferências relacionadas à experiência de estudo, caso no futuro os campos existentes realmente sejam usados.

Não misturaria aqui dados do perfil, gamificação ou progresso.

12. Conta / autenticação

Status: nova — necessária antes de considerar o produto completo

O briefing diz explicitamente que login/cadastro ainda não existem e que tudo hoje roda com um usuário fixo de teste.

Páginas

/entrar

/criar-conta

/recuperar-senha

E, depois:

/aluno/conta

para dados e segurança da conta.

Essa área é menos “bonita”, mas é parte da sensação de produto profissional.

13. Onboarding

Status: recomendação

Eu colocaria uma pequena experiência inicial depois do cadastro:

O que você quer aprender?

Qual é seu objetivo?

Quanto tempo pretende estudar?

Isso pode alimentar futuramente os dados que já existem como preferred_topics e learning_style. O briefing não diz que esses campos já possuem uma experiência de onboarding, então aqui estamos falando de uma extensão recomendada, não de algo que já existe.

O onboarding então termina em:

Seu espaço está pronto.

E leva para o Início.

A navegação que eu faria

Não colocaria 10 itens na sidebar.

Navegação primária

Início
Explorar
Meus cursos
Progresso

E no canto:

🔥 streak · nível · avatar/perfil

Dentro de Perfil:

Perfil
Conquistas
Preferências
Conta

Isso cria uma hierarquia muito mais profissional.

E o “Meus cursos”?

Eu faria essa distinção em relação ao painel.

Início

É o que fazer agora.

Meus cursos

É tudo que você está estudando.

Pode ter:

Em andamento

Concluídos

Salvos

Assim, as três variantes atuais do dashboard deixam de carregar responsabilidades demais.

A variante Retomar continua sendo excelente para Início.

A variante Biblioteca provavelmente deveria evoluir para Meus cursos.

A variante Trilha deveria migrar conceitualmente para a página do curso.

Essa é uma mudança importante porque deixa cada tela com uma responsabilidade clara.

O mapa completo ficaria assim
┌──────────────┐
│ ENTRAR │
└──────┬───────┘
↓
┌──────────────┐
│ ONBOARDING │
└──────┬───────┘
↓
┌──────────────┐
│ INÍCIO │
└──────┬───────┘
│
┌────────────────┼────────────────┐
↓ ↓ ↓
EXPLORAR MEUS CURSOS PROGRESSO
│ │ │
↓ ↓ ↓
CATEGORIA CURSO DETALHES
│ │ │
└────────────→ LIÇÃO ←────────────┘
│
↓
AVALIAÇÃO
│
┌─────┴─────┐
↓ ↓
DOMINOU REFORÇAR
│ │
↓ ↓
PRÓXIMA REVISÃO
LIÇÃO

                    INÍCIO
                       │
                 ┌─────┴──────┐
                 ↓            ↓
              PERFIL       NOTIFICAÇÕES
                 │
          ┌──────┴──────┐
          ↓             ↓
     CONQUISTAS     PREFERÊNCIAS

O que eu considero realmente prioritário

Eu não implementaria todas essas páginas na mesma ordem.

O NIA já tem o fluxo de estudo funcionando. O maior ganho agora vem de completar o contexto em torno dele.

P0 — transformar em produto

1. Início renovado
2. Página do curso
3. Explorar
4. Perfil
5. Evolução da página de Progresso
6. Resultado da avaliação como momento claro de conclusão

Essas seis telas já mudariam bastante a percepção do produto.

P1 — criar retenção e identidade

7. Conquistas
8. Notificações
9. Categorias
10. Onboarding

Aqui entram de verdade os dados de gamificação que hoje estão parados no banco.

P2 — acabamento de produto

11. Autenticação completa
12. Conta
13. Estados vazios / erros / conclusão / primeira experiência
14. Sistema de recomendação

A principal mudança conceitual

Hoje a arquitetura parece:

curso → lição → avaliação

Eu transformaria em:

descobrir → escolher → entender o caminho → estudar → ser avaliado → evoluir → decidir o próximo passo

Essa diferença é justamente o que falta para sair de um sistema que funciona para um produto que parece uma plataforma educacional de verdade.

E eu preservaria algo que o briefing deixa muito claro: a gamificação não deve tentar transformar o NIA num jogo. Pontos, nível, badges e streak devem funcionar como linguagem visual de progresso e motivação, enquanto o núcleo continua sendo o estudo ativo e o julgamento do Tutor.
