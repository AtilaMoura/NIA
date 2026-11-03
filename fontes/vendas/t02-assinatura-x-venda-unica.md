# Dossiê — T2 · Assinatura × venda única: recorrência, churn e LTV

Curso: **Vendas na Internet: do post ao primeiro cliente** (privado). Módulo 1 "Como se ganha dinheiro na internet" ·
Aula 1 "O mercado digital" · **Tópico 2** (fecha a Aula 1). Produção: `Topico.id=171` (lesson 138, `topico_index` 2) —
vazio na produção (`is_approved=false`, `content=None`, conferido em 2026-11-03). Local: id diferente (T1 = 66).

- **Antes (T1, tópico 170):** apresentou os 4 modelos (curso, assinatura, serviço, afiliado) e deixou prometido: "quanto um
  assinante vale ao longo do tempo e o que acontece quando ele cancela são assunto do próximo tópico".
- **Depois (não invadir):** Aula 2 — T3 "Funil de venda: da atenção à permanência" (tópico 172) e T4 "Público e persona".
  Também ficam para depois: CPM/CTR/CPC/CPA/ROAS e "custo por assinante" (Módulo 5, T21), checkout/Pix/cartão/Mercado Pago
  como configuração (Módulo 2), preço do Emaús e página de vendas.
- Perfil: já usa redes sociais, quer virar profissional de tráfego; texto neutro (sem nome, sem "a aluna"). Caso real: Emaús.
  **Sem verba de anúncio → todos os números do exercício são SIMULADOS e marcados como tal.**

## Fontes — o que foi LIDO de fato (2026-11-03, salvo indicação)

| # | Tipo | Referência | O que sustenta (citações exatas e curtas) |
|---|---|---|---|
| 1 | Instituição (Sebrae PE) — e-book | Sebrae PE, *Retenção de clientes: saiba tudo sobre o assunto!* (PDF, 36 p.; metadados do PDF: criado em 13/10/2020 — não há data impressa). https://bibliotecas.sebrae.com.br/chronus/ARQUIVOS_CHRONUS/bds/bds.nsf/43c63fdbac89418e556add0b4b5492a2/$File/30370.pdf (baixado e extraído com pypdf `-I`) | **Churn rate (p. 26):** "O foco principal dele é demonstrar a taxa de clientes que abandonaram, ou seja, deixaram de fazer negócios em um determinado estabelecimento." · "Ele é muito utilizado para quem trabalha com serviços de pagamentos recorrentes" · fórmula: "Churn Rate = total de clientes cancelados / número de clientes ativos x 100" · "Se a cada 20 clientes ativos, um para de consumir os seus produtos e serviços, isso significa que a sua taxa será de 5%." · "não há um número específico para determinar se o indicador é bom ou ruim" · "quanto menor ele estiver, melhor será para a empresa". **LTV (p. 25):** "O LTV é um valor monetário médio que indica a vida estimada do relacionamento de um cliente com a empresa." · "ele demonstra quanto um cliente gasta em dinheiro durante o tempo em que se relaciona" · cálculo: "multiplicar o valor médio das vendas pelo número de repetição das vendas anuais" · **LTV × CAC:** "Se o seu CAC é de R$ 5,00 e o seu indicador LTV demonstra que um cliente deixa uma receita líquida de R$ 4,80, significa que a lucratividade e a sustentabilidade do seu negócio correm um sério risco." **Taxa de retenção (p. 24):** fórmula impressa "[(CE - CN) / CS] / 100" com CE = clientes ativos no fim do período, CN = novos clientes no período, CS = clientes ativos no início; exemplo "200 clientes, perdeu 20 e ganhou 40" → "taxa de retenção de 90%". **Práticas de retenção (p. 14–16):** treinar quem atende e o suporte/pós-venda; "alinhe as expectativas do cliente"; "não prometa o que o produto não pode cumprir". **Custo:** "A redução de custos entre a aquisição e retenção de clientes pode chegar a incríveis 82%" (levantamento dos EUA, **sem fonte citada** no e-book — não usado) |
| 2 | Instituição (Sebrae/PR) | Sebrae/PR, *Economia da recorrência*, Patricia F. V. Santini, 10/08/2022 (lida no T1) | Recorrência = pagamento semanal/mensal/anual pelo acesso; receita previsível; "simplicidade na adesão E no cancelamento" e transparência |
| 3 | Empresa (blog de software de gestão) | Conta Azul, *Churn rate: tudo sobre a taxa de cancelamentos de clientes* (publicado 26/04/2021, atualizado 03/08/2026). https://contaazul.com/blog/o-que-e-churn-rate-taxa-de-cancelamento/ | "Churn é uma métrica utilizada para medir a perda de clientes na empresa." · "Churn rate (%) = total de clientes cancelados / número total de clientes ativos do último mês x 100" · exemplo "60 / 1500 x 100 = 4%" · churn de receita: "mostra qual percentual da receita contínua da empresa foi perdido com os cancelamentos no período." |
| 4 | Empresa (blog de software de gestão) | Omie, *O que é LTV e como ele pode ajudar seu negócio?* (atualizado 2023-02-15). https://www.omie.com.br/blog/o-que-e-ltv-e-como-ele-pode-ajudar-seu-negocio/ | LTV: "o quanto um cliente contribuiu financeiramente para a sua empresa durante o período em que se relacionou com ela." · "LTV= ticket médio x número de compras no ano x duração do relacionamento." (exemplo 500×3×2 = R$ 3.000) · CAC: "quanto a empresa precisa investir para conquistar um novo cliente" · "CAC= Investimentos em marketing e vendas ÷ número de clientes adquiridos." · "De maneira geral, o lifetime value deve ser maior que o CAC." (sem número e sem fonte) |
| 5 | Empresa de dados e crédito | Serasa Experian, *Lifetime Value (LTV): como calcular e aumentar o valor do cliente* (08/12/2025). https://www.serasaexperian.com.br/conteudos/ltv-o-que-e-o-que-analisar/ | "A taxa de churn indica a porcentagem de clientes que a empresa perde em um determinado período" · LTV = "a receita total que um cliente gera para uma empresa ao longo de todo o seu ciclo de vida" · duas fórmulas sem reconciliá-las: "(Ticket médio × média de compras por cliente ao ano) × média de tempo de retenção de clientes" e "(Ticket Médio × Frequência de Compra × Margem de Lucro Bruta) / Taxa de Churn" · LTV "significativamente maior" que o CAC indica retorno positivo (sem número) |
| 6 | Empresa (CRM) | Salesforce Brasil, *Customer Lifetime Value (LTV): O que é e como otimizar* (14/09/2026). https://www.salesforce.com/br/blog/customer-lifetime-value-o-que-e/ | LTV "projeta a receita que um cliente pode gerar para a empresa durante todo o seu ciclo de vida"; "Quando o valor do CAC é próximo ou maior que o do LTV, sua empresa está no prejuízo" (sem número) |
| 7 | Documentação oficial (empresa) | Mercado Pago Developers, *Assinaturas* (visão geral e gerenciamento), em português. https://www.mercadopago.com.br/developers/pt/docs/subscriptions/overview e …/subscription-management | "Esta solução permite que seus clientes assinem produtos e serviços, realizando pagamentos recorrentes de forma automática." · "Após o primeiro pagamento via Mercado Pago as cobranças seguintes ocorrem automaticamente, sem a necessidade de envio de lembretes." · "Frequência de cobrança personalizável: semanal, mensal ou anual." · "Ofereça um período de testes…" · vendedor pode "pausar, cancelar ou reativar uma assinatura já criada" (via API). A página traz taxas — **não usadas** |
| 8 | Órgão regulador (EUA) — caso | U.S. Federal Trade Commission, *FTC Secures Historic $2.5 Billion Settlement Against Amazon* (comunicado de 25/09/2025). https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-secures-historic-25-billion-settlement-against-amazon · alegação original: comunicado de 21/06/2023 (…/2023/06/ftc-takes-action-against-amazon-enrolling-consumers-amazon-prime-without-consent-sabotaging-their) · página do caso (FTC v. Amazon.com, Inc., 2:23-cv-0932, W.D. Wash.) · atualização de 17/09/2026 (pagamentos adicionais) | 2023: "The primary purpose of its Prime cancellation process was not to enable subscribers to cancel, but to stop them." (**alegação** da FTC) e "dark patterns". Acordo 2025: "Amazon will be required to pay a $1 billion civil penalty" e "provide $1.5 billion in refunds"; exige "an easy way for consumers to cancel Prime, using the same method that consumers used to sign up." e "The process cannot be difficult, costly, or time-consuming". **Nenhuma página lida diz que a Amazon admitiu ou negou irregularidade**; o texto da ordem (PDF) não foi extraído |
| 9 | Primária / lei | Decreto 7.962/2013, art. 5º (lido no T1 direto no Planalto): "O consumidor poderá exercer seu direito de arrependimento pela mesma ferramenta utilizada para a contratação, sem prejuízo de outros meios disponibilizados." (§ 1º); CDC art. 49 (7 dias) | arrependimento; mesma ferramenta |
| 10 | Documento interno | `PLANO_ACESSO_E_PAGAMENTO.md` | **Estado real do Emaús:** decisão D3 = assinatura mensal via Mercado Pago (Pix + cartão); Fase F (assinatura) é a **última** e **ainda não foi construída**; preço sugerido (mensal R$ 29,90) está **marcado como NÃO decidido**; a "Fase F" prevê página "Minha assinatura" com cancelar e matrícula que só muda de status, nunca apaga |

**Tipos cobertos (6 de 8):** instituição (Sebrae ×2), empresa/blog (×3), documentação oficial (Mercado Pago), órgão regulador
(FTC), primária/lei (CDC, Decreto), interno (Emaús). Faltam: livro-texto/artigo acadêmico de LTV (HBR bloqueado por paywall — só
introduções lidas) e dado estatístico com fonte primária (nenhuma das páginas lidas dá fonte para "LTV ≥ 3×CAC" ou "reter 5% = +25% de
lucro"; **esses números não entram no tópico**).

### O que NÃO foi possível verificar (declarado)
- **"LTV deve ser pelo menos 3× o CAC"** e **"1/churn = tempo de vida"**: apareceram só em blogs de busca; nenhuma página lida traz ou
  fundamenta. **Fora do tópico.** O tópico ensina só "o LTV precisa ser maior que o CAC" (fontes 1, 4, 5, 6) e deixa o número para o Módulo 5.
- **Stripe** (404), **HBR** (paywall) e o portal do **Sebrae** (sem artigo de churn): não usados.
- **Mercado Pago:** não foi achado nas páginas lidas (a) como o cliente cancela sozinho, (b) como a recorrência funciona por Pix/boleto
  (a visão geral lista Pix e boleto como meios, mas não explica a cobrança recorrente neles), (c) lista completa de status. O tópico
  **não afirma** nada disso; manda conferir na documentação.
- **Decreto 7.962, art. 4º, V ("…suspensão ou cancelamento do contrato")**: lido só pelo leitor automático (resumidor); o `curl` direto ao
  Planalto deu timeout. **Não usado no tópico**; conferir no Planalto antes de citar.
- **Decreto 11.034/2022 (SAC):** art. 14 trata de cancelamento "por todos os meios disponíveis para a contratação" e efeitos
  imediatos, **mas só se aplica ao SAC de serviços regulados pelo Poder Executivo federal** (art. 1º) e "não se aplica à oferta e à
  contratação de produtos e serviços" (art. 2º, parágrafo único). **Não é a regra do Emaús** → fora do tópico (evitar dizer que a lei X obriga o Emaús).
  Há um "Vide Decreto 13.135/2026" na página, não lido.
- Lei 14.181/2021 (superendividamento): lida; **não** trata de cancelamento de assinatura → fora.

## Afirmações centrais

| # | Afirmação | Fontes | Status |
|---|---|---|---|
| A1 | Venda única = o cliente paga uma vez; assinatura = paga por período (semana/mês/ano) enquanto tem acesso (recorrência) | 2, 7, T1 | ok |
| A2 | Na assinatura, a plataforma pode cobrar automaticamente depois da primeira cobrança; frequência semanal/mensal/anual | 7 | ok (Mercado Pago; sem afirmar nada sobre Pix recorrente) |
| A3 | O vendedor pode pausar, cancelar ou reativar uma assinatura | 7 | ok |
| A4 | **Churn rate** = clientes cancelados ÷ clientes ativos × 100; mede a taxa de clientes que abandonaram; é muito usado em pagamentos recorrentes; menor é melhor; não há número "bom" universal | 1, 3 | ok |
| A5 | Exemplo Sebrae: de 20 ativos, 1 para → 5% | 1 | ok |
| A6 | **Churn de receita** = % da receita recorrente perdida com os cancelamentos | 3 | ok |
| A7 | **Taxa de retenção** (fórmula do Sebrae PE: [(CE − CN) / CS] × 100): 200 no início, perdeu 20, ganhou 40 → 90% | 1 | ok — **nota:** o PDF imprime "/ 100", mas a conta do próprio exemplo dá 0,9 e o resultado é 90%, ou seja, ×100 (erro de digitação da fonte, registrado) |
| A8 | **LTV** = quanto um cliente gera de receita durante o tempo em que se relaciona com a empresa | 1, 4, 5, 6 | ok |
| A9 | Fórmula do LTV: ticket médio × compras por ano × duração (Omie; Serasa/Salesforce idem); Sebrae PE: valor médio das vendas × repetições anuais; Serasa traz uma 2ª fórmula com margem e churn | 1, 4, 5, 6 | ok — **fontes divergem** (ver abaixo) |
| A10 | **CAC** = investimento em marketing e vendas ÷ clientes conquistados | 4 | ok (fonte única) |
| A11 | O LTV precisa ser maior que o CAC; CAC de R$ 5,00 e LTV de R$ 4,80 = risco | 1, 4, 5, 6 | ok — **sem número de proporção** |
| A12 | Para baixar o churn: alinhar expectativas antes da venda, não prometer o que o produto não cumpre, cuidar do suporte/pós-venda | 1 (p. 14–16) | ok |
| A13 | Assinatura bem feita tem adesão **e cancelamento** simples e transparência | 2 | ok |
| A14 | O consumidor pode exercer o arrependimento pela mesma ferramenta da contratação (Decreto 7.962, art. 5º, § 1º) | 9 | ok |
| A15 | FTC alegou que a Amazon usou "dark patterns" e um processo de cancelamento cujo objetivo era impedir o cancelamento; em 25/09/2025 houve acordo de US$ 1 bi (multa civil) + US$ 1,5 bi (ressarcimento) e exigência de cancelar "using the same method" da inscrição, sem ser "difficult, costly, or time-consuming" | 8 | ok — apresentado como **alegação + acordo**, sem dizer que a Amazon "foi condenada" nem que "admitiu"; caso dos EUA, regra americana |
| A16 | O Emaús é planejado como assinatura mensal via Mercado Pago; o pagamento ainda não está construído; o preço ainda não foi decidido | 10 | ok — fato do projeto |

## Casos reais / casos que deram errado
- **Real:** Emaús (assinatura planejada, preço e pagamento ainda não decididos/construídos — **nada além disso**); Mercado Pago (plataforma).
- **Deu errado:** **Amazon Prime × FTC** (alegação de cancelamento sabotado → acordo bilionário). O MoviePass (preço abaixo do custo) já foi
  o caso do T1 e só é retomado em uma linha, para ligar com LTV × CAC.

## Divergências entre fontes
- **Fórmula do LTV:** Sebrae PE = valor médio das vendas × repetições anuais (sem duração); Omie = ticket × compras no ano × duração;
  Serasa e Salesforce = ticket × compras × tempo de relacionamento; Serasa também apresenta **margem de lucro ÷ churn**, sem reconciliar com a
  outra. **Decisão:** o tópico ensina a ideia (ticket × frequência × tempo) para a assinatura (mensalidade × meses que fica), diz que
  as fontes divergem em desconto de margem e **manda conferir qual fórmula a empresa adota**.
- **"Receita" × "lucro":** Sebrae PE fala "receita líquida"; Serasa mostra versão com margem bruta. O tópico trata LTV como **receita** e
  avisa que dá para refinar com margem (Serasa).
- **Churn:** Conta Azul usa "clientes ativos do **último mês**"; Sebrae PE usa "clientes ativos" sem dizer o período. **Decisão:** usa
  "no início do período" (alinhado com a retenção do Sebrae PE e com o exemplo de "a cada 20 clientes ativos").

## O que ficou de fora (e por quê)
- Número de referência de churn por setor (Baremetrics via Conta Azul: sem fonte primária lida).
- "LTV/CAC ≥ 3", "1/churn", "reter 5% = +25% de lucro" e "82% de redução de custo": sem fonte primária lida.
- Decreto 11.034 e Lei 14.181 (escopo errado), art. 4º do Decreto 7.962 (só leitor automático).
- Cohorts, MRR, ARPU, NPS, expansão/contração: acima do M1.
- Preço do Emaús, plano anual e plano igreja: **não decididos**.
- Passo a passo de ferramenta: **nenhum** (a tarefa usa só caderno ou planilha com fórmula simples; não há tela de plataforma para conferir na ajuda oficial).
