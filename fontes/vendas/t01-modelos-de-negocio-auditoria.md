# Auditoria — T1 · Modelos de negócio online: curso, assinatura, serviço e afiliado

Data: 2026-10-06 · Auditor: Claude · Régua: `t01-modelos-de-negocio.md` (dossiê, 11 fontes)
Versão auditada: `backend/_criar_t01_vendas.py` → `_t01_vendas_final.json` (15 slides).

## 1. Fato — afirmação → fonte → status

| Slide | Afirmação no tópico | Fonte (dossiê #) | Status |
|---|---|---|---|
| s1 | 157 milhões de usuários de internet no Brasil (TIC Domicílios 2025, Cetic.br) | 8 (PDF lido) | ok |
| s1 | Canvas (Osterwalder e Pigneur): fontes de receita — transacional ou recorrente | 7 (PDF UCSD lido) | ok |
| s2 | Papéis produtor / afiliado / comprador; produtor pode criar programa de afiliados | 4 (Central de Ajuda, trecho oficial via busca), 3 | ok |
| s2 | A plataforma processa pagamento, libera acesso e repassa já descontando taxa e comissão | 3 (blog oficial lido: "checkout, processamento de pagamento, entrega do conteúdo… repasse da comissão") | ok |
| s2 | CDC art. 49: 7 dias pra desistir em compra fora do estabelecimento, devolução imediata | 1 (lei lida no Planalto) | ok |
| s2 | Decreto 7.962/2013: informar como desistir; pode desistir pela mesma ferramenta | 11 (decreto lido no Planalto, art. 1º III e art. 5º §1º) | ok |
| s2 | Taxas de plataforma mudam com o tempo; conferir a tabela oficial | 3 + divergência registrada no dossiê | ok (data da mudança **removida** — só fonte secundária) |
| s4 | Assinatura = taxa semanal/mensal/anual pelo acesso; "economia da recorrência" | 5 (Sebrae/PR lido) | ok |
| s4 | Receita previsível; adesão e cancelamento simples; transparência | 5 | ok |
| s4 | O Emaús foi planejado pra assinatura mensal | PLANO_ACESSO_E_PAGAMENTO.md, decisão D3 (doc interno) | ok — redigido como "planejado", porque o pagamento ainda não existe |
| s5 | Definição de escalável e a pergunta "aumento de clientes exige aumento proporcional de custos ou mão de obra?" | 6 (Sebrae/PR lido) | ok |
| s5 | "Por esse critério", serviço não escala na mesma medida | 6 (aplicação explícita do critério, não afirmação nova) | ok |
| s7 | Afiliado: cadastro gratuito, link exclusivo, comissão por venda pelo link | 3 (blog oficial lido) | ok |
| s7 | Afiliado não precisa de produto próprio nem cuida de estoque, entrega ou atendimento | 3 ("Não há estoque, logística ou atendimento ao cliente") | ok |
| s7 | CONAR (2021): relação comercial "ainda que não financeira"; identificar com "publicidade", "publi", "publipost" | 2 (PDF lido; os dois trechos conferidos) | ok |
| s10 | MoviePass: ago/2017, US$ 9,95/mês, um filme por dia | 9 (Wikipedia, citando Variety; Fortune 15/08/2017 via busca) | ok |
| s10 | Pagava ao cinema o preço cheio do ingresso a cada sessão | Business Insider FAQ ago/2017 e Inverse 2017 (busca refeita) + Wikipedia | **corrigido** (versão anterior dizia "perto do ingresso cheio") |
| s10 | Prejuízo de centenas de milhões de dólares | Fortune 12/03/2019 (lido: US$ 256,4 mi só em 3 trimestres de 2018) | ok |
| s10 | Serviço encerrado em setembro de 2019; falência (Chapter 7, liquidação) em janeiro de 2020 | PYMNTS 2020 (lido) + Wikipedia (14/09/2019 e 28/01/2020) | ok — 2 fontes independentes |
| s10 | Reportagem da Agência Estado (2023); consultor do Sebrae-SP e professor de Direito Comercial da USP; "não existe milagre"; sem sucesso garantido; Procon, consumidor.gov, Reclame Aqui | 10 (página lida) | ok |

**Fatos de alto risco com busca refeita:** datas e preço do MoviePass (Wikipedia + Business
Insider/Inverse), texto do CDC e do decreto (Planalto), número do Cetic (PDF oficial).

## 2. Erros do rascunho (Groq) que NÃO entraram

| Erro no rascunho | Por que saiu |
|---|---|
| MoviePass descrito como "plataforma de streaming de cinema" | Errado: era assinatura de ingresso pra cinema físico (cartão pago na bilheteria) |
| "a empresa (como o Emaús) te dá um link exclusivo" | O Emaús não tem programa de afiliados — inventado |
| "o reembolso é processado no Emaús nos 7 dias" | O Emaús ainda não cobra; afirmação sobre processo que não existe |
| "Procon e Idec alertam… esquemas de afiliado que recrutam pessoas" (pirâmide) | Não está em nenhuma fonte do dossiê |
| Citações inventadas em bloco `quote` ("Vender na internet não é atalho…") | Bloco de citação só pra texto real de fonte |
| CONAR "exige" usar "afiliada"/"ganho comissão" | O guia orienta "publicidade", "publi", "publipost"; e o CONAR é autorregulação, não lei |
| Curso dá receita "em picos (lançamentos)" | Sem fonte |
| Assinatura "paga um valor menor" | Sem fonte |
| Conta de preço do Emaús (custo + margem) | Assunto de T2/T5; fora do escopo |

## 3. Pedagogia

- Ordem: ideia geral (como o dinheiro entra) → cada modelo → comparação → casos que deram
  errado → aplicação na vida da aluna. Exemplo antes da abstração em cada slide (academia,
  livro de receitas × confeiteira).
- Todas as perguntas são respondíveis com o que foi ensinado:
  ck1 (s1–s2), ck2 (s1, s4, s5), ck3 (s2–s7), ck4 (s4, s10, s11, s7 e s10 nas abertas).
- Tipos variados: mc, tf, classify, associar e 2 open. ✔
- Linguagem simples; termos em inglês explicados (checkout).
- Tarefa prática ligada ao Emaús (s11). ✔

## 4. Continuidade

- Primeiro tópico do curso: não há anterior. Não invade o T2 (churn/LTV só anunciados em s4)
  nem o T3/T4 (funil e persona não aparecem).
- Módulo 6 (carreira) só anunciado em s5.

## 5. Direito autoral

- Nenhum texto longo copiado. Canvas: paráfrase. Citação literal só de lei (domínio público) e
  dois trechos curtos do guia do CONAR, atribuídos.

## 6. Estrutura

- `validar_topico()` → `[]` ✔
- Render local (temas por-do-sol, lavanda, trigo-maduro): 0 "None", 0 "undefined" ✔
- Capa com `imagem_capa` ✔ · `fluxo` (3), nenhum `diagrama` ✔ · Reflexão + Resumo ✔
- 18 ids de pergunta/item, todos únicos ✔

## Resultado

**0 pendências de fato.** Aprovado para seguir para imagens e publicação.
Pendências que NÃO são de fato: estilo das imagens (escolha do Atila no catálogo, doc
`c-vendas`) e id de produção do tópico.
