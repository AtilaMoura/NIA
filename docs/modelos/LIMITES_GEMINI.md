# Limites do Gemini (plano gratuito) — projeto do Atila

Fonte: AI Studio → Rate limits, copiado pelo Atila em **2026-10-01**. São os limites do
projeto dele (não números de blog). **Cada modelo tem a sua própria cota** — usar o
3.5 Flash não gasta a cota do 3.8 Flash. Atualizar este arquivo quando o Google mudar.

RPM = pedidos por minuto · TPM = tokens por minuto · RPD = pedidos por dia.

## Texto

| Modelo | RPM | TPM | RPD | Observação |
|---|---|---|---|---|
| Gemini 3.8 Flash | 5 | 250K | 20 | Flash mais novo |
| Gemini 3.7 Flash | 5 | 250K | 20 | |
| Gemini 3.6 Flash | 5 | 250K | 20 | |
| Gemini 3.5 Flash | 5 | 250K | 20 | |
| Gemini 3 Flash | 5 | 250K | 20 | |
| Gemini 2.5 Flash | 5 | 250K | 20 | default antigo do `GeminiService` |
| **Gemini 3.5 Flash Lite** | **15** | 250K | **500** | hoje no Tutor |
| **Gemini 3.1 Flash Lite** | **15** | 250K | **500** | |
| Gemini 2.5 Flash Lite | 10 | 250K | 20 | |
| **Gemma 4 31B** | **30** | 16K | **14.400** | modelo aberto; TPM baixo (prompt curto) |
| **Gemma 4 26B** | **30** | 16K | **14.400** | idem |
| Gemini Robotics ER 2 Preview | 5 | 250K | 20 | não usar (robótica) |
| Gemini 2 Flash / 2 Flash Lite | 0 | 0 | 0 | sem acesso |
| Gemini 2.5 Pro / 3.1 Pro | 0 | 0 | 0 | **sem acesso a Pro no gratuito** |

## Áudio (TTS) e transcrição

| Modelo | RPM | TPM | RPD |
|---|---|---|---|
| Gemini 3.8 Flash TTS | 3 | 10K | 10 |
| Gemini 3.8 Flash Lite TTS | 3 | 10K | 10 |
| Gemini 3.1 Flash TTS | 3 | 10K | 10 |
| Gemini 2.5 Flash TTS | 3 | 10K | 10 |
| Gemini 2.5 Pro TTS | 0 | 0 | 0 |
| Gemini 3.5 Transcribe | 3 | 10K | 25 |

## API Live (tempo real, voz)

| Modelo | RPM | TPM | RPD |
|---|---|---|---|
| Gemini 3.8 Live | ilimitado | 65K | ilimitado |
| Gemini 3.8 Live Extended Thinking | ilimitado | 65K | ilimitado |
| Gemini 3 Flash Live | ilimitado | 65K | ilimitado |
| Gemini 2.5 Flash Native Audio Dialog | ilimitado | 1M | ilimitado |
| Gemini 3.5 Transcribe Live | ilimitado | 20K | ilimitado |
| Gemini 3.5 Live Translate | ilimitado | 20K | ilimitado |

## Outros

| Modelo | RPM | TPM | RPD |
|---|---|---|---|
| Gemini Embedding 1 / 2 | 100 | 30K | 1.000 |
| Antigravity (agentes) | 60 | 100K | 100 |
| Imagem (Nano Banana, Nano Banana 2/Lite/Pro) | 0 | 0 | 0 |
| Vídeo (Veo 3 / Fast / Lite) | 0 | — | 0 |
| Música (Lyria 3) | 0 | 0 | 0 |
| Deep Research Pro, Computer Use, Omni | 0 | 0 | 0 |

## Ferramentas (por dia)

| Ferramenta | Modelos com cota | RPD |
|---|---|---|
| Pesquisa Google (grounding) | Gemini 2 / 2.5 / Default | 1.500 |
| Pesquisa Google (grounding) | Gemini 3.x | 0 |
| Google Maps (grounding) | 2.5 Flash, 2.5/3.1/3.5 Flash Lite, 3.1 TTS, 3.5 Transcribe | 500 |

---

## O que isso muda nas decisões (análise de 2026-10-01)

1. **Gerar curso não cabe num modelo Flash só:** 20 por dia cada. Mas como a cota é
   separada, dá pra **revezar** 3.8 → 3.7 → 3.6 → 3.5 → 3 Flash (≈100 pedidos/dia de
   modelo forte). Um tópico em modo "pro" gasta ~6–10 pedidos.
2. **Tutor está no lugar certo:** 3.5 Flash Lite (500/dia), com 3.1 Flash Lite (outros
   500/dia) como reserva antes do Groq.
3. **Gemma 4 (14.400/dia)** é o candidato pra tarefas em volume com prompt curto (TPM 16K):
   texto da narração de cada bloco, perguntas, variações de exercício. Precisa de teste de qualidade.
4. **Áudio:** cada TTS dá só 10/dia, mas são 4 modelos separados → ~40 blocos/dia
   revezando. A **API Live é ilimitada** e devolve voz — caminho a testar pra narração em
   volume (e pra prática de conversa do curso de Inglês, que está no backlog).
5. **Pro e imagem pela API: sem acesso no gratuito.** Imagem continua pelo
   `scripts/gerar_imagem_gemini.py` (navegador).
6. **Pesquisa Google (grounding) só funciona nos modelos 2.x/2.5** (1.500/dia): útil pra
   ajudar a montar dossiê de fontes com link, usando o 2.5 Flash/Flash Lite.

Groq (consultado via API no mesmo dia): `openai/gpt-oss-120b`, `openai/gpt-oss-20b`,
`qwen/qwen3.8-27b`, `whisper-large-v3(-turbo)`, `canopylabs/orpheus-v1-english` (voz em inglês).
Limites do Groq não estão aqui — o teto conhecido é ~8.000 tokens/min por pedido no gpt-oss-120b.
