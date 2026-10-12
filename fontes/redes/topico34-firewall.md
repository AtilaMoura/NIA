# Dossiê — "Firewall — bloqueio de entrada vs. saída"

Curso Redes e Câmeras (Course 11) · Módulo 1 "Fundamentos de Rede" · Aula "NAT, Firewall e DNS"
(lesson 122) · `Topico.id=34` · 2026-10-11 · gerado pelo `/criar-topico`.

**Costura:** T33 (NAT) terminou com "NAT não é firewall: o bloqueio é efeito colateral da tabela
(RFC 4864). Quem decide de verdade o que entra e o que sai é o firewall — o próximo tópico." T31
ensinou portas (80, 443, 554, 37777) e citou o Mirai; T32 TCP × UDP. Depois vêm T35 "DNS e DDNS" e,
no Módulo 2, T36 "Como funciona o redirecionamento de porta" e T37 "Riscos de expor porta na
internet". → **Aqui: o que é firewall, a diferença entre ENTRADA e SAÍDA (quem começou a conversa),
o padrão "sai tudo, entra só resposta", a tabela de estados, negar por padrão + exceções, onde há
firewall na rede (roteador, computador, NVR) e por que a saída também importa.** **Não** ensinar a
abrir porta/redirecionar (T36), nem UPnP (Módulo 2), nem DNS (T35); o Mirai entra só como caso de
"entrada aberta", sem esgotar os riscos de expor porta (T37).

## Fontes

Todas lidas na fonte em 2026-10-11 (texto baixado e conferido, não de memória).

| # | Tipo | Referência | O que sustenta |
|---|---|---|---|
| 1 | Primária / oficial (guia de governo) | NIST SP 800-41 Rev. 1 — *Guidelines on Firewalls and Firewall Policy* (Scarfone & Hoffman, 2009). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf | **Definição** (glossário, p. A-1): "Firewall: A device or program that controls the flow of network traffic between networks or hosts that employ differing security postures." · **Política** (ES-1): "A firewall policy defines how an organization's firewalls should handle inbound and outbound network traffic…" · **Negar por padrão** (§4, p. 4-1): "Generally, firewalls should block all inbound and outbound traffic that has not been expressly permitted by the firewall policy… This practice, known as deny by default, decreases the risk of attack… deny by default is a more secure approach than permitting all traffic that is not explicitly forbidden." · **Entrada × saída na prática** (§4.1.3/4.1.4, p. 4-4): "deny by default policies should be used for incoming TCP and UDP traffic. Less stringent policies are generally used for outgoing TCP and UDP traffic because most organizations permit their users to access a wide range of external applications" · **Ingress/egress** (§2.1.1): "Filtering inbound traffic is known as ingress filtering. Outgoing traffic can also be filtered, a process referred to as egress filtering… blocking the use of external file transfer protocol (FTP) servers or preventing denial of service (DoS) attacks from being launched from within the organization against outside entities." · **Inspeção com estado** (§2.1.2): "stateful inspection keeps track of each connection in a state table… they typically include source IP address, destination IP address, port numbers, and connection state information"; UDP: "a DNS response from an external source would be permitted to pass only if the firewall had previously seen a corresponding DNS query from an internal source… the entry is removed from the state table after a preconfigured timeout value is reached"; "When a firewall provides NAT services, it often includes NAT information in its state table." · **Firewall pessoal** (§2.2.1): "it can restrict inbound communications and can often limit outbound communications as well. This not only allows personal firewalls to protect PCs from incoming attacks, but also limits the spread of malware from infected PCs" · **Roteador de casa** (§2.2.2): "a small, inexpensive device called a firewall appliance or firewall router to protect the computers on their home networks… Even if each computer on a home network is using a personal firewall, a firewall appliance is still a valuable added layer of security." · **Limite** (§2.3): "Firewalls can only work effectively on traffic that they can inspect." |
| 2 | Primária | RFC 6092 — *Recommended Simple Security Capabilities in CPE for Providing Residential IPv6 Internet Service* (Woodyatt, jan/2011). https://www.rfc-editor.org/rfc/rfc6092.txt | **Definição de direção** (§3): "Flows are said to be 'outbound' if the originator of the initial packet in any given transport association is an interior node… Flows are said to be 'inbound' if the originator of the initial packet is an exterior node"; pacotes: "'outbound' if they originate at nodes located in the interior network for exterior destinations, and 'inbound' if they arrive from exterior sources with interior destinations." · **Princípio do roteador residencial** (§2.3): "transport layer traffic is not forwarded into the interior network of a residential IPv6 gateway unless it has been solicited explicitly by interior transport endpoints, e.g., by matching the reverse path for previously forwarded outbound traffic, or by matching configured exceptions set by the network administrator." · **Objetivos** (§2): "Provide a barrier against untrusted external influences on the interior network by requiring filter state to be activated by traffic originating at interior network nodes"; "Allow manually configured exceptions to the stateful filtering rules". · **Elo com o NAT** (§2): "The stateful packet filtering behavior of NAT set user expectations that persist today with residential IPv6 service." (RFC é sobre IPv6; uso só as definições e o princípio, que ela mesma diz espelhar o que o usuário já esperava do NAT em IPv4.) |
| 3 | Primária | RFC 2979 — *Behavior of and Requirements for Internet Firewalls* (Freed, out/2000), §1. https://www.rfc-editor.org/rfc/rfc2979.txt · RFC 4949 — *Internet Security Glossary v2* (2007), verbete "firewall". https://www.rfc-editor.org/rfc/rfc4949.txt | RFC 2979: "A 'firewall' is an agent which screens network traffic in some way, blocking traffic it believes to be inappropriate, dangerous, or both." · RFC 4949: "An internetwork gateway that restricts data communication traffic to and from one of the connected networks (the one said to be 'inside' the firewall) and thus protects that network's system resources against threats from the other network (the one that is said to be 'outside' the firewall)." |
| 4 | Doc oficial de fabricante (SO) | Microsoft Learn — *Windows Firewall rules* (ms.date 2025-06-06). https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/rules | "there's a default *block* action in Windows Firewall, you must create inbound exception rules to allow the traffic"; "Maintain the default Windows Firewall settings whenever possible… One key example is the default *block behavior* for inbound connections."; precedência: "1. Explicitly defined allow rules take precedence over the default block setting. 2. Explicit block rules take precedence over any conflicting allow rules."; saída: "It's recommended to *allow outbound* by default for most deployments… Changing the outbound rules to *blocked* can be considered for certain highly secure environments. However, the inbound rule configuration should never be changed in a way that allows all traffic by default."; "A general security recommended practice when creating inbound rules is to be as specific as possible." |
| 5 | Especialista | David Anderson (Tailscale), *How NAT traversal works*, 21/08/2020, seção sobre firewalls com estado. https://tailscale.com/blog/how-nat-traversal-works | "the most common configuration allows all 'outbound' connections and blocks all 'inbound' connections. There might be a few handpicked exceptions, such as allowing inbound SSH."; "Stateful firewalls remember what packets they've seen in the past"; "the firewall allows an inbound UDP packet if it previously saw a matching outbound packet."; exemplos citados: Windows Defender firewall, ufw do Ubuntu. |
| 6 | Livro-texto (slides baseados nos dos autores) | Kurose & Ross, cap. 8, "Operational security: firewalls and IDS" — slides de curso baseados nos dos autores (York University EECS 3214, Chapter 8c: https://www.eecs.yorku.ca/course_archive/2013-14/W/3214/LEC/Chapter_8c.pdf). **Só paráfrase.** | O firewall isola a rede interna da internet, deixando alguns pacotes passar e bloqueando outros; três tipos (filtro sem estado, filtro com estado, gateway de aplicação); filtro sem estado decide pacote a pacote por IP de origem/destino, portas TCP/UDP, tipo ICMP e bits SYN/ACK; filtro com estado acompanha cada conexão TCP e deixa de aceitar pacotes de conexão inativa (timeout); limitação: equilíbrio entre comunicação com o mundo de fora e nível de segurança — "many highly protected sites still suffer from attacks". |
| 7 | Caso real (fabricante) | Intelbras — Manual do usuário NVRs NVD 1304/1308/1316 (03-20), p. 62 (menu Rede) e **p. 67-68 (Filtro IP)**. Link no dossiê do T31. | "Clique no item Filtro IP para acessar a interface de configuração dos IPs que terão acesso ao NVR. Caso habilite essa opção, somente os IPs contidos na lista de IPs permitidos terão acesso ao NVR." · Exemplo do manual: "em uma empresa há várias câmeras… apenas o computador do chefe de segurança e o do presidente da empresa devem ter acesso ao NVR. Habilite a opção Filtro IP e inclua os IPs… Somente os dois terão acesso ao NVR." · Campos: Habilitar (regra "Permitido ou Bloqueado"), Adicionar IP, Seção IP (faixa Início–Fim), MAC, Editar, Apagar. · Obs.: "quando essa função for habilitada, somente os IPs permitidos da lista poderão ser conectados ao NVR." |
| 8 | Caso que deu errado (pesquisa + dado) | Antonakakis et al., *Understanding the Mirai Botnet*, USENIX Security 2017. https://www.usenix.org/system/files/conference/usenixsecurity17/sec17-antonakakis.pdf | "peak of 600k infections"; "Mirai primarily targeted IP cameras, DVRs, and consumer routers"; propagação: "sent TCP SYN probes to pseudorandom IPv4 addresses… on Telnet TCP ports 23 and 2323… attempted to establish a Telnet connection using 10 username and password pairs selected randomly from a pre-configured list of 62 credentials"; ao conseguir, "sent the victim IP and associated credentials to a hard-coded report server"; ataque a Krebs on Security "exceeded 600 Gbps" (a partir de set/2016; também OVH e Dyn). |
| 9 | Caso que deu errado (aviso de governo) | CISA (US-CERT) — Alert TA16-288A, *Heightened DDoS Threat Posed by Mirai and Other Botnets* (14/10/2016, rev. 17/10/2017). https://www.cisa.gov/news-events/alerts/2016/10/14/heightened-ddos-threat-posed-mirai-and-other-botnets | Aparelhos atingidos: "primarily home routers, network-enabled cameras, and digital video recorders"; "The Mirai bot uses a short list of 62 common default usernames and passwords to scan for vulnerable devices"; prevenção: "Ensure all default passwords are changed to strong passwords", atualizar; monitorar "port 2323/TCP and port 23/TCP"; "Look for suspicious traffic on port 48101" (aparelho infectado usa essa porta para espalhar/enviar resultados). O aviso **não** cita firewall — as recomendações principais são senha e atualização. |

Tipos: primária/oficial (NIST, 3 RFCs), doc de fabricante de SO, especialista, livro-texto, caso real,
caso que deu errado (pesquisa + aviso de governo), dado (600 mil infecções; > 600 Gbps) — **7 tipos** ✔.

Tentada e não usada: Cloudflare Learning "What is a Firewall" (em `FONTES.md`) respondeu 403 — nada dela entrou.

## Afirmações centrais

| Afirmação | Fontes | Status |
|---|---|---|
| Firewall = aparelho ou programa que controla o fluxo de tráfego entre redes/hosts com níveis de segurança diferentes; filtra e bloqueia o que julga impróprio | 1 (glossário), 3 | ok |
| Existe um "dentro" (rede protegida) e um "fora" | 3 (RFC 4949), 2 (interior/exterior) | ok |
| Direção = quem mandou o primeiro pacote: fluxo de SAÍDA começa num aparelho de dentro; de ENTRADA começa num de fora | 2 (§3) | ok |
| Filtrar a entrada = ingress filtering; filtrar a saída = egress filtering | 1 (§2.1.1) | ok — termos em inglês só citados |
| Configuração mais comum: libera toda conexão de saída e bloqueia toda conexão de entrada, com poucas exceções escolhidas | 5, 4 (Windows: entrada bloqueada por padrão; saída liberada recomendada), 1 (§4.1: negar por padrão na entrada, política menos rígida na saída) | ok |
| Roteador residencial: tráfego não é encaminhado pra dentro a não ser que tenha sido solicitado de dentro (caminho de volta de tráfego de saída) ou case com exceção configurada | 2 (§2.3) | ok — RFC de IPv6; dito como "princípio recomendado" |
| Firewall com estado guarda uma tabela de estados (IP origem, IP destino, portas, estado da conexão); a resposta só passa se casa com uma linha | 1 (§2.1.2), 5, 6 | ok |
| UDP: resposta de fora só passa se o firewall viu antes o pedido correspondente saindo; a linha some depois de um tempo configurado | 1 (§2.1.2), 5 | ok — liga com o relógio do NAT (T33) |
| Quando o firewall também faz NAT, costuma guardar a informação do NAT na mesma tabela de estados | 1 (§2.1.2) | ok — explica por que NAT "parece" firewall (T33) |
| Filtro sem estado decide pacote a pacote (IP, porta, bits TCP); com estado acompanha a conexão | 6, 1 | ok — paráfrase |
| "Negar por padrão": bloquear tudo que não foi expressamente permitido é mais seguro do que permitir tudo que não foi proibido | 1 (§4) | ok |
| Exceção de entrada deve ser a mais específica possível; nunca mudar a entrada pra "permitir tudo" | 4 | ok |
| No Windows: regra de permissão explícita vence o bloqueio padrão; regra de bloqueio explícita vence permissão conflitante | 4 | ok |
| Onde há firewall: roteador (firewall appliance/firewall router), computador (firewall pessoal), e são camadas que se somam | 1 (§2.2) | ok |
| NVR Intelbras tem "Filtro IP": habilitado, só os IPs da lista de permitidos acessam o NVR (aceita IP, faixa ou MAC) | 7 (p. 67-68) | ok |
| Mirai: varria a internet nas portas Telnet TCP 23 e 2323, tentava login com lista de 62 usuários/senhas padrão; pico de 600 mil infecções; alvos principais câmeras IP, DVRs e roteadores; ataque > 600 Gbps | 8, 9 | ok |
| Recomendação da CISA contra o Mirai: trocar senha padrão e atualizar | 9 | ok — **não** dizer "a CISA mandou usar firewall" |
| Saída também importa: filtrar a saída limita a propagação de malware de máquina infectada e impede ataque lançado de dentro; aparelho infectado pelo Mirai falava pra fora (servidor de relatório; tráfego suspeito na porta 48101) | 1 (§2.1.1, §2.2.1), 8, 9 | ok |
| Bloquear saída por padrão só em ambiente de alta segurança; o usual é liberar | 4, 1 (§4.1) | ok |
| Firewall não resolve tudo: só funciona no tráfego que consegue inspecionar; lugares muito protegidos ainda sofrem ataques | 1 (§2.3), 6 | ok |

## Casos reais / casos que deram errado
- **Real:** tela Filtro IP do NVR Intelbras (fonte 7) — o exemplo do próprio manual (chefe de segurança + presidente).
- **Real:** Firewall do Windows no computador que abre o NVR (fonte 4).
- **Deu errado:** Mirai, 2016 (fontes 8 e 9) — câmeras e DVRs alcançáveis da internet no Telnet, com senha padrão.

## Exemplos (regra do curso)
- NVR real: 192.168.1.19 (Piazza Fontana). IP público de exemplo: **203.0.113.x** (RFC 5737). IPs
  privados de exemplo pro Filtro IP: 192.168.1.50 e 192.168.1.51 (inventados, faixa privada, marcados "exemplo").
- Variados: residência, condomínio/portaria, comércio, empresa (o exemplo do manual).
- O IP 130.207.x dos slides de Kurose e os 7.7.7.7/2.2.2.2 do Tailscale **não** usar (IPs reais).

## Divergências entre fontes
- **Saída:** NIST (texto geral, §4) diz bloquear por padrão entrada E saída; o próprio NIST (§4.1) e a
  Microsoft reconhecem que na prática a saída fica mais solta ("less stringent", "allow outbound by
  default"), e bloquear saída é pra "highly secure environments". → o tópico **mostra as duas coisas**:
  o ideal (só o necessário) e o usual (saída liberada), sem esconder a diferença.
- RFC 6092 é de IPv6 e permite até "modo transparente" como padrão (REC-49) → não afirmar "todo
  roteador bloqueia entrada"; dizer "a configuração mais comum" (fonte 5) e "o princípio recomendado".

## O que ficou de fora (e por quê)
- Como abrir porta / redirecionamento / DMZ do roteador → T36 (Módulo 2).
- UPnP (NIST §2.2.2 diz que é risco e costuma vir desligado; CISA manda desativar) → Módulo 2 / T37.
- Gateway de aplicação/proxy, IDS/IPS, NGFW, WAF → fora do nível.
- Comandos (`netsh`, `ufw`, iptables) → não há necessidade; nenhum comando no tópico.
- Detalhe dos bits SYN/ACK e estados TCP → fora do nível (só "acompanha a conexão").
- "Filtro de IP por tempo" do NVR (marcado com ¹ no manual, só em alguns modelos) → fora.
- Afirmar que o Intelbras Cloud funciona "porque a conexão sai de dentro": sem fonte do fabricante → não entra.
