"""
Testa app/agents/pipeline.py (Fase 7) ponta a ponta — SEM banco e SEM API real —
mesma técnica de todos os testes mockados desta sessão.

Critério do plano: "gerar um curso pequeno do zero (2-3 tópicos, assunto novo) ponta
a ponta ... e completar o ciclo de avaliação sem nenhum passo manual."

O que este teste cobre (o banco/HTTP fica em app/routers/pipeline.py, que só faz
leitura/escrita de dicts prontos — o que precisa de teste é a ORQUESTRAÇÃO, e essa
não depende de Postgres):

1. EstruturaAgent gera um curso pequeno de 1 módulo / 2 tópicos (Fase 3).
2. Tópico 1: ContentAgent (modo comum) -> QuizAgent -> montar_topico -> ReviewerAgent
   aprova (Fase 2+5). Confirma override determinístico de topico_id/aula/numero.
3. Tutor avalia um resumo bom do Tópico 1 -> "dominado" (Fase 6).
4. Tópico 2: mesma cadeia, mas agora com contexto_topicos_anteriores citando o
   Tópico 1 -> confirma que o texto de continuidade realmente chega no prompt.
5. Tutor avalia o resumo do Tópico 2 -> "dominado" -> ciclo completo.
6. Cenário extra: um tópico SEM diagrama -> confirma que o Reviewer reprova na
   camada estrutural e gasta 1 chamada de IA a menos (não chega a revisar
   semanticamente algo que já falhou na estrutura).

Rodar de dentro de backend/:  python _test_pipeline_e2e.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.pipeline import gerar_estrutura_curso, gerar_e_revisar_topico
from app.agents.tutor_agent import TutorAgent


class FakeService:
    """Devolve respostas pré-escritas em ordem; guarda os prompts recebidos."""
    def __init__(self, respostas: list[dict]):
        self._respostas = list(respostas)
        self.prompts = []

    async def generate_json(self, prompt: str) -> dict:
        self.prompts.append(prompt)
        if not self._respostas:
            raise AssertionError(f"FakeService ficou sem respostas na chamada {len(self.prompts)}")
        return self._respostas.pop(0)


ESTRUTURA_MOCK = {
    "titulo": "Aplicação prática do agente (mock)",
    "descricao": "Curso pequeno de teste, 1 módulo, 2 tópicos.",
    "nivel": "básico",
    "modulos": [
        {
            "titulo": "Módulo 1 — Fundamentos aplicados",
            "descricao": "...",
            "licoes": [
                {"titulo": "O orquestrador do agente", "foco": "o que o orquestrador decide antes do LLM responder"},
                {"titulo": "Grounding no checkout", "foco": "por que o preço final nunca pode vir do modelo"},
            ],
        }
    ],
}


def _conteudo(titulo: str, checkpoint2_tipo: str = "tf") -> dict:
    return {
        "topico_id": "placeholder-sera-sobrescrito", "titulo": titulo, "aula": 99, "numero": 99,
        "duracao_estimada_min": 14, "roteiro": ["Definição", "Fluxo", "Aplicação"],
        "slides": [
            {"tipo": "capa", "secao": "Início", "titulo": titulo, "subtitulo": "...",
             "instrucoes_box": {"label": "x", "texto": "x"}},
            {"tipo": "conteudo", "secao": "Aplicação", "titulo_secao": "Definição", "blocos": [
                {"tipo": "box", "variante": "def", "label": "📘 Definição", "texto": "..." * 3},
                {"tipo": "box", "variante": "analogy", "label": "🌱 Analogia", "texto": "..." * 3},
            ], "checkpoint_apos": {"gate_id": "ck1", "tipo": "mc", "testar": "conceito central"}},
            {"tipo": "conteudo", "secao": "Aplicação", "titulo_secao": "Fluxo", "blocos": [
                {"tipo": "diagrama", "id": "d1",
                 "descricao": "Cliente pergunta → orquestrador decide tool → tool retorna dado real → LLM formata resposta",
                 "svg_raw": None},
            ], "checkpoint_apos": {"gate_id": "ck2", "tipo": checkpoint2_tipo, "testar": "ordem tool antes do LLM"}},
        ],
        "avaliacao_conceitos": [
            {"gate_id": "ef1", "tipo": "mc", "testar": "..."},
            {"gate_id": "ef2", "tipo": "mc", "testar": "..."},
            {"gate_id": "ef3", "tipo": "tf", "testar": "..."},
            {"gate_id": "ef4", "tipo": "open", "testar": "..."},
            {"gate_id": "ef5", "tipo": "open", "testar": "integrativo"},
        ],
    }


def _perguntas(prefixo: str, checkpoint2_tipo: str = "tf") -> dict:
    pergunta_ck2 = (
        {"tipo": "tf", "id": "ck2_1", "enunciado": f"[{prefixo}] A tool é chamada antes do LLM formatar a resposta.",
         "cenario": None, "correta_bool": True, "explicacao": "..."}
        if checkpoint2_tipo == "tf" else
        {"tipo": "mc", "id": "ck2_1", "enunciado": f"[{prefixo}] O que acontece antes do LLM formatar a resposta?",
         "cenario": None, "opcoes": ["A tool roda", "Nada", "O CSS carrega"], "correta_idx": 0, "explicacao": "..."}
    )
    return {
        "checkpoints": {
            "ck1": [{"tipo": "mc", "id": "ck1_1", "enunciado": f"[{prefixo}] Qual o papel central deste tópico?",
                     "cenario": None, "opcoes": ["Resposta certa", "Errada 1", "Errada 2"], "correta_idx": 0, "explicacao": "..."}],
            "ck2": [pergunta_ck2],
        },
        "avaliacao": {
            "ef1": {"tipo": "mc", "id": "ef1_1", "enunciado": f"[{prefixo}] Pergunta objetiva 1?", "cenario": None,
                    "opcoes": ["A", "B", "C"], "correta_idx": 0, "explicacao": "..."},
            "ef2": {"tipo": "mc", "id": "ef2_1", "enunciado": f"[{prefixo}] Pergunta objetiva 2?", "cenario": None,
                    "opcoes": ["A", "B", "C"], "correta_idx": 0, "explicacao": "..."},
            "ef3": {"tipo": "tf", "id": "ef3_1", "enunciado": f"[{prefixo}] Afirmação objetiva 3.", "cenario": None,
                    "correta_bool": False, "explicacao": "..."},
            "ef4": {"tipo": "open", "id": "ef4_1", "enunciado": f"[{prefixo}] Pergunta aberta 1?", "cenario": None,
                    "placeholder": "...", "explicacao": None},
            "ef5": {"tipo": "open", "id": "ef5_1", "enunciado": f"[{prefixo}] Pergunta aberta integrativa?", "cenario": None,
                    "placeholder": "...", "explicacao": None},
        },
    }


REVISAO_APROVADA = {"score": 8.5, "aprovado": True, "pontos_fortes": ["Diagrama concreto", "Boa cobertura"], "problemas": []}

RESUMO_BOM = """=== RESUMO — Tópico de teste ===
ck1_1: ACERTOU (confiança: alta)
ck2_1: ACERTOU (confiança: alta)
ef1_1: ACERTOU (confiança: alta)
ef2_1: ACERTOU (confiança: alta)
ef3_1: ACERTOU (confiança: média)
ef4_1 (confiança: alta):
  "Resposta aberta coerente usando o critério certo."
ef5_1 (confiança: média):
  "Conecta com o tópico anterior corretamente."

Pontuação objetiva: 5/5
Sinalizações (alta confiança + errou): nenhuma
Questões abertas registradas: 2/2

Peço avaliação honesta como especialista: devo seguir para o próximo tópico ou preciso de reforço antes?"""

AVALIACAO_DOMINADO = {
    "veredito": "dominado", "resumo_diagnostico": "5/5 objetiva, abertas coerentes.",
    "pontos_fortes": ["Todos os itens corretos com confiança condizente"], "lacunas": [],
    "reforco_sugerido": {"necessario": False, "foco": "", "instrucao_para_gerar": ""},
}


async def main():
    print("=== 1. Fase 3: gerar estrutura do curso (1 módulo, 2 tópicos) ===")
    estrutura = await gerar_estrutura_curso(FakeService([ESTRUTURA_MOCK]), assunto="Agente Garden Center (mock)", nivel="básico")
    modulos = estrutura["modulos"]
    licoes = modulos[0]["licoes"]
    assert len(licoes) == 2
    titulo_t1, foco_t1 = licoes[0]["titulo"], licoes[0]["foco"]
    titulo_t2, foco_t2 = licoes[1]["titulo"], licoes[1]["foco"]
    print(f"✅ Estrutura: {estrutura['titulo']} — {len(licoes)} tópicos: '{titulo_t1}', '{titulo_t2}'")

    print("\n=== 2. Tópico 1: gerar (modo comum) + revisar -> esperado aprovado ===")
    service_t1 = FakeService([_conteudo(titulo_t1), _perguntas("t1"), REVISAO_APROVADA])
    resultado_t1 = await gerar_e_revisar_topico(
        service_t1, titulo=titulo_t1, aula=1, numero=1,
        topico_id="curso-mock-m1-t1", modo="comum", nivel="básico",
        contexto_topicos_anteriores="", foco=foco_t1, proximo_topico_label=titulo_t2,
    )
    assert resultado_t1["revisao"]["aprovado"] is True
    assert resultado_t1["topico"]["topico_id"] == "curso-mock-m1-t1"
    assert resultado_t1["topico"]["aula"] == 1 and resultado_t1["topico"]["numero"] == 1
    assert len(service_t1.prompts) == 3, "esperado 3 chamadas de IA (conteudo, perguntas, revisão semântica)"
    print(f"✅ Tópico 1 aprovado (score {resultado_t1['revisao']['score']}), topico_id/aula/numero sobrescritos corretamente.")

    print("\n=== 3. Aluno estuda Tópico 1 e cola o resumo -> Tutor avalia ===")
    service_tutor1 = FakeService([AVALIACAO_DOMINADO])
    avaliacao_t1 = await TutorAgent(service_tutor1).avaliar_resumo(RESUMO_BOM, contexto_topico=titulo_t1)
    assert avaliacao_t1["veredito"] == "dominado"
    print(f"✅ Tutor: '{avaliacao_t1['veredito']}' -> can_advance liberado pro Tópico 2.")

    print("\n=== 4. Tópico 2: gerar + revisar, agora COM contexto do Tópico 1 ===")
    contexto = f"- Módulo 1, Tópico 1: {titulo_t1}"
    service_t2 = FakeService([_conteudo(titulo_t2), _perguntas("t2"), REVISAO_APROVADA])
    resultado_t2 = await gerar_e_revisar_topico(
        service_t2, titulo=titulo_t2, aula=1, numero=2,
        topico_id="curso-mock-m1-t2", modo="comum", nivel="básico",
        contexto_topicos_anteriores=contexto, foco=foco_t2, proximo_topico_label="conclusão do módulo",
    )
    assert resultado_t2["revisao"]["aprovado"] is True
    assert contexto in service_t2.prompts[0], "contexto do Tópico 1 deveria estar no prompt do ContentAgent"
    assert contexto in service_t2.prompts[2], "contexto do Tópico 1 deveria estar no prompt do Reviewer também"
    print("✅ Tópico 2 aprovado, e o prompt confirma que ele viu o Tópico 1 como contexto de continuidade.")

    print("\n=== 5. Aluno estuda Tópico 2 e cola o resumo -> Tutor avalia -> ciclo completo ===")
    service_tutor2 = FakeService([AVALIACAO_DOMINADO])
    avaliacao_t2 = await TutorAgent(service_tutor2).avaliar_resumo(RESUMO_BOM, contexto_topico=titulo_t2)
    assert avaliacao_t2["veredito"] == "dominado"
    print(f"✅ Tutor: '{avaliacao_t2['veredito']}' -> curso de 2 tópicos completo, sem nenhum passo manual.")

    print("\n=== 6. Cenário extra: tópico SEM diagrama -> Reviewer reprova sem gastar a 3a chamada ===")
    conteudo_sem_diagrama = _conteudo("Tópico sem diagrama (mock)")
    conteudo_sem_diagrama["slides"][2]["blocos"] = [{"tipo": "paragrafo", "texto": "Só texto, sem diagrama."}]
    service_ruim = FakeService([conteudo_sem_diagrama, _perguntas("ruim")])  # só 2 respostas — se pedir a 3a, o teste quebra
    resultado_ruim = await gerar_e_revisar_topico(
        service_ruim, titulo="Tópico sem diagrama (mock)", aula=1, numero=3,
        topico_id="curso-mock-m1-t3", modo="comum",
    )
    assert resultado_ruim["revisao"]["aprovado"] is False
    assert resultado_ruim["revisao"]["camada"].startswith("estrutural")
    assert len(service_ruim.prompts) == 2, "Reviewer não deveria ter chamado a IA — devia reprovar na camada estrutural"
    print(f"✅ Reprovado na camada '{resultado_ruim['revisao']['camada']}', sem gastar a chamada semântica.")
    for p in resultado_ruim["revisao"]["problemas"]:
        print(f"   - {p['descricao']}")

    print("\n✅ Fase 7 (pipeline ponta a ponta) confirmada: estrutura -> conteúdo -> perguntas ->")
    print("   montagem -> revisão -> avaliação do tutor, encadeados sem passo manual, com contexto")
    print("   de continuidade propagado corretamente entre tópicos.")


if __name__ == "__main__":
    asyncio.run(main())
