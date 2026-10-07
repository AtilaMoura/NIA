# Auditoria — Prova do T33 "NAT (Network Address Translation)"

Curso Redes e Câmeras (11) · `Topico.id=33` · 2026-10-07 · piloto do `/criar-provas-topicos`.
Banco: `backend/_prova_topico33.json` (gerado por `backend/_montar_prova_topico33.py`).
Regra do curso (PROVA.md §3): banco 18, rodada 6, nota 70%, `tipos_minimos {"open": 1}`.
Fontes: conteúdo publicado do tópico 33 (slides s1–s14) + `fontes/redes/topico33-nat.md`.

## Perguntas

| id | assunto | tipo | o que cobra | sustentação | status |
|---|---|---|---|---|---|
| p33_01 | A | mc | vários aparelhos, 1 IP público, portas diferentes | s1 box "O que é NAT" + s2 box NAPT; RFC 3022 (dossiê f.1) | ok |
| p33_02 | A | tf (F) | na saída troca a ORIGEM, não o destino | s2 fluxo passos 2 e 5; Kurose & Ross (f.5) | ok |
| p33_03 | A | associar | troca na saída / anota / desfaz na volta | s2 fluxo passos 2, 3, 5 | ok |
| p33_04 | A | mc | a porta pública decide a entrega (mesma porta privada em 2 aparelhos) | s2 fluxo passo 5 + box NAPT | ok — aplicação nova do mecanismo, sem fato novo |
| p33_05 | A | tf (V) | NAT de casa/pequeno escritório com 1 IP do provedor | s1 box "Onde isso acontece"; RFC 3022 SOHO (f.1) | ok |
| p33_06 | A | open | descrever ida, anotação e volta | s2 fluxo inteiro; resposta-modelo = os 3 passos | ok |
| p33_07 | B | tf (V) | linha nasce quando o de dentro começa | s4 parágrafo + citação RFC 3022 §2 | ok |
| p33_08 | B | mc | linha UDP parada pode expirar (mínimo 2 min) | s5 citação RFC 4787 REQ-5 + box | ok — "pode", não "vai", porque o tempo varia |
| p33_09 | B | tf (F) | 2 min é mínimo, não valor exato | s5 box: "no mínimo… varia de roteador para roteador" | ok — inverso do ck2_2, não cópia |
| p33_10 | B | mc | 1 porta pública → 1 aparelho (porta 80) | s8 citação RFC 4864 §2; porta 80 do T31 | ok — cenário diferente do ck3_2 (loja, porta 80) |
| p33_11 | B | classify | chega × não chega (tabela, expiração) | s4 + s5 (linha expirada não acha caminho) | ok |
| p33_12 | B | open | analogia da portaria aplicada ao NVR | s4 box analogia + box "É por isso que o NVR não abre" | ok |
| p33_13 | C | tf (V) | bridge desativa DHCP e roteamento | s7 fluxo passo 4; Google Nest (f.6) | ok |
| p33_14 | C | mc | WAN 100.80.3.7 = CGNAT, bridge não resolve | s7 box "Antes de mexer" (100.64–100.127); T29 | ok — 100.80.3.7 é do espaço compartilhado (RFC 6598), não host real |
| p33_15 | C | tf (F) | mapeamento fixo expõe o que estava "protegido por acaso" | s10 box, item 2 | ok |
| p33_16 | C | mc | origem da "segurança" do NAT | s10 citação RFC 4864 §2 | ok |
| p33_17 | C | classify | NAT × firewall (só o que o tópico disse) | s10 citação + box item 3 | ok — não ensina firewall (T34), só a frase da RFC |
| p33_18 | C | open | por que "NAT é firewall" está errado | s10 inteiro | ok |

## Checagens gerais

| Checagem | Resultado |
|---|---|
| Gabarito de cada pergunta conferido contra o tópico | ok (18/18) |
| mc com uma só opção certa (p33_01, 04, 08, 10, 14, 16) | ok — as erradas contradizem o tópico de forma direta |
| Pegadinha de redação | nenhuma; o "DESTINO" do p33_02 está em maiúsculas de propósito, pra o foco ser o conceito |
| Nada além do tópico e dos anteriores | ok — sem redirecionamento de porta/UPnP (T36), sem regras de firewall (T34), sem tipos de NAT (cone/simétrico) |
| Cópia de checkpoint | nenhuma: cenários e afirmações novos (comparado com ck1_1…ck5_3) |
| Regra do curso Redes | IPs de exemplo: privados 192.168.x e documentação 203.0.113.x (RFC 5737); CGNAT do espaço compartilhado; NVR real 192.168.1.19 só como no tópico |
| Ids únicos (perguntas e itens) | ok — `p33_NN` e `p33_NN_x`, nenhum id de checkpoint reaproveitado |
| Abertas com resposta-modelo | 3 (uma por assunto) → toda rodada tem 1 aberta |
| `_publicar_prova.py --checar` | ✅ validação + simulação de 3 rodadas × 2 pessoas |

## Erros pegos durante a escrita

- Rascunho do p33_10 repetia o cenário do ck3_2 (dois NVRs na porta 554) → trocado para loja com duas câmeras na porta 80.
- Rascunho do p33_05 era "a porta separa as conversas", muito perto do ck1_2 → trocado para o modelo SOHO da RFC 3022.
- Rascunho do p33_13 era "qual correção o Google recomenda", igual ao ck4_2 → virou tf sobre o que o modo bridge faz.

**Pendências: 0.** Liberado pra publicar.
