"""
Testa o pipeline inteiro (ContentAgent modo Pro -> QuizAgent -> montar_topico ->
validate_topico) SEM chamar nenhuma API de IA — um "service" falso devolve respostas
pré-escritas em sequência, simulando o que um LLM bem-comportado (ou mal-comportado,
no segundo cenário) devolveria.

Serve pra: (1) provar que o código dos 3 ajustes do modo Pro funciona de ponta a ponta
sem depender do limite diário da Groq, e (2) provar que as redes de segurança em código
(validate.py + clamp de duração em montar_topico.py) realmente pegam os 3 problemas
originais se a IA voltar a cometê-los.

Rodar de dentro de backend/:  python _test_mock_pipeline.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.specialists.ia_agent import ContentAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.montar_topico import montar_topico
from app.renderer.validate import validar_topico


class FakeService:
    """Devolve as respostas da lista, uma por chamada, na ordem."""
    def __init__(self, respostas: list[dict]):
        self._respostas = list(respostas)
        self.chamadas = 0

    async def generate_json(self, prompt: str) -> dict:
        self.chamadas += 1
        if not self._respostas:
            raise AssertionError(f"FakeService ficou sem respostas na chamada {self.chamadas}")
        return self._respostas.pop(0)


ESQUELETO_BOM = {
    "titulo": "Aplicação no agente (mock)",
    "subtitulo": "Teste sem API",
    "duracao_estimada_min": 14,
    "roteiro": ["Assunto 1", "Assunto 2", "Assunto 3"],
    "assuntos": [
        {"titulo": "Orquestrador", "foco": "o que faz", "precisa_diagrama": False,
         "checkpoint_apos": {"gate_id": "ck1", "tipo": "mc", "testar": "papel do orquestrador"}},
        {"titulo": "Fluxo de uma pergunta", "foco": "o caminho completo", "precisa_diagrama": True,
         "checkpoint_apos": None},
        {"titulo": "Temperatura no agente", "foco": "quando usar baixa/alta", "precisa_diagrama": False,
         "checkpoint_apos": {"gate_id": "ck2", "tipo": "tf", "testar": "temperatura baixa pra fatos"}},
    ],
    "avaliacao_conceitos": [
        {"gate_id": "ef1", "tipo": "mc", "testar": "orquestrador"},
        {"gate_id": "ef2", "tipo": "open", "testar": "integrativo"},
    ],
}

ASSUNTO_1 = {"secao": "Aplicação", "titulo_secao": "Orquestrador",
             "blocos": [{"tipo": "paragrafo", "texto": "O orquestrador chama o check_stock antes de responder."}]}
ASSUNTO_2_COM_DIAGRAMA = {"secao": "Aplicação", "titulo_secao": "Fluxo de uma pergunta",
             "blocos": [{"tipo": "diagrama", "id": "d1",
                         "descricao": "Cliente pergunta → orquestrador decide → tool responde → LLM formata",
                         "svg_raw": None}]}
ASSUNTO_3 = {"secao": "Aplicação", "titulo_secao": "Temperatura no agente",
             "blocos": [{"tipo": "paragrafo", "texto": "Fatos usam temperatura baixa, criativo usa alta."}]}

PERGUNTAS_BOAS = {
    "checkpoints": {
        "ck1": [{"tipo": "mc", "id": "ck1_1", "enunciado": "Qual o papel do orquestrador?",
                 "cenario": None, "opcoes": ["Gerencia tools", "Nada", "Só estilo"], "correta_idx": 0,
                 "explicacao": "..."}],
        "ck2": [{"tipo": "tf", "id": "ck2_1", "enunciado": "Fatos pedem temperatura baixa.",
                 "cenario": None, "correta_bool": True, "explicacao": "..."}],
    },
    "avaliacao": {
        "ef1": {"tipo": "mc", "id": "ef1_1", "enunciado": "O que o orquestrador faz?", "cenario": None,
                "opcoes": ["Gerencia tools", "Nada", "Só estilo"], "correta_idx": 0, "explicacao": "..."},
        "ef2": {"tipo": "open", "id": "ef2_1", "enunciado": "Conecte tokens e temperatura no agente.",
                "cenario": None, "placeholder": "...", "explicacao": None},
    },
}


async def cenario(nome: str, esqueleto: dict, assuntos: list[dict], perguntas: dict):
    print(f"\n=== Cenário: {nome} ===")
    content_service = FakeService([esqueleto, *assuntos])
    quiz_service = FakeService([perguntas])

    content_agent = ContentAgent(content_service)
    quiz_agent = QuizAgent(quiz_service)

    conteudo = await content_agent.generate_conteudo_pro(
        titulo="Aplicação no agente", aula=1, numero=6,
        topico_id="aula1-topico6-mock", pausa_entre_chamadas_s=0,
    )
    perguntas_geradas = await quiz_agent.generate_perguntas(conteudo)
    topico = montar_topico(conteudo, perguntas_geradas, proximo_topico_label="fim (mock)")

    problemas = validar_topico(topico)
    print(f"duracao_estimada_min final: {topico['duracao_estimada_min']}")
    print(f"badges_capa: {topico['badges_capa']}")
    if problemas:
        print(f"⚠️ {len(problemas)} problema(s):")
        for p in problemas:
            print(f"   - {p}")
    else:
        print("✅ validate.py: nenhum problema encontrado.")
    return topico, problemas


async def main():
    # Cenário 1: IA "bem-comportada" — respeitando os 3 ajustes do prompt.
    await cenario(
        "tudo certo (simula IA respeitando os 3 ajustes)",
        ESQUELETO_BOM, [ASSUNTO_1, ASSUNTO_2_COM_DIAGRAMA, ASSUNTO_3], PERGUNTAS_BOAS,
    )

    # Cenário 2: IA "mal-comportada" de novo — igual às 3 falhas reais que vimos:
    # duração 60min, nenhum diagrama, checkpoint pedia "tf" mas veio "open".
    esqueleto_ruim = {**ESQUELETO_BOM, "duracao_estimada_min": 60}
    assunto_2_sem_diagrama = {"secao": "Aplicação", "titulo_secao": "Fluxo de uma pergunta",
                               "blocos": [{"tipo": "paragrafo", "texto": "Existe um fluxo (sem diagrama)."}]}
    perguntas_ruins = {
        **PERGUNTAS_BOAS,
        "checkpoints": {
            **PERGUNTAS_BOAS["checkpoints"],
            "ck2": [{"tipo": "open", "id": "ck2_1", "enunciado": "Fale sobre temperatura.",
                     "cenario": None, "placeholder": "...", "explicacao": None}],  # devia ser "tf"
        },
    }
    topico_2, problemas_2 = await cenario(
        "IA ignora os 3 ajustes (repete os bugs originais de propósito)",
        esqueleto_ruim, [ASSUNTO_1, assunto_2_sem_diagrama, ASSUNTO_3], perguntas_ruins,
    )
    assert topico_2["duracao_estimada_min"] == 20, "clamp de duração em montar_topico.py deveria ter travado em 20"
    assert topico_tem(problemas_2, "diagrama"), "deveria ter pego a falta de diagrama"
    assert topico_tem(problemas_2, "tipo"), "deveria ter pego o tipo errado no checkpoint"
    print("\n✅ Cenário 2 confirmou: validate.py pega os 3 problemas quando a IA volta a cometê-los.")
    print("   (duração já vem corrigida por montar_topico.py antes mesmo de chegar no validate — por isso não aparece como problema)")


def topico_tem(problemas: list[str], palavra: str) -> bool:
    return any(palavra in p.lower() for p in problemas)


if __name__ == "__main__":
    asyncio.run(main())
