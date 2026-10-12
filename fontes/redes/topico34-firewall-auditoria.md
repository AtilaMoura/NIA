# Auditoria — T34 "Firewall — bloqueio de entrada vs. saída"

Conteúdo final: `backend/_criar_topico34_redes.py` → `_topico34_redes_final.json` (16 slides,
8 imagens, 2 fluxos, 5 checkpoints). Dossiê: `topico34-firewall.md`. 2026-10-11.

## 1. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | Retomada do T33: bloqueio do NAT é efeito colateral; quem decide é o firewall | T33 (RFC 4864) | ✔ |
| s1 | Citação RFC 2979 §1: agente que filtra o tráfego, bloqueando o que julga impróprio, perigoso ou ambos (tradução livre) | 3 | ✔ |
| s1 | NIST: aparelho ou programa que controla o fluxo de tráfego entre redes ou computadores com níveis ("posturas") de segurança diferentes | 1 (glossário A-1) | ✔ |
| s1 | Analogia do porteiro com caderno de regras | didática, coerente com 1 e 3 | ✔ |
| s2 | Dois lados: dentro (rede protegida) e fora (a outra rede) | 3 (RFC 4949), 2 (interior/exterior) | ✔ |
| s2 | Saída = quem mandou o primeiro pacote está dentro; entrada = está fora; é a definição da RFC 6092 | 2 (§3) | ✔ |
| s2 | RFC 6092 "recomenda como o roteador de uma casa deve filtrar" | 2 (título/§2: residential gateways) | ✔ — não digo "IPv4"; ver nota no §2 |
| s2 | A resposta de um site pertence à conversa de saída | 2 (§3, definição por fluxo) | ✔ |
| s2 | Telas em inglês: inbound / outbound | 1, 2, 4 (termos das fontes) | ✔ |
| s4 | Configuração mais comum: libera toda saída, bloqueia toda entrada, poucas exceções — paráfrase atribuída a David Anderson (Tailscale) | 5 | ✔ |
| s4 | Citação RFC 6092 §2.3 (tradução livre, resumida — marcada como resumida: tirei "transport layer", "residential IPv6 gateway" e "interior transport endpoints") | 2 | ✔ |
| s4 | Windows: bloqueio por padrão na entrada, exceção por regra; saída liberada por padrão recomendada na maioria dos casos | 4 | ✔ |
| s5 | Inspeção com estado: acompanha cada conexão numa tabela de estados | 1 (§2.1.2) | ✔ |
| s5 | Fluxo notebook → site (linha anotada na saída, resposta conferida, pacote não solicitado barrado) | 1 (§2.1.2), 5 | ✔ — IPs/porta marcados "exemplos" |
| s5 | Linha: IP de origem, IP de destino, portas, estado; detalhes variam por produto | 1 (§2.1.2) | ✔ |
| s5 | UDP sem abertura/encerramento formal; resposta só entra se o pedido saiu antes; linha apagada após tempo configurado | 1 (§2.1.2), 5 | ✔ |
| s5 | Firewall que faz NAT costuma guardar a informação do NAT na mesma tabela | 1 (§2.1.2) | ✔ |
| s5 | Kurose & Ross: filtro sem estado (pacote a pacote) × com estado (acompanha a conexão; para de aceitar conexão parada) — paráfrase | 6 | ✔ |
| s7 | Citação NIST §4 "negar por padrão" (tradução livre, com […]) | 1 | ✔ |
| s7 | Microsoft: regra de entrada a mais específica possível; nunca mudar a entrada pra permitir tudo | 4 | ✔ |
| s7 | Windows: permissão explícita vence o bloqueio padrão; bloqueio explícito vence permissão conflitante | 4 | ✔ |
| s7 | Liberar o NVR pra fora = exceção de entrada; como fazer é Módulo 2 | 2 (§2.3 "configured exceptions") | ✔ |
| s8 | Roteador com firewall: aparelho pequeno e barato que protege os computadores da rede de casa | 1 (§2.2.2) | ✔ |
| s8 | Firewall pessoal controla o que entra e sai da máquina; Firewall do Windows como exemplo | 1 (§2.2.1, glossário), 4 | ✔ |
| s8 | Se o firewall do computador falhar/for desligado/mal configurado, o do roteador ainda protege | 1 (§2.2.2) | ✔ |
| s8 | Filtro IP do NVR Intelbras: só IPs da lista de permitidos acessam; exemplo do chefe de segurança e do presidente; aceita IP, faixa (início–fim) ou MAC | 7 (p. 67-68) | ✔ |
| s8 | "Antes de habilitar": incluir o próprio computador; e conferir o Filtro IP se o NVR parar de responder a um computador | 7 (dedução direta de "somente os IPs permitidos… poderão ser conectados") | ✔ — 192.168.1.50 marcado "por exemplo" |
| s10 | Mirai: varredura de IPs sorteados nas portas TCP 23 e 2323 (Telnet); lista de 62 combinações; envio a servidor de relatório; infecção | 8 (§2), 9 | ✔ |
| s10 | Pico de 600 mil; alvos principais câmeras IP, DVRs e roteadores domésticos; Krebs on Security, set/2016, > 600 Gbps | 8 (abstract, §1, §3), 9 (620 Gbps em 20/09/2016) | ✔ |
| s10 | 1º passo do Mirai é conversa de entrada; só acontece se o aparelho estiver alcançável de fora | 8 + 2 (definição de entrada) — dedução | ✔ |
| s10 | CISA: trocar senhas de fábrica por fortes e atualizar | 9 | ✔ — **não** atribuí "usar firewall" à CISA |
| s11 | Aparelho infectado fala pra fora (relatório, varredura, ataques) = saída | 8, 2 | ✔ |
| s11 | NIST: filtrar saída impede ataques lançados de dentro; no computador, limita a propagação de malware | 1 (§2.1.1, §2.2.1) | ✔ |
| s11 | Ideal (bloquear também a saída não permitida) × usual (saída menos rígida); Microsoft: bloquear saída em ambientes de alta segurança | 1 (§4 e §4.1), 4 | ✔ — divergência mostrada, não escondida |
| s11 | CISA: procurar tráfego suspeito na porta 48101, usada pelos aparelhos infectados | 9 | ✔ |
| s11 | Firewall só funciona no tráfego que consegue inspecionar; lugares muito protegidos ainda sofrem ataques | 1 (§2.3), 6 | ✔ |
| s13 | Resumo = só o que foi dito; cada bullet se sustenta sozinho (vira o "Relembrando" do T35) | — | ✔ |

## 2. Fatos de alto risco — busca refeita (além do dossiê)

| Fato | Conferência independente | Resultado |
|---|---|---|
| Portas 23 e 2323 (Telnet) | Texto do artigo USENIX (extraído do PDF) **e** página da CISA lida de novo com `curl` | batem |
| Lista de 62 usuários/senhas | USENIX ("pre-configured list of 62 credentials") e CISA ("62 common default usernames and passwords") | batem |
| 600 mil infecções | USENIX, abstract e §4 ("peak of 600,000 infections") | ok |
| > 600 Gbps, set/2016, Krebs | USENIX ("exceeded 600 Gbps") e CISA ("September 20, 2016… exceeding 620 Gbps") | batem — escrevi "passou de 600 Gbps" |
| Porta 48101 | CISA, frase lida na página: "Look for suspicious traffic on port 48101. Infected devices often attempt to spread malware by using port 48101 to send results to the threat actor." (uma busca na web não trouxe 2ª fonte; ficou só a primária, citada como "o alerta da CISA manda…") | ok |
| Filtro IP (comportamento) | Texto do manual extraído do PDF, p. 67-68, duas frases independentes dizem o mesmo | ok |
| RFC 6092 é de IPv6 | O tópico usa dela só a **definição** de direção e o **princípio**; a própria RFC diz que o filtro com estado do NAT "set user expectations that persist today". O padrão em IPv4 está sustentado por 4 e 5, não por ela | ok |

## 3. Regras do curso (Redes)
- IPs: NVR real 192.168.1.19; público de exemplo **203.0.113.20** (RFC 5737); privado de exemplo
  192.168.1.50. Os IPs reais das fontes (130.207.x de Kurose; 7.7.7.7/2.2.2.2 do Tailscale) **não** foram usados. ✔
- Exemplos variados: portaria/condomínio, loja/comércio, casa, escritório, empresa (exemplo do manual). ✔
- Nenhum comando. Nenhum "sempre/nunca" técnico sem fonte ("nunca mudar a entrada pra permitir tudo" é da Microsoft). ✔
- Nada inventado sobre o NVR real: dele só o IP; o Filtro IP vem do manual do modelo. ✔

## 4. Erros pegos nesta auditoria (corrigidos antes de publicar)
- O roteiro dos rascunhos pedia o fluxo da tabela de estados com o NVR abrindo uma conexão pra fora —
  seria inventar comportamento do NVR (os dois rascunhos inventaram: NTP, firmware, nuvem). No texto
  final o fluxo usa um notebook da portaria abrindo um site.
- Cogitado e descartado antes de escrever: "o Intelbras Cloud funciona porque a conexão sai de
  dentro" — sem fonte do fabricante (registrado no dossiê, "o que ficou de fora").
- Tailscale entra como paráfrase atribuída, não citação (material moderno — regra de direito autoral).

## 5. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-2.5-flash`, depois de 503/504 nos 3.x) e Groq (`qwen3.8-27b`). Arquivos
`backend/_conteudo_{conteudo,segunda_opiniao}_topico34.json`. A ordem bateu com o roteiro; o conteúdo
trouxe muita coisa fora do dossiê:

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| Gemini | NVR "envia NTP na porta UDP 123 para o pool NTP.br"; "verifica firmware em update.fabricante.com" | comportamento do NVR real **inventado** |
| Gemini | Mirai "em setembro de 2016 derrubou Dyn, Twitter, Spotify e Netflix" | data/alvos misturados e sem fonte no dossiê (set/2016 foi Krebs) |
| Gemini | "Um firewall de entrada teria evitado a infecção global… tornando irrelevante a senha fraca" | **sem fonte** e contra a CISA (a recomendação é senha + atualização) |
| Gemini | Estados RELATED/ESTABLISHED, SYN_SENT, FIN_WAIT, "implicit deny", ACCEPT/DROP, camadas 3/4/7 | fora do dossiê e do nível |
| Gemini | Ensina regra de redirecionamento da 37777 e fala de DMZ | T36 (Módulo 2) — proibido no foco |
| Gemini | "Se o NVR fosse um modelo Intelbras…" | o NVR real É Intelbras; texto inseguro |
| **Groq** | IP público **200.150.80.45**; câmera "Hikvision DS-2CD2143G0-I em 192.168.1.45"; regras "do projeto" com 443 redirecionada | IP com cara de real (**viola a regra do curso**) e configuração **inventada** do projeto |
| Groq | Timeout UDP "padrão de 30 s"; câmera mandando UDP na porta 5000 | **números inventados** (o NIST só diz "tempo configurado") |
| Groq | Passo a passo no pfSense | comando/tela fora do dossiê |
| Groq | Mirai varrendo "23, 80 e 554" | **errado** — as fontes dizem 23 e 2323 |
| Groq | RFC 6092 "define egress/ingress" e "descreve stateful packet inspection" | atribuição errada (ingress/egress é do NIST) |
| Groq | Duas citações entre aspas sem autor | **citações inventadas** |
| Groq | Blocos `timeline`, `cards`, `badges` | fora do padrão do tópico |

Aproveitado dos rascunhos: só uma **ideia didática** do Groq ("o roteador liberou, mas não funciona" —
o Filtro IP barrando outro computador), reescrita como dica de diagnóstico no s8, sustentada pelo manual.
Nenhum texto dos rascunhos foi copiado.

## 6. Pedagogia
- Do simples ao complexo: o que é → direção → padrão → como lembra → negar por padrão → onde fica → caso real → saída → limites.
- Exemplo antes da abstração (site que carrega, portaria) e analogia que continua a do T33.
- Checkpoints: tf (3), classify (2), mc com cenário (3), mc, associar + **2 abertas** ✔. Toda pergunta
  é respondível com o que foi ensinado no próprio tópico. Reflexão + Resumo ✔.
- Caso real (Filtro IP do manual; Firewall do Windows) e caso que deu errado (Mirai) ✔.

## 7. Continuidade
- Retoma T33 (NAT não é firewall; relógio do UDP; analogia da portaria) e T31 (Mirai, portas).
- Não ensina a abrir porta/redirecionar/DMZ (T36), não detalha os riscos de expor porta (T37), não
  cita UPnP, não entra em DNS (T35). Próximo tópico indicado: "DNS e DDNS".

## 8. Direito autoral
- RFCs e NIST (documento de governo dos EUA): citação curta traduzida. Manual Intelbras: conteúdo
  funcional parafraseado. Tailscale, Microsoft e Kurose & Ross: só paráfrase atribuída. ✔

## 9. Estrutura
- `validar_topico()` vazio; ids de pergunta e de item únicos; `fluxo` (nenhum `diagrama`); capa com `imagem_capa` ✔.

**Pendências: 0.**

## 10. Imagens
8 geradas (capa + 7 inline), todas aprovadas na primeira: estilo isométrico do curso, sem texto nem
pseudo-texto, sem pessoas. Dois textos alternativos foram reescritos pra descrever o que a imagem
realmente mostra (`t34-entrada-saida`: a seta âmbar chega ao gravador, não "para no portão";
`t34-tres-camadas`: há mais de três escudos). Densidade 0,78 (7 inline + capa em 9 slides). Em
produção, as 8 respondem 200.

## 11. Áudio
32 narrações (cadeia "narracao"), **todas revisadas antes da voz; 11 reescritas**:
- frase sem sentido ("funcionando igualzinho ao controle de um notebook na portaria") — s5;
- causa invertida no UDP/NAT ("é por isso que… guarda a informação do NAT") — s5;
- fato acrescentado: "roteador **da operadora**", "contra invasões externas" (s8), "tráfego malicioso" (s10),
  "uma rede de câmeras quase não precisa falar com o lado de fora" (a reflexão virou afirmação — s13);
- "NVD 1304, NVD 1308 e NVD 1316" em sequência (risco de número lido errado, lição do T31) → "NVR Intelbras";
- "Gbps" → "gigabits por segundo"; "CISA" → "alerta do governo americano"; "o órgão NIST" → "o NIST";
- narrações do s10/s11 que terminavam no ar → apontam pro fluxo na tela;
- resumo (vira o "Relembrando" do T35) reescrito pra cobrir os 8 pontos sem enfileirar números.

Voz 32/32, `_conferir_audio.py` com **0 problemas**. Achado fora do conferidor: no 1º áudio o corte
deixou "É o firewall." no começo do 2º arquivo (semelhança 0,96 — passou no limite). Corrigido
recortando os dois WAV pela transcrição com tempo por palavra, sem nova chamada de voz; reconferido 1,00.
Em produção: 32 MP3 respondendo 200, diagnóstico sem ✗.

Ajuste de ferramenta (fora de `app/`): `_gerar_audio_topico.py` e `_conferir_audio.py` agora tentam de
novo o envio ao Whisper quando a rede cai — antes, uma queda de SSL jogava fora o áudio recém-gerado
(cota de voz de 10/dia por modelo); nesta sessão isso desperdiçou algumas chamadas antes da correção.
