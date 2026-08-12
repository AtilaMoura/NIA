# backend/app/agents/specialists/shared.py
"""Trechos de prompt reaproveitados pelo ContentAgent e pelo QuizAgent da área de IA."""

FIO_CONDUTOR_IA = """
Fio condutor pedagógico obrigatório desta área (nunca contradizer):
O LLM é só a camada de linguagem. Fatos de negócio (estoque, preço, memória de cliente,
qualquer dado que precise ser sempre correto) NUNCA devem vir "da memória" do modelo —
sempre de tools/código determinístico (grounding). O modelo é ótimo em linguagem e padrões,
não é uma fonte de verdade sobre fatos do mundo real ou do negócio.
""".strip()

EXEMPLO_DE_PROFUNDIDADE = """
Exemplo real de um bloco "box" já publicado (Tópico 5, Alucinação) — use como calibração
de nível de detalhe e especificidade. Repare que ele nomeia um MECANISMO concreto
(tool check_stock, dado real vs. ausência dele), não fica no nível de "o agente usa IA":

{
  "tipo": "box", "variante": "def", "label": "📘 Definição",
  "texto": "Alucinação é quando o modelo afirma algo com confiança — uma data, um número,
  uma disponibilidade, uma fonte — que é falso ou não tem nenhuma base real, sem sinalizar
  dúvida. Não é o modelo 'mentindo de propósito': é o mecanismo de geração (Tópico 4)
  fazendo exatamente o que ele sempre faz — prever o texto mais plausível — só que sem
  nenhum dado real por trás."
}

PROIBIDO: frases genéricas tipo "o agente usa IA pra entender e responder mensagens do
usuário" repetidas sem nunca dizer QUAL mecanismo, QUAL tool, QUAL decisão específica.
""".strip()
