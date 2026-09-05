# backend/app/agents/specialists/ia_agent.py
"""
Fase 2 (revisada) — Agente de CONTEÚDO da área de IA/LLM.

Faz só uma coisa: escreve os slides de ensino (capa + conteúdo) de um tópico,
e marca ONDE checkpoints deveriam entrar e O QUE a avaliação final deveria testar
— sem escrever nenhuma pergunta. Quem escreve pergunta é o QuizAgent (quiz_agent.py),
que lê este JSON pronto antes de perguntar, pra não inventar pergunta desalinhada
com o conteúdo e não se repetir (ver PLANO_IMPLEMENTACAO_ESTUDO_IA.md, Fase 2).
"""

from ..base_agent import BaseAgent
from ..perfis import PerfilDominio, PERFIL_TECH

SCHEMA_CONTEUDO = """
Devolva APENAS um JSON válido (sem markdown, sem ```), neste formato:

{
  "topico_id": "aulaN-topicoM-slug",
  "titulo": "...",
  "aula": N,
  "numero": M,
  "duracao_estimada_min": 12,
  "roteiro": ["item 1 do roadmap", ...],
  "slides": [ ... ],
  "avaliacao_conceitos": [ {"gate_id":"ef1","tipo":"mc","testar":"..."}, ... ]
}

Tipos de slide (campo "tipo") — SÓ ESTES DOIS, sem checkpoint nem avaliação:
- "capa": primeiro slide. Campos: secao="Início", titulo, subtitulo, instrucoes_box:{label,texto}.
- "conteudo": Campos: secao, titulo_secao (ou null), blocos: [Bloco],
  "checkpoint_apos": null OU {"gate_id": "ck1", "tipo": "mc"|"tf"|"classify"|"open",
  "testar": "descrição do que essa pergunta deveria verificar que o aluno entendeu neste ponto"}.
  Use "checkpoint_apos" em pelo menos 2 dos slides de conteúdo (gate_ids ck1, ck2, ck3, ...,
  em ordem, um por slide marcado). VARIE o "tipo" entre os checkpoints — nunca todos "open"
  nem todos do mesmo tipo (o QuizAgent vai escrever a pergunta respeitando esse tipo, não
  escolhe sozinho).

Bloco (dentro de "blocos"), campo "tipo":
- "paragrafo": {texto}
- "box": {variante: "def"|"analogy"|"app"|"error"|"summary"|"instr", label, texto} (ou "itens":[string] pra lista)
- "cols2": {esquerda:{variante,label,texto}, direita:{variante,label,texto}}
- "timeline": {itens:[{numero,cor,titulo,descricao}]} — "cor" é OBRIGATORIAMENTE um hex tipo "#2c7fb8" (nunca nome de cor tipo "azul"/"blue" — vira CSS inválido e a cor some)
- "badges": {itens:[string]}
- "cards": {itens:[{icone,nome,descricao}]}
- "quote": {texto}
- "diagrama": {id, descricao (narrando um FLUXO de pelo menos 3 passos com uma decisão,
  ex: "cliente pergunta X → sistema decide Y → resultado Z" — nunca uma frase única
  decorativa), svg_raw: null}
- "imagem_sugerida": {descricao} — USE RARAMENTE, só quando uma referência visual real
  (mapa, foto histórica, rota, retrato) ajudaria muito mais que texto/diagrama. A maioria
  dos slides NÃO deveria ter isso — não force um bloco desses em todo slide nem em toda
  lição. Não gera imagem nenhuma, só descreve o que seria útil pra alguém buscar depois.
- "vocab": {termo, classe_gramatical, traducao, exemplo_en, exemplo_pt, cuidado} — pra
  palavra/expressão nova de idioma. Use isso em vez de "box" quando o perfil do domínio
  pedir (ver fio_condutor do perfil) — "box" vira parede de texto se usado pra
  vocabulário.
- "fluxo": {passos: [{texto, decisao: bool}]} — sequência de passos desenhada em
  HTML/CSS, sem coordenada nenhuma pra acertar. Prefira isso a "diagrama"/svg_raw quando
  só precisar mostrar uma sequência linear (com no máximo 1 decisão) — svg_raw cru
  escrito por você tende a sair com texto vazando das caixas.

"avaliacao_conceitos": exatamente 5 itens, gate_ids ef1..ef5, cada um com "tipo" (mc, mc,
tf-ou-classify, open, open — a última open sendo integrativa, testando conexão com tópicos
anteriores) e "testar" (o que especificamente essa pergunta deve verificar — 1 frase).

REGRAS:
- Não force um número fixo de slides de conteúdo — o que fizer sentido pro tema (normalmente 6-10).
- IDs de bloco/diagrama únicos. gate_ids (ck1, ck2, ... e ef1..ef5) todos únicos.
- Todo texto em português do Brasil. Slide de definição precisa ter uma analogia (bloco box variante "analogy").
- "duracao_estimada_min" tem que ser realista pra um slide deck de estudo — entre 10 e 20
  (nunca mais que isso, mesmo com vários slides — é tempo de leitura, não de um curso inteiro).
- Pelo menos 1 slide de conteúdo PRECISA ter um bloco "diagrama" — escolha o assunto mais
  "mecanismo" (tem um fluxo/decisão pra mostrar), não o mais abstrato.
""".strip()


class ContentAgent(BaseAgent):
    """Gera só os slides de ensino de um tópico — nenhuma pergunta."""

    async def generate_conteudo(
        self,
        titulo: str,
        aula: int,
        numero: int,
        nivel: str = "básico",
        contexto_topicos_anteriores: str = "",
        foco: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
        texto_biblico_base: str = "",
    ) -> dict:
        prompt = f"""
Você é o especialista de CONTEÚDO (não de perguntas) desta área, escrevendo os slides
de ensino de um tópico pro {perfil.contexto_curso}. Você NÃO escreve nenhuma pergunta
— só marca onde e o que testar.

{perfil.fio_condutor}

{perfil.exemplo_calibracao}

{perfil.exemplo_diagrama}

{"TEXTO BÍBLICO DE REFERÊNCIA (fonte real — toda citação literal TEM que vir exatamente daqui, nunca de memória): " + chr(10) + texto_biblico_base if texto_biblico_base else ""}

NÍVEL DESTE TÓPICO: {nivel}

TÓPICOS JÁ COBERTOS NESTA AULA (referencie pelo menos 2 vezes, tipo "lembra do Tópico X..."):
{contexto_topicos_anteriores or "(nenhum — este é o primeiro tópico da aula)"}

TÓPICO A GERAR AGORA:
- Título: {titulo}
- Aula: {aula}, número do tópico: {numero}
{"- Foco específico OBRIGATÓRIO — cada ponto precisa aparecer nomeado explicitamente em algum bloco: " + foco if foco else ""}

{SCHEMA_CONTEUDO}
"""
        return await self.run_json_com_retry(prompt)

    # =========================================================================
    # MODO "PRO" — gera assunto por assunto (1 chamada de IA por assunto), em vez
    # de escrever o tópico inteiro numa passada só. Mesma lógica que separar
    # Conteúdo de Quiz melhorou a qualidade (Fase 2): unidades menores de geração
    # são mais fáceis de acertar e mais fáceis de regenerar individualmente se
    # saírem fracas. Custo: mais chamadas de IA (mais lento, mais exposto a rate
    # limit) — por isso "comum" (generate_conteudo, 1 chamada) continua existindo
    # como opção padrão; o admin escolhe.
    #
    # Produz exatamente o mesmo formato de saída de generate_conteudo(), então
    # QuizAgent/montar_topico/validate/render não precisam saber qual modo gerou
    # o conteúdo.
    # =========================================================================

    async def gerar_esqueleto_assuntos(
        self,
        titulo: str,
        aula: int,
        numero: int,
        nivel: str = "básico",
        contexto_topicos_anteriores: str = "",
        foco: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> dict:
        """Decide a lista de assuntos do tópico (só títulos + foco, sem conteúdo ainda)."""
        prompt = f"""
Você é o especialista que decide EM QUANTOS ASSUNTOS um tópico de estudo se divide —
sem escrever o conteúdo de nenhum deles ainda (isso vem depois, um assunto de cada vez).
Isso é pro {perfil.contexto_curso}.

{perfil.fio_condutor}

NÍVEL: {nivel}
TÓPICOS JÁ COBERTOS NESTA AULA:
{contexto_topicos_anteriores or "(nenhum — primeiro tópico da aula)"}

TÓPICO: {titulo} (Aula {aula}, número {numero})
{"FOCO OBRIGATÓRIO — cada ponto precisa virar pelo menos 1 assunto: " + foco if foco else ""}

Devolva APENAS um JSON válido:
{{
  "titulo": "...", "subtitulo": "...",
  "duracao_estimada_min": 12,
  "roteiro": ["...", ...],
  "assuntos": [
    {{"titulo": "...", "foco": "1 frase: o que esse assunto especificamente ensina",
      "precisa_diagrama": true|false,
      "checkpoint_apos": null OU {{"gate_id":"ck1","tipo":"mc"|"tf"|"classify"|"open","testar":"..."}}}}
  ],
  "avaliacao_conceitos": [ {{"gate_id":"ef1","tipo":"mc","testar":"..."}}, ... (5 itens, ef1..ef5) ]
}}

REGRAS:
- O primeiro assunto deve obrigatoriamente ser a definição técnica + analogia.
- Marque "checkpoint_apos" em pelo menos 2 assuntos (gate_ids ck1, ck2, ck3... em ordem).
  VARIE o "tipo" entre eles — nunca todos "open", nunca todos do mesmo tipo.
- Marque "precisa_diagrama": true em EXATAMENTE 1 assunto — o mais "mecanismo" (tem um
  fluxo/decisão real pra mostrar, não o mais abstrato). Os outros ficam false.
- "duracao_estimada_min" realista: entre 10 e 20, nunca mais que isso mesmo com vários assuntos.
- Não force um número fixo de assuntos — o que fizer sentido pro tema (normalmente 5-9).
"""
        return await self.run_json_com_retry(prompt)

    async def gerar_assunto(
        self,
        topico_titulo: str,
        assunto_titulo: str,
        assunto_foco: str,
        assuntos_anteriores: str,
        contexto_topicos_anteriores: str = "",
        precisa_diagrama: bool = False,
        perfil: PerfilDominio = PERFIL_TECH,
        texto_biblico_base: str = "",
    ) -> dict:
        """Gera os blocos de conteúdo de UM assunto, vendo o que já foi escrito antes dele
        (nos assuntos anteriores do mesmo tópico) pra manter costura e não repetir."""
        prompt = f"""
Você é o especialista de CONTEÚDO escrevendo só UM assunto dentro do tópico
"{topico_titulo}", do {perfil.contexto_curso}. Não escreva nenhuma pergunta.

{perfil.fio_condutor}

{perfil.exemplo_calibracao}

{"TEXTO BÍBLICO DE REFERÊNCIA (fonte real — toda citação literal TEM que vir exatamente daqui, nunca de memória): " + chr(10) + texto_biblico_base if texto_biblico_base else ""}

TÓPICOS JÁ COBERTOS EM AULAS ANTERIORES:
{contexto_topicos_anteriores or "(nenhum)"}

ASSUNTOS JÁ ESCRITOS NESTE MESMO TÓPICO (não repita nada do que já foi dito aqui,
e conecte com eles se fizer sentido):
{assuntos_anteriores or "(nenhum — este é o primeiro assunto do tópico)"}

ASSUNTO A ESCREVER AGORA: {assunto_titulo}
O QUE ESTE ASSUNTO PRECISA ENSINAR: {assunto_foco}

Devolva APENAS um JSON válido com os blocos deste assunto:
{{
  "secao": "...", "titulo_secao": "...",
  "blocos": [ Bloco, ... ]
}}

Bloco, campo "tipo":
- "paragrafo": {{texto}}
- "box": {{variante: "def"|"analogy"|"app"|"error"|"summary"|"instr", label, texto}} (ou "itens":[string])
- "cols2": {{esquerda:{{variante,label,texto}}, direita:{{variante,label,texto}}}}
- "timeline": {{itens:[{{numero,cor,titulo,descricao}}]}} — "cor" é OBRIGATORIAMENTE um hex tipo "#2c7fb8" (nunca nome de cor tipo "azul"/"blue" — vira CSS inválido e a cor some)
- "badges": {{itens:[string]}}
- "cards": {{itens:[{{icone,nome,descricao}}]}}
- "quote": {{texto}}
- "diagrama": {{id, descricao (FLUXO de 3+ passos com uma decisão, nunca frase única), svg_raw: null}}
- "vocab": {{termo, classe_gramatical, traducao, exemplo_en, exemplo_pt, cuidado}} — use no
  lugar de "box" pra palavra/expressão nova, se o fio_condutor do perfil pedir.
- "fluxo": {{passos: [{{texto, decisao: bool}}]}} — sequência linear em HTML/CSS (sem
  coordenada nenhuma pra acertar); prefira a "diagrama" quando o fluxo for só uma
  sequência de passos com no máximo 1 decisão.
- "imagem_sugerida": {{descricao, alt, legenda}} — SEM "url" (você não gera imagem, só
  descreve o que deveria existir ali; alguém gera depois e preenche "url"). USE RARAMENTE
  — só quando uma referência visual real ajudaria muito mais que texto.
- "audio_video": {{midia_tipo: "youtube"|"audio", legenda}} — SEM "url" pelo mesmo motivo
  (espaço reservado, alguém preenche depois). Só quando fizer sentido de verdade (ex.:
  ouvir a pronúncia de uma expressão, ou trecho de vídeo/música sendo estudado).

{("OBRIGATÓRIO: narre um fluxo real (não decorativo) com pelo menos 3 passos e 1 decisão explícita neste assunto — use o bloco 'fluxo' (preferível, nunca estoura) OU 'diagrama' com svg_raw desenhado à mão." + chr(10) + chr(10) + perfil.exemplo_diagrama) if precisa_diagrama else "Não é obrigatório usar diagrama/fluxo neste assunto."}

Todo texto em português do Brasil.
"""
        return await self.run_json_com_retry(prompt)

    async def generate_conteudo_pro(
        self,
        titulo: str,
        aula: int,
        numero: int,
        topico_id: str,
        nivel: str = "básico",
        contexto_topicos_anteriores: str = "",
        foco: str = "",
        pausa_entre_chamadas_s: float = 2.0,
        perfil: PerfilDominio = PERFIL_TECH,
        texto_biblico_base: str = "",
    ) -> dict:
        import asyncio

        esqueleto = await self.gerar_esqueleto_assuntos(
            titulo, aula, numero, nivel, contexto_topicos_anteriores, foco, perfil=perfil
        )

        slides = [{
            "tipo": "capa", "secao": "Início",
            "titulo": esqueleto["titulo"], "subtitulo": esqueleto["subtitulo"],
            "instrucoes_box": {
                "label": "📋 Como funciona este estudo",
                "texto": (
                    "Use as setas ← → ou os botões embaixo para navegar. Alguns slides "
                    "são checkpoints — pedem uma resposta antes de liberar o próximo."
                ),
            },
        }]

        assuntos_ja_escritos_resumo = []
        for assunto_meta in esqueleto["assuntos"]:
            assunto = await self.gerar_assunto(
                topico_titulo=titulo,
                assunto_titulo=assunto_meta["titulo"],
                assunto_foco=assunto_meta["foco"],
                assuntos_anteriores="\n".join(assuntos_ja_escritos_resumo),
                contexto_topicos_anteriores=contexto_topicos_anteriores,
                precisa_diagrama=bool(assunto_meta.get("precisa_diagrama")),
                perfil=perfil,
                texto_biblico_base=texto_biblico_base,
            )
            slide = {
                "tipo": "conteudo",
                "secao": assunto.get("secao", assunto_meta["titulo"]),
                "titulo_secao": assunto.get("titulo_secao", assunto_meta["titulo"]),
                "blocos": assunto.get("blocos", []),
                "checkpoint_apos": assunto_meta.get("checkpoint_apos"),
            }
            slides.append(slide)
            assuntos_ja_escritos_resumo.append(f"- {assunto_meta['titulo']}: {assunto_meta['foco']}")

            if pausa_entre_chamadas_s:
                await asyncio.sleep(pausa_entre_chamadas_s)

        return {
            "topico_id": topico_id,
            "titulo": esqueleto["titulo"],
            "aula": aula,
            "numero": numero,
            "duracao_estimada_min": esqueleto.get("duracao_estimada_min", 12),
            "roteiro": esqueleto.get("roteiro", []),
            "slides": slides,
            "avaliacao_conceitos": esqueleto.get("avaliacao_conceitos", []),
        }
