# Auditoria IA — T30 "Máscara de sub-rede e gateway"

Curso Redes e Câmeras · `Topico.id=30` · auditado em 2026-10-01 (revisão dos tópicos antigos).
Dossiê: [topico28-30-enderecamento-ip.md](topico28-30-enderecamento-ip.md).

## Fato

| # | Afirmação | Fonte | Status |
|---|---|---|---|
| 1 | Máscara separa rede e host | 12 | ok |
| 2 | 255.255.255.0 = /24; 3 primeiros octetos = rede | 12 | ok |
| 3 | "praticamente todo sistema de câmeras usa 255.255.255.0" | — | **ajustado** → "a maioria… a mais comum" |
| 4 | Faixa de hosts 192.168.1.1–254 | 12 (.0 rede, .255 broadcast) | ok |
| 5 | Câmeras precisam estar no mesmo segmento do NVR | 10 (manual p.26) | **acrescentado** com citação do manual |
| 6 | Gateway = saída pra fora da rede local; costuma ser o .1 | 12 | ok ("geralmente", não "sempre") |
| 7 | NTP como exemplo de saída pela internet | — | ok (exemplo, não afirmação técnica arriscada) |
| 8 | Decisão rede local x gateway pela máscara | 12 | ok (simplificação válida pra /24) |
| 9 | "No próximo módulo: port forwarding, VPN" | grade do curso | **corrigido**: o próximo agora é o T31 (Portas); NAT/firewall/DNS no mesmo módulo; acesso de fora no Módulo 2. `proximo_topico_label` atualizado |
| 10 | IP 189.45.12.30 na recapitulação | 5 | **corrigido** → 203.0.113.30 |
| 11 | Checkpoints e respostas | — | ok |

## Padrão novo
- [x] Reflexão adicionada (2 perguntas)
- [x] 2ª pergunta aberta (ck3_3: câmera de fábrica em 192.168.0.100)
- [x] Imagens: 4 + capa em 6 slides (0,67) — ok
- [ ] Áudio — depois da revisão aprovada

**Resultado:** continuidade e 1 IP real corrigidos, 1 ajuste de precisão, 1 fato do fabricante acrescentado. 0 pendências.
