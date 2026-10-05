# Fila de criação de tópicos

A tarefa diária (`scripts/tarefa_topico_diaria.ps1`) pega o **primeiro tópico com status
`pendente`**, pergunta ao Atila se pode gerar e, com o Sim, roda `/criar-topico <id>` no Claude
Code. Reordene as linhas pra mudar a prioridade. Status: `pendente`, `em andamento`, `feito`,
`parcial` (publicado, mas falta algo — ver "falta"), `pulado`.

| ordem | topico_id | curso | módulo / aula | título | status | falta |
|---|---|---|---|---|---|---|
| 1 | 21 | IA (5) | Aula 2 · Transformers por dentro | Positional Encoding | pendente | |
| 2 | 68 | Obreiro I (8) | M2 · A Bíblia como Autoridade | Suficiência das Escrituras (2Pe 1:19-21) | pendente | |
| 3 | 33 | Redes (11) | M1 · NAT, Firewall e DNS | NAT (Network Address Translation) | pendente | |
| 4 | 69 | Obreiro I (8) | M2 · A Bíblia como Autoridade | A Palavra acima da tradição (Mc 7:6-13) | pendente | |

## Já feitos (processo novo)
| topico_id | curso | título | data |
|---|---|---|---|
| 31 | Redes | Portas TCP/UDP (554, 1935, 80, 443) | 2026-10-01 |
| 66 | Obreiro I | Inspiração: a Escritura soprada por Deus | 2026-10-01 |
| 32 | Redes | TCP vs UDP aplicado a vídeo (1º via /criar-topico) | 2026-10-03 |
| 67 | Obreiro I | Confiabilidade da Palavra (Sl 19:7-11) | 2026-10-05 |
