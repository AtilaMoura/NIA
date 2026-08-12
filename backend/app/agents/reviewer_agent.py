# backend/app/agents/reviewer_agent.py
"""
Fase 5 — ReviewerAgent (reescrito do zero). A versão antiga só pegava um texto solto
e pedia pra IA "deixar mais didático" — não verificava cobertura nem corretude, e não
tinha como reprovar nada (sempre devolvia algo, sem veredito).

Este aqui faz revisão de verdade, em duas camadas:
1. Determinística (validate.py) — grátis, sem IA, roda sempre primeiro. Se achar
   problema estrutural, reprova na hora, sem gastar chamada de IA nenhuma.
2. Semântica (IA) — só roda se a camada 1 passou limpo. Pega o que checagem de
   string não pega: referência errada a tópico anterior, pergunta redundante com
   ideia igual mas palavras diferentes, conteúdo genérico demais, gabarito
   ambíguo ou plausivelmente errado.

Saída no formato que Module.review_score / Module.review_feedback já esperam
(ver models.py) — nada de schema novo no banco.
"""

import json

from .base_agent import BaseAgent
from ..renderer.validate import validar_topico

SCHEMA_REVISAO = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "score": 0-10,
  "aprovado": true|false,
  "pontos_fortes": ["...", ...],
  "problemas": [
    {"gravidade": "bloqueante"|"leve", "onde": "ex: assunto 'Temperatura' ou 'ck2'/'ef3'", "descricao": "..."}
  ]
}

"aprovado" só pode ser true se score >= 7 E não houver nenhum problema "bloqueante".

O QUE VERIFICAR (cada um vira um "problema" se falhar, com o "onde" apontando o local exato):
1. Fio condutor: o conteúdo contradiz em algum momento que o LLM é só camada de linguagem
   e que fatos de negócio vêm sempre de tools/grounding? Isso é BLOQUEANTE se acontecer.
2. Continuidade: toda referência a "Tópico N" ou a um conceito de tópico anterior está
   CORRETA (bate com o resumo de tópicos anteriores fornecido)? Uma referência errada
   (ex: atribuir tokenização ao tópico errado) é BLOQUEANTE — é o modelo alucinando sobre
   o próprio curso.
3. Cobertura do foco: se um foco obrigatório foi pedido, cada ponto dele aparece nomeado
   de verdade em algum bloco (não só citado de passagem)? Falta = BLOQUEANTE.
4. Duplicidade semântica: alguma pergunta pergunta ESSENCIALMENTE A MESMA COISA que outra
   pergunta do mesmo tópico, mesmo com palavras diferentes (não é duplicata literal —
   checagem de string já cobre isso, aqui é sobre IDEIA repetida)? LEVE se for parcial,
   BLOQUEANTE se for a mesma pergunta disfarçada.
5. Genérico demais: algum bloco de conteúdo fica no nível de "o agente usa IA pra
   responder mensagens" sem nomear nenhum mecanismo/tool/decisão concreta? LEVE.
6. Gabarito: alguma pergunta objetiva (mc/tf/classify) tem resposta correta ambígua,
   discutível, ou uma alternativa incorreta que também poderia estar certa? LEVE, a
   menos que a resposta marcada como certa esteja claramente errada (aí é BLOQUEANTE).
""".strip()


class ReviewerAgent(BaseAgent):
    """Revisa um tópico já montado (ver montar_topico.py) — estrutural + semântico."""

    async def revisar_topico(
        self,
        topico: dict,
        contexto_topicos_anteriores: str = "",
        foco_esperado: str = "",
    ) -> dict:
        problemas_estruturais = validar_topico(topico)
        if problemas_estruturais:
            return {
                "score": 0.0,
                "aprovado": False,
                "camada": "estrutural (validate.py, sem IA)",
                "pontos_fortes": [],
                "problemas": [
                    {"gravidade": "bloqueante", "onde": "estrutura", "descricao": p}
                    for p in problemas_estruturais
                ],
            }

        topico_resumido = _resumir_para_revisao(topico)
        prompt = f"""
Você é o revisor pedagógico do tópico abaixo, do curso "LLM aplicado a um agente de
vendas via WhatsApp para um Garden Center". Já passou pelas checagens estruturais —
sua parte é julgamento de conteúdo, não formato.

FIO CONDUTOR DA ÁREA (nunca pode ser contradito): o LLM é só a camada de linguagem;
fatos de negócio sempre vêm de tools/grounding, nunca "da memória" do modelo.

TÓPICOS ANTERIORES (pra checar se as referências no conteúdo batem com isso):
{contexto_topicos_anteriores or "(nenhum — primeiro tópico)"}

{"FOCO QUE ERA OBRIGATÓRIO NESTE TÓPICO: " + foco_esperado if foco_esperado else ""}

TÓPICO A REVISAR:
{json.dumps(topico_resumido, ensure_ascii=False, indent=2)}

{SCHEMA_REVISAO}
"""
        resultado = await self.run_json_com_retry(prompt)
        resultado.setdefault("camada", "semântica (IA)")
        return resultado


def _resumir_para_revisao(topico: dict) -> dict:
    """Remove svg_raw (verboso, irrelevante pro julgamento semântico) pra economizar
    tokens — self.run_json_com_retry já é a segunda linha de defesa contra rate limit,
    mas gastar menos token por chamada ajuda a não bater no teto tão rápido."""
    slides_limpos = []
    for slide in topico.get("slides", []):
        slide_copia = dict(slide)
        if slide_copia.get("tipo") == "conteudo":
            slide_copia["blocos"] = [
                {k: v for k, v in b.items() if k != "svg_raw"} for b in slide_copia.get("blocos", [])
            ]
        slides_limpos.append(slide_copia)
    return {**topico, "slides": slides_limpos}
