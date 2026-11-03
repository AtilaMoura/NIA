# Fila de criação de tópicos

A tarefa diária (`scripts/tarefa_topico_diaria.ps1`) pega o **primeiro tópico com status
`pendente`**, pergunta ao Atila se pode gerar e, com o Sim, roda `/criar-topico <id>` no Claude
Code. Reordene as linhas pra mudar a prioridade. Status: `pendente`, `em andamento`, `feito`,
`parcial` (publicado, mas falta algo — ver "falta"), `pulado`.

| ordem | topico_id | curso | módulo / aula | título | status | falta |
|---|---|---|---|---|---|---|
| 1 | 34 | Redes (11) | M1 · NAT, Firewall e DNS | Firewall — bloqueio de entrada vs. saída | feito | |
| 2 | 22 | IA (5) | Aula 2 · Transformers por dentro | Self-Attention: Query, Key, Value | feito | |
| 3 | 70 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Como os 66 livros se formaram (Lc 24:44) ⚠️ cânon 66×73 — nota de neutralidade | feito | |
| 4 | 194 | Inglês (9) | M0 · Quando eu não entendo | "Sorry, I don't understand", "Can you repeat that?", "Can you speak more slowly?" | feito | |
| 5 | 35 | Redes (11) | M1 · NAT, Firewall e DNS | DNS e DDNS | pendente | |
| 6 | 23 | IA (5) | Aula 2 · Transformers por dentro | Causal Masking + Multi-Head Attention | pendente | |
| 7 | 71 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Antigo Testamento: criação, aliança, reino e exílio (Gn 12:1-3) | pendente | |
| 8 | 195 | Inglês (9) | M0 · Quando eu não entendo | "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto | feito | |
| 9 | 36 | Redes (11) | M2 · Port Forwarding | Como funciona o redirecionamento de porta | pendente | |
| 10 | 24 | IA (5) | Aula 2 · Transformers por dentro | Dentro do bloco Transformer | pendente | |
| 11 | 72 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Novo Testamento: Cristo, igreja e consumação (Hb 1:1-2) | pendente | |
| 12 | 196 | Inglês (9) | M0 · Quando eu não entendo | Prática: pedir ajuda numa conversa curta | feito | |
| 13 | 37 | Redes (11) | M2 · Port Forwarding | Riscos de expor porta na internet | pendente | |
| 14 | 25 | IA (5) | Aula 2 · Transformers por dentro | Dos logits ao desempenho — KV Cache, Prefill/Decode | pendente | |
| 15 | 73 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Cristo em toda a Escritura (Lc 24:27) | pendente | |
| 16 | 197 | Inglês (9) | M0 · Entendendo o professor | As instruções de todo exercício: read, listen, write, answer, choose, match, repeat | feito | conferência humana: "Match the words and the pictures." é exemplo próprio e match = "ligar/combinar" não foi checado em dicionário (Oxford/Collins/M-W bloqueiam acesso automatizado); níveis CEFR dos 7 verbos não verificados |
| 17 | 170 | Vendas (13, privado) | M1 · O mercado digital | T1 Modelos de negócio online: curso, assinatura, serviço e afiliado | feito | áudio completo (26/26) em 2026-11-02; os outros 23 tópicos do curso 13 ainda estão vazios. O `_diagnostico_topicos.py` acusa "dossiê + auditoria: NÃO EXISTEM" porque procura `topico170-*`, e os arquivos estão em `fontes/vendas/t01-*` |
| 18 | 198 | Inglês (9) | M0 · Entendendo o professor | Confirmar o que entendeu: "You mean…? / Exactly" | feito | conferência humana: "Exactly." = "Exatamente." só tem o vídeo como fonte (dicionários bloqueiam o leitor automático); "You mean…?" sem fonte institucional (só vídeo; "Do you mean…?" tem o British Council) |
| 19 | 199 | Inglês (9) | M0 · Entendendo o professor | Juntando tudo: uma aula inteira em inglês simples | feito | síntese simulada (não é aula real); herda de T197/T198: "Match the words and the pictures." é exemplo próprio; "Exactly." e "You mean …?" com fonte só no vídeo |
| 20 | 200 | Inglês (9) | M1 · He/she/it + -s | He works, she lives: o -s da 3ª pessoa (e a grafia -es, -ies) | pendente | |
| 21 | 201 | Inglês (9) | M1 · He/she/it + -s | Doesn't: a negativa com he/she/it | pendente | |
| 22 | 202 | Inglês (9) | M1 · He/she/it + -s | Prática: he/she/it no dia a dia | pendente | |
| 23 | 203 | Inglês (9) | M1 · He/she/it + -s | Juntando tudo: I, you e he/she/it sem pista | pendente | |
| 24 | 204 | Inglês (9) | M1 · Fazendo perguntas | "Do you…? / Does she…?" e as respostas curtas | pendente | |
| 25 | 205 | Inglês (9) | M1 · Fazendo perguntas | Palavras de pergunta: what, where, who, when, how, how old | pendente | |
| 26 | 206 | Inglês (9) | M1 · Fazendo perguntas | Prática: perguntar e responder | pendente | |
| 27 | 207 | Inglês (9) | M1 · Fazendo perguntas | Juntando tudo: uma entrevista de apresentação | pendente | |
| 28 | 208 | Inglês (9) | M2 · Números | Números de 0 a 20 | pendente | |
| 29 | 209 | Inglês (9) | M2 · Números | De 20 a 1000: preços, idade e telefone | pendente | |
| 30 | 210 | Inglês (9) | M2 · Números | Prática: ditado de números | pendente | |
| 31 | 211 | Inglês (9) | M2 · Horas | "What time is it?": o'clock, half past, quarter past/to | pendente | |
| 32 | 212 | Inglês (9) | M2 · Horas | a.m./p.m. e morning, afternoon, evening, night | pendente | |
| 33 | 213 | Inglês (9) | M2 · Horas | Prática: horários do dia | pendente | |
| 34 | 214 | Inglês (9) | M2 · Dias, semanas, meses e datas | Dias da semana e meses do ano | pendente | |
| 35 | 215 | Inglês (9) | M2 · Dias, semanas, meses e datas | Números ordinais e datas (first… thirty-first) | pendente | |
| 36 | 216 | Inglês (9) | M2 · Dias, semanas, meses e datas | Preposições de tempo: at, in, on | pendente | |

## Já feitos (processo novo)
| topico_id | curso | título | data |
|---|---|---|---|
| 31 | Redes | Portas TCP/UDP (554, 1935, 80, 443) | 2026-10-01 |
| 66 | Obreiro I | Inspiração: a Escritura soprada por Deus · **prova 38 no padrão novo (18/6, 60%) em 2026-10-07** | 2026-10-01 |
| 32 | Redes | TCP vs UDP aplicado a vídeo (1º via /criar-topico) | 2026-10-03 |
| 67 | Obreiro I | Confiabilidade da Palavra (Sl 19:7-11) | 2026-10-05 |
| 21 | IA | Positional Encoding | 2026-10-05 |
| 68 | Obreiro I | Suficiência das Escrituras (2Pe 1:19-21) | 2026-10-05 |
| 33 | Redes | NAT (Network Address Translation) — áudio terminado depois · **prova 37 no padrão novo (18/6, 70%) em 2026-10-07** | 2026-10-05 |
| 69 | Obreiro I | A Palavra acima da tradição (Mc 7:6-13) — fecha a Aula 60 | 2026-10-06 |
| 34 | Redes | Firewall — bloqueio de entrada vs. saída (16 slides, 8 imagens, 32 áudios) | 2026-10-11 |
| 22 | IA | Self-Attention: Query, Key, Value (17 slides, 8 imagens, 35 áudios) | 2026-10-12 |
| 70 | Obreiro I | Como os 66 livros se formaram (Lc 24:44) — abre a Aula 58 (17 slides, 8 imagens, 36 áudios); leitura do teólogo/pastor recomendada | 2026-10-13 |
| 194 | Inglês | "Sorry, I don't understand", "Can you repeat that?", "Can you speak more slowly?" — 1º tópico do curso (M0); título ajustado: nenhuma fonte ensina "More slowly, please" solto (16 slides, 7 imagens, 15 áudios) | 2026-10-14 |
| 195 | Inglês | "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto — 2º tópico do M0 (17 slides, 7 imagens, 15 perguntas, 16 áudios); conferir de ouvido os 🔊 dos cards de letra ("Letter X") no navegador | 2026-10-28 |
| 196 | Inglês | Prática: pedir ajuda numa conversa curta — fecha a Aula 1 do M0 (16 slides, 7 imagens, 14 perguntas, 12 áudios; sem palavra nova, só diálogos com a lista fechada T194+T195) | 2026-10-31 |
| 197 | Inglês | As instruções de todo exercício: read, listen, write, answer, choose, match, repeat — abre a Aula 2 do M0 (16 slides, 7 imagens, 14 perguntas, 15 áudios); fontes lidas: ELTeach, Cambridge Young Learners (Starters/Movers), British Council A1; "match" sem instrução literal nas fontes → ver coluna "falta" | 2026-10-31 |
| 198 | Inglês | Confirmar o que entendeu: "You mean…?" / "Exactly" — 2º tópico da Aula 2 do M0 (16 slides, 7 imagens, 13 perguntas, 14 áudios); fontes lidas: British Council *Checking understanding* (A1) e vídeo Teacher Abelhinha (T7 guardado) | 2026-11-02 |
| 170 | Vendas | Modelos de negócio online — áudio concluído (26/26 blocos; 2026-11-02) | 2026-11-02 |
| 199 | Inglês | Juntando tudo: uma aula inteira em inglês simples — fecha a Aula 2 e o M0 inteiro (16 slides, 7 imagens, 13 perguntas, 14 áudios); aula simulada em 4 cenas só com a lista fechada T194–T198; frase do módulo "Eu consigo pedir ajuda em inglês quando não entendo." | 2026-11-03 |
| 171 | Vendas | Assinatura × venda única: recorrência, churn e LTV — T2 do curso 13, fecha a Aula 1 do M1 (16 slides, 9 imagens sketchnote, 13 perguntas, 35 áudios); fontes lidas: Sebrae PE (e-book de retenção), Sebrae/PR, Conta Azul, Omie, Serasa, Salesforce, Mercado Pago Developers, FTC × Amazon, CDC/Decreto 7.962; números do exercício SIMULADOS; nenhum número de taxa/renda; Emaús só no que é verdade hoje (pagamento não construído, preço não decidido) | 2026-11-03 |
| 172 | Vendas | Funil de venda: da atenção à permanência — T3 do curso 13, abre a Aula 2 do M1 (14 slides, 8 imagens sketchnote, 12 perguntas, 27 áudios); fontes lidas: Sebrae ×4 (PDF E-commerce, Sebrae SC, Comunidade Sebrae PR ×2, e-book Sebrae PE), Baymard, LGPD arts. 5º/6º/8º; números de conversão do exercício SIMULADOS; Emaús só no que é verdade hoje (página de visitante + "Criar conta grátis" existem; assinatura é só plano). McKinsey não lida → fora; tipos de fonte 5 de 8 | 2026-11-03 |
| 173 | Vendas | Público e persona: quem assina o Emaús — T4 do curso 13, fecha a Aula 2 e o Módulo 1 (13 slides, 7 imagens sketchnote, 12 perguntas, 23 áudios); fontes lidas: Sebrae PE (guia de persona), Sebrae MG, Meta ×3 (anúncio 2021, blog de desenvolvedores, política de atributos pessoais 2024), LGPD arts. 5º II e 11; persona do Emaús = HIPÓTESE (sem dados de assinantes); convicção religiosa = dado sensível e a Meta proíbe afirmar/sugerir atributos → nada de segmentar por religião. A conferir por humano: lista de alunos × LGPD art. 11 §1º (advogado); regras de públicos personalizados da Meta (Módulo 4) | 2026-11-03 |
