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

Comum a todos: [FONTES_GUIA.md](FONTES_GUIA.md) (o que buscar de fonte e o dossiê).

Regra de leitura: **ler a BASE + a especificação do curso antes de começar qualquer
tópico.** Onde as duas discordarem, vale a especificação.

---

## Passo 0 — Localizar o tópico

- Hierarquia: `Course → Module → Lesson (aula) → Topico`. Conteúdo vai em
  `Topico.content` (JSON no schema de `docs/schema/schema-conteudo-topico.md`).
- Achar o próximo tópico vazio do curso (conteúdo `None`, `is_approved=false`):
  consulta no banco local (`docker exec nia_backend python -c ...`) ou `GET` da árvore.
- Anotar `Topico.id`, `lesson_id` e o título do tópico anterior (pra costura/continuidade).

## Passo 1 — Dossiê de fontes

- Seguir **[FONTES_GUIA.md](FONTES_GUIA.md)**: 8 tipos de fonte (meta: 5+ tipos por
  tópico), hierarquia de confiança, direito autoral, lista de fontes por curso.
- **Nunca escrever fato verificável de memória** (versículo, porta, data, palavra,
  número, nome de paper).
- Entregável: `fontes/<curso>/topicoN-<slug>.md` (modelo no guia). É a matéria-prima do
  Passo 2 e a régua do Passo 5.

## Passo 2 — Escrever o conteúdo (híbrido, a partir do dossiê)

Padrão de todo curso (decidido 2026-10-01): Groq e Gemini geram **separados** a partir do
dossiê ("organize este material"), eu comparo, junto o melhor e completo o que ficou de
fora. Se os dois falharem, escrevo direto do dossiê. Detalhes e exceções por curso na
especificação.

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

## Passo 5 — Auditoria IA (obrigatória pra aprovar)

O Atila cria vários cursos **pra aprender**, então não tem como revisar o conteúdo. **A
validação é minha (Claude)**, formal, com relatório. Sem relatório aprovado, não existe
`is_approved=true`.

Entregável: `fontes/<curso>/topicoN-<slug>-auditoria.md`

| Checagem | Como |
|---|---|
| **Fato** | Cada afirmação verificável do tópico → fonte do dossiê que a sustenta. Sem fonte = corrigir ou remover |
| **Fato de alto risco** | Em Redes e IA (número, porta, comportamento, data), refazer 1 busca independente, não só reler o dossiê |
| **Pedagogia** | Toda pergunta é respondível com o que foi ensinado; ordem do simples ao complexo; exemplo antes de abstração |
| **Direito autoral** | Nenhum bloco longo copiado de material moderno; letra de música nunca |
| **Continuidade** | Não repete nem contradiz o tópico anterior; usa o vocabulário já ensinado |
| **Estrutura** | `validar_topico()` vazio, `grep None` limpo, Reflexão + Resumo, tipos de pergunta variados |
| **Checklist do curso** | O da especificação (ex.: neutralidade doutrinária, exemplo ancorado em caso real) |

Formato do relatório: tabela `afirmação | fonte | status (ok / corrigido / removido)` +
lista do que foi mudado. **Aprovar só com zero pendências.** Revisão humana (Atila,
teólogo, professor) continua bem-vinda quando houver, mas não é pré-requisito.

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
- **Áudio de explicação por bloco, pra todo curso** (2026-10-01, piloto T31: 22 blocos,
  11 min, 5 MB): `backend/_gerar_audio_topico.py <topico_id> <course_id> <etapa>`:
  1. `narracao` — texto de professor por bloco (cadeia "narracao" de `app/services/modelos.py`)
  2. **REVISAR as narrações antes da voz** (`backend/_audio_topico<ID>.json`): no T31, 6 de 22
     tinham erro — número por extenso errado ("443" lido como 434, "NVD 1304" como 304),
     sigla soletrada, link lido caractere por caractere. Corrigir no JSON.
  3. `voz` — ~5 blocos por chamada de TTS (só texto puro: o modelo LÊ qualquer instrução),
     revezando 3 vozes, corte pela transcrição do Whisper. Falha de corte fica guardada em
     `backend/_audio_falhas/`.
  4. `mp3` — comprime (WAV 30 MB → MP3 5 MB) com ffmpeg num container descartável
  5. `aplicar` (local) → `scp` dos `.mp3` pra `~/NIA/backend/static/audio/curso<N>/` da VM1
     → `aplicar prod` (NIA_EMAIL/NIA_SENHA)
- Antes de propor gerar/hospedar mídia nova, checar se o navegador já resolve (lição do Inglês).

## Passo 8 — Salvar / deploy (só API, nunca SSH/git pra conteúdo)

1. Local: `PUT http://localhost:8100/topicos/{id}` com
   `{content, titulo, is_approved: true, estimated_read_time_minutes}` — **`is_approved`
   no MESMO PUT** (sem isso o aluno vê "em preparação" e não abre).
2. Imagens em produção: `scp` pra `static/course-images/curso<N>/` da VM (é volume).
3. Produção: mesmo PUT em `https://nia-api.duckdns.org` (login admin).
4. Só código de verdade (bloco novo, template, front) precisa de commit + rebuild.

## Passo 9 — Conferência final (checklist)

- [ ] Dossiê com 5+ tipos de fonte e relatório de auditoria sem pendências
- [ ] `validar_topico()` vazio e `grep None` sem resultado
- [ ] Capa + imagens carregam (nenhum 404), local e produção
- [ ] Reflexão + Resumo + avaliação com tipos variados
- [ ] Tópico abre no Emaús (`/curso/{courseId}` → tópico), modo Slide e Corrido
- [ ] Memória do curso atualizada (estado + próximo tópico)
- [ ] Scripts `_criar_*`/`_montar_*` do tópico guardados em `backend/` (fora do git)
