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
| 4 | 194 | Inglês (9) | M0 · Quando eu não entendo | "Sorry, I don't understand", "Can you repeat that?", "More slowly, please" | pendente | |
| 5 | 35 | Redes (11) | M1 · NAT, Firewall e DNS | DNS e DDNS | pendente | |
| 6 | 23 | IA (5) | Aula 2 · Transformers por dentro | Causal Masking + Multi-Head Attention | pendente | |
| 7 | 71 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Antigo Testamento: criação, aliança, reino e exílio (Gn 12:1-3) | pendente | |
| 8 | 195 | Inglês (9) | M0 · Quando eu não entendo | "How do you say…?", "What does … mean?", "How do you spell…?" e o alfabeto | pendente | |
| 9 | 36 | Redes (11) | M2 · Port Forwarding | Como funciona o redirecionamento de porta | pendente | |
| 10 | 24 | IA (5) | Aula 2 · Transformers por dentro | Dentro do bloco Transformer | pendente | |
| 11 | 72 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Novo Testamento: Cristo, igreja e consumação (Hb 1:1-2) | pendente | |
| 12 | 196 | Inglês (9) | M0 · Quando eu não entendo | Prática: pedir ajuda numa conversa curta | pendente | |
| 13 | 37 | Redes (11) | M2 · Port Forwarding | Riscos de expor porta na internet | pendente | |
| 14 | 25 | IA (5) | Aula 2 · Transformers por dentro | Dos logits ao desempenho — KV Cache, Prefill/Decode | pendente | |
| 15 | 73 | Obreiro I (8) | M2 · Panorama Geral da Bíblia | Cristo em toda a Escritura (Lc 24:27) | pendente | |
| 16 | 197 | Inglês (9) | M0 · Entendendo o professor | As instruções de todo exercício: read, listen, write, answer, choose, match, repeat | pendente | |
| 17 | 170 | Vendas (13, privado) | M1 · O mercado digital | T1 Modelos de negócio online: curso, assinatura, serviço e afiliado | parcial | áudio: 5/26 blocos com voz (cota TTS do dia, 2026-10-07). Continuar: `AUDIO_FONTE=prod python backend/_gerar_audio_topico.py 170 13 voz` (pula os prontos; narrações já revisadas) → mp3 → `_conferir_audio.py 170 13` → scp -r `static/audio/curso13` → aplicar prod |
| 18 | 198 | Inglês (9) | M0 · Entendendo o professor | Confirmar o que entendeu: "You mean…? / Exactly" | pendente | |
| 19 | 199 | Inglês (9) | M0 · Entendendo o professor | Juntando tudo: uma aula inteira em inglês simples | pendente | |
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
