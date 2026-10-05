# Dossiê — "NAT (Network Address Translation)"

Curso Redes e Câmeras (Course 11) · Módulo 1 "Fundamentos de Rede" · Aula "NAT, Firewall e DNS"
(lesson 122) · `Topico.id=33` · 2026-10-05 · gerado pelo `/criar-topico`.

**Costura:** T29 já ensinou IP privado × público (RFC 1918), a armadilha do CGNAT (RFC 6598) e o
teste "WAN do roteador × site de 'meu IP'"; T31 portas; T32 terminou com "um dos motivos mais
comuns pro UDP não passar é o NAT". O dossiê do T28-30 deixou pra cá: "prática de modo bridge".
Depois vêm T34 Firewall, T35 DNS/DDNS e, no Módulo 2, T36 "Como funciona o redirecionamento de
porta". → **Aqui: o MECANISMO do NAT** (tabela de tradução, por que a saída funciona e a entrada
não), NAT duplo + modo bridge, NAT ≠ firewall (só a ponte pro T34). **Não** ensinar a configurar
redirecionamento de porta (T36) nem repetir o teste de CGNAT do T29 (só retomar).

## Fontes

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Primária | RFC 3022 — Traditional IP NAT (2001). https://www.rfc-editor.org/rfc/rfc3022.txt | NAPT: "many network addresses and their TCP/UDP ports are translated into a single network address and its TCP/UDP ports"; "nodes on the private network could be allowed simultaneous access to the external network, using the single registered IP address with the aid of NAPT"; "In a traditional NAT, sessions are uni-directional, outbound from the private network. Sessions in the opposite direction may be allowed on an exceptional basis using static address maps for pre-selected hosts."; a ligação (binding) "is determined when the first outgoing session is initiated"; modelo atende "Small Office Home Office (SOHO)" com um único IP do provedor |
| 2 | Primária | RFC 1918 (1996), §3 | Faixas privadas 10/8, 172.16/12, 192.168/16 (já no T29 — só retomar) |
| 3 | Primária | RFC 4787 — NAT Behavioral Requirements for Unicast UDP (2007). https://www.rfc-editor.org/rfc/rfc4787.txt | "REQ-5: A NAT UDP mapping timer MUST NOT expire in less than two minutes" (com exceção pra portas 0-1023); o timer pode ser configurável → mapeamento UDP parado some depois de um tempo |
| 4 | Primária | RFC 4864 — Local Network Protection for IPv6 (2007), §2. https://www.rfc-editor.org/rfc/rfc4864.txt | "The perceived security of NAT comes from the lack of pre-established or permanent mapping state."; "This role, often marketed as a firewall, is really an arbitrary artifact, while a real firewall often offers explicit and more comprehensive management controls."; "In situations where two or more devices need to host the same application or otherwise use the same public port, this complexity shifts from difficult to impossible." |
| 5 | Livro-texto (slides dos autores) | Kurose & Ross, cap. 4, NAT — slides baseados nos dos autores (Chalmers EDA344: https://www.cse.chalmers.se/edu/year/2017/course/EDA344/SLIDESNOTES16/6.lectureChapter4a.pdf) + exercício interativo oficial https://www-net.cs.umass.edu/kurose_ross/interactive/nat.php | O roteador NAT, na saída, troca (IP de origem, porta) por (IP do NAT, porta nova); guarda o par na **tabela de tradução**; na entrada, troca de volta o destino usando a tabela |
| 6 | Especialista (suporte de fabricante) | Google Nest Ajuda — NAT dupla. https://support.google.com/googlenest/answer/6277579?hl=pt-BR (+ Edovia, já no dossiê T28-30) | "Uma NAT dupla acontece quando outro roteador… está conectado ao modem ou gateway do ISP. Isso significa que os dados passam por um processo NAT duas vezes"; problemas com "encaminhamento de portas e UPnP"; correção recomendada: modo bridge no equipamento do provedor (ou ligar o modem direto); modo bridge desativa DHCP e roteamento, deixando só um roteador fazer NAT |
| 7 | Caso real (fabricante) | Intelbras — Manual NVD 1304/1308/1316 (03-20), p. 62-63 | Menu Rede do NVR: TCP/IP, Portas, DDNS, Filtro IP, … Intelbras Cloud (acesso pelo app iSIC via nº de série/QR) — opções que o Módulo 2 vai explicar |
| 8 | Caso que deu errado (suporte) | Google Nest (fonte 6) + RFC 4864 (fonte 4) | Redirecionamento de porta que "não funciona" por NAT duplo; dois aparelhos que precisam da mesma porta pública: "de difícil a impossível" |

Tipos: primária (4 RFCs), livro-texto, especialista/fabricante, caso real, caso que deu errado — **5+ tipos** ✔.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| NAT existe pra ligar uma rede com endereços privados à internet com endereços públicos | 1 (abstract) | ok |
| NAPT: vários dispositivos saem pela internet usando UM IP público, diferenciados pela porta | 1, 5 | ok |
| Tabela de tradução: na saída troca (IP privado, porta) por (IP público, porta nova) e guarda; na resposta, desfaz | 1 (binding), 5 | ok |
| A ligação é criada quando o dispositivo de dentro inicia a conexão; no NAT tradicional, as sessões são de dentro pra fora | 1 | ok |
| Conexão que chega de fora sem ninguém ter pedido não acha entrada na tabela → não chega a nenhum aparelho, a não ser que exista um mapeamento fixo ("static address maps") | 1 | ok — o como configurar é T36 |
| Mapeamento UDP parado expira (no mínimo 2 minutos, pela RFC 4787) | 3 | ok — liga com o T32 (vídeo UDP) |
| NAT não é firewall: a "segurança" é efeito colateral; firewall de verdade tem controle explícito | 4 | ok — só ponte pro T34 |
| Dois aparelhos que precisam da mesma porta pública: de difícil a impossível | 4 | ok — ex.: dois NVRs querendo 554 de fora |
| NAT duplo (modem/ONT da operadora + roteador próprio): NAT duas vezes; atrapalha encaminhamento de porta e UPnP; modo bridge no equipamento da operadora resolve | 6 | ok |
| CGNAT = tradução na operadora (T29) — retomar só | T29 | ok |
| O NVR Intelbras tem no menu Rede: Portas, DDNS, Intelbras Cloud | 7 | ok — sem afirmar "por causa do NAT" |

## Exemplos (regra do curso)
- Real: NVR Intelbras 192.168.1.19 (Piazza Fontana).
- IP público de exemplo: **203.0.113.10** (RFC 5737). Portas de saída de exemplo (ex.: 50001) marcadas como "exemplo".
- Variados: residência (celulares + TV), condomínio (portaria), comércio.

## Divergências / cuidados
- Não dizer "NAT protege" nem "NAT é um firewall" — RFC 4864.
- Não ensinar redirecionamento de porta nem UPnP (T36 / Módulo 2); só dizer que existem.
- Valor exato do tempo de expiração varia por roteador — só o mínimo da RFC.
- Exemplo de IP da RFC 3022 (138.76.x) **não** usar — IP real; usar a faixa de documentação.

## O que ficou de fora
- Tipos de NAT (cone, simétrico), STUN/TURN → Módulo 2 (P2P).
- IPv6 e o fim do NAT → fora do nível.
- Hairpinning, ALGs (FTP/SIP) → fora do nível.
