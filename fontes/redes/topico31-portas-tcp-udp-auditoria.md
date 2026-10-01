# Auditoria IA — Tópico 31 "Portas TCP/UDP (554, 1935, 80, 443)"

Curso Redes e Câmeras (Course 11) · `Topico.id=31` · auditado em 2026-10-01 por Claude,
seguindo `docs/processo-topico/BASE.md` (Passo 5). Dossiê:
[topico31-portas-tcp-udp.md](topico31-portas-tcp-udp.md) (fontes numeradas abaixo).
Conteúdo auditado: `backend/_topico31_redes_final.json` (gerado por `_criar_topico31_redes.py`).

## 1. Fato (afirmação → fonte)

| # | Afirmação no tópico | Fonte | Status |
|---|---|---|---|
| 1 | Porta é número de 0 a 65535; IP acha o aparelho, porta acha o serviço | 1, 10 | ok |
| 2 | Toda porta pertence a TCP ou UDP; TCP 554 ≠ UDP 554 (par protocolo+porta) | 1, 2 | ok |
| 3 | TCP abre conexão e garante entrega em ordem | 12 (RFC 9293) | ok |
| 4 | UDP não garante entrega ("delivery … not guaranteed") | 12 (RFC 768, citação) | ok |
| 5 | 80 e 443 (página), 554 (controle RTSP), 1935 (RTMP) são TCP | 3, 4, 6 | ok |
| 6 | Faixas 0–1023 / 1024–49151 / 49152–65535; dinâmicas nunca são de serviço fixo | 1 | ok |
| 7 | 1935 e 37777 estão na faixa registrada (não na 0–1023) | 1 (faixa), 2, 7 | ok — conta direta |
| 8 | HTTP = TCP 80 padrão; HTTPS = TCP 443 padrão | 3 (citação) | ok |
| 9 | RTSP = 554 padrão do servidor; controle tem que funcionar em TCP (RFC 2326) | 4 (citação) | ok |
| 10 | RTMP = 1935/TCP, usado pra enviar vídeo; YouTube/Twitch/Facebook aceitam ingest RTMP | 6 | ok (secundária confiável) |
| 11 | "A câmera manda UDP pra 554" é errado | 4 | ok |
| 12 | Porta de origem temporária; Windows 49152–65535, Linux 32768–60999 | 9, 12 | ok |
| 13 | NVR é o cliente quando puxa vídeo da câmera (destino 554 na câmera) | 4, 7 (NVR adiciona câmera por RTSP/Onvif) | ok |
| 14 | Tela Portas Intelbras: 37777 serviço (imagens + autenticação), 80, 443 (habilitar), 554 | 7 (manual p. 65) | ok |
| 15 | Link RTSP `rtsp://user:senha@ip:porta/cam/realmonitor?channel=N&subtype=0` | 7 (manual p. 65) | ok |
| 16 | Não usar caractere especial no fim da senha pra RTSP | 7 (manual p. 65) | ok |
| 17 | `Test-NetConnection IP -Port N` testa TCP; saída `TcpTestSucceeded` | 13 | ok |
| 18 | O comando não tem opção pra UDP | 13 (sintaxe oficial lista só -Port TCP) | ok |
| 19 | Mirai varria Telnet TCP 23 e 2323 | 8 | ok |
| 20 | Tentava lista de 62 credenciais padrão | 8 (resumo do paper via busca) | ok |
| 21 | Pico ~600 mil infecções; Krebs > 600 Gbps; depois OVH e Dyn | 8 (abstract e introdução, lidos no PDF) | ok |
| 22 | Muitos dos infectados eram câmeras e gravadores | 8 | ok |

**Fatos de alto risco com busca refeita/fonte primária lida:** 6, 8, 9, 14, 17, 18, 21
(RFC 6335, RFC 9110, RFC 2326, manual Intelbras PDF, doc Microsoft, PDF USENIX).

## 2. Erros do rascunho do Groq que NÃO entraram (corrigidos/removidos)

| Erro no rascunho Groq | Correção |
|---|---|
| 1935 listada como porta "Well-Known" (0–1023) | Removido; virou pegadinha explícita no slide de faixas |
| Faixa dinâmica "49252–65535" | Corrigido pra 49152 |
| 37777 = "interface web de gerenciamento", acesso `http://IP:37777` | Corrigido pelo manual: porta de serviço (imagens + autenticação); web = 80 |
| Caminho de menu e campo "Porta da Interface Web" inventados | Removido |
| Câmera pedindo stream ao NVR | Invertido pro correto: NVR é o cliente |
| `Test-NetConnection -Udp` | Removido; parâmetro não existe (fonte 13) |
| Câmera Dahua IPC-HFW5231E-S2, IP 192.168.1.45, "Praça da República", "nuvem XYZ" | Removidos (inventados) |
| Citação atribuída a "Instrutor do curso" | Removida (inventada) |
| RTP 5000–5005/UDP, ONVIF 3702/UDP, handshake TCP | Fora do dossiê e do escopo (T32/Módulo 3/4) — removidos |
| Regra de firewall "abrir faixa dinâmica de saída" | Fora do dossiê — removida |
| Caso Mirai ausente | Incluído (slide s11) |

**Gemini** (503 na 1ª tentativa; 2ª respondeu depois da versão final pronta) — comparado:

| Erro no rascunho Gemini | Decisão |
|---|---|
| Mirai infectou "milhões" de dispositivos | Não entrou — paper: pico ~600 mil |
| Test-NetConnection "ou enviar um pacote UDP" | Não entrou — só TCP (fonte 13) |
| Senha `admin123` no exemplo de link RTSP | Não entrou — mau exemplo num tópico de segurança |
| Intelbras e Dahua "compartilham a mesma base", portas baixas "exigem administrador" | Não entrou — fora do dossiê |
| Quíntupla (5-tuple), modelo OSI/TLS na camada de apresentação | Não entrou — além do nível e fora do dossiê |

| Acerto do Gemini que faltava na versão final | Decisão |
|---|---|
| HTTP (80) não criptografa; senha trafega aberta → preferir 443 | **Entrou** no item 443 do s5 (fonte 3: HTTPS = HTTP sobre TLS) |

Afirmação nova auditada: #23 "pela 80 usuário e senha passam abertos; prefira 443" — fonte 3 — ok.

## 3. Pedagogia

- [x] Ordem: recapitula IP (T28–30) → porta → protocolo → faixas → portas do curso →
      origem/destino → caso real (NVR) → ferramenta → caso que deu errado → reflexão/resumo.
- [x] Exemplo concreto antes da abstração (prédio/apartamento antes da definição de faixa).
- [x] Toda pergunta é respondível com o que foi ensinado (ck1–ck4 conferidos um a um;
      ck2_2 exige a conta 1935 ∈ 1024–49151, ensinada explicitamente no s4).
- [x] Exemplos variados: condomínio, comércio, igreja (live), Piazza Fontana.

## 4. Direito autoral

- [x] Nenhum trecho longo copiado. Citações curtas de RFC (domínio público/IETF) e do
      manual (link RTSP e aviso de senha, conteúdo técnico funcional). Kurose & Ross só em paráfrase.

## 5. Continuidade

- [x] Usa 192.168.1.19 e o gateway do T30; não reabre máscara/gateway.
- [x] Não invade o T32: TCP/UDP só em "dois jeitos de entregar", com chamada explícita pro próximo tópico.
- [x] Port forwarding/riscos de expor porta só mencionados como Módulo 2.

## 6. Estrutura

- [x] `validar_topico()` → sem problemas
- [x] Render (`alto-contraste`) → 0 ocorrências de `None`
- [x] Reflexão + Resumo (s12); 4 checkpoints com mc, tf, associar, classify, lacuna, open (2)
- [ ] Imagens geradas e copiadas (Passo 6) — em andamento

## Resultado

**Conteúdo APROVADO** — 22 afirmações verificadas, 0 pendências de fato. Aprovação final
(`is_approved=true`) depois das imagens aplicadas e conferidas.
