# Dossiê — Aula "Endereçamento IP" (T28, T29, T30)

Curso Redes e Câmeras (Course 11) · Módulo 1 · lesson 120. Montado em 2026-10-01 na
**revisão dos tópicos antigos** (escritos em 2026-09-19/21, antes do processo novo).
Formato: `docs/processo-topico/FONTES_GUIA.md`.

- T28 "O que é um endereço IP" · T29 "IP privado vs. IP público" · T30 "Máscara de sub-rede e gateway"

## Fontes

| # | Tipo | Referência | Acesso | O que sustenta |
|---|---|---|---|---|
| 1 | Primária | RFC 791 — Internet Protocol (1981) | 2026-10-01 | IPv4: endereço de 32 bits (4 octetos) |
| 2 | Primária | RFC 8200 — IPv6 (2017) | 2026-10-01 | IPv6: endereço de 128 bits |
| 3 | Primária | RFC 1918 — Address Allocation for Private Internets. https://www.rfc-editor.org/rfc/rfc1918.html | 2026-10-01 | 3 faixas privadas (10/8, 172.16/12, 192.168/16); "private addresses have no global meaning"; provedores "expected to … reject (filter out) routing information about private networks"; pacotes com destino privado "should not be forwarded" entre redes |
| 4 | Primária | RFC 6598 — Shared Address Space (2012). https://www.rfc-editor.org/rfc/rfc6598.html | 2026-10-01 | 100.64.0.0/10 reservado pra ligar o CGN da operadora ao equipamento do cliente (CGNAT) |
| 5 | Primária | RFC 5737 — IPv4 Address Blocks Reserved for Documentation. https://www.rfc-editor.org/rfc/rfc5737.html | 2026-10-01 | 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24 são pra exemplo e "SHOULD NOT appear on the public Internet" → o IP público de exemplo do curso passa a ser **203.0.113.30** (antes 189.45.12.30, que é um endereço real de provedor) |
| 6 | Primária | RFC 2131 — DHCP (1997) | — | DHCP entrega IP automaticamente; "alocação manual" = o servidor sempre entrega o mesmo IP pra aquele equipamento (o que os roteadores chamam de reserva de DHCP) |
| 7 | Primária (registro) | NRO — "Free Pool of IPv4 Address Space Depleted" (3/fev/2011). https://www.nro.net/ipv4-free-pool-depleted/ | 2026-10-01 | A IANA entregou os últimos blocos IPv4 livres em 3/fev/2011 |
| 8 | Dado | IoT Analytics — State of IoT 2025. https://iot-analytics.com/number-connected-iot-devices/ | 2026-10-01 | ~21,1 bilhões de dispositivos IoT conectados em 2025 (só IoT) — mais que os ~4,3 bilhões de endereços IPv4 |
| 9 | Dado | APNIC Blog — "Google hits 50% IPv6" (abr/2026). https://blog.apnic.net/2026/04/28/google-hits-50-ipv6/ · Internet Society Pulse — "18 Years Later, IPv6 Reaches Majority". https://pulse.internetsociety.org/en/blog/2026/04/18-years-later-ipv6-reaches-majority/ | 2026-10-01 | Metade do acesso ao Google já é por IPv6; Brasil na faixa de ~50% |
| 10 | Caso real (fabricante) | Intelbras — Manual NVD 1304/1308/1316 (03-20), p. 26 e 64 | 2026-10-01 | p.26: "Por padrão o NVR obtém IP por DHCP. Caso a rede não disponha de um servidor DHCP, o IP da interface de rede será 192.168.1.108"; "o dispositivo remoto deve estar configurado no mesmo segmento de rede IP do NVR". p.64: tela de rede tem "Versão: … IPv4 ou IPv6" e opção DHCP liga/desliga |
| 11 | Especialista (suporte) | Google Nest Ajuda — "Corrigir a NAT dupla quando dois roteadores são executados ao mesmo tempo" e "Modo bridge". https://support.google.com/googlehome/answer/6277579?hl=pt-BR · Edovia — "Cenário de NAT duplo". https://help.edovia.com/pt-BR/screens-connect-5/troubleshooting/double-nat | 2026-10-01 | Modem/ONT da operadora + roteador próprio = NAT duplo: o roteador recebe IP privado na WAN e o redirecionamento de porta não funciona; modo bridge desliga NAT/DHCP de um deles e resolve |
| 12 | Livro-texto | Kurose & Ross, cap. 4 (camada de rede) — paráfrase | — | Sub-rede, máscara, gateway padrão como saída pra outras redes |

Tipos cobertos: primária, livro-texto, especialista, caso real, dado — 5 de 8 (meta ✔).

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| IPv4 = 4 octetos de 0–255, 32 bits; 2^32 ≈ 4,3 bilhões | 1 | ok |
| IPv4 livre da IANA acabou em 2011; só de IoT já são ~21 bilhões de aparelhos | 7, 8 | ok (substitui "o mundo já tem mais dispositivos" sem fonte) |
| IPv6 = 128 bits; ~50% do acesso ao Google já é por IPv6 | 2, 9 | ok |
| O NVR Intelbras deixa escolher IPv4 ou IPv6, mas o curso usa IPv4 | 10 | ok (substitui "CFTV opera quase todo / só oferece IPv4", que a fonte contradiz) |
| DHCP x IP fixo x reserva de DHCP; NVR vem de fábrica em DHCP (192.168.1.108 sem DHCP) | 6, 10 | ok |
| Faixas privadas e que elas não são roteadas na internet | 3 | ok |
| Pacote pra IP privado não sai pela internet até o roteador do prédio | 3 | **corrige o fluxo do T28 s8** |
| CGNAT = 100.64.0.0–100.127.255.255 | 4 | ok |
| WAN privada (192.168/10/172.16) = NAT duplo com o modem da operadora, resolvível (bridge) | 11 | **novo — corrige o teste de CGNAT do T29** |
| Atrás de CGNAT o redirecionamento de porta não funciona, mas VPN/P2P (Módulo 2) funcionam | 4 + grade do curso (T38–T41) | **corrige "nenhuma configuração resolve acesso remoto"** |
| /24 = 255.255.255.0; hosts .1 a .254; câmeras no mesmo segmento do NVR | 10, 12 | ok |
| Gateway = saída pra outras redes; costuma ser o .1 | 12 | ok ("costuma", não "sempre") |

## O que ficou de fora
- Cálculo binário de sub-rede (/25, /26…) — além do nível do Módulo 1.
- Prática de modo bridge passo a passo — fica pro tópico de NAT (T33).
