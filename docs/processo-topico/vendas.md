# Especificação — Vendas na Internet (estudo privado da Amanda)

Segue a [BASE](BASE.md). Curso criado em 2026-10-06, **privado** (só o Master e quem ele liberar
em Pessoas veem). Grade aprovada pelo Atila: 6 módulos × 2 aulas × 2 tópicos = 24 tópicos
(`backend/_criar_curso_vendas_internet.py`).

- **Course.id:** local 12 · produção: conferir na saída do script de criação (o 12 de produção é
  o Obreiro II — não confundir).
- **Aluna:** já usa redes sociais; objetivo **virar profissional** (gestora de tráfego).
- **Canais:** Meta Ads, orgânico + WhatsApp, TikTok Ads (Google fora).
- **Prática:** cada tópico termina com tarefa usando o **Emaús** como caso real, com passo a passo
  nas ferramentas. **Sem verba de anúncio:** campanha montada até antes de publicar, números
  simulados.
- **Inclui:** criativos básicos (copy, roteiro, Canva, CapCut) e módulo de carreira.
- **Tema e estilo de imagem:** escolha do Atila no catálogo visual, doc `c-vendas` (id fixo, não
  depende do Course.id). Pasta de imagens: `backend/static/course-images/vendas/`.
- **Perfil do tutor/geração:** `PERFIL_VENDAS` montado dentro de `backend/_gerar_tNN_vendas.py`
  (o processo de tópico não mexe em `app/agents/perfis.py`). O tutor ao vivo em produção usa o
  perfil padrão até alguém criar o perfil no app (tarefa de código, separada).
- **Nomes de arquivo:** `fontes/vendas/tNN-<slug>.md` (pelo número do tópico no curso, não pelo
  id do banco, que é diferente entre local e produção).

## Regras do curso

- **Nunca prometer ganho** nem citar renda, taxa, comissão ou percentual sem fonte primária lida
  (taxas de plataforma mudam — ensinar a conferir a tabela oficial).
- Ferramentas (Gerenciador de Anúncios, TikTok Ads Manager, WhatsApp Business, Canva, CapCut)
  mudam a tela com frequência: passo a passo **conferido na central de ajuda oficial** na data do
  tópico, com a data anotada no dossiê.
- Políticas de anúncio (Meta, TikTok), CDC, Decreto 7.962/2013, LGPD e guia do CONAR: sempre
  lidos na fonte primária.
- O Emaús é o caso real, mas **não inventar o que ele não tem** (ex.: o rascunho do T1 inventou
  programa de afiliados e reembolso do Emaús). Estado real do Emaús: assinatura planejada
  (PLANO_ACESSO_E_PAGAMENTO.md), pagamento ainda não construído.

## Passo 5 — Auditoria (checklist do curso)

- [ ] Nenhum número de taxa/comissão/renda sem fonte primária
- [ ] Nenhuma afirmação sobre o Emaús que não seja verdade hoje
- [ ] Passo a passo de ferramenta conferido na ajuda oficial (com data)
- [ ] Publicidade/afiliado sempre com a regra de identificação (CONAR)
