# Teste comparativo de modelos — 2026-10-01

Régua: Tópico 31 "Portas TCP/UDP" (curso Redes). Mesma tarefa pra todos: organizar o
dossiê (`fontes/redes/topico31-portas-tcp-udp.md`) em 3 slides + 4 perguntas, em JSON,
**1 pedido por modelo**. Pontuação automática (`backend/_benchmark_modelos_t31.py`) +
**leitura completa por Claude** contra a auditoria do T31. Respostas cruas em
`backend/_benchmark_t31/`. Limites de cota: [LIMITES_GEMINI.md](LIMITES_GEMINI.md).

## Texto (gerar conteúdo + perguntas)

| # | Modelo | Erros de fato (lidos) | Tempo | Qualidade | Disponibilidade |
|---|---|---|---|---|---|
| 1 | **gemini-3.5-flash** | 0 | 26s | A mais rica: incluiu Windows/Linux, perguntas que exigem raciocínio | 503 em 3 de 4 tentativas · 20/dia |
| 2 | **gemini-3.7-flash** | 0 | 12s | Correta e clara, boas perguntas | 503 em 3 de 4 · 20/dia |
| 3 | **gemini-2.5-flash** (default atual) | 0 | 20s | Correta e completa | respondeu de primeira · 20/dia |
| 4 | **gemini-3.5-flash-lite** | 0 | 6s | Correta, mas pulou parte do pedido (não disse a faixa da 554/37777) | de primeira · **500/dia** |
| 5 | **gemma-4-31b** | 0 | **111s** | Correta; 1 pergunta fraca ("qual o IP do NVR") | de primeira · **14.400/dia** |
| 6 | groq qwen3.8-27b | **1** (554 na faixa registrada) | 3s | Rica, mas errou raciocínio numérico | de primeira |
| 7 | groq gpt-oss-120b (usado hoje) | **3** (554 "faixa de usuário", 37777 "faixa dinâmica", "trocar porta aumenta segurança" — fora do dossiê) | 3s | Rápida, erra número | de primeira |
| — | gemini-3.8-flash | sem resultado | — | — | **503 nas 4 tentativas** |

**Padrões observados**
- Os dois modelos do **Groq erram quando precisam raciocinar com número** ("em que faixa
  cai a 554?"), mesmo com a resposta no dossiê. Servem como segunda opinião, nunca como
  fonte final de fato.
- Os **Gemini não erraram** com o dossiê na mão. O problema deles é **503 (alta demanda)**
  nos modelos mais novos, não qualidade.
- Pontuação automática: pegou os erros do Groq depois de ganhar 3 armadilhas novas, mas
  deu 1 falso positivo (3.7 Flash: pergunta V/F correta "37777 é pro navegador? Falso").
  A leitura humana/Claude continua obrigatória.

## Voz (TTS) — mesmo trecho do T31

| Modelo | Tempo | Arquivo |
|---|---|---|
| gemini-2.5-flash-preview-tts (atual) | 15s (1 timeout 504 antes) | `_benchmark_t31/tts-gemini-2.5-flash-preview-tts.wav` |
| gemini-3.8-flash-tts | 11s (1 timeout 504 antes) | `_benchmark_t31/tts-gemini-3.8-flash-tts.wav` |
| gemini-3.8-flash-lite-tts | 9–10s | `_benchmark_t31/tts-gemini-3.8-flash-lite-tts.wav` |

Escolha da voz (Atila, 2026-10-01): **as 3 são boas → revezar as 3** (3 × 10/dia = 30
chamadas/dia; com o 3.1 Flash TTS, 40).

## Áudio de vários blocos numa chamada só (ideia do Atila) — FUNCIONA

Script: `backend/_teste_audio_lote.py`. 5 blocos reais do T31 numa única chamada TTS:

| Tentativa | Como cortou | Resultado |
|---|---|---|
| 1 — instrução "faça pausa de 3s" junto do texto | por silêncio | ❌ O modelo **leu a instrução em voz alta** ("Leia em português…", "Trecho 1") e não fez pausa longa (maior pausa 1,1s ≈ pausa normal de frase) → cortes errados, correlação −0,58 |
| 2 — só o texto puro, blocos separados por parágrafo | **Whisper do Groq** (`whisper-large-v3-turbo`, tempo por palavra): acha onde começam as 4 primeiras palavras de cada bloco | ✅ 1 chamada (3.8 Flash TTS, 35s) → 100s de áudio → 5 pedaços certos, 7–9s por 100 caracteres, correlação 0,945. Whisper levou 2,7s |

**Regras que saíram do teste:**
1. O modelo de voz **lê tudo o que recebe** — nunca mandar instrução, rótulo ou número de trecho junto do texto.
2. Cortar pela **transcrição com tempo por palavra**, não por silêncio.
3. Conta: 30 chamadas/dia × ~5 blocos = **~150 blocos/dia** (antes: 30). Um tópico tem ~15–25 blocos → 3–5 chamadas.
4. Ainda a medir: quantos blocos cabem por chamada antes de estourar (TPM do TTS é 10K) — testar 8 e 12.

## Recomendação (aguardando aprovação)

| Função | Primeira opção | Se der 503/cota | Depois |
|---|---|---|---|
| Gerar conteúdo (a partir do dossiê) | 3.5 Flash | 3.7 Flash → 2.5 Flash → 3.8 Flash | Gemma 4 31B (lento, mas 14.400/dia) |
| Segunda opinião (híbrido) | Groq qwen3.8-27b (errou menos que o gpt-oss) | gpt-oss-120b | — |
| Perguntas (QuizAgent) | 3.5 Flash | 3.7 / 2.5 Flash | 3.5 Flash Lite |
| Tutor da plataforma | 3.5 Flash Lite (mantém) | 3.1 Flash Lite | Groq qwen3.8-27b |
| Texto da narração (volume) | Gemma 4 31B | 3.5 Flash Lite | — |
| Voz (TTS) | a escolhida pelo Atila | revezar os outros TTS (10/dia cada) | testar API Live (ilimitada) |

O ponto central: como o maior problema é **503**, o arquivo único de modelos precisa de
**cadeia de reserva automática** (tenta o próximo modelo quando um dá 503/cota), não só
um modelo por função.
