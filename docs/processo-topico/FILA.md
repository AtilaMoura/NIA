# Fila de criação de tópicos

A tarefa diária (`scripts/tarefa_topico_diaria.ps1`) pega o **primeiro tópico com status
`pendente`**, pergunta ao Atila se pode gerar e, com o Sim, roda `/criar-topico <id>` no Claude
Code. Reordene as linhas pra mudar a prioridade. Status: `pendente`, `em andamento`, `feito`,
`parcial` (publicado, mas falta algo — ver "falta"), `pulado`.

| ordem | topico_id | curso | módulo / aula | título | status | falta |
|---|---|---|---|---|---|---|
| 1 | 34 | Redes (11) | M1 · NAT, Firewall e DNS | Firewall — bloqueio de entrada vs. saída | pendente | |
| 2 | 22 | IA (5) | Aula 2 · Transformers por dentro | Self-Attention: Query, Key, Value | pendente | |
| 3 | 70 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Como os 66 livros se formaram (Lc 24:44) ⚠️ cânon 66×73 — nota de neutralidade | pendente | |
| 4 | 35 | Redes (11) | M1 · NAT, Firewall e DNS | DNS e DDNS | pendente | |
| 5 | 23 | IA (5) | Aula 2 · Transformers por dentro | Causal Masking + Multi-Head Attention | pendente | |
| 6 | 71 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Antigo Testamento: criação, aliança, reino e exílio (Gn 12:1-3) | pendente | |
| 7 | 36 | Redes (11) | M2 · Port Forwarding | Como funciona o redirecionamento de porta | pendente | |
| 8 | 24 | IA (5) | Aula 2 · Transformers por dentro | Dentro do bloco Transformer | pendente | |
| 9 | 72 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Novo Testamento: Cristo, igreja e consumação (Hb 1:1-2) | pendente | |
| 10 | 37 | Redes (11) | M2 · Port Forwarding | Riscos de expor porta na internet | pendente | |
| 11 | 25 | IA (5) | Aula 2 · Transformers por dentro | Dos logits ao desempenho — KV Cache, Prefill/Decode | pendente | |
| 12 | 73 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Cristo em toda a Escritura (Lc 24:27) | pendente | |
| 13 | ? (prod) · 66 (local) | Vendas (privado) | M1 · O mercado digital | T1 Modelos de negócio online: curso, assinatura, serviço e afiliado | em andamento | imagens (sketchnote) → id de produção + NIA_EMAIL/NIA_SENHA pra publicar → áudio |

## Já feitos (processo novo)
| topico_id | curso | título | data |
|---|---|---|---|
| 31 | Redes | Portas TCP/UDP (554, 1935, 80, 443) | 2026-10-01 |
| 66 | Obreiro I | Inspiração: a Escritura soprada por Deus | 2026-10-01 |
| 32 | Redes | TCP vs UDP aplicado a vídeo (1º via /criar-topico) | 2026-10-03 |
| 67 | Obreiro I | Confiabilidade da Palavra (Sl 19:7-11) | 2026-10-05 |
| 21 | IA | Positional Encoding | 2026-10-05 |
| 68 | Obreiro I | Suficiência das Escrituras (2Pe 1:19-21) | 2026-10-05 |
| 33 | Redes | NAT (Network Address Translation) — áudio terminado depois | 2026-10-05 |
| 69 | Obreiro I | A Palavra acima da tradição (Mc 7:6-13) — fecha a Aula 60 | 2026-10-06 |
