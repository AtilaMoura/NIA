"""
Testa o ReviewerAgent (Fase 5) sem chamar API — mesma técnica do _test_mock_pipeline.py.

3 cenários:
1. Tópico com problema ESTRUTURAL (validate.py pega) -> reprova sem nem chamar a IA
   (prova isso com um FakeService que quebra se for chamado).
2. Tópico estruturalmente limpo mas semanticamente fraco (o caso pedido no plano:
   "sem aplicação prática, ou pergunta com gabarito errado") -> IA mockada reprova
   e aponta o problema certo.
3. Tópico bom -> aprova.

Rodar de dentro de backend/:  python _test_reviewer.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.reviewer_agent import ReviewerAgent


class FakeServiceQuebraSeChamado:
    """Simula 'a API nunca deveria ser chamada' — se generate_json rodar, o teste falha."""
    async def generate_json(self, prompt: str) -> dict:
        raise AssertionError("ReviewerAgent chamou a IA mesmo com problema estrutural — não deveria!")


class FakeService:
    def __init__(self, resposta: dict):
        self._resposta = resposta
        self.chamadas = 0

    async def generate_json(self, prompt: str) -> dict:
        self.chamadas += 1
        return self._resposta


TOPICO_QUEBRADO = {
    "topico_id": "t-quebrado", "titulo": "Teste", "aula": 1, "numero": 9,
    "duracao_estimada_min": 12, "roteiro": [], "badges_capa": [],
    "slides": [
        {"tipo": "capa", "secao": "Início", "titulo": "Teste", "subtitulo": "...",
         "instrucoes_box": {"label": "x", "texto": "x"}},
        {"tipo": "checkpoint", "secao": "Checkpoint", "gate_id": "ck1", "titulo_secao": "x",
         "perguntas": []},  # <- sem pergunta nenhuma: validate.py pega isso
        {"tipo": "resultado", "secao": "Resultado", "titulo": "Fim", "proximo_topico_label": "x"},
    ],
}

TOPICO_LIMPO_BASE = {
    "topico_id": "t-limpo", "titulo": "Teste", "aula": 1, "numero": 9,
    "duracao_estimada_min": 14, "roteiro": [], "badges_capa": [],
    "slides": [
        {"tipo": "capa", "secao": "Início", "titulo": "Teste", "subtitulo": "...",
         "instrucoes_box": {"label": "x", "texto": "x"}},
        {"tipo": "conteudo", "secao": "Aplicação", "titulo_secao": "Definição",
         "blocos": [
             {"tipo": "box", "variante": "def", "label": "x", "texto": "..."},
             {"tipo": "diagrama", "id": "d1",
              "descricao": "Cliente pergunta → orquestrador decide → tool responde", "svg_raw": None},
         ]},
        {"tipo": "checkpoint", "secao": "Checkpoint", "gate_id": "ck1", "titulo_secao": "x",
         "perguntas": [{"tipo": "mc", "id": "ck1_1", "enunciado": "Pergunta de teste?",
                        "cenario": None, "opcoes": ["a", "b", "c"], "correta_idx": 0,
                        "explicacao": "..."}]},
        {"tipo": "resultado", "secao": "Resultado", "titulo": "Fim", "proximo_topico_label": "x"},
    ],
}


async def main():
    print("=== Cenário 1: problema estrutural -> reprova sem chamar IA ===")
    reviewer = ReviewerAgent(FakeServiceQuebraSeChamado())
    resultado = await reviewer.revisar_topico(TOPICO_QUEBRADO)
    assert resultado["aprovado"] is False
    assert resultado["camada"].startswith("estrutural")
    print(f"✅ Reprovado na camada '{resultado['camada']}', sem gastar chamada de IA.")
    print(f"   Problemas: {[p['descricao'] for p in resultado['problemas']]}")

    print("\n=== Cenário 2: estruturalmente limpo, mas fraco/gabarito ruim -> IA reprova ===")
    resposta_ia_reprova = {
        "score": 4.5,
        "aprovado": False,
        "pontos_fortes": ["Diagrama descreve um fluxo real"],
        "problemas": [
            {"gravidade": "bloqueante", "onde": "conteudo/Definição",
             "descricao": "Não há nenhum slide de aplicação prática no Garden Center — o tópico fica todo abstrato."},
            {"gravidade": "bloqueante", "onde": "ck1_1",
             "descricao": "A alternativa marcada como correta (índice 0) não é claramente a melhor resposta pro enunciado — gabarito questionável."},
        ],
    }
    reviewer2 = ReviewerAgent(FakeService(resposta_ia_reprova))
    resultado2 = await reviewer2.revisar_topico(
        TOPICO_LIMPO_BASE,
        contexto_topicos_anteriores="1. O que é um LLM...",
        foco_esperado="aplicação prática no Garden Center",
    )
    assert resultado2["aprovado"] is False
    assert resultado2["camada"] == "semântica (IA)"
    assert len(resultado2["problemas"]) == 2
    print(f"✅ Reprovado na camada '{resultado2['camada']}' (score {resultado2['score']}).")
    for p in resultado2["problemas"]:
        print(f"   [{p['gravidade']}] {p['onde']}: {p['descricao']}")

    print("\n=== Cenário 3: tópico bom -> aprova ===")
    resposta_ia_aprova = {
        "score": 8.5, "aprovado": True,
        "pontos_fortes": ["Diagrama concreto", "Boa continuidade"],
        "problemas": [],
    }
    reviewer3 = ReviewerAgent(FakeService(resposta_ia_aprova))
    resultado3 = await reviewer3.revisar_topico(TOPICO_LIMPO_BASE)
    assert resultado3["aprovado"] is True
    print(f"✅ Aprovado, score {resultado3['score']}.")

    print("\n✅ Fase 5 (ReviewerAgent) confirmada: reprova sem IA quando estrutural falha,")
    print("   reprova com detalhe quando a IA aponta problema semântico, aprova quando tá bom.")


if __name__ == "__main__":
    asyncio.run(main())
