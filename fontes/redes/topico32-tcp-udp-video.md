# Dossiê — "TCP vs UDP aplicado a vídeo"

Curso Redes e Câmeras (Course 11) · Módulo 1 · Aula "Portas e Tráfego" (lesson 121) ·
`Topico.id=32` · 2026-10-03 · gerado pelo comando `/criar-topico` (1º teste).

**Costura:** vem depois do T31 (Portas — onde TCP e UDP apareceram só como "dois jeitos de
entregar", com a promessa de aprofundar aqui) e antes do T33 "NAT" (próxima aula). O Módulo 3
detalha RTSP, RTMP, HLS e WebRTC → **aqui só o necessário**: por que a escolha TCP × UDP muda o
vídeo, o que se vê quando dá errado, e onde essa escolha aparece na prática.

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Primária | RFC 9293 — TCP (2022). https://www.rfc-editor.org/rfc/rfc9293.html | "TCP provides a reliable, in-order, byte-stream service to applications" (§2.2); "TCP reliability consists of detecting packet losses (via sequence numbers)… as well as correction via retransmission" (§2.2); "every octet of data sent over a TCP connection has a sequence number" (§3.4); "TCP uses retransmission to ensure delivery of every segment" (§3.8) |
| 2 | Primária | RFC 768 — UDP (1980). https://www.rfc-editor.org/rfc/rfc768.html | "delivery and duplicate protection are not guaranteed" |
| 3 | Primária | RFC 3550 — RTP (2003). https://www.rfc-editor.org/rfc/rfc3550.html | "Applications typically run RTP on top of UDP"; RTP "does not guarantee delivery or prevent out-of-order delivery"; números de sequência permitem ao receptor "reconstruct the sender's packet sequence" e "estimate how many packets are being lost" |
| 4 | Primária | RFC 2326 — RTSP (1998), §10.12 e §12.39. https://www.rfc-editor.org/rfc/rfc2326.html | Dados (RTP) podem ir "interleaved" dentro da conexão TCP do RTSP; "SHOULD only be used if RTSP is carried over TCP"; motivo: "Certain firewall designs and other circumstances may force a server to interleave"; exemplos de Transport: `RTP/AVP;unicast;client_port=…` (UDP) × `RTP/AVP/TCP;interleaved=0-1` (TCP) |
| 5 | Doc oficial (especialista) | MediaMTX — "Decrease packet loss". https://mediamtx.org/docs/features/decrease-packet-loss | "most protocols are built on UDP, which is an 'unreliable transport', specifically picked because it allows dropping late packets in case of network congestion"; trocar pra TCP: "less performant but has a packet retransmission mechanism"; config `rtspTransports: [tcp]` / por câmera `rtspTransport: tcp` |
| 6 | Referência (enciclopédia) | Wikipedia — "Compression artifact". https://en.wikipedia.org/wiki/Compression_artifact | Erros de transmissão no fluxo comprimido podem causar "'break-up' of the picture"; o decodificador continua aplicando atualizações à imagem danificada, "creating a 'ghost image' effect, until receiving the next independently compressed frame" |
| 7 | Caso real (fabricante) | Intelbras — Manual NVD 1304/1308/1316, p. 41 (já no dossiê do T31) | Ao adicionar câmera Onvif: "Escolha o protocolo RTSP entre as opções TCP, UDP, Multicast ou Automático" |
| 8 | Doc de ferramenta | Wowza — "Configure VLC to play RTSP/RTP streams". https://www.wowza.com/docs/how-to-configure-vlc-media-player-for-rtsp-rtp-playback-rtsp-rtp-interleaved-and-tuning | VLC: Ferramentas › Preferências › Entrada/Codecs › Rede › "Live555 stream transport" = "RTP over RTSP (TCP)"; "may work better when streaming through a firewall or router that doesn't have UDP streaming available" |
| 9 | Caso real (relato de problema) | MediaMTX — discussão #1386 "RTP Packet Lost". https://github.com/bluenviron/mediamtx/discussions/1386 | Usuário com transmissão RTSP sobre UDP vendo "RTP packet lost" no log; resposta do mantenedor: ver em qual sessão a perda acontece e reduzir bitrate ou usar as técnicas da doc (fonte 5) |
| 10 | Livro-texto | Kurose & Ross, cap. 2–3 — paráfrase | Aplicações de tempo real toleram alguma perda, mas são sensíveis a atraso — por isso costumam usar UDP |

Tipos cobertos: primária, doc oficial/especialista, referência, caso real, caso que deu errado
(perda de pacote → imagem quebrada / fantasma), livro-texto — 6 de 8 ✔.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| TCP entrega tudo, em ordem, numerando os dados e retransmitindo o que se perde | 1 | ok |
| UDP não garante entrega | 2 | ok |
| Consequência: no TCP, como a entrega é em ordem, o que vem depois de um pedaço perdido espera a retransmissão → atraso/"travada" | 1 (dedução direta de "in-order" + "retransmission"), 5 ("less performant") | ok — apresentar como consequência, não como citação |
| Vídeo ao vivo prefere UDP porque pode descartar pacote atrasado em congestionamento | 5, 10 | ok |
| Pacote de vídeo perdido aparece como imagem "quebrada" e "fantasma" até o próximo quadro completo | 6 | ok |
| RTP normalmente roda sobre UDP; numera os pacotes; não garante entrega | 3 | ok |
| No RTSP, o vídeo pode ir em UDP separado ou "embutido" na conexão TCP do RTSP (interleaved), útil quando firewall bloqueia | 4, 8 | ok |
| NVR Intelbras: escolher TCP, UDP, Multicast ou Automático | 7 | ok |
| VLC "RTP over RTSP (TCP)"; MediaMTX `rtspTransport: tcp` | 8, 5 | ok |
| Trocar pra TCP é o remédio clássico quando há perda (mais confiável, mais lento) | 5 | ok |

## Divergências / cuidados
- A Wowza também usa a porta 1935 pro RTSP nos servidores dela — **não** citar porta pela fonte 8;
  a porta padrão do RTSP continua 554 (RFC 2326, T31).
- Multicast: só citar que existe na tela do NVR; explicação fica pro Módulo 3.
- "Head-of-line blocking" (nome técnico): não achei fonte primária legível → explicar o efeito
  sem usar o termo.

## O que ficou de fora
- Funcionamento interno de RTSP/RTP/RTCP, HLS, WebRTC → Módulo 3.
- Handshake TCP passo a passo, controle de congestionamento → além do nível.
- NAT e por que ele dificulta UDP → T33 (só a ponte).
