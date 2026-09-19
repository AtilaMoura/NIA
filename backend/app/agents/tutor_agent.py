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

import json

from .base_agent import BaseAgent
from .perfis import PerfilDominio, PERFIL_TECH

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

SCHEMA_CORRECAO = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "correcao_personalizada": "explicação curta (2-4 frases) do erro ESPECÍFICO que o aluno cometeu — não repita a 'explicacao' da pergunta original com as mesmas palavras, use um ângulo ou exemplo diferente, apoiado no que ele de fato respondeu",
  "pergunta_reforco": Pergunta
}

"pergunta_reforco" é um objeto Pergunta NOVO — mesmo "tipo" da pergunta original, mesmo
conceito, mas com enunciado/exemplo DIFERENTE (nunca repita o enunciado original). Um dos
formatos abaixo (o campo "tipo" é obrigatório dentro do objeto):
- "tipo":"mc": {tipo, id, enunciado, cenario:null, opcoes:[string,string,string,string], correta_idx, explicacao}
- "tipo":"tf": {tipo, id, enunciado, cenario:null, correta_bool, explicacao}
- "tipo":"lacuna": {tipo, id, enunciado, cenario:null, placeholder, respostas_aceitas:[string,...] (aceite variações razoáveis), explicacao}
- "tipo":"open": {tipo, id, enunciado, cenario:null, placeholder, explicacao:null}
- "tipo":"ditado": {tipo, id, enunciado ("Ouça a frase e escreva exatamente o que ouviu."), cenario:null, frase_audio (a frase, NUNCA escrita no enunciado), placeholder, respostas_aceitas:[string,...], explicacao}

O "id" da pergunta_reforco deve ser o id da pergunta original com sufixo "_reforco" (ex:
pergunta original "ck3_1" -> pergunta_reforco "ck3_1_reforco").
""".strip()


class TutorAgent(BaseAgent):
    """Avalia o resumo estruturado que um aluno cola ao final de um tópico."""

    async def avaliar_resumo(
        self,
        resumo_texto: str,
        contexto_topico: str = "",
        historico_reforcos: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> dict:
        prompt = f"""
Você é o tutor pedagógico do {perfil.contexto_curso}. Um aluno acabou de terminar um
tópico e colou o resumo estruturado das respostas dele. Avalie como um especialista
faria manualmente — sem puxar saco.

{perfil.fio_condutor}

{"CONTEXTO DO TÓPICO (o que era esperado que o aluno dominasse): " + contexto_topico if contexto_topico else ""}

{"HISTÓRICO DE REFORÇOS ANTERIORES DESTE ALUNO NESTE CURSO (pra notar se um erro já corrigido antes voltou a aparecer — isso é sempre lacuna 'real'): " + historico_reforcos if historico_reforcos else ""}

RESUMO COLADO PELO ALUNO:
{resumo_texto}

{SCHEMA_AVALIACAO}
"""
        return await self.run_json_com_retry(prompt)

    async def corrigir_exercicio(
        self,
        pergunta: dict,
        resposta_dada,
        contexto_topico: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> dict:
        """Tutor ao vivo (2026-09-19) — dispara só quando o aluno ERRA um
        exercício dentro do render (não no fim do tópico, como avaliar_resumo).
        Gera, na MESMA chamada pequena: (1) uma correção personalizada pro erro
        específico (nunca repete o "explicacao" estático com as mesmas
        palavras) e (2) uma pergunta NOVA, mesmo conceito, exemplo diferente,
        pro aluno tentar de novo antes de seguir. Ver [[nia-correcao-ia-
        avaliacoes]] na memória do projeto pro desenho completo — deliberadamente
        por pergunta, nunca o tópico/prova inteiro numa chamada (teto de
        tokens/minuto do Groq + achado de que ele "esquece" item em respostas
        com muitos objetos)."""
        prompt = f"""
Você é o tutor pedagógico do {perfil.contexto_curso}. Um aluno ERROU o exercício abaixo,
dentro do próprio material de estudo (não é avaliação final, é feedback na hora).

{perfil.fio_condutor}

{"CONTEXTO (tópico/aula em que isso está inserido): " + contexto_topico if contexto_topico else ""}

PERGUNTA ORIGINAL (JSON):
{json.dumps(pergunta, ensure_ascii=False, indent=2)}

RESPOSTA QUE O ALUNO DEU:
{json.dumps(resposta_dada, ensure_ascii=False)}

{SCHEMA_CORRECAO}
"""
        return await self.run_json_com_retry(prompt, max_tokens=1500)

    async def responder_duvida(
        self,
        pergunta_aluno: str,
        contexto_slide: str = "",
        contexto_topico: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> str:
        """Tira-dúvida ao vivo (2026-09-19) — o aluno pergunta algo específico
        sobre o ponto em que está (slide/exercício) e recebe resposta em texto
        direto, sem JSON, sem gerar pergunta nova (isso é só do
        corrigir_exercicio). Chamada pequena e separada de propósito — não
        acumula o contexto de outras dúvidas na mesma janela de token."""
        prompt = f"""
Você é o tutor pedagógico do {perfil.contexto_curso}, tirando uma dúvida de um aluno AO
VIVO, no meio do estudo (não é avaliação, é uma pergunta direta dele).

{perfil.fio_condutor}

{"CONTEXTO (tópico/aula): " + contexto_topico if contexto_topico else ""}

{"O QUE ESTÁ NA TELA AGORA (o trecho do material que o aluno está vendo quando perguntou): " + contexto_slide if contexto_slide else ""}

PERGUNTA DO ALUNO:
{pergunta_aluno}

Responda direto, em português, curto (2-4 frases) e específico pro que ele perguntou —
sem repetir o material da tela palavra por palavra, sem "boa pergunta!" nem elogio vazio.
Se a pergunta sair do assunto deste material, diga isso e redirecione pro que está sendo
estudado. Devolva só o texto da resposta, sem markdown, sem JSON.
"""
        return await self.service.generate(prompt, temperature=0.4, max_tokens=500)
