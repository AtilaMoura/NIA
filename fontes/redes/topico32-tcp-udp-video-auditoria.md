# Auditoria — T32 "TCP vs UDP aplicado a vídeo"

Conteúdo final: `backend/_criar_topico32_redes.py` → `_topico32_redes_final.json` (14 slides,
7 imagens, 3 fluxos, 4 checkpoints). Dossiê: `topico32-tcp-udp-video.md`. 2026-10-03.

## 1. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | TCP: serviço "confiável e em ordem" | 1 (RFC 9293 §2.2) | ✔ |
| s1 | UDP: entrega "não é garantida" | 2 (RFC 768) | ✔ |
| s2 | Todo byte da conexão TCP é numerado | 1 (§3.4 "every octet… has a sequence number") | ✔ |
| s2 | Quem recebe confirma o que chegou | 1 (§3.1 campo Acknowledgment Number — lido na RFC) | ✔ |
| s2 | "usa retransmissão pra garantir a entrega de cada segmento" | 1 (§3.8) | ✔ |
| s2 | Página do NVR (80/443) e controle RTSP (554) em TCP | T31 (já auditado) + RFC 2326 (554 padrão) | ✔ |
| s4 | No TCP, o que vem depois de um pedaço perdido espera o reenvio → atraso | 1 ("in-order" + "retransmission"), 5 ("less performant") — apresentado como consequência, não citação | ✔ |
| s4 | Citação MediaMTX "a maioria dos protocolos é construída sobre UDP…" (tradução livre) | 5 | ✔ |
| s4 | Analogia telefone × documento | didática, sem fato | ✔ |
| s5 | Vídeo comprimido: quadro completo de tempos em tempos + mudanças no meio | 6 ("next independently compressed frame", atualizações) | ✔ |
| s5 | "quebrar" + "imagem fantasma" até o próximo quadro completo | 6 | ✔ |
| s5 | Sintoma prático: borrões que se arrastam ↔ perda; imagem inteira com atraso ↔ reenvio | 6 + 1/5 (dedução direta, marcada "típico"/"costuma") | ✔ |
| s6 | RTP "normalmente roda por cima do UDP"; numeração reconstrói ordem e estima perda; "não garante a entrega" | 3 (RFC 3550) | ✔ |
| s6 | Media server escreve "RTP packet lost" | 9 (discussão MediaMTX #1386) | ✔ |
| s8 | RTSP: vídeo em UDP separado ou "interleaved" na conexão TCP | 4 (RFC 2326 §10.12, §12.39) | ✔ |
| s8 | Motivo: "certos firewalls e outras circunstâncias"; só com RTSP em TCP | 4 | ✔ |
| s8 | NAT como motivo comum pro UDP não passar | só ponte pro T33 (sem detalhe técnico) | ✔ |
| s9 | NVR Intelbras: "TCP, UDP, Multicast ou Automático" | 7 (manual p.41) | ✔ |
| s9 | VLC: Ferramentas › Preferências › Entrada / Codecs › Rede › "RTP over RTSP (TCP)" | 8 (Wowza) | ✔ |
| s9 | MediaMTX `rtspTransport: tcp` / `rtspTransports: [tcp]`; TCP "menos performático, mas com retransmissão" | 5 | ✔ |
| s9 | MediaMTX = media server do Módulo 5 | memória do curso (estrutura dos módulos) | ✔ |
| s9 | Rede saturada → reduzir a taxa de bits | 9 (mantenedor: reduzir bitrate) | ✔ (corrigido, ver §2) |
| s11 | Resumo = só o que foi dito nos slides | — | ✔ |

## 2. Erros pegos nesta auditoria (corrigidos antes de publicar)

- s9 e ck4_3 diziam "reduzir a carga (resolução, taxa de bits)": **resolução não está na fonte**
  (o mantenedor fala só em bitrate) → ficou só "taxa de bits (bitrate)".
- ck3_1 tinha o distrator "Trocar a porta do RTSP pra 1935": contraria o cuidado do dossiê (porta
  vinda da Wowza; 1935 é RTMP no T31) e poderia confundir → trocado por "Trocar o IP da câmera".

## 3. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-3.5-flash`, cadeia "conteudo") e Groq (`gpt-oss-120b`, "segunda_opiniao" —
o qwen caiu pro gpt-oss). Arquivos `backend/_conteudo_{conteudo,segunda_opiniao}_topico32.json`.
Mesmo com "se não está no dossiê, NÃO escreva", os dois inventaram:

| Rascunho | O que inventou | Por que ficou de fora |
|---|---|---|
| ambos | "porta UDP 5004" como porta do vídeo RTP (Groq: "5004 vídeo / 5005 áudio") | não está no dossiê; no RTSP as portas UDP são negociadas na hora (RFC 2326 `client_port=`), não fixas |
| Gemini | "6970 pro RTP e 6971 pro RTCP" | número sem fonte |
| Groq | câmera "IPC-HFW4431R" na Piazza Fontana com IP 192.168.1.45 | modelo e IP inventados — o único equipamento real é o NVR 192.168.1.19 |
| Gemini | IP de câmera 192.168.1.50 | inventado |
| Gemini | "TCP garante a entrega de 100% dos pacotes" | exagero; a RFC fala em retransmitir, não em 100% (conexão pode cair) |
| ambos | handshake / "3-way handshake" | fora do nível (dossiê: "o que ficou de fora") |
| Groq | "jitter", relógio de "90 kHz" | fora do dossiê e do nível (Módulo 3) |
| Groq | bloco `diagrama` | proibido (usar `fluxo`) |
| Gemini | tf "RTP garante 100% com retransmissão" (como falsa) | ok como ideia, mas já coberto por ck2_2 |

Aproveitado: só a estrutura (ordem TCP/UDP → dilema → defeito → RTP → RTSP → prática), que bate
com o roteiro já planejado. Nenhum texto dos rascunhos foi copiado.

## 4. Pedagogia
- Abre retomando a promessa do T31 ("dois jeitos de entregar"); fecha com ponte pro T33 (NAT).
- Sintoma → causa → ajuste: o aluno sai sabendo reconhecer "borrão que arrasta" × "atraso".
- Checkpoints: tf, mc, associar, mc com cenário, classify + 2 abertas (ck4_2, ck4_3) ✔.
- Reflexão "💭 Pra pensar" + Resumo ✔. Exemplos variados: portaria, comércio, condomínio implícito (NVR).
- Nenhum IP no tópico (não precisou) — regra RFC 5737 não se aplica.

## 5. Continuidade
- Não repete o T31 (portas e faixas) nem invade o T33 (NAT só como ponte) e o Módulo 3
  (RTSP/RTP só no nível "o que muda pro vídeo"; RTCP, HLS, WebRTC fora).
- Termo "head-of-line blocking" não usado (sem fonte primária legível) ✔. Multicast só citado ✔.

## 6. Estrutura
- `validar_topico()` vazio; 0 `None` no render (alto-contraste); ids de pergunta e item únicos;
  `fluxo` (nenhum `diagrama`); capa com `imagem_capa`.

**Pendências: 0.**
