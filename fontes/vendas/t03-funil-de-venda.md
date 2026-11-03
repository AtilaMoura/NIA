# Dossiê — T3 · Funil de venda: da atenção à permanência

Curso: **Vendas na Internet: do post ao primeiro cliente** (privado). Módulo 1 "Como se ganha dinheiro na internet" ·
Aula 2 "Funil e público" · **Tópico 3** (abre a Aula 2). Produção: `Topico.id=172` (lesson 139, `topico_index` 1) — vazio na
produção (`is_approved=false`, `content=None`, conferido em 2026-11-03).

- **Antes:** T1 (modelos de negócio) e T2 (assinatura, churn, LTV, CAC). O T2 já ensinou churn, retenção, LTV e CAC — aqui só se **liga** o
  funil a eles ("permanência" = retenção), sem reensinar as contas.
- **Depois (não invadir):** T4 "Público e persona: quem assina o Emaús" (tópico 173); T5/T6 oferta e copy (**AIDA e PAS ficam no T6**); Módulo 3
  (Instagram, WhatsApp, criativos); Módulo 4 (Meta Ads: objetivos de campanha, Pixel); Módulo 5 (CPM/CTR/CPC/CPA/ROAS, "custo por assinante",
  teste A/B, LGPD aprofundada no T22).
- Perfil: já usa redes sociais, quer virar profissional de tráfego; texto neutro. Caso real: Emaús. **Sem verba de anúncio → todo número do
  exercício é SIMULADO e marcado.**

## Fontes — o que foi LIDO de fato (2026-11-03)

| # | Tipo | Referência | O que sustenta (citações exatas e curtas) |
|---|---|---|---|
| 1 | Instituição (Sebrae) — material técnico | Sebrae, *Funil de Vendas e Jornada de Compras no Digital* (série E-commerce; PDF, 27 p.; metadados: criado em 08/07/2020 — sem data impressa). https://bibliotecas.sebrae.com.br/chronus/ARQUIVOS_CHRONUS/bds/bds.nsf/3f8f9380ac384b273d6ea0ba8b040c4c/$File/19770.pdf (baixado e extraído com pypdf `-I`) | **Jornada:** "a jornada de compras geralmente consiste em 4 etapas… Aprendizado e descoberta, reconhecimento do problema, consideração da solução e decisão de compra." **Funil:** "O funil de vendas é um modelo teórico que analisa a jornada de compra e tenta identificar onde a empresa pode atuar desde o momento em que os clientes vão ter o primeiro contato com sua marca até a realização de uma compra." · "afunilar a sua base de interessados em 3 etapas: Topo, meio e fundo" · "identificar pontos onde a sua empresa está perdendo clientes". **Topo:** "É onde está a maior base, e, portanto, onde ela é menos qualificada"; visitante = "alguém que buscou um produto ou uma informação no Google" ou "viu um anúncio patrocinado e clicou"; papel: "educá-lo"; "é preciso um controle de quem está entrando e saindo… você precisa registrá-lo de algum modo" (formulário de cadastro em troca de conteúdo); landing page "totalmente focada em conversões… porta de entrada". **Meio:** quem se cadastra e se interessa "agora é o que chamamos de lead"; o meio "engloba o reconhecimento do problema e a consideração de solução"; "qualificar e nutri-lo"; "a empresa estabeleça métricas específicas para determinar quando um lead está qualificado ou não"; sugere "um pouco de senso de urgência ou oportunidade perdida". **Fundo:** conectado à decisão de compra |
| 2 | Instituição (Sebrae SC) — blog institucional | Sebrae SC, *O que é funil de vendas e como aplicar na sua empresa* (01/08/2025). https://www.sebrae-sc.com.br/blog/o-que-e-funil-de-vendas-e-como-aplicar-na-sua-empresa | "O funil de vendas é um modelo estratégico que representa a jornada do cliente desde o primeiro contato com a empresa até a compra." · "em geral, são três etapas principais: topo (atração), meio (consideração) e fundo (decisão)" · "A estrutura do funil pode variar." · "acompanhe métricas como taxa de conversão, custo por lead (CPL), tempo de fechamento de venda, taxa de fechamento, taxa de abandono do funil" · "Etapa extra: pós-venda (fidelização e suporte)": "Embora não seja uma etapa oficial do funil, o pós-venda é essencial para manter o cliente engajado" · "O funil de vendas não termina na conversão." · "O funil de vendas nunca é uma solução pronta e definitiva." |
| 3 | Instituição (Comunidade Sebrae PR) — artigo de colaborador | Thomas Manning Sheppard Berkes, *Funil de Conversão: Uma estratégia essencial para o Sucesso do Marketing Digital* (18/04/2024). https://sebraepr.com.br/comunidade/artigo/funil-de-conversao-uma-estrategia-essencial-para-o-sucesso-do-marketing-digital ⚠ **a Comunidade Sebrae é blog colaborativo: a página diz que o Sebrae não se responsabiliza pelo conteúdo de terceiros, e a bio do autor promove uma plataforma** | "O funil de conversão é um modelo que representa o processo pelo qual um visitante se transforma em cliente, passando por diferentes estágios." · topo: "atrair a atenção do público-alvo e gerar consciência sobre sua marca, produtos ou serviços"; meio: "considerando suas opções"; fundo: "prontos para tomar uma decisão de compra" · "Taxa de Conversão por Etapa: Acompanhe a taxa de conversão em cada etapa do funil para identificar onde os leads estão se perdendo ou abandonando o processo." · "Taxa de Churn ou Cancelamento: Caso seu funil inclua etapas pós-venda, como renovações de contratos ou assinaturas, acompanhe a taxa de churn" |
| 3b | Instituição (Comunidade Sebrae PR) — artigo de colaborador ⚠ mesma ressalva da fonte 3 | Edson Santos, *O que é Marketing de Fundo de Funil — e por que ele é o momento decisivo da conversão* (10/12/2025). https://sebraepr.com.br/comunidade/artigo/o-que-e-marketing-de-fundo-de-funil-%E2%80%94-e-por-que-ele-e-o-momento-decisivo-da-conversao | "O funil de vendas existe para representar a evolução gradual do interesse. O topo amplia a consciência, o meio fortalece o relacionamento, enquanto o fundo transforma intenção em ação." · "O fundo do funil é o 'momento da verdade': ou o lead compra, ou abandona o processo para sempre." (o tópico usa só a ideia de momento da verdade, sem o "para sempre") |
| 4 | Instituição (Sebrae PE) — e-book (lido no T2) | Sebrae PE, *Retenção de clientes: saiba tudo sobre o assunto!* (metadados: out/2020) | Jornada em 4 etapas (idem fonte 1, p. 18); "Quem pensa que a jornada é encerrada no momento em que o cliente sai da loja, está muito enganado." (p. 19); **taxa de conversão (p. 27):** "basta dividir a quantidade de vendas pelo número de pessoas que tiveram contato com os seus produtos ou serviços" |
| 5 | Pesquisa de mercado (instituto) | Baymard Institute, *50 Cart Abandonment Rate Statistics* (atualizada em 22/09/2025) e *Reasons for Cart Abandonment*. https://baymard.com/lists/cart-abandonment-rate · https://baymard.com/research-articles/ecommerce-checkout-usability-report-and-benchmark | "we've calculated the average cart abandonment rate of 70.22%" — "an average calculated based on 50 different studies"; motivos (excluído o grupo "só navegando"): 40% custos extras (frete, taxa), 20% entrega lenta, 19% desconfiança com o cartão, 18% exigência de criar conta, 17% checkout longo/complicado; "42% of US online shoppers have abandoned a cart because 'I was just browsing / not ready to buy'"; ressalva da própria fonte: "a large portion of cart abandonments are simply a natural consequence of how users browse ecommerce sites" |
| 6 | Primária / lei | Lei 13.709/2018 (LGPD), lida no Planalto: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (a página veio truncada no art. 20; acentos corrompidos e restaurados pelo leitor) | Art. 5º, I: "dado pessoal: informação relacionada a pessoa natural identificada ou identificável"; art. 6º, I (finalidade): "propósitos legítimos, específicos, explícitos e informados ao titular"; art. 6º, III (necessidade): "limitação do tratamento ao mínimo necessário para a realização de suas finalidades"; art. 8º, § 4º: "O consentimento deverá referir-se a finalidades determinadas, e as autorizações genéricas para o tratamento de dados pessoais serão nulas." |
| 7 | Documento interno + código | `PLANO_ACESSO_E_PAGAMENTO.md`; `emaus-web/app/page.tsx` e `criar-conta/criar-conta-ui.tsx` (lidos 2026-11-03) | **Estado real do Emaús:** existe **página de visitante** (cursos em destaque, 3 passos, botão "Criar conta grátis"); o cadastro pede **nome, e-mail e senha**; a **assinatura é planejada, não existe** (pagamento não construído, preço não decidido) |

**Tipos cobertos (5 de 8):** instituição (Sebrae ×4), pesquisa de mercado (Baymard), primária/lei (LGPD), interno/código (Emaús), caso de dado real.
Faltam: livro-texto/artigo acadêmico sobre funil (ver abaixo), especialista nomeado e "caso real que deu errado" no sentido de empresa (o
Baymard entra como dado de "vazamento", não como caso de empresa).

### O que NÃO foi possível ler (declarado)
- **McKinsey, *The consumer decision journey* (2009):** timeout nos dois endereços (página e PDF) e `curl` direto também falhou. **Não usado.**
  O tópico **não** diz que o funil foi "substituído" por outro modelo (isso só apareceu em resumo de busca, não lido).
- **Sebrae Respostas** (funil de vendas): DNS falhou. Não usado.
- **Definição acadêmica de AIDA:** o Sebrae SC a atribui a E. St. Elmo Lewis, mas a página que cita o nome varia a grafia; AIDA **fica para o T6** (copy).
- **Baymard — "abandono" não é definido** na página (por sessão? por carrinho?); a média é **simples** de 50 estudos de fornecedores variados (conta
  refeita pelo leitor: soma 3510,96 ÷ 50); as duas páginas divergem (70,22% × 70,19%) e há rótulos "2026" com dados de 2025. O tópico fala em "cerca de
  sete em cada dez", com a ressalva de que é e-commerce de produto, não assinatura.
- **LGPD:** só os artigos acima foram lidos (a página truncou no art. 20). Não afirmar nada sobre multas, ANPD, bases legais além do art. 7º, I (só
  citado como exemplo de consentimento) nem sobre o que o Emaús faz com os dados.

## Afirmações centrais

| # | Afirmação | Fontes | Status |
|---|---|---|---|
| A1 | Funil = modelo (teórico) da jornada do primeiro contato até a compra; filtra potenciais clientes; ajuda a ver onde se perdem clientes | 1, 2, 3 | ok |
| A2 | Três etapas: topo (atração/atenção), meio (consideração), fundo (decisão) | 1, 2, 3 | ok (3 fontes concordam) |
| A3 | Jornada de compra em 4 etapas: aprendizado e descoberta, reconhecimento do problema, consideração da solução, decisão de compra; topo ≈ descoberta; meio ≈ reconhecimento + consideração; fundo ≈ decisão | 1, 4 | ok |
| A4 | Topo: maior base, menos qualificada; visitante ainda não conhece a empresa; papel: educar (conteúdo, posts, e-books) | 1, 3 | ok |
| A5 | Para o visitante entrar de fato no funil é preciso registrá-lo (formulário de cadastro, em troca de conteúdo); landing page = porta de entrada | 1 | ok |
| A6 | Lead = visitante que se cadastrou e se interessou; meio: qualificar e nutrir; definir métricas para saber quando um lead está qualificado | 1 | ok |
| A7 | Fundo: o lead está pronto para decidir a compra | 1, 2, 3 | ok |
| A8 | Taxa de conversão = vendas ÷ pessoas que tiveram contato; acompanhar a conversão **por etapa** para ver onde se perde gente | 3, 4 | ok |
| A9 | O funil não termina na compra; pós-venda (fidelização e suporte) é "etapa extra"; para assinatura acompanha-se o churn | 2, 3, 4 | ok |
| A10 | A estrutura do funil pode variar; nunca é solução pronta e definitiva | 2 | ok |
| A11 | Carrinhos abandonados: média de 70,22% em 50 estudos (Baymard); motivos principais: custos extras (40%), entrega lenta (20%), desconfiança com o cartão (19%), criar conta (18%), checkout longo (17%); grande parte é "só navegando" e inevitável | 5 | ok com as ressalvas acima |
| A12 | Pedir cadastro é coletar dado pessoal; a LGPD pede finalidade específica e informada, e mínimo necessário; consentimento (quando é a base) tem de se referir a finalidades determinadas | 6 | ok (artigos citados) |
| A13 | Emaús hoje: página de visitante + "Criar conta grátis" (nome, e-mail, senha); assinatura planejada, não existe | 7 | ok — verificado no código em 2026-11-03 |
| A14 | "Use urgência só se for verdadeira" | — (conselho do curso, **marcado como tal**; o Sebrae só cita "senso de urgência") | ok como recomendação do curso, sem apresentar como regra de fonte |

## Divergências entre fontes
- **Nomes das etapas:** Sebrae PR = "topo (awareness), meio (consideration), fundo (decision)"; Sebrae SC = "topo (atração)…"; Sebrae PDF/PE e-book =
  jornada de 4 etapas. **Decisão:** ensinar topo/meio/fundo e mostrar a correspondência com a jornada de 4 etapas; o título do tópico usa "atenção"
  (fonte 3) e "permanência" (retenção, fontes 2 e 4).
- **Pós-venda:** Sebrae SC diz que "não é uma etapa oficial do funil"; o título do tópico fala em "permanência". **Decisão:** apresentar como o
  Sebrae diz — extensão do funil, não etapa "oficial" — e ligar ao churn do T2.
- **Fonte 3 é texto de colaborador** (com ressalva do Sebrae); as afirmações dela só entram quando **confirmadas** por 1 ou 2.

## O que ficou de fora (e por quê)
- AIDA/PAS (T6), objetivos de campanha da Meta e Pixel (Módulo 4), métricas de anúncio (Módulo 5), automação de e-mail/CRM, landing page como ferramenta
  (Módulo 2), segmentação e persona (T4).
- "Funil substituído pela jornada em círculo" (McKinsey): não lido.
- Números de benchmark de conversão por etapa: nenhuma fonte primária lida → **nenhum percentual de conversão real**; só simulados.
- LGPD completa (bases legais, direitos, encarregado, sanções): Módulo 5/T22.
- Passo a passo de ferramenta: **nenhum** (tarefa em caderno/planilha).
