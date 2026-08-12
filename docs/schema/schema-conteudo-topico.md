# Schema de conteúdo estruturado — Tópico (Fase 0)

Formato JSON que um agente Specialist deve produzir para descrever um tópico inteiro. O renderizador (Fase 1) transforma isso em HTML interativo; o schema em si **não contém HTML nem CSS** — só conteúdo e estrutura.

Princípio-guia: cada slide é uma sequência de **blocos** reaproveitáveis (o mesmo vocabulário de `.box-*`, `.timeline`, `.cols2`, cards etc. já usado à mão em `Estudo IA/exercicios/`). Isso deixa o schema genérico o bastante pra qualquer assunto, não só LLM.

## Nível raiz

```
{
  "topico_id": string,       // ex: "aula1-topico4-geracao-resposta"
  "titulo": string,
  "aula": number,
  "numero": number,
  "duracao_estimada_min": number,
  "roteiro": [string, ...],  // itens do roadmap na capa
  "badges_capa": [string, ...],
  "slides": [ Slide, ... ]
}
```

## Tipos de Slide

Todo slide tem `id`, `secao` (rótulo mostrado no topo) e `tipo`. Slides de `tipo: "checkpoint"` ou com perguntas na avaliação final carregam `gate_id` — o renderizador bloqueia o botão "Próximo" até todas as perguntas daquele grupo serem respondidas (mesma função `checkGate()` já usada).

### `capa`
Único, sempre o primeiro slide.
```
{ "tipo": "capa", "secao": "Início", "titulo": string, "subtitulo": string,
  "instrucoes_box": { "label": string, "texto": string } }
```
(`roteiro` e `badges_capa` vêm do nível raiz — o renderizador monta a lista/roadmap automaticamente.)

### `conteudo`
Slide genérico de conteúdo — definição, analogia, aplicação, resumo, tudo isso é a mesma estrutura, só muda quais blocos entram.
```
{ "tipo": "conteudo", "secao": string, "titulo_secao": string | null, "blocos": [ Bloco, ... ] }
```

### `checkpoint`
```
{ "tipo": "checkpoint", "secao": "Checkpoint", "gate_id": string,
  "titulo_secao": string, "perguntas": [ Pergunta, ... ] }
```

### `avaliacao_intro`
```
{ "tipo": "avaliacao_intro", "secao": "Avaliação Final", "titulo": string, "subtitulo": string,
  "instrucoes_box": { "label": string, "texto": string } }
```

### `avaliacao_pergunta`
Uma pergunta por slide na avaliação final (mesmo padrão de `Pergunta` do checkpoint, mas 1:1 com o slide e cada uma com seu próprio `gate_id`).
```
{ "tipo": "avaliacao_pergunta", "secao": "Avaliação Final", "gate_id": string, "pergunta": Pergunta }
```

### `resultado`
Único, sempre o último slide. O placar (acertos/total, sinalizações, abertas registradas) e o texto do resumo pra copiar **são calculados pelo renderizador automaticamente**, varrendo todas as perguntas do tópico — não precisa ser descrito aqui.
```
{ "tipo": "resultado", "secao": "Resultado", "titulo": string, "proximo_topico_label": string }
```

## Blocos (usados dentro de `conteudo.blocos`)

| tipo | campos | equivalente em Estudo IA |
|---|---|---|
| `paragrafo` | `texto` | `<p>` |
| `box` | `variante` (`def`\|`analogy`\|`app`\|`error`\|`summary`\|`instr`), `label`, `texto` (prosa) **ou** `itens: [string]` (lista com marcadores — usa um dos dois, não os dois) | `.box-*` |
| `cols2` | `esquerda: {variante,label,texto}`, `direita: {...}` | `.cols2` (antes/depois, ✔/✕) |
| `timeline` | `itens: [{numero,cor,titulo,descricao}]` | `.timeline` (ex: 3 fases de treino) |
| `badges` | `itens: [string]` | `.badge-row` |
| `cards` | `itens: [{icone,nome,descricao}]` | `.type-cards` (ex: tipologia de alucinação) |
| `quote` | `texto` | `.quote-block` |
| `diagrama` | `id`, `descricao` (pro agente/futuro gerador entender a intenção), `svg_raw` (markup já pronto, opcional nesta fase) | `<svg class="diagram">` |

`diagrama.svg_raw` existe porque hoje os diagramas ainda são desenhados à mão (ou por mim). Decisão em aberto pra uma fase futura: substituir por um `diagram_spec` estruturado (nós + arestas + posições) que o renderizador desenha sozinho, sem depender de SVG literal gerado por IA (isso tende a sair com coordenadas ruins se pedido cru pra um LLM). Por ora, a Fase 2 deve gerar `descricao` sempre, e `svg_raw` só quando disponível.

## Pergunta

```
{
  "id": string,
  "tipo": "mc" | "tf" | "classify" | "open",
  "enunciado": string,
  "cenario": string | null,       // caixa itálica de contexto, ex: diálogo cliente/agente

  // tipo == "mc"
  "opcoes": [string, ...],
  "correta_idx": number,

  // tipo == "tf"
  "correta_bool": boolean,

  // tipo == "classify"
  "rotulos_opcoes": [ {"valor": string, "rotulo": string}, {"valor": string, "rotulo": string} ],
     // ex: [{"valor":"baixa","rotulo":"Temperatura baixa"},{"valor":"alta","rotulo":"Temperatura alta"}]
  "itens": [ {"id": string, "texto": string, "correta": string} ],  // "correta" usa um dos "valor" acima

  // tipo == "open"
  "placeholder": string,

  // comum a mc/tf/classify (correção objetiva)
  "explicacao": string
}
```

## Exemplo completo

Ver `schema-conteudo-topico.example.json` — o Tópico 4 (Geração de resposta) inteiro, convertido pra este schema. Validado: 19 slides, nenhum perdido, os 8 gates (`ck1`, `ck2`, `ck3`, `ef1`-`ef5`) preservados, os 2 diagramas mantidos com `svg_raw` original.

## Checagem de genericidade contra o Tópico 5 (Alucinação)

Conferido item a item se o schema também descreveria o Tópico 5 sem alterações:
- 3 diagramas grandes → bloco `diagrama`, ok.
- Cards de tipologia (5 tipos de alucinação) → bloco `cards`, ok.
- Antes/depois (resposta arriscada vs. correta) → bloco `cols2`, ok.
- Checkpoints com MC/TF/classify/aberta → mesmos 4 tipos de `Pergunta`, ok.

**Gap encontrado**: o reforço visual (`aula1-topico4-reforco-visual.html`) usa um "mini-check" — pergunta rápida, sem gate, com feedback instantâneo, fora do fluxo de avaliação. Esse padrão ainda não tem lugar no schema (hoje só existe `checkpoint`, que sempre bloqueia). Decisão adiada pra quando a Fase 2 precisar gerar conteúdo de reforço — não bloqueia a Fase 0, mas fica registrado aqui pra não esquecer.
