# Auditoria — T68 "Suficiência das Escrituras" (2Pe 1:19-21)

Conteúdo final: `backend/_criar_topico68_obreiro.py` → `_topico68_obreiro_final.json` (16 slides,
7 imagens, 1 fluxo, 5 checkpoints). Dossiê: `topico68-suficiencia.md`. 2026-10-05.

## 1. Citações bíblicas (conferência automática, letra por letra)
**10/10 blocos `quote` ✓ e 18/18 trechos curtos ✓** contra o texto da bible-api normalizado + correções.

Erros da FONTE corrigidos:
| Ref. | Fonte trazia | Corrigido | Conferência |
|---|---|---|---|
| 2Tm 3:15 | "pela que há em Cristo" | "pela **fé** que há em Cristo" | mesmo erro já achado no T66 (ACF) |
| Is 8:20 | "A Lei e ao Testemunho!" | "**À** Lei e ao Testemunho!" | ACF "À lei e ao testemunho!" |

## 2. Afirmação → fonte → status

| Slide | Afirmação | Fonte (dossiê) | Status |
|---|---|---|---|
| s1 | Definição: basta para o que Deus quis revelar sobre salvação, fé e vida; não é manual de tudo | 1, 6, 7 | ✔ |
| s2 | 2Pe 1:19-21 (citação); contexto v.16-18 (monte) | 1 | ✔ |
| s2 | "Mais firme" = comparativo de *bebaios* (estável, firme, seguro) | 2 | ✔ |
| s2 | "Lugar escuro" = *auchmēros* (sombrio; lit. sujo/esquálido), única vez no NT | 3 | ✔ |
| s2 | Guzik: palavra profética mais segura que a experiência de Pedro no monte (paráfrase, atribuída) + nota de tradução ACF | 5, 1 | ✔ — apresentada como leitura dele |
| s2 | Matthew Henry "aplicar a mente… o coração…" (tradução livre) | 4 | ✔ |
| s4 | 2Pe 1:3; 2Tm 3:15, 17; Jo 20:30-31 | 1 | ✔ |
| s5 | Dt 29:29; Dt 4:2; 1Co 4:6; Tg 1:5 | 1 | ✔ |
| s5 | Westminster I.6: "indispensável a iluminação interior do Espírito"; "luz da natureza e prudência cristã, segundo as regras gerais da Palavra" | 6 | ✔ |
| s7 | Lc 16:29-31 (rico e Lázaro) | 1 | ✔ |
| s8 | At 17:11 (bereanos); Gl 1:8; Mt 22:29 | 1, 9, 10 | ✔ |
| s10 | Westminster I.6 (literal) | 6 | ✔ |
| s10 | Artigo VI anglicano (1571) — paráfrase | 7 | ✔ (não citado literal: texto exato não foi lido) |
| s10 | Dei Verbum nº 9 (literal) e nº 10 "não está acima da palavra de Deus, mas sim ao seu serviço" | 8 | ✔ |
| s10 | Nota de neutralidade: Escritura × Tradição (raso, remete ao T69) e profecia/revelação hoje (pentecostais/carismáticos × cessacionistas); não toma partido; remete ao pastor | 6, 8, obreiro.md | ✔ |
| s12 | Is 8:20 (corrigido), Sl 119:105; aplicações práticas | 1 | ✔ |
| s13 | Resumo = só o que foi dito | — | ✔ |

## 3. Rascunhos (Gemini/Groq) — o que NÃO entrou

Rascunho Gemini (`gemini-3.5-flash`, depois de 7 tentativas com 503 em outros modelos da cadeia);
o do Groq (`gpt-oss-120b`) chegou depois da publicação — a versão final foi escrita a partir do
dossiê e não depende dele. Arquivos `backend/_conteudo_{conteudo,segunda_opiniao}_topico68.json`.

| Rascunho | O que trouxe | Por que ficou de fora |
|---|---|---|
| Gemini | Usa Cl 2:8 ("tradição dos homens") pra concluir que "nenhuma… tradição histórica… está acima do texto" | **toma partido** no debate Escritura × Tradição (a Dei Verbum também diz que o magistério está a serviço da Palavra) e invade o T69 |
| Gemini | Rótulo "Sola Scriptura" pra posição protestante, em contraste com a Dei Verbum | termo não está no dossiê; o contraste é feito com as palavras dos próprios documentos |
| Gemini | Parágrafos longos sobre cessacionismo × continuísmo ("um dos temas mais debatidos…") | fora do escopo — o tópico só nomeia a divergência e remete ao Módulo 1 e ao pastor |
| **Groq** | "A Confissão de Westminster (Capítulo III, Seção 1) declara que o Espírito ilumina…" | **referência errada** — a iluminação está no cap. I.6; o cap. III trata dos decretos |
| Groq | Artigos anglicanos "(1563)" | o dossiê traz 1571 (a fonte lida); a data não foi conferida em fonte primária → no final, 1571 conforme a fonte |
| Groq | "alguns anglicanos se alinham à reformada… outros aceitam papel da Tradição similar ao católico" | afirmação sem fonte |
| Groq | linha do tempo com Lutero, Calvino, Concílio de Trento | fora do dossiê (não conferido) e invade o T69 |
| Groq | "nenhuma tradição humana… pode ser colocada acima dela ou ao lado dela" | **toma partido** no debate Escritura × Tradição |
| Groq | "a revelação profética foi concluída com o 'fechamento do cânon'" apresentado como conclusão | toma partido no debate da profecia hoje |
| Gemini | Estrutura (definição → 2Pe 1:19 → alcance → limites → bereanos → tradições → aconselhamento) | ✔ aproveitada como confirmação da ordem — bate com o roteiro do dossiê |

Nenhum texto do rascunho foi copiado.

## 4. Pedagogia
- Abre retomando T66 e T67 (inspirada → confiável → suficiente); fecha com ponte pro T69.
- Separa explicitamente o que suficiência É e NÃO É (evita a leitura ingênua de "manual de tudo").
- Checkpoints: tf, mc, associar, mc com cenário, classify (6 itens) + **2 abertas** (ck5_2, ck5_3) ✔.
- Reflexão "💭 Pra pensar" + Resumo ✔. Caso que deu certo (bereanos) e que deu errado (Gálatas) ✔.

## 5. Continuidade
- Não repete 2Pe 1:20-21 como argumento de inspiração (T66) — só dentro da citação central.
- Mc 7 e a tradição ficam pro T69 (a nota só aponta a divergência).
- Dons/profecia: só nomeia a divergência e remete ao debate do Módulo 1.

## 6. Estrutura
- `validar_topico()` vazio; 0 `None` no render (trigo-maduro); ids únicos; `fluxo` (nenhum `diagrama`);
  capa com `imagem_capa`.

## 7. Revisão humana
- `is_approved=true` = só estrutural. Leitura do professor teólogo e do pastor:
  `curso de obreiro/topico68-suficiencia-completo.html` (não é pré-requisito pra publicar).

**Pendências: 0.**

## 8. Imagens
7 geradas. Regerada: `t68-aconselhamento` — trazia um quadro de Nossa Senhora na parede (puxa pra uma tradição num tópico com nota de neutralidade); prompt com "parede lisa, sem imagens religiosas". `t68-rico-lazaro`: o rolo saiu aberto (pedido fechado) — alt ajustado. Densidade 0,67 (6 inline + capa em 9 slides), aceita pelo diagnóstico.
