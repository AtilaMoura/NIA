# Auditoria — T33 "NAT (Network Address Translation)"

Conteúdo final: `backend/_criar_topico33_redes.py` → `_topico33_redes_final.json` (16 slides,
7 imagens, 2 fluxos, 5 checkpoints). Dossiê: `topico33-nat.md`. 2026-10-05.

## 1. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | NAT liga rede privada à internet; NAPT: muitos endereços e portas → um endereço e as portas dele | 1 (RFC 3022 abstract) | ✔ |
| s1 | Modelo atende residências e pequenos escritórios com um único IP do provedor | 1 (§2.2 "SOHO") | ✔ |
| s2 | Fluxo da tabela de tradução (troca na saída, anota, resposta, desfaz) | 1 (§3.1 binding), 5 (Kurose) | ✔ — portas 50001/40001 e IP 203.0.113.10 marcados "exemplo" |
| s2 | NAPT: (IP privado, porta) → (IP público, porta atribuída) | 1 (§2.2) | ✔ |
| s4 | Citação RFC 3022: sessões unidirecionais, de dentro pra fora; exceção por mapeamentos fixos (tradução livre) | 1 (§2) | ✔ |
| s4 | Analogia da portaria (encomenda pedida × pacote sem destinatário) | didática, coerente com 1 | ✔ |
| s4 | NVR responde dentro e não de fora (retomada do T29); redirecionamento = Módulo 2 | T29, 1 | ✔ |
| s5 | Citação RFC 4787 REQ-5 (mínimo 2 minutos) (tradução livre); tempo exato varia e pode ser configurável | 3 | ✔ |
| s5 | Linha expirada → pacote de fora não acha o caminho | 1 + 3 (dedução direta da tabela) | ✔ |
| s7 | Citação Google NAT dupla; sintomas: encaminhamento de portas e UPnP, jogos online | 6 | ✔ |
| s7 | Correção: modo bridge no equipamento da operadora (ou modem direto); bridge desativa DHCP e roteamento | 6 | ✔ |
| s7 | CGNAT (100.64–100.127): bridge não resolve | T29 + RFC 6598 (dossiê T28-30) | ✔ |
| s7 | "Antes de mexer": anotar config, combinar com quem administra/operadora | prudência, sem fato técnico novo | ✔ |
| s8 | Citação RFC 4864 "de difícil a impossível" (tradução livre) | 4 | ✔ |
| s8 | Exemplo condomínio com dois NVRs na 554 | 4 + porta 554 (T31) | ✔ — contorno só citado (Módulo 2) |
| s10 | Citação RFC 4864 "segurança percebida… vendido como firewall… efeito arbitrário" (tradução livre) | 4 | ✔ |
| s10 | Mapeamento fixo expõe de propósito o que estava "protegido" por acaso | 4 (dedução direta) | ✔ |
| s11 | Menu Rede do NVR Intelbras: TCP/IP, Portas, DDNS, Intelbras Cloud (app iSIC, nº de série/QR) | 7 (manual p.62-63) | ✔ — sem afirmar que a nuvem existe "por causa do NAT" |
| s13 | Resumo = só o que foi dito | — | ✔ |

## 2. Regras do curso (Redes)
- IPs: NVR real 192.168.1.19; público de exemplo **203.0.113.10** (RFC 5737); privados de exemplo
  192.168.0.2 / 192.168.1.2; CGNAT de exemplo 100.72.15.9 (faixa compartilhada RFC 6598 — não é IP
  de provedor). O IP de exemplo da RFC 3022 (138.76.x) **não** foi usado. ✔
- Exemplos variados: residência, comércio, condomínio (portaria + garagem). ✔
- Nenhum comando citado (não precisou). Nenhum "sempre/nunca" técnico sem fonte. ✔

## 3. Erros pegos nesta auditoria (corrigidos antes de publicar)
- Referências "Tópico 2/4/5" e "Tópicos 1 a 3": o curso numera tópicos POR AULA, então ficava
  ambíguo → trocadas pelos nomes ("tópico de IP privado e público", "tópico de portas"…).

## 4. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-3.5-flash`) e Groq (`qwen3.8-27b`). Arquivos
`backend/_conteudo_{conteudo,segunda_opiniao}_topico33.json`. A ordem dos dois bateu com o roteiro;
o conteúdo trouxe erros que o dossiê pedia pra evitar:

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| Gemini | NAT "adiciona uma camada de segurança, pois os IPs internos não são visíveis" | **contradiz a RFC 4864** (segurança percebida = efeito arbitrário) |
| Gemini | servidor "da internet" com IP **172.16.0.10** | IP privado (RFC 1918) não é servidor de internet — erro técnico |
| Gemini | "configurar redirecionamento pra usar a nuvem/P2P é conceitualmente errado" | afirmação sem fonte (Módulo 2) |
| Gemini | explica UPnP abrindo portas automaticamente; "economiza endereços IPv4" | fora do dossiê |
| **Groq** | IPs públicos **200.150.30.12, 200.150.45.22, 200.150.80.25, 200.160.10.5** | parecem IPs reais de provedor — **viola a regra do curso** (só 203.0.113.x) |
| Groq | citação entre aspas "Um NAT duplo é como ter duas portas de segurança em série…" sem autor | **citação inventada** |
| Groq | "enquanto houver pacotes UDP chegando, o temporizador é reiniciado" | impreciso — a RFC 4787 trata a renovação com mais detalhe (saída × entrada); o tópico ficou só no mínimo de 2 min |
| Groq | STUN/TURN como solução | Módulo 2 (P2P) |
| Groq | bloco `diagrama` | proibido |

Nenhum texto dos rascunhos foi copiado.

## 5. Pedagogia
- Retoma T29 (IP privado/público, CGNAT) e T32 (UDP); fecha com ponte pro T34 (firewall) e Módulo 2.
- Checkpoints: tf, mc, mc com cenário, associar, classify (6) + **2 abertas** ✔. Reflexão + Resumo ✔.
- Caso real (NAT duplo, manual NVR) e caso que deu errado (porta que "não abre"; dois NVRs na 554) ✔.

## 6. Continuidade
- Não ensina a configurar redirecionamento de porta/UPnP (T36, Módulo 2); não detalha firewall (T34)
  nem DNS (T35). Não repete o teste de CGNAT — só retoma.

## 7. Estrutura
- `validar_topico()` vazio; 0 `None` (alto-contraste); ids únicos; `fluxo` (nenhum `diagrama`); capa ✔.

**Pendências: 0.**

## 8. Imagens
7 geradas, todas aprovadas na primeira (sem texto; pessoas só estilizadas na portaria). Densidade 0,67 (6 inline + capa em 9 slides), aceita pelo diagnóstico.
