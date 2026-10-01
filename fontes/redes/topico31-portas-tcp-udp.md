# Dossiê — Portas TCP/UDP (554, 1935, 80, 443)

Curso Redes e Câmeras (Course 11) · Módulo 1 · Aula "Portas e Tráfego" (lesson 121) ·
`Topico.id=31` · montado em 2026-10-01 seguindo `docs/processo-topico/FONTES_GUIA.md`.

Costura: vem depois do T30 (máscara e gateway, fecha "endereço IP"). Vem antes do T32
"TCP vs UDP aplicado a vídeo" → aqui TCP/UDP só no nível "dois jeitos de entregar, cada
porta é TCP ou UDP"; confiabilidade, perda de pacote e latência ficam pro T32.

## Fontes

| # | Tipo | Referência | Acesso | O que usei |
|---|---|---|---|---|
| 1 | Primária | RFC 6335 — IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry (2011). https://www.rfc-editor.org/rfc/rfc6335.html | 2026-10-01 | As 3 faixas: System 0–1023, User 1024–49151, Dynamic 49152–65535 (dinâmicas nunca são atribuídas a serviço) |
| 2 | Primária | IANA — Service Name and Transport Protocol Port Number Registry. https://www.iana.org/assignments/service-names-port-numbers | 2026-10-01 | Registro oficial: rtsp 554 tcp/udp; 1935 registrada pra Macromedia (hoje Adobe) |
| 3 | Primária | RFC 9110 — HTTP Semantics (2022), §4.2.1 e §4.2.2. https://www.rfc-editor.org/rfc/rfc9110.html | 2026-10-01 | Citação: "TCP port 80 … is the default" (http) e "TCP port 443 (the reserved port for HTTP over TLS) is the default" (https) |
| 4 | Primária | RFC 2326 — Real Time Streaming Protocol (1998). https://www.rfc-editor.org/rfc/rfc2326.html | 2026-10-01 | "If the port is empty or not given, port 554 is assumed"; rtsp exige protocolo confiável (TCP); "The default port for the RTSP server is 554 for both UDP and TCP"; implementações MUST suportar TCP |
| 5 | Primária | RFC 7826 — RTSP 2.0 (2016) | 2026-10-01 | Versão atual do RTSP; controle sobre TCP, mídia negociada à parte (detalhe fica pro T32/Módulo 3) |
| 6 | Especialista / referência | Wikipedia — Real-Time Messaging Protocol; Wowza — RTMP Streaming explained. https://en.wikipedia.org/wiki/Real-Time_Messaging_Protocol · https://www.wowza.com/blog/rtmp | 2026-10-01 | RTMP criado pela Macromedia (Flash), Adobe publicou spec; roda sobre TCP, porta padrão 1935; RTMPS usa 443. YouTube Live/Twitch/Facebook aceitam ingest RTMP |
| 7 | Caso real (fabricante) | Intelbras — Manual do usuário NVRs NVD 1304/1308/1316 (03-20), p. 41 e 65. https://backend.intelbras.com/sites/default/files/2020-08/Manual%20do%20usu%C3%A1rio%20-%20NVRs%20Intelbras%20(NVD%201304,%20NVD%201308,%20NVD%201316)%2003-20.pdf | 2026-10-01 | Tela "Portas": Porta de serviço 37777 (envio de imagens e autenticação), HTTP 80, HTTPS 443 (habilitar), RTSP 554; link RTSP `rtsp://user:senha@ip:porta/cam/realmonitor?channel=N&subtype=0`; RTSP pode ser TCP/UDP/Multicast/Automático na câmera Onvif |
| 8 | Caso que deu errado (pesquisa) | Antonakakis et al., *Understanding the Mirai Botnet*, USENIX Security 2017. https://www.usenix.org/system/files/conference/usenixsecurity17/sec17-antonakakis.pdf | 2026-10-01 | Pico de 600 mil infecções; dispositivos IoT (câmeras, DVRs, roteadores) com senha padrão; varria Telnet nas portas TCP 23 e 2323; ataque a Krebs on Security > 600 Gbps (set/2016); também OVH e Dyn |
| 9 | Primária (SO) | Microsoft Learn — "The default dynamic port range for TCP/IP has changed" · Linux kernel docs `ip_local_port_range`. https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/default-dynamic-port-range-tcpip-chang · https://docs.kernel.org/networking/ip-sysctl.html | 2026-10-01 | Windows usa 49152–65535 como porta de origem; Linux por padrão 32768–60999 |
| 10 | Livro-texto | Kurose & Ross, *Computer Networking: A Top-Down Approach* (cap. 3, camada de transporte) — paráfrase | — | Analogia clássica de multiplexação: IP leva até a casa (host), porta leva até o processo/aplicação certo |
| 12 | Primária | RFC 768 — User Datagram Protocol (1980). https://www.rfc-editor.org/rfc/rfc768.html · RFC 9293 — Transmission Control Protocol (2022) | 2026-10-01 | UDP: "delivery and duplicate protection are not guaranteed"; porta de origem = porta do processo que envia, pra onde vai a resposta. TCP: conexão confiável e ordenada (detalhe fica pro T32) |
| 13 | Primária (ferramenta) | Microsoft Learn — Test-NetConnection. https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection | 2026-10-01 | `-Port` = "the TCP port number on the remote computer"; saída `TcpTestSucceeded : True`. **Não existe parâmetro -Udp** (o Groq inventou) |
| 11 | Pesquisa (risco) | Modat — Internet-Exposed RTSP: A Global Analysis. https://www.modat.io/post/exposed-rtsp (já em `estudo-redes-cameras/FONTES.md`) | 2026-10-01 | Existem streams RTSP expostos na internet sem autenticação — risco real de porta 554 aberta |

Tipos cobertos: primária, livro-texto, especialista, caso real, caso que deu errado,
pesquisa — 6 de 8 (meta ≥5 ✔).

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| Porta é um número de 0 a 65535 que identifica o serviço/aplicação dentro de um dispositivo (o IP acha o aparelho, a porta acha o serviço) | 1, 10 | ok |
| Faixas: 0–1023 sistema (bem conhecidas), 1024–49151 registradas, 49152–65535 dinâmicas | 1 | ok |
| Cada porta existe em TCP e em UDP separadamente (o par protocolo+porta é que identifica) | 1, 2 | ok |
| HTTP = TCP 80 por padrão; HTTPS = TCP 443 por padrão | 3 | ok |
| RTSP = 554 por padrão (TCP obrigatório pro controle; registro também em UDP) | 2, 4, 5 | ok |
| RTMP = TCP 1935 por padrão; usado pra ENVIAR vídeo a plataformas/servidores | 6 | ok (fonte secundária confiável; spec da Adobe é a primária) |
| Quem inicia a conexão usa uma porta de origem temporária (dinâmica), quem recebe usa a porta fixa do serviço | 1, 9 | ok |
| NVR Intelbras: 37777 (serviço), 80, 443, 554 por padrão, todas alteráveis na tela "Portas" | 7 | ok |
| Mirai: 600 mil dispositivos no pico, câmeras/DVRs com senha padrão, portas 23/2323, ataque > 600 Gbps | 8 | ok |

## Casos reais / casos que deram errado

- **Real:** tela de Portas do NVR Intelbras (fonte 7) — o aluno vai ver exatamente esses
  números na tela do equipamento de Piazza Fontana (192.168.1.19).
- **Real (variado):** live de culto/evento enviada ao YouTube por RTMP (porta 1935);
  porteiro abrindo a câmera no navegador (80/443); app/VMS puxando RTSP (554).
- **Deu errado:** Mirai (fonte 8) — portas de administração abertas + senha padrão
  viraram arma. Streams RTSP expostos sem senha (fonte 11).

## Divergências entre fontes

- 1935: IANA registra como serviço da Macromedia (nome "macromedia-fcs"); na prática do
  mercado é "a porta do RTMP". O tópico diz "porta padrão do RTMP" — sem contradição.
- Faixa de porta de origem: IANA recomenda 49152–65535, Linux usa 32768–60999 por padrão.
  O tópico menciona as duas.
- 554 aparece no registro em TCP e UDP; na prática de câmera o controle RTSP é TCP. O
  tópico NÃO afirma que "câmera manda UDP na 554" (erro real do Groq em 2026-09-21).

## O que ficou de fora (e por quê)

- Detalhe de confiabilidade/latência de TCP vs UDP → T32.
- Port forwarding / expor porta na internet → Módulo 2 (T36/T37). Aqui só o alerta.
- Porta UDP 37778 da Intelbras: citada em fórum, não confirmada no manual consultado → fora.
- HTTP/3 sobre UDP 443 (QUIC) → detalhe avançado, fora do nível do tópico.
