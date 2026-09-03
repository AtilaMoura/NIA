# Ilustrações — Estudo "O Caminho de Emaús"

Geradas pelo `scripts/gerar_imagem_gemini.py` (Gemini web, grátis) a partir de
`estudo-emaus/imagens_emaus.json`. Salvas em `imagem/emaus/cenas/v1/`.
Copiar as aprovadas para `backend/static/course-images/` **não** se aplica aqui — este
estudo é servido como Artifact (HTML), as imagens entram embutidas como data URI.

> A API do Gemini **não** gera imagem no tier grátis destas chaves (cota 0). Por isso o
> caminho é o script de navegador (mesmo do curso de obreiro).

## Base de estilo (colada em cada prompt)
Illustrated Bible storybook art, hand-painted **colourful** watercolour and gouache, warm
and tender, loose expressive linework, simplified faces, no photorealism. Landscape of
ancient Judea (dry terraced hills, olive trees, dusty dirt road, stone village houses).
**Personagens consistentes:** older traveller = rust-terracotta robe; younger companion =
olive-green robe; Jesus = deep indigo-blue robe with a very subtle warm glow.
**Nunca:** text/lettering, haloes, modern objects, denominational symbols.

## Cenas (10)
| Arquivo | Seção no HTML | Cena |
|---|---|---|
| 01-capa-estrada.png | hero | 3 caminhantes de costas na estrada ao pôr do sol, Jerusalém ao longe |
| 02-caminhada-triste.png | §2 | os dois cabisbaixos, conversa triste, sem o terceiro |
| 03-cleopas-conta.png | §4 | Cléopas gesticulando, contando; Jesus de costas ouvindo |
| 04-jesus-ensina.png | §5 | Jesus no meio, mão erguida, ensinando; luz mais quente |
| 05-fica-connosco.png | §6 | aldeia ao anoitecer, os dois seguram o braço dele à porta |
| 06-partir-do-pao.png | §7 | à mesa, Jesus parte o pão sob a lamparina, reconhecimento |
| 07-cadeira-vazia.png | §7 | cadeira vazia, pão na mesa, os dois olhando o lugar |
| 08-coracao-ardia.png | §8 | os dois à mesa, inclinados, brilho quente no peito |
| 09-volta-noite.png | §9 | volta a Jerusalém à noite com tocha, cidade iluminada |
| 10-reunidos-jerusalem.png | §9 | sala em Jerusalém, discípulos reunidos ouvindo os dois |

## Status
Ver `_raw/_log_geracao.txt` e `imagem/emaus/cenas/v1/`. Regerar uma cena: apagar o PNG e
rodar `python scripts/gerar_imagem_gemini.py estudo-emaus/imagens_emaus.json` (pula as que
já existem).
