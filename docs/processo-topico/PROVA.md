# Prova do tópico: regras gerais, regras por curso e o comando /criar-provas-topicos

**Status:** APROVADA pelo Atila (2026-10-07). **Código C1–C4 + C6 feitos e testados no local**
(sem deploy): `app/services/prova_service.py` (sorteio, nota, gravar), `app/schemas/avaliacao.py`,
`validar_prova()` em `app/renderer/validate.py`, rotas `GET/PUT /avaliacoes/topico/{topico_id}`
(Master), render e correção usando as perguntas sorteadas. Comando `.claude/commands/criar-provas-topicos.md`
+ script `backend/_publicar_prova.py`. Teste local (tópico 33, prova de teste desativada depois):
validação recusa banco pequeno (422), sem login 401, rodada fixa ao recarregar, rodada 2 com 0
repetidas e todos os assuntos, a correção recalcula o mesmo conjunto, prova antiga (17) abre igual.
**Não testado:** a chamada real da correção por IA (gasta cota do Gemini). Fica pro piloto.
**Deploy feito 2026-10-07** (VM1, `176e786`, backup `~/backups/antes_prova_banco_2026-10-07.sql.gz`). **Falta:** o piloto no T33 NAT na produção.

## 1. Como funciona hoje (verificado no código, 2026-10-07)

| Ponto | Hoje | Onde |
|---|---|---|
| Relação | 1 prova por tópico (`Avaliacao.topico_id` único) | `models.py:762` |
| Conteúdo | `{intro, perguntas[], resultado}`; tipos mc, tf, classify, associar, lacuna, open, ditado | `Avaliacao.conteudo` |
| Quem tem prova | só os **18 tópicos antigos** (prova gerada pelo QuizAgent no pipeline) | produção |
| Quem NÃO tem | os **14 do processo novo**: 66, 67, 68, 69 (Obreiro) · 11, 27 (Inglês) · 21 (IA) · 28, 29, 30, 31, 32, 33 (Redes) · 170 (Vendas) | produção |
| Como cria | só dentro do pipeline antigo; **não existe rota pra criar/editar prova à mão** | `pipeline.py:295` |
| Liberação | só depois de concluir o tópico | `pipeline.py` (gating) |
| Nota | cada pergunta vale 1 (meio acerto 0,5); passa com **60%**, igual pra todo curso | `pipeline.py:728` |
| Correção | IA no fim da prova (cadeia "correcao", Gemini primeiro), que corrige também as abertas | `pipeline.py:745+` |
| Não passou | revisão do que errou + rodada nova | `pipeline.py:730` |
| **Refazer** | só abre rodada nova; **as perguntas são as MESMAS** | `avaliacao_progress.py:219` |
| Tutor de dúvidas | **já fica escondido na prova** | `topico.html.j2:1667` |
| Anotação | **já fica escondida na prova** | `topico.html.j2:1533` |
| Tema | o Emaús já manda o tema do curso pro render da prova (`f2621f5`, `emaus-web/app/topico/[topicoId]/prova/page.tsx`) | ok |

## 2. Regras gerais (valem pra todo curso)

1. **1 prova por tópico** (mantém o modelo atual). Prova de aula/módulo fica pra depois (pergunta 4).
2. **Banco de perguntas maior que a prova.** Cada prova guarda um banco (ex.: 18 a 24 perguntas) e
   cada rodada **sorteia** um conjunto menor (ex.: 6 a 8). Ao refazer, as perguntas mudam, que é o
   pedido do Atila.
   - O sorteio é **equilibrado**: cada assunto do tópico e cada tipo de pergunta aparecem em toda
     rodada, e não sai tudo de um assunto só.
   - O sorteio **evita repetir** as perguntas da rodada anterior sempre que o banco permitir.
   - O sorteio é **fixo por pessoa e rodada**: recarregar a página mostra as mesmas perguntas.
     Ele é calculado a partir de (pessoa, prova, rodada), sem tabela nova no banco.
   - Prova antiga sem banco continua funcionando como hoje (lista fixa).
3. **Só cobra o que foi ensinado.** Nenhuma pergunta usa assunto ou palavra de tópico seguinte. A
   fonte das perguntas é o **conteúdo publicado do tópico + o dossiê** (`fontes/<curso>/…`).
4. **Toda pergunta tem gabarito e explicação**, e a explicação aponta o trecho do tópico.
5. **Auditoria obrigatória**, igual à do tópico: relatório `fontes/<curso>/topico<id>-prova-auditoria.md`
   (pergunta → trecho do tópico/fonte → ok). Sem zero pendências, a prova não publica.
6. **Sem tutor de dúvidas na prova** (já é assim). **Anotação:** hoje fica desligada; **ideia pro
   futuro:** liberar por curso quando o curso permitir.
7. **Correção por IA no fim continua** (é ela que corrige as abertas), sempre com o gabarito na mão.
8. **Nota mínima por curso** (seção 3), guardada na própria prova. Não precisa de coluna nova.
9. **Tema da prova = tema do curso**, igual ao tópico (já é assim).

## 3. Regras por curso (aprovadas 2026-10-07)

| Curso | O que a prova cobra | Tipos de pergunta | Banco / rodada | Nota mínima | Particularidade |
|---|---|---|---|---|---|
| **Inglês (9)** | as 4 habilidades do tópico | ditado (ouvir) · lacuna e associar (vocabulário/gramática) · tf · open "escreva a frase" | 24 / 8 | **70%** | só palavras da **lista fechada** acumulada; ao menos 1 ditado e 1 escrita por rodada; áudio en-US nos ditados |
| **Obreiro I (8)** | compreensão do texto + aplicação no serviço | mc · tf · classify · open "explique com suas palavras" · cenário de igreja | 18 / 6 | **60%** | toda citação conferida no `biblia_service`; ponto controverso só com a nota de neutralidade do tópico (ex.: cânon 66×73) |
| **Redes (11)** | conceito + cenário prático | cenário (câmera, NVR, roteador) · classify · tf de armadilha comum · mc | 18 / 6 | **70%** | porta, protocolo e RFC conferidos; IP de exemplo só de documentação (192.0.2.x etc.) |
| **IA (5)** | conceito + raciocínio + aplicação | mc · tf · ordenar etapas · open aplicado ao agente (Garden Center / portaria) | 18 / 6 | **70%** | número/fórmula conferidos com a apostila/paper do dossiê |
| **Vendas (13)** | decisão de negócio | cenário (escolher modelo, calcular margem) · mc · tf · open | 18 / 6 | **60%** | nada de promessa de ganho; número só com fonte do dossiê; sem nome de pessoa |

## 4. O comando `/criar-provas-topicos <id> [<id>…]`

Arquivo `.claude/commands/criar-provas-topicos.md`, no mesmo espírito do `/criar-topico`:

1. **Ler** o tópico publicado na produção, o dossiê, a regra do curso (seção 3) e esta página.
   Se o tópico não estiver aprovado, **parar**.
2. **Montar o banco** em `backend/_prova_topico<id>.json`, com assunto, tipo, gabarito e explicação
   em cada pergunta. Feito à mão por mim (Claude) a partir do conteúdo; IA só como rascunho, e
   rascunho sempre conferido.
3. **Auditar** (regra 5) e **validar a estrutura** (validador novo, seção 5).
4. **Publicar** na produção pela API (rota nova, seção 5), conferir que a prova abre (render 200)
   e que duas rodadas seguidas sorteiam conjuntos diferentes.
5. Se a prova já existe: **backup** `backend/_backup_prova<id>_<data>.json` antes (nunca apagar).
   As respostas antigas continuam no banco, ligadas à rodada delas.
6. Registrar na `FILA.md` / `REVISOES_PENDENTES.md` + commit local. **Sem push/deploy** (regra do comando).

## 5. O que precisa mudar no código (antes do comando funcionar)

| # | Mudança | Onde |
|---|---|---|
| C1 | Rota de Master pra **criar/atualizar a prova** de um tópico (com schema Pydantic e validação) | router → service → repository de avaliações |
| C2 | **Validador da prova**: tipos, gabarito, explicação, ids únicos, banco ≥ rodada, distribuição possível | `app/renderer/validate.py` |
| C3 | **Sorteio por rodada** (pessoa + prova + rodada → conjunto fixo), usado no render, nas respostas e na correção | service de avaliação |
| C4 | **Nota mínima** lida da prova (com 60% de padrão pras antigas) | `pipeline.py` (correção) |
| C5 | ~~Render da prova com o tema do curso~~: já existia (o Emaús manda o tema) | — |
| C6 | Teste ponta a ponta local: criar banco → fazer rodada 1 → refazer → perguntas mudam → correção com nota do curso | local, depois produção |

Depois do C1–C6, deploy normal (`DEPLOY.md`), com backup do banco antes.

## 6. Ordem de execução proposta

1. Atila aprova este documento e responde as perguntas abaixo.
2. Código C1–C6, local, testado.
3. `/criar-provas-topicos` testado em **1 tópico** (sugestão: **T33 NAT**, Redes, curso público e
   já com conteúdo maduro). Atila faz a prova e aprova.
4. Deploy.
5. As outras 13 provas que faltam, uma por vez, com revisão. Depois disso, o `/criar-topico`
   ganha um passo final: "criar a prova com `/criar-provas-topicos`".

## 7. Decisões do Atila (2026-10-07)

1. **Nota mínima:** como na seção 3 (70% Inglês/Redes/IA, 60% Obreiro/Vendas).
2. **Tamanho:** banco de 18–24, rodada de 6–8. Aprovado.
3. **Refazer:** **liberado na hora**, sem espera e sem limite, por enquanto.
4. **Prova de aula/módulo:** **fica pra depois** (ver seção 8).
5. **As 18 provas antigas:** **refazer no padrão novo** junto com a revisão do tópico. Todo tópico
   que não passou pelo processo novo precisa ser revisado pra ficar 100%, e a prova vai junto.
   Regra registrada no `REVISOES_PENDENTES.md`.

## 8. Anotado pro futuro (não fazer agora)

- **Página de configuração por curso** (Master), pra alterar sem mexer em código: nota mínima,
  regra de refazer (espera, limite de tentativas), anotação liberada ou não na prova, tutor na prova.
  Até ela existir, os valores ficam na própria prova (nota) e no padrão (refazer liberado).
- **Prova de aula e de módulo** (junta vários tópicos). O `PLANO_AVALIACAO_SEPARADA.md` já tinha
  deixado isso fora de escopo.
- **Anotação na prova** liberada por curso (depende da página de configuração).
