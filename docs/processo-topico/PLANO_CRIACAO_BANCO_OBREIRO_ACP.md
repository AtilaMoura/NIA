# Plano — criar o curso Obreiro ACP no banco (item 4 do TASKS.md) — AGUARDA OK DO ATILA

Base lida: `backend/_criar_grade_ingles_fase1.py` (esqueleto idempotente por API, local/prod) e
`backend/_dividir_curso_obreiro_I_II.py` (cria curso novo, `--dry-run`, backup, `structure`, `referencia_biblica`).
Grade: [GRADE_OBREIRO_ACP.md](GRADE_OBREIRO_ACP.md) (7 módulos · 24 aulas · 87 tópicos).

## O que descobri
- **Não existe "tenant" no modelo `Course`.** O Emaús é só o front: o catálogo é fixo em
  `emaus-web/app/_lib/catalogo.ts` (cada curso aponta para um `courseId`). Então "dentro do Emaús" = criar
  o curso no banco **e** acrescentar uma entrada no catálogo.
- **Tema `trigo-maduro` já é o padrão** (`TEMA_PADRAO` em `caderno_service.py`) e o publicador dos tópicos
  usa `theme_id="trigo-maduro"`. Não há campo de tema no curso: não precisa de nada no banco.
- O curso de Obreiro I é o `8` e o II é o `12`. **Não mexo em nenhum dos dois**: o ACP é um curso novo (id novo).
- `Course` exige: `title`, `level` ∈ {básico, intermediário, avançado, especialista}, `duration_hours > 0`,
  `structure` (JSON). Tem `visibilidade` (`publico`/`privado`) e `status` (`draft`/`published`).
- Módulo e aula começam no índice 1; tópico vazio com `is_approved=false` aparece como "em preparação".

## Passos (nada roda sem o seu OK)
1. **Escrever `backend/_criar_grade_obreiro_acp.py`** com a grade completa (87 títulos + `referencia_biblica`
   de cada tópico, tirada da grade). Mesmo padrão dos outros: idempotente (acha por título/índice antes de
   criar), nada é apagado, `--dry-run`, backup do estado antes, `structure` espelhando a grade.
2. **`--dry-run` no local** → você vê a lista do que seria criado.
3. **Rodar no local** (`master@emaus.local`) e conferir: 1 curso, 7 módulos, 24 aulas, 87 tópicos, ordem certa.
4. **Produção:** o script vai por API (conteúdo nunca sobe por SSH/git). **Quem roda é você** (precisa de
   `NIA_EMAIL`/`NIA_SENHA` da conta Master; não passo credencial pelo chat). Primeiro `--dry-run` em prod.
5. **Catálogo do front:** entrada `obreiro-acp` em `catalogo.ts` (com o `courseId` que o banco devolver) e
   `TITULO_CURTO`. Capa e logo da ACP entram depois (logo limpo ainda pendente). Isso precisa de deploy da VM2,
   que é seu.
6. **Fila (item 5):** colocar os 87 tópicos em `FILA.md`, M1 → M7.

## Decisões que preciso de você
| # | Decisão | Minha recomendação |
|---|---|---|
| A | `visibilidade` do curso | **`privado`**: o curso traz o Estatuto e regras internas (segurança, escala). Só Master e quem tiver matrícula ativa vê. Dá para abrir depois. |
| B | `status` ao criar | **`draft`** até o 1º tópico do M1 ficar pronto; aí publica. Evita curso vazio no ar. |
| C | Nível e carga | `básico` (público que não conhece a Bíblia). Horas: 1 por aula = **24 h** (no Obreiro I/II foi 1 h por aula). |
| D | Título no catálogo | "Obreiro ACP — Servir na Casa da Palavra"; título curto "Obreiro ACP"; tom `latao` (dourado, próximo do logo). |
| E | Prova | Segue o padrão novo (banco de perguntas + sorteio), criada por tópico depois, não neste script. |

## Fora deste plano
Conteúdo dos tópicos, imagens, áudio, prova, tema visual com logo (item 9) e revisão do pastor/Adriano.
