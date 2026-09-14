# backend/app/agents/quiz_agent.py
"""
QuizAgent (reescrito) — lê um tópico de CONTEÚDO já pronto (gerado pelo ContentAgent,
ver specialists/ia_agent.py) e escreve as perguntas: uma pra cada "checkpoint_apos"
marcado no conteúdo, e uma pra cada item de "avaliacao_conceitos".

Diferença chave pro QuizAgent antigo: ele via só um texto solto e "chutava" 10 perguntas
sem gabarito estruturado. Este vê o conteúdo real (JSON) e escreve em cima dele — evita
pergunta desalinhada com o que foi ensinado, e como é uma chamada só vendo todas as
perguntas que ele mesmo vai escrever, fica mais fácil não se repetir (ver Fase 2 no
PLANO_IMPLEMENTACAO_ESTUDO_IA.md — o agente único antigo repetia pergunta entre rodadas).
"""

import json

from .base_agent import BaseAgent
from .perfis import PerfilDominio, PERFIL_TECH

SCHEMA_PERGUNTAS = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "checkpoints": {
    "ck1": [ Pergunta, ... ],
    "ck2": [ Pergunta, ... ]
  },
  "avaliacao": {
    "ef1": Pergunta,
    "ef2": Pergunta,
    "ef3": Pergunta,
    "ef4": Pergunta,
    "ef5": Pergunta
  }
}

As chaves de "checkpoints" devem ser exatamente os gate_ids marcados em "checkpoint_apos"
no conteúdo (uma lista de 1 a 2 perguntas cada). As chaves de "avaliacao" devem ser
exatamente ef1..ef5, seguindo o "tipo" e o "testar" de cada item em "avaliacao_conceitos".

REGRA CRÍTICA DE TIPO: cada "checkpoint_apos" no conteúdo já vem com um campo "tipo"
(mc/tf/classify/associar/lacuna/open/ditado) — a pergunta que você escrever pra aquele gate_id TEM que usar
EXATAMENTE esse tipo, não escolha livremente. Isso existe porque, sem essa trava, os
checkpoints tendem a sair todos do mesmo tipo (geralmente todos "open") — já aconteceu
numa geração real (ver Fase 2b no plano) e deixa a avaliação desbalanceada, com mais
digitação pro aluno do que o necessário.

Cada objeto Pergunta é um desses formatos — e TODOS exigem o campo "tipo"
LITERALMENTE ESCRITO DENTRO DO OBJETO (não é só a categoria, é uma chave
de verdade: {"tipo": "mc", "id": ..., ...}). Um objeto Pergunta sem a chave "tipo"
é inválido, mesmo que todos os outros campos estejam certos:
- "tipo":"mc": {tipo, id, enunciado, cenario:null, opcoes:[string,string,string], correta_idx, explicacao}
- "tipo":"tf": {tipo, id, enunciado, cenario:null, correta_bool, explicacao}
- "tipo":"classify": {tipo, id, enunciado, cenario:null, rotulos_opcoes:[{valor,rotulo},{valor,rotulo}], itens:[{id,texto,correta}] (3 a 5 itens), explicacao}
- "tipo":"associar": MESMO formato de "classify" (rotulos_opcoes + itens) — use quando o
  checkpoint pedir "associar" em vez de "classify": aqui "rotulos_opcoes" tende a ter o
  MESMO tamanho de "itens" (pares 1:1 — cada opção usada uma vez), não poucas categorias
  reaproveitadas.
- "tipo":"lacuna": {tipo, id, enunciado, cenario:null, placeholder, respostas_aceitas:
  [string,...] (aceite variações razoáveis, ex: com/sem contração), explicacao}
- "tipo":"open": {tipo, id, enunciado, cenario (string ou null — use pra cenários de checkpoint aplicado), placeholder, explicacao: null}
- "tipo":"ditado": {tipo, id, enunciado ("Ouça a frase e escreva exatamente o que ouviu."),
  cenario:null, frase_audio (a frase em inglês que será falada, NUNCA escrita no enunciado),
  placeholder, respostas_aceitas:[string,...] (com/sem ponto final, com/sem contração),
  explicacao}

REGRA CRÍTICA: nenhum "enunciado" pode se repetir nem ser muito parecido com outro
enunciado em NENHUM outro lugar deste mesmo JSON de saída — releia todas as perguntas
que você mesmo escreveu antes de finalizar e reescreva qualquer uma parecida demais com
outra. Cada pergunta testa um ângulo diferente do "testar"/"checkpoint_apos" pedido.

IDs de pergunta devem seguir o padrão do gate: ck1 com 1 pergunta -> id "ck1_1"; ck2 com
2 perguntas -> "ck2_1","ck2_2"; classify usa itens "ck1_1_1","ck1_1_2",...; avaliação usa
"ef1_1", "ef2_1" etc. Todo texto em português do Brasil.
""".strip()


TRUNCAR_EM = 100  # chars por campo de texto — ver _resumir_blocos_para_quiz


def _truncar(texto: str, limite: int = TRUNCAR_EM) -> str:
    if not isinstance(texto, str) or len(texto) <= limite:
        return texto
    return texto[:limite].rstrip() + "…"


def _resumir_blocos_para_quiz(blocos: list) -> list:
    """Corta o texto de cada bloco pro QuizAgent não estourar o teto de
    tokens/minuto do Groq (achado real, 2026-08-26: um tópico rico — modo
    pro com prosa longa — mandou 14628 tokens numa chamada só contra um
    limite de 8000; ReviewerAgent já cortava svg_raw mas o QuizAgent não
    cortava nada). Mantém o suficiente de cada bloco pra escrever pergunta
    em cima (a primeira frase geralmente carrega a ideia central), sem
    mandar o parágrafo inteiro. Não mexe no conteúdo de verdade (isso é
    só o resumo mandado pra IA escrever pergunta, o slide salvo continua
    com o texto completo)."""
    resumidos = []
    for b in blocos:
        b = dict(b)
        tipo = b.get("tipo")
        if tipo == "diagrama":
            b.pop("svg_raw", None)
            if "descricao" in b:
                b["descricao"] = _truncar(b["descricao"])
        elif "texto" in b:
            b["texto"] = _truncar(b["texto"])
        elif "itens" in b and isinstance(b["itens"], list):
            b["itens"] = [
                {**i, "descricao": _truncar(i["descricao"])} if isinstance(i, dict) and "descricao" in i
                else (_truncar(i) if isinstance(i, str) else i)
                for i in b["itens"]
            ]
        elif tipo == "cols2":
            for lado in ("esquerda", "direita"):
                if lado in b and isinstance(b[lado], dict) and "texto" in b[lado]:
                    b[lado] = {**b[lado], "texto": _truncar(b[lado]["texto"])}
        resumidos.append(b)
    return resumidos


class QuizAgent(BaseAgent):
    """Gera as perguntas de um tópico a partir do conteúdo já escrito."""

    async def generate_perguntas(
        self,
        conteudo: dict,
        max_tokens: int = 2800,
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> dict:
        conteudo_resumido = {
            "titulo": conteudo.get("titulo"),
            "slides": [
                {
                    "secao": s.get("secao"),
                    "titulo_secao": s.get("titulo_secao"),
                    "blocos": _resumir_blocos_para_quiz(s.get("blocos", [])),
                    "checkpoint_apos": s.get("checkpoint_apos"),
                }
                for s in conteudo.get("slides", [])
                if s.get("tipo") == "conteudo"
            ],
            "avaliacao_conceitos": conteudo.get("avaliacao_conceitos", []),
        }

        prompt = f"""
Você é o especialista em avaliação pedagógica do {perfil.contexto_curso}. Abaixo está o
conteúdo JÁ ESCRITO de um tópico de estudo (não é seu trabalho editar o conteúdo, só
escrever perguntas sobre ele).

{perfil.fio_condutor}

A regra acima vale também pra pergunta e gabarito: nunca escreva "correta_idx",
"respostas_aceitas", "frase_audio" ou "explicacao" que contradiga ou invente algo que
o fio condutor proíbe (ex: frase em inglês não-natural, citação bíblica que não vem do
texto fornecido) — mesmo padrão exigido de quem escreveu o conteúdo original.

CONTEÚDO DO TÓPICO:
{json.dumps(conteudo_resumido, ensure_ascii=False, indent=2)}

{SCHEMA_PERGUNTAS}
"""
        # max_tokens baixo por padrão (2800): a resposta esperada aqui é só um
        # punhado de perguntas (não um tópico inteiro), e no Groq isso deixa mais
        # espaço de prompt dentro do teto de 8000/min (ver base_agent.py e achado
        # de 2026-08-26 no histórico do projeto). Esse teto NÃO se aplica ao
        # Gemini (cuja restrição é 20 requisições/dia, não tokens/requisição) —
        # em tópicos ricos com vários itens "classify", 2800 tokens de saída
        # cortam a resposta no meio do JSON; quem chama com GeminiService deve
        # passar um max_tokens maior (achado gerando o Tópico 3, 2026-09-01).
        return await self.run_json_com_retry(prompt, max_tokens=max_tokens)
