# backend/app/agents/estrutura_agent.py
"""
Fase 3 — Agente de ESTRUTURA de curso. Decide módulos e tópicos (lições) dentro
de cada módulo, com quantidade variável por assunto e por nível — nunca um número
fixo (o `generate_course_structure` original em specialist_agent.py tinha "3 módulos
com 3 aulas cada" travado no prompt; aqui a quantidade é uma decisão da IA, orientada
por regras de bom senso, não um número deixado a critério dela sem guia nenhum).

Não gera conteúdo nenhum — só o esqueleto (títulos + foco de 1 frase por tópico).
Quem escreve o conteúdo de cada tópico é o ContentAgent (specialists/ia_agent.py ou
o especialista equivalente da área do curso).
"""

from .base_agent import BaseAgent

SCHEMA_ESTRUTURA = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "titulo": "Título do curso",
  "descricao": "1-2 frases sobre o que o curso cobre e pra quem é",
  "nivel": "básico" | "intermediário" | "avançado" | "especialista",
  "modulos": [
    {
      "titulo": "Título do módulo",
      "descricao": "1 frase",
      "licoes": [
        {"titulo": "Título do tópico", "foco": "1 frase: o que especificamente esse tópico precisa ensinar"}
      ]
    }
  ]
}

REGRAS PRA DECIDIR A QUANTIDADE (não existe número fixo certo — decida pelo assunto):
- Nível "básico": módulos maiores, tópicos mais numerosos e mais fatiados (passos menores,
  mais checkpoints implícitos) — o aluno precisa de mais degraus, não menos conteúdo.
- Nível "avançado"/"especialista": menos tópicos, cada um cobrindo mais terreno de uma vez
  — o aluno já tem base, não precisa do mesmo ritmo passo a passo.
- Um assunto naturalmente mais amplo (ex: "programação web completa") precisa de mais
  módulos que um assunto estreito (ex: "um único conceito técnico aplicado a um caso").
- Cada lição deve ser algo que dá pra ensinar de verdade num tópico de ~12-20 slides —
  se o "foco" de uma lição ainda parece grande demais pra isso, quebre em 2 lições.
- Não force nenhuma contagem específica de módulos ou lições — o número certo é
  consequência do assunto e do nível, não uma meta a bater.
""".strip()


class EstruturaAgent(BaseAgent):
    """Gera a estrutura (módulos + tópicos) de um curso, com quantidade variável."""

    async def gerar_estrutura(
        self,
        assunto: str,
        nivel: str,
        objetivo: str = "",
    ) -> dict:
        prompt = f"""
Você é o especialista em desenhar a estrutura pedagógica de um curso — decidir em
quantos módulos e tópicos o conteúdo se organiza, sem nunca gerar o conteúdo em si.

ASSUNTO DO CURSO: {assunto}
NÍVEL: {nivel}
{"OBJETIVO DO ALUNO: " + objetivo if objetivo else ""}

{SCHEMA_ESTRUTURA}
"""
        return await self.run_json_com_retry(prompt)
