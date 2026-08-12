"""
Testa o TutorAgent (Fase 6) sem chamar API — mesma técnica das Fases 2b e 5.

Critério de teste do plano: alimentar o agente com um resumo real já avaliado
manualmente (o do Tópico 4, que teve reforço — ver Estudo IA/progresso.md) e comparar
a decisão dele com a que foi tomada manualmente.

O resumo abaixo é uma reconstrução fiel do que está documentado em progresso.md pro
Tópico 4 ANTES do reforço (não tenho o texto colado literal daquela sessão, só o
registro estruturado do que aconteceu): 2 erros de classificação temperatura
baixa/alta com confiança alta, confusão repetida na aberta e num exemplo próprio
fraco ("vaso" vs "oliveira", que na real era sobre o Tópico 2).

Como não há API disponível (quota Groq esgotada), a IA é mockada com a resposta que
uma avaliação honesta DEVERIA dar dado esse resumo — o teste prova que o código do
agente monta o prompt certo e repassa o veredito estruturado sem alterar nada, não
prova que o Groq de fato produz esse raciocínio (isso fica pendente pra quando a
quota resetar, mesma ressalva já registrada na Fase 5).

Rodar de dentro de backend/:  python _test_tutor.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.agents.tutor_agent import TutorAgent

RESUMO_TOPICO4_PRE_REFORCO = """=== RESUMO — Tópico 4: Geração de resposta (logits/temperatura/sampling) ===
Checkpoint 1 - Classificar (confirmar estoque disponível): ERROU (confiança: alta)
Checkpoint 1 - Classificar (variações de descrição de produto): ERROU (confiança: alta)
Checkpoint 2 - V/F sobre logits e distribuição de probabilidade: ACERTOU (confiança: média)
Avaliação Final 1 - Múltipla escolha sobre sampling: ACERTOU (confiança: alta)
Avaliação Final 2 (confiança: média):
  "Temperatura baixa é usada quando a resposta soa mais como um conselho e temperatura alta quando é mais criativa."
Avaliação Final 3 - V/F sobre top-p: ACERTOU (confiança: alta)
Avaliação Final 4 (confiança: baixa):
  "Um exemplo com temperatura baixa seria escolher entre vaso ou oliveira pro cliente, e com temperatura alta seria sugerir uma combinação criativa de plantas."

Pontuação objetiva: 3/5
Sinalizações (alta confiança + errou): Checkpoint 1 - Classificar (confirmar estoque disponível), Checkpoint 1 - Classificar (variações de descrição de produto)
Questões abertas registradas: 2/2

Peço avaliação honesta como especialista: devo seguir para Tópico 5: Alucinação ou preciso de reforço antes?"""

RESUMO_TOPICO4_POS_REFORCO = """=== RESUMO — Tópico 4: Geração de resposta (logits/temperatura/sampling) [reaplicação] ===
Checkpoint 1 - Classificar (confirmar estoque disponível): ACERTOU (confiança: alta)
Checkpoint 1 - Classificar (variações de descrição de produto): ACERTOU (confiança: alta)
Checkpoint 2 - V/F sobre logits e distribuição de probabilidade: ACERTOU (confiança: alta)
Avaliação Final 1 - Múltipla escolha sobre sampling: ACERTOU (confiança: alta)
Avaliação Final 2 (confiança: alta):
  "Temperatura baixa quando existe uma única resposta certa por trás (ex: confirmar se tem Strelitzia em estoque); temperatura alta quando há várias respostas válidas (ex: sugerir uma combinação de plantas pro jardim)."
Avaliação Final 3 - V/F sobre top-p: ACERTOU (confiança: alta)
Avaliação Final 4 (confiança: alta):
  "Confirmar preço = temperatura baixa (existe uma resposta certa, vem do banco). Sugerir nome criativo pra um combo de plantas = temperatura alta (não existe resposta certa única)."

Pontuação objetiva: 5/5
Sinalizações (alta confiança + errou): nenhuma
Questões abertas registradas: 2/2

Peço avaliação honesta como especialista: devo seguir para Tópico 5: Alucinação ou preciso de reforço antes?"""


class FakeService:
    def __init__(self, resposta: dict):
        self._resposta = resposta
        self.ultimo_prompt = None

    async def generate_json(self, prompt: str) -> dict:
        self.ultimo_prompt = prompt
        return self._resposta


async def main():
    print("=== Cenário 1: resumo do Tópico 4 ANTES do reforço -> esperado 'reforco' ===")
    resposta_mock_1 = {
        "veredito": "reforco",
        "resumo_diagnostico": "Confundiu o critério de temperatura (resposta única vs. várias válidas) tanto no objetivo quanto na aberta, e reforçou o erro com um exemplo emprestado do Tópico 2.",
        "pontos_fortes": ["Acertou logits e top-p com confiança condizente"],
        "lacunas": [
            {"tema": "Critério de temperatura baixa vs. alta", "evidencia": "Checkpoint 1 - Classificar (confirmar estoque disponível): ERROU (confiança: alta)", "gravidade": "real"},
            {"tema": "Critério de temperatura baixa vs. alta", "evidencia": "Avaliação Final 2: 'soa mais como um conselho' — critério errado, não é sobre tom", "gravidade": "real"},
        ],
        "reforco_sugerido": {
            "necessario": True,
            "foco": "O critério real é 'existe uma única resposta certa por trás?', não 'soa criativo ou não'.",
            "instrucao_para_gerar": "Gerar fluxograma de decisão usando os próprios erros do aluno (confirmar estoque, variações de descrição) como exemplos corrigidos, mostrando o teste 'tem resposta certa por trás?' — não repetir a explicação original de logits/temperatura com as mesmas palavras.",
        },
    }
    service1 = FakeService(resposta_mock_1)
    tutor1 = TutorAgent(service1)
    resultado1 = await tutor1.avaliar_resumo(
        RESUMO_TOPICO4_PRE_REFORCO,
        contexto_topico="Tópico 4 — geração de resposta via logits/temperatura/sampling, aplicado a quando usar temperatura baixa vs alta no agente do Garden Center.",
    )
    assert resultado1["veredito"] == "reforco"
    assert resultado1["reforco_sugerido"]["necessario"] is True
    assert "temperatura" in service1.ultimo_prompt.lower()
    assert RESUMO_TOPICO4_PRE_REFORCO in service1.ultimo_prompt
    print(f"✅ Veredito: '{resultado1['veredito']}' — bate com a decisão manual registrada em progresso.md.")
    print(f"   Diagnóstico: {resultado1['resumo_diagnostico']}")
    for l in resultado1["lacunas"]:
        print(f"   [lacuna {l['gravidade']}] {l['tema']}: {l['evidencia']}")

    print("\n=== Cenário 2: resumo do Tópico 4 DEPOIS do reforço (reaplicação) -> esperado 'dominado' ===")
    resposta_mock_2 = {
        "veredito": "dominado",
        "resumo_diagnostico": "5/5 objetiva com confiança alta e as duas respostas abertas já usam o critério certo (existência de resposta única).",
        "pontos_fortes": ["Classificação de temperatura correta nos dois itens que antes errou", "Exemplos abertos novos, já com o critério certo, sem repetir os erros anteriores"],
        "lacunas": [],
        "reforco_sugerido": {"necessario": False, "foco": "", "instrucao_para_gerar": ""},
    }
    service2 = FakeService(resposta_mock_2)
    tutor2 = TutorAgent(service2)
    resultado2 = await tutor2.avaliar_resumo(
        RESUMO_TOPICO4_POS_REFORCO,
        historico_reforcos="Tópico 4 já teve 1 reforço anterior sobre confusão de temperatura baixa/alta.",
    )
    assert resultado2["veredito"] == "dominado"
    assert resultado2["lacunas"] == []
    print(f"✅ Veredito: '{resultado2['veredito']}' — bate com 'Liberado como dominado' registrado em progresso.md.")

    print("\n✅ Fase 6 (TutorAgent) confirmada no nível de código: monta o prompt com resumo +")
    print("   contexto + histórico, e repassa o veredito estruturado sem alterar o conteúdo.")
    print("   Raciocínio real da IA sobre o resumo fica pendente de reteste quando a quota resetar.")


if __name__ == "__main__":
    asyncio.run(main())
