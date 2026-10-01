# Auditoria IA — T29 "IP privado vs. IP público"

Curso Redes e Câmeras · `Topico.id=29` · auditado em 2026-10-01 (revisão dos tópicos antigos).
Dossiê: [topico28-30-enderecamento-ip.md](topico28-30-enderecamento-ip.md).

## Fato

| # | Afirmação | Fonte | Status |
|---|---|---|---|
| 1 | IP privado só tem sentido na rede local; se repete em várias redes | 3 | ok |
| 2 | "nenhum roteador da internet sabe rotear pacotes até ele" | 3 | **ajustado** pra formulação da RFC: provedores filtram endereços privados |
| 3 | IP público "único e exclusivo" da sua rede | 4 | **ajustado**: "normalmente um por conexão" — o próprio tópico ensina CGNAT, que contradiz "exclusivo" |
| 4 | 3 faixas RFC 1918 (10/8, 172.16–31, 192.168/16) | 3 | ok |
| 5 | IP público é dado pela operadora | — | ok (definição) |
| 6 | "na maioria dos planos residenciais é dinâmico" | — | **ajustado** → "em muitos planos" (sem fonte pra "maioria") |
| 7 | DNS/DDNS "mais à frente nesta mesma aula" | grade do curso | **corrigido**: é outra aula do mesmo módulo |
| 8 | CGNAT = vários clientes num IP público; faixa 100.64–100.127 | 4 | ok |
| 9 | Atrás de CGNAT "nenhuma configuração resolve acesso remoto" | 4 + grade (T38–T41) | **ERRO, corrigido**: o que não funciona é redirecionar porta; VPN/P2P (Módulo 2) funcionam |
| 10 | Teste: WAN ≠ "meu IP" → CGNAT | 4, 11 | **ERRO, corrigido**: WAN em faixa privada = NAT duplo com o modem da operadora (resolve com bridge); CGNAT só com WAN em 100.64–100.127. Fluxo e texto refeitos |
| 11 | V/F: "WAN diferente = sinal de CGNAT" (Verdadeiro) | 4, 11 | **reescrita**: cenário WAN 192.168.0.5 → "mais provável CGNAT" = Falso (é NAT duplo) |
| 12 | Alternativa "189.45.0.0–189.45.255.255" e IP 189.45.12.30 | 5 | **corrigido**: faixa real de provedor → 8.8.8.0–8.8.8.255 (pública) e 203.0.113.30 (documentação) |
| 13 | NAT "no módulo mais à frente" | grade | ajustado no texto novo ("tópico de NAT") |

## Padrão novo
- [x] Reflexão adicionada (3 perguntas)
- [x] 2ª pergunta aberta (ck3_3: WAN 100.72.15.9)
- [x] Resumo atualizado (CGNAT x NAT duplo)
- [x] Imagens: 4 + capa em 6 slides (0,67 — limite inferior da meta, ok)
- [ ] Áudio — depois da revisão aprovada

**Resultado:** 2 erros de conceito, 1 pergunta com gabarito enganoso, 3 ajustes de precisão, continuidade e IP real corrigidos. 0 pendências.
