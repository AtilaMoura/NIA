# Auditoria — T3 · Funil de venda: da atenção à permanência

Data: 2026-11-03 · Conteúdo: `backend/_criar_t03_vendas.py` → `_t03_vendas_final.json` (14 slides, 8 imagens, 12 perguntas) ·
Dossiê: `t03-funil-de-venda.md`.

**Resultado: 0 pendências BLOQUEANTES.** Itens "a conferir por humano" na seção 5.

## 1. Checklist do curso (`docs/processo-topico/vendas.md`)

| Item | Resultado |
|---|---|
| Nenhum número de taxa/comissão/renda sem fonte primária | ✔ Nenhuma taxa, comissão ou renda. Números no texto: (a) das fontes — Baymard (70,22%, 50 estudos; motivos 40/20/19/18/17/9%; 42% navegando), datas e artigos da LGPD; (b) **simulados e marcados** ("números inventados para treinar"): 1.000→100→20, 500→25, 800→80→16. **Nenhum percentual de conversão "real"** é afirmado |
| Nenhuma afirmação sobre o Emaús que não seja verdade hoje | ✔ Só diz: existe página de visitante com cursos em destaque, 3 passos e botão "Criar conta grátis"; o cadastro pede nome, e-mail e senha; a assinatura é plano (pagamento não construído, preço não decidido). **Conferido no código em 2026-11-03** (`emaus-web/app/page.tsx`: `PASSOS` com 3 itens e `LinkBotao href="/criar-conta">Criar conta grátis`; `criar-conta-ui.tsx`: campos `name`, `email`, senha). Não afirma nada sobre o que o Emaús faz com os dados nem sobre conformidade com a LGPD |
| Passo a passo de ferramenta conferido na ajuda oficial | ✔ N/A — nenhum passo a passo de ferramenta (tarefa em caderno/planilha) |
| Publicidade/afiliado com regra de identificação (CONAR) | ✔ N/A — não aparece |
| Políticas, CDC, Decreto, LGPD, CONAR lidos na fonte primária | ✔ LGPD lida no Planalto (arts. 5º, I; 6º, I e III; 8º, § 4º). Só os artigos citados; a página truncou no art. 20 |

## 2. Afirmações × fontes (lidas em 2026-11-03)

| Afirmação no tópico | Fonte | Status |
|---|---|---|
| Funil = modelo da jornada do primeiro contato até a compra | Sebrae SC (01/08/2025); PDF Sebrae E-commerce ("modelo teórico") | ok |
| Três etapas: topo (atenção), meio (consideração), fundo (decisão) | Sebrae SC; PDF Sebrae; Comunidade Sebrae PR (3 fontes concordam) | ok |
| Topo: atrair atenção/visibilidade; maior base, menos qualificada; visitante; educar com posts, vídeos, e-books | PDF Sebrae; Sebrae PR | ok |
| Registrar o visitante (formulário em troca de conteúdo); landing page = porta de entrada | PDF Sebrae | ok |
| Lead = visitante cadastrado e interessado que ainda não comprou | PDF Sebrae | ok |
| Meio: qualificar e nutrir; relação de confiança; métricas para saber quando o lead está qualificado; conversão sutil (conteúdo, não interrupção) | PDF Sebrae | ok |
| "Senso de urgência ou oportunidade perdida" | PDF Sebrae | ok (citado) |
| "Só use urgência verdadeira… inventar escassez é enganar" | — | **marcado como "regra do curso"** (A14 do dossiê), não como regra de fonte |
| Jornada em 4 etapas e correspondência topo/meio/fundo | PDF Sebrae; e-book Sebrae PE | ok |
| A estrutura do funil pode variar; nunca é solução pronta e definitiva | Sebrae SC | ok |
| Fundo: "momento da verdade": ou compra ou abandona | Comunidade Sebrae PR (E. Santos, 10/12/2025) | ok — fonte de colaborador (ressalva do Sebrae); frase atribuída ao autor, sem o "para sempre" |
| Baymard: média 70,22% (50 estudos); motivos 40/20/19/18/17%; 42% só navegando; "grande parte é consequência natural" | Baymard (lista de 22/09/2025) | ok |
| Ressalvas sobre o Baymard (média simples; "abandono" não definido; valem para lojas de produto) | leitura do agente + conta refeita (3510,96 ÷ 50) | ok — declaradas no slide |
| Taxa de conversão = vendas ÷ pessoas que tiveram contato | Sebrae PE e-book p. 27 | ok |
| Acompanhar a conversão por etapa para ver onde os leads se perdem | Comunidade Sebrae PR | ok |
| Usar a mesma conta para cada passagem | — | **marcado como "o curso usa a mesma ideia"** (adaptação do curso à definição do Sebrae) |
| O funil não termina na compra; pós-venda é "etapa extra" (fidelização e suporte), "não oficial" mas essencial | Sebrae SC | ok |
| "Quem pensa que a jornada acaba… está muito enganado" | Sebrae PE e-book p. 19 | ok |
| Acompanhar o churn quando o funil inclui assinaturas | Comunidade Sebrae PR | ok |
| Nome/e-mail = dado pessoal; finalidade "legítimos, específicos, explícitos e informados"; "mínimo necessário"; consentimento com finalidades determinadas, autorizações genéricas nulas | LGPD arts. 5º I, 6º I/III, 8º § 4º | ok (citações exatas; acentos restaurados pelo leitor — conferir no Planalto antes de uso formal) |
| Cálculos: 100÷1000=10%; 20÷100=20%; 20÷1000=2%; 25÷500=5%; 80÷800=10%; 16÷80=20%; 16÷800=2% | aritmética | ✔ todas conferidas |

## 3. Ideias que NÃO entraram (e correções do próprio rascunho)

- **McKinsey (2009), "funil substituído por jornada circular":** não lida (timeout). O tópico não diz que o funil foi superado; diz que é um modelo e pode variar (Sebrae SC).
- **Sebrae Respostas:** DNS falhou; não usado.
- **AIDA/PAS:** ficam no T6 (copy). **Benchmarks de conversão por etapa:** nenhuma fonte primária lida → nenhum.
- **LGPD completa** (bases legais, direitos, sanções, ANPD): fora; só os artigos citados.
- **Erro corrigido no rascunho:** o bloco "Para conferir sozinho" da tarefa saiu com uma comparação de etapas confusa e com ponto de interrogação no meio da frase; reescrito para "a passagem com a menor conversão é visitante → conta (10%)".
- **Ajuste de atribuição:** a taxa de conversão por etapa vem da Comunidade Sebrae PR (fonte 3), não do guia do Sebrae PE (que só dá a taxa geral); o texto do slide separa as duas atribuições.

## 4. Pedagogia e continuidade

- Abre a Aula 2 retomando o T2 (churn, retenção, LTV) sem reensinar as contas; "Próximo" aponta o T4 (público e persona).
- Não invade: AIDA/PAS (T6), objetivos de campanha/Pixel (M4), CPM/CTR/CPC/CPA/ROAS (M5), persona/segmentação (T4), LGPD aprofundada (T22).
- Cada checkpoint usa só o já ensinado (ck1 = topo/meio + lead + LGPD; ck2 = fundo + Baymard; ck3 = conversão, permanência; ck4 = síntese).
- Dificuldade: reconhecimento (classify, tf, mc, associar) → cálculo (lacuna) → escrita livre (2 abertas).
- Texto neutro (sem nome, sem "a aluna").

## 5. Itens a conferir por humano (não bloqueiam)

- **Tipos de fonte:** 5 de 8 (instituição, pesquisa, lei, interno/código, dado). Faltam artigo acadêmico sobre funil e especialista nomeado (a McKinsey seria a via; não carregou).
- **Fontes do Sebrae** não têm data impressa (PDF: metadados jul/2020; e-book: out/2020); a Comunidade Sebrae é conteúdo de colaboradores (ressalva do Sebrae).
- **LGPD:** conferir o texto exato no Planalto antes de usar em material formal (o leitor corrompeu acentos e a página veio truncada).
- **Baymard:** a página usa rótulos "2026" com dados de 2025 e apresenta 70,22% × 70,19% em páginas diferentes; o tópico usa a lista de 22/09/2025.

## 6. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (1) ✔ · bloco `cards` das 3 etapas ✔ · Reflexão "💭 Pra pensar" + Resumo ✔ · tarefa com o Emaús (caderno/planilha) ✔.
- Perguntas: **12** — classify 1, associar 1, tf 3, mc 4, lacuna 1, **open 2** ✔; ids únicos ✔; `validar_topico()` vazio ✔.
