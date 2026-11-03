# Auditoria — T4 · Público e persona: quem assina o Emaús

Data: 2026-11-03 · Conteúdo: `backend/_criar_t04_vendas.py` → `_t04_vendas_final.json` (13 slides, 7 imagens, 12 perguntas) ·
Dossiê: `t04-publico-e-persona.md`.

**Resultado: 0 pendências BLOQUEANTES.** Itens "a conferir por humano" na seção 5 — leia o item de **dado sensível/LGPD**.

## 1. Checklist do curso (`docs/processo-topico/vendas.md`)

| Item | Resultado |
|---|---|
| Nenhum número de taxa/comissão/renda sem fonte primária | ✔ Nenhuma taxa, comissão ou renda. Números no texto: datas e artigos de lei/política (fonte), "30 a 60 anos", "35 anos", "oito horas" (do exemplo do guia do Sebrae PE). Nenhuma estatística de mercado (as do Sebrae MG 2005–2016 estavam sem fonte e **não foram usadas**) |
| Nenhuma afirmação sobre o Emaús que não seja verdade hoje | ✔ Só diz: (a) o texto de apresentação do site e títulos/subtítulos do catálogo (lidos no código em 2026-11-03: `emaus-web/app/page.tsx` e `_lib/catalogo.ts`); (b) a assinatura é só plano, o preço não foi decidido (PLANO_ACESSO); (c) "os documentos do projeto não trazem dado sobre quem assinaria". **Não afirma** número de alunos, perfil real de usuários nem que "nenhuma pesquisa foi feita" (retirado: não verificável). As duas "hipóteses de partida" são **marcadas** como tiradas do texto do catálogo, não dados |
| Passo a passo de ferramenta conferido na ajuda oficial | ✔ N/A — nenhum passo a passo de ferramenta (nada de Gerenciador de Anúncios; isso é do Módulo 4). A tarefa usa caderno/planilha |
| Publicidade/afiliado com regra de identificação (CONAR) | ✔ N/A — afiliado não aparece |
| Políticas de anúncio e LGPD lidos na fonte primária | ✔ LGPD lida no Planalto (arts. 5º II, 11 caput/I/§ 1º, 6º III); Meta lida em 3 páginas oficiais (anúncio 09/11/2021, blog de desenvolvedores 08/12/2021, política de atributos pessoais com change log de 26/06/2024) |

## 2. Afirmações × fontes (lidas em 2026-11-03)

| Afirmação no tópico | Fonte | Status |
|---|---|---|
| Marketing gera custo; definir público otimiza o gasto | Sebrae PE guia, p. 4 | ok |
| Público-alvo = consumidores que o empresário escolhe e define | Sebrae MG (27/12/2017) | ok, citação exata |
| 5 critérios (geográficas, demográficas, socioeconômicas, psicográficas, comportamentais) com as descrições | Sebrae MG | ok |
| Público-alvo = características comuns a várias pessoas (gênero, idade, local, profissão, escolaridade) | Sebrae PE guia, p. 7 | ok |
| Exemplo dos esportes radicais: nem todo entusiasta compraria | Sebrae PE guia, p. 8 | ok |
| Persona = personagem semifictício baseado em dados e no comportamento real dos clientes ideais; avatar; medos, anseios, dores, sonhos | Sebrae PE guia, p. 7 | ok, citação exata |
| Exemplo da Maria / clínica estética; a maioria dos clientes eram mulheres de 30 a 60 anos | Sebrae PE guia, p. 18 | ok — **resumo**, sem aspas, rotulado "(Resumo do exemplo do próprio guia.)" |
| Comunicação dirigida a uma pessoa específica | Sebrae PE guia, p. 19 | ok |
| Passos para criar: dados dos próprios clientes; planejar pesquisa; 4 grupos de perguntas; tabular e achar padrões; estruturar; divulgar à equipe | Sebrae PE guia, p. 12–19 | ok |
| "Uma simples tabela de Excel resolve" | Sebrae PE guia, p. 17 | ok |
| Texto de apresentação do Emaús; títulos/subtítulos do catálogo | código (`page.tsx`, `catalogo.ts`) | ok — verificado |
| Assinatura só plano; preço não decidido | PLANO_ACESSO_E_PAGAMENTO.md; código | ok |
| Convicção religiosa = dado pessoal sensível (art. 5º, II); art. 11 caput, I e § 1º | LGPD (Planalto) | ok, citações exatas |
| Meta: remoção de opções ligadas a saúde, raça/etnia, política, religião, orientação sexual; 19/01/2022; exemplos; o que continua | Meta (09/11/2021; 08/12/2021) | ok — fonte é a própria Meta, dito no slide |
| Política: anúncios não podem afirmar ou sugerir atributos pessoais; religião; "Are you Christian?" ❌ | Meta Transparency Center (change log 26/06/2024) | ok |
| ✕/✔ de títulos de post | adaptação do exemplo da política (✕) e frase do próprio site (✔) | ok — "adaptado do exemplo da política" dito no slide |
| Pesquisa só com o necessário; art. 11 § 1º para listas | LGPD arts. 6º III, 11 § 1º | ok — **sem parecer jurídico**, "consulte alguém da área" |

## 3. Ideias que NÃO entraram (e correções do próprio rascunho)

- **"Segmentar por religião"/"interesse religioso" como técnica:** fora; a Meta removeu e a política proíbe afirmar/sugerir. O tópico diz o contrário.
- **Persona com demografia inventada do "assinante do Emaús":** fora; só hipóteses marcadas, derivadas do texto do catálogo.
- **Afirmar que "ser aluno de curso bíblico é dado sensível":** fora; o tópico só diz que um dado que **revele** convicção religiosa merece o cuidado do art. 11.
- **Estatísticas do Sebrae MG** (2005–2016, quase todas sem fonte): fora.
- **Frase do guia sobre postagens que "conversam com as partes mais profundas do subconsciente":** fora (incentiva manipulação).
- **Mapa de empatia:** aparece em buscas do Sebrae, mas não foi lido → fora.
- **Correções feitas no rascunho:** (a) o exemplo da Maria estava entre aspas como citação, mas era resumo → tirei as aspas e rotulei; (b) "dar um nome" à persona não é passo literal do guia → reescrito para "perfil bem definido (rosto, gênero, características)"; (c) "Formação do Obreiro…" é título, não subtítulo → "títulos e subtítulos"; (d) "nenhuma pesquisa com alunos foi feita" não verificável → "os documentos do projeto não trazem dado"; (e) "pede consentimento específico" escrito como se fosse a única regra → "uma das hipóteses é o consentimento específico e destacado"; (f) duração 22 min fora da faixa do validador → 20.

## 4. Pedagogia e continuidade

- Fecha o Módulo 1: T3 (funil) → "para quem" → T5 (oferta). "Próximo" aponta o T5.
- Não invade: passo a passo de públicos no Gerenciador, regras de listas de clientes/Pixel, políticas completas da Meta (Módulo 4); AIDA/PAS (T6); LGPD aprofundada (T22).
- Cada checkpoint usa só o já ensinado (ck1 = público × persona; ck2 = 4 grupos + estado do Emaús; ck3 = LGPD/Meta; ck4 = síntese).
- Dificuldade: reconhecimento (classify, associar, mc, tf) → escrita livre (2 abertas, com modelo).
- Texto neutro (sem nome, sem "a aluna"); a única pessoa nominada é a "Maria" do guia e o "Paulo" inventado do modelo de resposta, ambos fictícios e marcados.
- A tarefa evita coletar crença e rotula a persona como HIPÓTESE.

## 5. Itens a conferir por humano (não bloqueiam)

- **LGPD e Emaús:** o tópico **não afirma** nada sobre o que o Emaús faz com dados de alunos nem sobre conformidade. Se o Atila for subir lista de alunos para uma plataforma de anúncios, a questão do art. 11 § 1º deve ir a um profissional da área jurídica (o tópico diz isso).
- **Meta:** só a política de atributos pessoais e os anúncios de 2021 foram lidos. As regras de públicos personalizados (listas de clientes), de conteúdo religioso e as ferramentas atuais do Gerenciador **não foram lidas** (Módulo 4).
- **Tipos de fonte:** 5 de 8 (faltam artigo acadêmico, especialista nomeado e caso de empresa que deu errado). O "erro" ensinado é de método (público largo) e a remoção da segmentação da Meta.
- **Datas:** o guia do Sebrae PE só tem data por metadados (jun/2021); Sebrae MG é de 2017 (blog). A política da Meta é de 2024 e pode ter mudado depois.
- **LGPD:** texto lido pelo leitor automático (acentos restaurados); conferir no Planalto antes de uso formal.

## 6. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (1) ✔ · bloco `cards` com os 5 critérios ✔ · Reflexão "💭 Pra pensar" + Resumo ✔ · tarefa com o Emaús (caderno/planilha) ✔.
- Perguntas: **12** — classify 1, associar 1, tf 3, mc 5, **open 2** ✔; ids únicos ✔; `validar_topico()` vazio ✔ (após ajustar a duração para 20 min).
