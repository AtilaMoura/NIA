# Processo de criação de Tópico — BASE (vale pra todo curso)

Criado em 2026-09-30 juntando o que os 4 cursos com conteúdo real (Obreiro, Inglês,
Redes, IA) já fazem igual. **Cada curso tem sua especificação** nesta mesma pasta, que
diz o que ACRESCENTA ou SUBSTITUI aqui:

| Curso | Course.id | Especificação |
|---|---|---|
| Formação do Obreiro I / II | 8 / 12 | [obreiro.md](obreiro.md) |
| Inglês | 9 | [ingles.md](ingles.md) |
| Redes e Câmeras | 11 | [redes.md](redes.md) |
| Engenharia de Agentes LLM (IA) | 5 | [ia.md](ia.md) |

Regra de leitura: **ler a BASE + a especificação do curso antes de começar qualquer
tópico.** Onde as duas discordarem, vale a especificação.

---

## Passo 0 — Localizar o tópico

- Hierarquia: `Course → Module → Lesson (aula) → Topico`. Conteúdo vai em
  `Topico.content` (JSON no schema de `docs/schema/schema-conteudo-topico.md`).
- Achar o próximo tópico vazio do curso (conteúdo `None`, `is_approved=false`):
  consulta no banco local (`docker exec nia_backend python -c ...`) ou `GET` da árvore.
- Anotar `Topico.id`, `lesson_id` e o título do tópico anterior (pra costura/continuidade).

## Passo 1 — Pesquisa / fonte (específico por curso)

- **Nunca escrever fato verificável de memória** (versículo, porta, data, palavra,
  número). A fonte muda por curso — ver a especificação.
- Guardar a pesquisa (arquivo `_pesquisa*.md`/JSON), não descartar: é a base da
  auditoria do Passo 5.

## Passo 2 — Escrever o conteúdo (quem escreve é específico por curso)

Padrão mínimo de estrutura de todo tópico:

1. **Capa** com `imagem_capa`, `roteiro` e `badges_capa`.
2. Slides de conteúdo divididos por assunto, cada um com uma ideia central.
3. **Checkpoints** espalhados (`checkpoint_apos`), tipos variados — nunca tudo `mc`.
4. **Reflexão** (perguntas abertas, sem gate, ligando com o tópico anterior).
5. **Resumo do Tópico** (bullets) antes da avaliação.
6. Avaliação final: pelo menos 1 `tf`/`classify` e 2 `open`.

Regras de bloco que valem pra todo curso:

- **Nunca `diagrama`/`svg_raw`** pra sequência/mecanismo — usar **`fluxo`** (HTML/CSS,
  nunca estoura). SVG cru vazou texto das caixas em 3 cursos diferentes.
- Imagem inline = bloco `imagem_sugerida` (primeiro sem `url`, com `descricao`;
  a url entra no Passo 6). Slide com **exatamente 1** imagem vira layout em 2 colunas.
- Nada de `None`/campo vazio em `cols2`, `fluxo`, checkpoint.

## Passo 3 — Perguntas

- Se usar `QuizAgent.generate_perguntas()` em cima do conteúdo fechado: **conferir
  sempre** — ele às vezes esquece 1 pergunta (checkpoint com `perguntas: []`) e o Gemini
  tende a deixar tudo `mc`. Com Gemini, passar `max_tokens` maior (~6500).
- Toda pergunta tem que ser respondível com o que foi ENSINADO no tópico.

## Passo 4 — Montar e validar (determinístico)

1. `montar_topico(conteudo, perguntas, proximo_topico_label=...)` quando o conteúdo veio
   separado das perguntas.
2. `app/renderer/validate.py::validar_topico(content)` → lista tem que sair **vazia**.
3. Renderizar (`GET /topicos/{id}/render?theme=<tema>`) e fazer `grep -n "None"` no HTML.
4. Conferir: `imagem_capa` presente, nenhum checkpoint vazio, Reflexão + Resumo existem.

## Passo 5 — Auditoria de conteúdo (contra a pesquisa do Passo 1)

- Toda afirmação verificável bate com a fonte? (checklist próprio na especificação)
- Continuidade com o tópico anterior (não repetir, não contradizer).

## Passo 6 — Imagens

- **Sempre** por `scripts/gerar_imagem_gemini.py` (Gemini web no navegador, perfil
  `~/.nia-playwright-profile`, `python` do sistema — não o venv do backend). **Nunca pela
  API** (cota 0 pra imagem). ~1 min/imagem, grátis.
- Lote: `scripts/imagens_<curso>_<topico>.json` com `descricao` (prompt em inglês =
  base de estilo do curso + cena), `arquivo`, pasta de saída em `imagem/<curso>/...`.
- Densidade alvo (pedido do Atila, "boas mas poucas" + referência dos cursos top):
  **1 capa + ~0,7–1 imagem por slide de conteúdo** (≈5–7 por tópico). Só onde a imagem
  ensina algo — não enfeite.
- Regras comuns: sem texto/letras/números nas imagens internas, sem logo, estilo do
  curso (ver especificação).
- **Catálogo de estilos e temas:** `docs/estilos/catalogo.json` (24 estilos, prompt-base
  de cada um) → página `docs/estilos/catalogo-estilos.html`, publicada como Artifact
  https://claude.ai/artifact/STiLhsFdwS38mojyNiaBYc. As escolhas por curso (estilos,
  estilo principal e tema) ficam no banco do Artifact, coleção `cursos`, doc `c<CourseId>`.
  **Ler de lá** (`ArtifactData list cursos`) antes de gerar imagem. Prompt da imagem =
  `prompt_base` do estilo + cena. Estilo novo: acrescentar no JSON e rodar
  `python docs/estilos/_montar_temas.py && python docs/estilos/_montar_catalogo.py`,
  depois republicar.
- Cena com muitos objetos faz o Gemini escrever placas e rótulos mesmo quando o prompt
  proíbe. Preferir cena simples e conferir cada imagem.
- Converter pra JPEG ~1024px e copiar pra `backend/static/course-images/curso<N>/`.
  **Conferir que TODAS as imagens da rodada foram copiadas** (a capa já ficou pra trás
  uma vez → 404). Script `scripts/aplicar_imagens_<curso>_<topico>.py` troca os
  placeholders pelas URLs.

## Passo 7 — Áudio

- **Já existe pra todo curso, sem fazer nada:** botão "🔊 ouvir este slide" (Web Speech
  API do navegador, pt-BR). Campo opcional `slide.narracao` substitui o texto lido.
- Áudio "de verdade" por bloco (`bloco.audio_url` → botão "🎧 Ouvir explicação") hoje só
  existe no Obreiro — ver [obreiro.md](obreiro.md). Antes de propor gerar/hospedar mídia
  nova, checar se o navegador já resolve (lição do Inglês).

## Passo 8 — Salvar / deploy (só API, nunca SSH/git pra conteúdo)

1. Local: `PUT http://localhost:8100/topicos/{id}` com
   `{content, titulo, is_approved: true, estimated_read_time_minutes}` — **`is_approved`
   no MESMO PUT** (sem isso o aluno vê "em preparação" e não abre).
2. Imagens em produção: `scp` pra `static/course-images/curso<N>/` da VM (é volume).
3. Produção: mesmo PUT em `https://nia-api.duckdns.org` (login admin).
4. Só código de verdade (bloco novo, template, front) precisa de commit + rebuild.

## Passo 9 — Conferência final (checklist)

- [ ] `validar_topico()` vazio e `grep None` sem resultado
- [ ] Capa + imagens carregam (nenhum 404), local e produção
- [ ] Reflexão + Resumo + avaliação com tipos variados
- [ ] Tópico abre no Emaús (`/curso/{courseId}` → tópico), modo Slide e Corrido
- [ ] Memória do curso atualizada (estado + próximo tópico)
- [ ] Scripts `_criar_*`/`_montar_*` do tópico guardados em `backend/` (fora do git)
