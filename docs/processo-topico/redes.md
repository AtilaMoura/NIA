# Especificação — Redes e Câmeras (Course 11)

Segue a [BASE](BASE.md). Processo definido em 2026-09-21 depois de o pipeline Groq
reprovar 2× na estrutura e afirmar um **erro técnico real** ("câmera envia UDP pra porta
554") que nada no pipeline pegou.

- **Tema:** `alto-contraste` (claro + escuro; escolhido 2026-10-01 em `TEMA_POR_CURSO`
  do `emaus-web/app/_lib/config.ts`, antes caía no default `trigo-maduro`)
- **Perfil:** `PERFIL_REDES` (`backend/app/agents/perfis.py`) — ⚠️ existe só local,
  nunca commitado (arquivo tinha WIP da feature Avaliação misturado).
- **Âncora de exemplos:** o projeto real — NVR Intelbras em Piazza Fontana
  (`192.168.1.19`), BeNuvem, RTSP/RTMP, MediaMTX.
- **Referência de qualidade:** Tópicos 28, 29, 30 (Módulo 1, Aula "Endereçamento IP").

## Por que é diferente

O Atila está aprendendo o assunto — **não consegue revisar fato técnico**. Então a
verificação por fonte é a única rede de segurança, não a revisão humana.

## Passo 1 — Fonte (obrigatório ANTES de escrever)

0. Dossiê no formato do [FONTES_GUIA.md](FONTES_GUIA.md): além de RFC/doc, buscar livro
   (Kurose & Ross, Tanenbaum, CCNA), caso real e **caso que deu errado** (Mirai, câmera
   exposta sem senha).
1. `estudo-redes-cameras/FONTES.md` primeiro (RFCs, specs ONVIF/W3C/ITU-T, docs
   oficiais Tailscale/AWS/MediaMTX/Backblaze, OWASP, Kurose & Ross — organizado por módulo).
2. Tudo que não estiver lá: `WebSearch`/`WebFetch` em fonte primária (RFC, doc oficial).
3. Toda afirmação verificável — porta, protocolo, faixa de IP, comportamento padrão,
   prática recomendada — tem fonte anotada. Se não achou fonte, não escreve.
4. Fonte nova achada → acrescentar em `FONTES.md` no módulo certo.

## Passo 2 — Escrita

- **Híbrido a partir do dossiê** (BASE, Passo 2; mudou em 2026-10-01 — antes era 100% à
  mão). Groq/Gemini só **organizam** o dossiê; nunca entra afirmação técnica deles que não
  esteja no dossiê. O erro real que motivou o cuidado: Groq escreveu de memória "câmera
  envia UDP pra porta 554" (RTSP usa TCP por padrão). Toda afirmação técnica passa pela
  checagem de alto risco da auditoria.
- **Exemplos variados**, não só o NVR de Piazza Fontana: condomínio, pequena empresa,
  residência, comércio, portaria. O NVR real continua como fio condutor.
- Conectar sempre com a tela real de config de câmera/NVR/roteador (o "pra que serve isso
  no meu projeto").
- Mecanismo/sequência → `fluxo`. Comparações → `cols2`/tabela.
- Achados fora do plano que o aluno PRECISA saber entram (ex.: CGNAT no T29).
- Scripts: `backend/_criar_topicoN_redes.py` → `_topicoN_redes_final.json` (+ `_prod.json`
  com URLs de produção).

## Passo 5 — Auditoria

- [ ] Toda porta/protocolo/faixa/RFC citada confere com a fonte anotada
- [ ] Nenhum "sempre/nunca" técnico sem fonte
- [ ] Exemplo ancorado no equipamento real sem inventar configuração dele

## Passo 6 — Imagens

- Estilos (catálogo visual, 2026-10-01): ★ `isometrico-claro` (principal, paleta
  `#1c2b33` / `#3d9bd1` / `#f2a541`, sem pessoas fotorrealistas, sem pseudo-texto —
  `Course.identidade_visual`), `isometrico-escuro`, `blueprint` (planta de instalação;
  cuidado: o Gemini tende a escrever rótulos em inglês nesse estilo).
- Densidade: ~6-7 por tópico (os T28-30 têm 5-7).
- Lote: `scripts/imagens_redes_topicoN.json`; aplicar: `scripts/aplicar_imagens_redes_topicoN.py`.
- Pasta: `backend/static/course-images/curso11/`.

## Passo 7 — Áudio

- Só o TTS por slide da BASE. Áudio por bloco não existe pra este curso.
