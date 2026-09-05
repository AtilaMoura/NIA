"""
Passo 3-6 do processo (adaptado): monta o híbrido do Tópico 1 (Inglês, Aula 1 —
"História & contexto da música") a partir do conteúdo já gerado (Groq e Gemini,
ver _gerar_topico1_ingles_myway.py), decide a base, corrige/ajusta, roda o
QuizAgent e monta o tópico final com montar_topico().

Decisão (comparação manual feita fora deste script, ver conversa):
- Base = GEMINI. Motivos: data de gravação correta (30/dez/1968, Western
  Recorders — Groq errou pra "30 de outubro"), rótulos de seção (`secao`)
  consistentes (Groq variava historia-contexto-musica/historia_contexto/
  historia_contexto_musica — isso aparece na barra superior do render), um
  diagrama SVG real (Groq deixou svg_raw:null, que renderiza a palavra
  "None" no HTML), vocabulário mais rico, e nenhuma citação fabricada.
- Groq violou a regra de não reproduzir a letra (um bloco "quote" citava um
  verso real da música: "And now, the end is near...") e tinha 2 citações
  atribuídas a Anka/Sinatra que não vêm da pesquisa real (parecem
  inventadas) — descartado por completo, não só editado.
- Ajuste no híbrido: Gemini só tinha 2 checkpoints (tf, mc) — adicionado um
  3º checkpoint tipo "classify" (ideia boa que o Groq teve, reescrita do
  zero) no assunto "Frank Sinatra e o Lançamento", que não tinha checkpoint.

Rodar: docker exec nia_backend python _montar_topico1_ingles.py
"""
import asyncio
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService
from app.agents.quiz_agent import QuizAgent
from app.agents.montar_topico import montar_topico


def montar_hibrido() -> dict:
    conteudo = json.loads(Path("/app/_conteudo_gemini_ingles_topico1.json").read_text(encoding="utf-8"))

    # Renumerar o checkpoint existente (assunto "Cultura Global") de ck2 -> ck3,
    # abrindo espaço pro novo ck2 no assunto "Frank Sinatra e o Lançamento".
    for slide in conteudo["slides"]:
        if slide.get("titulo_secao", "").startswith("\"My Way\" na Cultura Global"):
            cp = slide["checkpoint_apos"]
            assert cp["gate_id"] == "ck2"
            cp["gate_id"] = "ck3"

    # Novo checkpoint ck2 (classify) no assunto "Frank Sinatra e o Lançamento"
    # (hoje sem checkpoint_apos).
    for slide in conteudo["slides"]:
        if slide.get("titulo_secao") == "Frank Sinatra e o Lançamento de \"My Way\"":
            slide["checkpoint_apos"] = {
                "gate_id": "ck2",
                "tipo": "classify",
                "testar": (
                    "Classifique cada versão de \"My Way\" pela sua origem: original "
                    "francesa (Comme d'habitude, Claude François), adaptação em inglês "
                    "(Frank Sinatra) ou cover/regravação posterior (outro artista "
                    "cantando a versão em inglês já adaptada)."
                ),
            }
            break

    return conteudo


async def main():
    conteudo = montar_hibrido()

    n_checkpoints_marcados = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    print(f"Híbrido montado: {n_checkpoints_marcados} checkpoints marcados (esperado: 3)")

    quiz_agent = QuizAgent(GroqService())
    perguntas = await quiz_agent.generate_perguntas(conteudo)

    print("Checkpoints gerados:", list(perguntas.get("checkpoints", {}).keys()))
    print("Avaliação gerada:", list(perguntas.get("avaliacao", {}).keys()))

    topico_final = montar_topico(
        conteudo,
        perguntas,
        proximo_topico_label="Vocabulário & expressões de My Way",
    )

    saida = Path("/app/_topico1_ingles_final.json")
    saida.write_text(json.dumps(topico_final, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Tópico final salvo em {saida}")


if __name__ == "__main__":
    asyncio.run(main())
