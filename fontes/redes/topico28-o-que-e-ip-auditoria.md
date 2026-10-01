# Auditoria IA — T28 "O que é um endereço IP"

Curso Redes e Câmeras · `Topico.id=28` · auditado em 2026-10-01 (revisão dos tópicos antigos).
Dossiê: [topico28-30-enderecamento-ip.md](topico28-30-enderecamento-ip.md). Correções aplicadas por
`backend/_revisar_redes_t28_30.py`.

## Fato

| # | Afirmação | Fonte | Status |
|---|---|---|---|
| 1 | IP identifica um dispositivo na rede | 1, 12 | ok |
| 2 | IPv4: 4 octetos de 0–255, 32 bits | 1 | ok |
| 3 | 32 bits ≈ 4,3 bilhões de endereços | conta (2^32) | ok |
| 4 | "o mundo já tem mais dispositivos conectados do que isso" | — | **corrigido**: sem fonte → "reserva livre da IANA acabou em fev/2011; só de IoT eram ~21 bi em 2025" (7, 8) |
| 5 | IPv6 = 128 bits, ex. 2001:db8::1 | 2 | ok (2001:db8:: é prefixo de documentação) |
| 6 | "não tem risco de esgotar de novo" | — | **corrigido** → "resolve a falta de endereços; ~metade dos acessos ao Google já é IPv6" (9) |
| 7 | "CFTV opera quase todo em IPv4; equipamentos só oferecem IPv4" | — | **corrigido**: a fonte contradiz — o NVR Intelbras oferece IPv4 ou IPv6 (10). Novo texto: o dia a dia (e Piazza Fontana) é IPv4 |
| 8 | DHCP x IP fixo x reserva de DHCP | 6 | ok |
| 9 | NVR/câmeras devem ter IP fixo ou reserva | 10 (vem de fábrica em DHCP) | ok + **acrescentado** o fato do manual (DHCP de fábrica, 192.168.1.108 sem DHCP) |
| 10 | Fluxo s8: pedido a 192.168.1.19 "viaja pela internet até o roteador de Piazza Fontana" | 3 | **ERRO DE CONCEITO, corrigido**: IP privado não é roteado na internet; o pedido fica na rede do celular ou é descartado, e pode até achar OUTRO aparelho com o mesmo IP |
| 11 | IP público de exemplo 189.45.12.30 | 5 | **corrigido**: era endereço real de provedor → 203.0.113.30 (faixa de documentação) |
| 12 | Checkpoints e respostas | — | ok, todas conferidas |

## Padrão novo
- [x] Reflexão adicionada (box "💭 Pra pensar", 3 perguntas)
- [x] 2ª pergunta aberta adicionada (ck3_3: por que 192.168.1.19 não chega de fora)
- [x] Imagens: 6 + capa em 7 slides (densidade 0,86) — ok
- [ ] Áudio — depois da revisão aprovada

**Resultado:** 1 erro de conceito, 3 afirmações sem fonte e 1 IP real corrigidos. 0 pendências.
