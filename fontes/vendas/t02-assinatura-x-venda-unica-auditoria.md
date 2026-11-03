# Auditoria — T2 · Assinatura × venda única: recorrência, churn e LTV

Data: 2026-11-03 · Conteúdo: `backend/_criar_t02_vendas.py` → `_t02_vendas_final.json` (16 slides, 9 imagens, 13 perguntas) ·
Dossiê: `t02-assinatura-x-venda-unica.md`.

**Resultado: 0 pendências BLOQUEANTES.** Itens "a conferir por humano" estão listados na seção 5 (não são fato afirmado como verificado).

## 1. Checklist do curso (`docs/processo-topico/vendas.md`)

| Item | Resultado |
|---|---|
| Nenhum número de taxa/comissão/renda sem fonte primária | ✔ O tópico não cita taxa, comissão nem renda. Números no texto: (a) das fontes — exemplos do Sebrae PE (1 em 20 = 5%; 200/20/40 = 90%; CAC R$ 5,00 × LTV R$ 4,80), valores do acordo FTC (US$ 1 bi + US$ 1,5 bi) e datas; (b) **simulados e marcados** ("números inventados para treinar"). A página do Mercado Pago traz taxas: **não usadas** |
| Nenhuma afirmação sobre o Emaús que não seja verdade hoje | ✔ Só diz: assinatura mensal via Mercado Pago **planejada**, página "Minha assinatura" **prevista**, pagamento **ainda não construído**, preço **ainda não decidido** (PLANO_ACESSO_E_PAGAMENTO.md D3 / Fase F / preço "NÃO decidido"). Conferido no código em 2026-11-03: nenhuma ocorrência de Mercado Pago/preapproval/pagamentos em `backend/app` nem em `emaus-web` (exceto `node_modules`) |
| Passo a passo de ferramenta conferido na ajuda oficial | ✔ N/A — o tópico **não ensina passo a passo de ferramenta** (a tarefa usa caderno ou planilha com a conta; nenhuma tela). Só descreve o que a documentação do Mercado Pago diz que a solução faz |
| Publicidade/afiliado com regra de identificação (CONAR) | ✔ N/A — afiliado não aparece neste tópico |

## 2. Afirmações × fontes (todas lidas em 2026-11-03)

| Afirmação no tópico | Fonte | Status |
|---|---|---|
| Recorrência = pagamento por semana/mês/ano pelo acesso; vantagem receita previsível; cuidado com adesão e cancelamento simples | Sebrae/PR (lida no T1) | ok |
| MP: "permite que seus clientes assinem… pagamentos recorrentes de forma automática"; cobranças seguintes automáticas, sem lembretes; frequência semanal/mensal/anual; vendedor pausa/cancela/reativa; período de testes | Mercado Pago Developers (Assinaturas) | ok (citações exatas no dossiê) |
| Não afirmar como Pix/boleto se comportam na cobrança recorrente; o cancelamento pelo cliente | MP: **não encontrado nas páginas lidas** | ok — o slide manda **conferir** na documentação |
| Churn rate = cancelados ÷ ativos × 100; taxa de clientes que abandonaram; muito usado em pagamentos recorrentes; "não há um número específico" bom/ruim; "quanto menor… melhor" | Sebrae PE, p. 26 (PDF baixado e extraído) | ok |
| Exemplo "a cada 20 clientes ativos, um para… 5%" | Sebrae PE, p. 26 | ok, citação exata |
| Conta Azul traz a mesma fórmula; churn de receita = % da receita contínua perdida | Conta Azul (26/04/2021, atualizado 03/08/2026) | ok |
| Retenção = (CE − CN) ÷ CS × 100; exemplo 200/20/40 → 90%; "indicador mais importante" | Sebrae PE, p. 24 | ok. **Erro de digitação da fonte** ("/ 100" em vez de "× 100") **declarado no slide** |
| No exemplo, churn = 20 ÷ 200 = 10% | cálculo direto do exemplo da fonte | ok (derivado, aritmética verificada) |
| LTV = valor monetário médio / receita total ao longo do relacionamento | Sebrae PE p. 25; Serasa; Salesforce | ok |
| LTV = ticket × compras no ano × duração | Omie | ok |
| Fontes divergem na fórmula do LTV; Serasa traz variante com margem/churn | Sebrae PE, Omie, Serasa | ok — declarado no slide |
| CAC = investimento em marketing e vendas ÷ clientes adquiridos | Omie | ok (fonte única) |
| LTV precisa ser maior que o CAC; CAC R$ 5,00 × LTV R$ 4,80 = risco | Omie, Serasa, Salesforce, Sebrae PE | ok — **sem proporção** (nenhuma fonte dá número; o tópico diz isso) |
| Práticas que reduzem churn: alinhar expectativas, não prometer o que não cumpre, suporte/pós-venda | Sebrae PE, p. 14–16 | ok |
| Arrependimento: 7 dias (CDC art. 49) e "mesma ferramenta" (Decreto 7.962, art. 5º, § 1º) | lido direto no Planalto no T1 | ok — texto limitado ao **arrependimento** ("as regras de cada serviço podem ter mais exigências") |
| FTC 2023: "dark patterns" e cancelamento cujo objetivo era impedir; **alegação** | comunicado FTC 21/06/2023 | ok — marcado como alegação, tradução livre |
| FTC 25/09/2025: US$ 1 bi multa civil + US$ 1,5 bi ressarcimento; informar termos; cancelar "using the same method"; "cannot be difficult, costly, or time-consuming" | comunicado FTC 25/09/2025 | ok |
| Páginas da FTC lidas não dizem se a Amazon admitiu ou negou | comunicados 2023/2025/2026 e página do caso | ok — declarado no slide e no ck4_2 |
| Caso é dos EUA, não lei brasileira | — | ok (dito no slide) |
| Cálculos dos exemplos: 2÷40=5%; 5÷50=10%; (220−40)÷200=90%; 30×10=300; 400÷10=40; 3÷50=6%; (57−10)÷50=94%; 20×6=120; 4÷80=5%; 25×8=200 | aritmética | ✔ todas conferidas |

## 3. Erros de rascunho / ideias que NÃO entraram

- "LTV ≥ 3× o CAC", "tempo de vida = 1 ÷ churn", "reter 5% aumenta o lucro em 25%", "reduzir custo em 82%": **só apareceram em blogs/buscas ou em e-book sem fonte; nenhuma fonte lida fundamenta** → fora.
- Decreto 11.034/2022 (SAC): regula SAC de serviços **regulados pelo governo federal** e não se aplica à contratação → não é a regra do Emaús; citá-lo seria afirmar algo falso.
- Decreto 7.962, art. 4º, V (atendimento para "cancelamento do contrato"): lido só pelo leitor automático (curl direto ao Planalto deu timeout) → fora até conferir.
- Lei 14.181/2021: trata de superendividamento, não de cancelamento → fora.
- Benchmark de churn por setor (Baremetrics via Conta Azul): sem fonte primária lida → fora.
- Afirmar que o Pix/boleto "renovam sozinhos": a documentação lida não diz → fora (slide manda conferir).

## 4. Pedagogia e continuidade

- Responde as duas perguntas que o T1 deixou ("quanto um assinante vale" e "o que acontece quando ele cancela"); fecha a Aula 1; "Próximo" aponta o T3 (funil).
- Não invade: funil, persona, CPM/CTR/CPC/CPA/ROAS e custo por assinante (Módulo 5), checkout/Pix/cartão como configuração, preço do Emaús.
- Ordem: duas contas → cobrança repete → churn → retenção → LTV → CAC → cancelar fácil (ética + caso real) → tarefa Emaús → reflexão/resumo.
- Cada checkpoint usa só conceitos já ensinados até aquele ponto (ck1 = recorrência; ck2 = churn/retenção; ck3 = churn, CAC×LTV, LTV; ck4 = caso FTC; ck5 = síntese).
- Dificuldade: reconhecimento (classify, mc, tf, associar) → cálculo (lacuna, mc numérico) → escrita livre (2 abertas).
- Texto neutro (sem nome, sem "a aluna"); "profissional" e "você".
- Caso que deu errado: Amazon × FTC (alegação + acordo) e uma linha do MoviePass do T1.

## 5. Itens a conferir por humano (não bloqueiam)

- **Decreto 7.962, art. 4º, V**: se o Atila quiser usá-lo depois, conferir o texto no Planalto (o leitor automático é um resumidor).
- **Tipos de fonte:** só 6 dos 8 tipos (faltam livro-texto/artigo acadêmico de LTV — HBR só com introdução por paywall — e dado estatístico primário sobre churn). As fórmulas vêm do guia do **Sebrae PE (instituição)** e de 3 blogs de empresas (Conta Azul, Omie, Serasa/Salesforce); por isso o tópico declara a divergência e não afirma número de referência.
- **Data do guia do Sebrae PE:** só os metadados do PDF (criado em 13/10/2020); não há data impressa.
- **Mercado Pago:** documentação lida em 2026-11-03; mudanças futuras da plataforma exigem reler.

## 6. Estrutura

- Capa com `imagem_capa` ✔ · `fluxo` (2) ✔ · Reflexão "💭 Pra pensar" + Resumo ✔ · tarefa com o Emaús (caderno/planilha) ✔.
- Perguntas: **13** — classify 1, associar 1, tf 4, mc 4, lacuna 1, **open 2** ✔; ids únicos ✔; `validar_topico()` vazio ✔.
