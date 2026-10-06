# Auditoria — T69 "A Palavra acima da tradição" (Mc 7:6-13)

Conteúdo final: `backend/_criar_topico69_obreiro.py` → `_topico69_obreiro_final.json` (14 slides,
6 imagens, 2 fluxos, 4 checkpoints). Dossiê: `topico69-palavra-tradicao.md`. 2026-10-06.

## 1. Citações bíblicas (conferência automática, letra por letra)
**6/6 blocos `quote` ✓ e 20/20 trechos curtos ✓** contra a bible-api normalizada + correções.

Erros da FONTE corrigidos:
| Ref. | Fonte trazia | Corrigido | Conferência |
|---|---|---|---|
| Mc 7:9 | "mandamento de **d**eus" | "mandamento de **D**eus" | ACF |
| Mc 7:11 | "**poderías**" | "**poderias**" | ACF |
| Mt 15:7 | "Isaias" | "Isaías" | acento (Mt 15 não citado em bloco) |

## 2. Afirmação → fonte → status

| Slide | Afirmação | Fonte | Status |
|---|---|---|---|
| s1 | Costumes de igreja podem ser bons e trazer ordem | 6 (tradições locais podem ser mantidas) | ✔ — sem nomear denominação |
| s2 | Mc 7:1-3 (citação); "tradição dos anciãos"; lavagem de copos, jarros, vasos (v.4); pergunta v.5 | 1 | ✔ |
| s2 | Guzik: lavagem cerimonial, não higiene (paráfrase) | 4 | ✔ |
| s4 | Mc 7:6-8; Is 29:13 ("boca e lábios", "mandamentos de homens, aprendidos de cor") | 1 | ✔ |
| s5 | Mc 7:9-13; Êx 20:12; Corbã = oferta dedicada a Deus | 1, 2 | ✔ |
| s5 | Matthew Henry: a prática livrava o filho de sustentar os pais (paráfrase, não citação) | 3 | ✔ |
| s7 | 2Ts 2:15; 1Co 15:3; 1Co 11:2; 2Tm 2:2; Gl 1:14 — tradição no sentido positivo | 1 | ✔ — equilíbrio de neutralidade |
| s8 | Westminster I.10 (literal) | 5 | ✔ |
| s8 | Catecismo §83 (literal, com cortes […]) | 6 | ✔ |
| s8 | Dei Verbum 9 e 10 | 7 | ✔ |
| s8 | Nota de neutralidade: concordam (costume que anula mandamento é errado), divergem (lugar da Tradição apostólica); Mc 7 não deve rotular a tradição de outra igreja; não toma partido; remete ao pastor | 5, 6, 7 | ✔ |
| s10 | At 5:29; fluxo "o costume ajuda ou anula?"; aplicações | 1 | ✔ — "Corbã com outro nome" (serviço que abandona a família) é aplicação, não fato |
| s11 | Resumo = só o que foi dito | — | ✔ |

## 3. Erros pegos nesta auditoria (corrigidos antes de publicar)
- Selo da capa dizia "7 imagens"; o tópico tem 6 → corrigido.
- Guzik tem uma frase de que dar peso igual à tradição e à Escritura é abandonar a autoridade bíblica
  → **não usada** (posição de um lado; quebraria a neutralidade).
- Matthew Henry: o trecho que a busca devolveu era o texto bíblico da KJV, não o comentário dele →
  usado só como paráfrase atribuída, sem aspas.

## 4. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunhos: Gemini (`gemini-2.5-flash`) e Groq (`gpt-oss-120b`). Arquivos
`backend/_conteudo_{conteudo,segunda_opiniao}_topico69.json`. Os dois seguiram a ordem do roteiro e
usaram as fontes certas (Westminster, Catecismo, Dei Verbum), mas **os dois tomaram partido** — o
risco central deste tópico:

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| Gemini | "esses recursos humanos nunca possuem o mesmo peso… A Escritura permanece como o padrão final" + último slide "A Palavra de Deus como Autoridade Final" | conclusão de um lado (protestante) apresentada como do curso |
| Gemini | "teologia ortodoxa" junto com a católica | sem fonte lida no dossiê |
| Gemini | Magistério com "autoridade exclusiva" de interpretar | não está no dossiê (as citações usadas foram DV 9-10 e CIC 83) |
| Gemini | "a tradição dos anciãos passou a ser tratada com o mesmo peso das Escrituras" | afirmação histórica sem fonte no dossiê |
| Groq | "definição técnica": "A autoridade final é sempre o texto bíblico; tudo o que se acrescenta deve ser verificado contra ele" | **toma partido já na definição** |
| ambos | rótulo "Sola Scriptura" | termo fora do dossiê; o tópico usa as palavras de cada documento |

O final mostra as duas posições com as palavras de cada uma e diz explicitamente que Mc 7 não deve
ser usado pra rotular a tradição de outra igreja. Nenhum texto dos rascunhos foi copiado.

## 5. Pedagogia
- Ponte com T66-T68; fecha a aula; ponte pro T70 (cânon).
- Checkpoints: tf, mc, lacuna, mc, associar, tf, classify (4) + **2 abertas** ✔. Reflexão + Resumo ✔.
- Caso que deu errado (Corbã) e caso real (Paulo: de "zeloso das tradições" a "entreguei o que recebi") ✔.

## 6. Continuidade
- Não trata de cânon (T70). Não cita Trento nem "Sola Scriptura" (sem fonte lida, risco de partido).

## 7. Estrutura
- `validar_topico()` vazio; 0 `None` (trigo-maduro); ids únicos; `fluxo` (nenhum `diagrama`); capa ✔.
- Densidade: 5 inline + capa em 8 slides de conteúdo — o diagnóstico calcula 0,62 (abaixo da meta 0,7, aceito com ✓).

## 8. Revisão humana
- `is_approved=true` = só estrutural. Leitura do teólogo e do pastor:
  `curso de obreiro/topico69-palavra-tradicao-completo.html` — **tópico sensível**, vale priorizar a leitura deles.

**Pendências: 0.**

## 9. Imagens
6 geradas. Regeradas: capa (rolo aberto com pseudo-letras em destaque → rolo fechado amarrado) e `t69-familia` (caneca com a palavra "Volunteer" legível → objetos sem nada escrito).
