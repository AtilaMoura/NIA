# backend/app/agents/tutor_agent.py
"""
Fase 6 — TutorAgent. Automatiza o que hoje é feito manualmente no chat, no fim de cada
slide deck: o aluno cola o "=== RESUMO ===" (montado por buildSummary() no template, ver
topico.html.j2) e recebe uma avaliação honesta — dominado ou reforço, com motivo
específico — e, quando precisa reforço, uma instrução de COMO reforçar (nunca repetir a
explicação original com as mesmas palavras — ver histórico em Estudo IA/progresso.md,
onde isso já foi feito manualmente várias vezes, ex: Tópico 4 - reforço visual dedicado).

Entrada = o texto cru do resumo (não é JSON estruturado — é literalmente o que o aluno
cola, no formato que o template já gera). Isso poupa o front de ter que parsear o
placar/flags antes de mandar pro agente; a IA lê o texto igual leria no chat.
"""

from .base_agent import BaseAgent
from .specialists.shared import FIO_CONDUTOR_IA

SCHEMA_AVALIACAO = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "veredito": "dominado" | "reforco",
  "resumo_diagnostico": "1-2 frases, direto, sem elogio vazio",
  "pontos_fortes": ["...", ...],
  "lacunas": [
    {"tema": "...", "evidencia": "cite o item exato do resumo (label da pergunta ou trecho da resposta aberta) que mostra o erro", "gravidade": "superficial"|"real"}
  ],
  "reforco_sugerido": {
    "necessario": true|false,
    "foco": "qual conceito específico precisa de reforço (vazio se necessario=false)",
    "instrucao_para_gerar": "o que um material de reforço deve cobrir, USANDO o erro específico do aluno (citado em 'lacunas') como exemplo corrigido. Escreva como uma instrução pra quem for gerar o material, não como o material em si. Vazio se necessario=false."
  }
}

CRITÉRIO DE VEREDITO:
- "dominado" só se não houver nenhuma lacuna de gravidade "real". Erro isolado com
  confiança baixa/média, já reconhecido pelo próprio aluno como dúvida, conta como
  "superficial" — não bloqueia. Erro com confiança ALTA + errou é sempre o sinal mais forte
  de lacuna real (é a "sinalização" que o próprio resumo já destaca).
- "reforco" quando há pelo menos 1 lacuna "real": confusão conceitual repetida (mesmo erro
  aparecendo em mais de um lugar do resumo, ex: no objetivo E na resposta aberta), resposta
  aberta que usa o critério errado, ou taxa de acerto objetiva baixa no tema central do
  tópico.

REGRAS DE TOM (aplicar sempre):
- NUNCA elogie por elogiar. Só entra em "pontos_fortes" o que é evidência real de acerto.
- Seja específico: "errou X" não vale, tem que ser "confundiu X com Y na pergunta Z".
- Se "reforco_sugerido.necessario" for true, "instrucao_para_gerar" NÃO PODE pedir pra
  repetir a explicação original — tem que pedir uma analogia ou ângulo novo, apoiado no
  erro específico do aluno (não um erro genérico inventado).
""".strip()


class TutorAgent(BaseAgent):
    """Avalia o resumo estruturado que um aluno cola ao final de um tópico."""

    async def avaliar_resumo(
        self,
        resumo_texto: str,
        contexto_topico: str = "",
        historico_reforcos: str = "",
    ) -> dict:
        prompt = f"""
Você é o tutor pedagógico do curso "LLM aplicado a um agente de vendas via WhatsApp para
um Garden Center". Um aluno acabou de terminar um tópico e colou o resumo estruturado das
respostas dele. Avalie como um especialista faria manualmente — sem puxar saco.

{FIO_CONDUTOR_IA}

{"CONTEXTO DO TÓPICO (o que era esperado que o aluno dominasse): " + contexto_topico if contexto_topico else ""}

{"HISTÓRICO DE REFORÇOS ANTERIORES DESTE ALUNO NESTE CURSO (pra notar se um erro já corrigido antes voltou a aparecer — isso é sempre lacuna 'real'): " + historico_reforcos if historico_reforcos else ""}

RESUMO COLADO PELO ALUNO:
{resumo_texto}

{SCHEMA_AVALIACAO}
"""
        return await self.run_json_com_retry(prompt)
