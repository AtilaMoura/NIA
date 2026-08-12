"""
Teste da Fase 2 (revisada): ContentAgent + QuizAgent separados, montagem determinística,
validação, e render nos 4 temas. Gera o Tópico 6 (Aplicação no agente) de verdade via IA.

Rodar de dentro de backend/:  python _test_gerar_topico6.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService
from app.agents.specialists.ia_agent import ContentAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.montar_topico import montar_topico
from app.renderer.render import render_topico
from app.renderer.validate import validar_topico

CONTEXTO_ANTERIOR = """
1. O que é um LLM — definição (previsão do próximo token), analogia do "vendedor lido"
   que nunca viu a prateleira de hoje, as 3 fases de treino, representações latentes,
   por que não "pensa" mas parece inteligente.
2. Tokens — o que são, tokenização por sub-palavras, o que vira 1 token vs. vários,
   por que português custa mais tokens que inglês.
3. Context Window — limite de tokens que cabe numa chamada (sistema + histórico +
   contexto + resposta), o que acontece quando estoura, por que janela grande não é
   desculpa pra mandar tudo.
4. Geração de resposta — logits, softmax, sampling, temperatura (baixa = consistente,
   alta = variado), top-k/top-p, e que temperatura não é a mesma coisa que alucinação.
5. Alucinação — modelo afirmar algo com confiança sem base real, o mecanismo (com
   grounding vs. sem grounding), tipos comuns, como mitigar (tool obrigatória pra fatos).
""".strip()


async def main():
    service = GroqService()
    content_agent = ContentAgent(service)
    quiz_agent = QuizAgent(service)

    print("📝 ContentAgent gerando os slides de ensino do Tópico 6...")
    conteudo = await content_agent.generate_conteudo(
        titulo="Aplicação no agente",
        aula=1,
        numero=6,
        nivel="básico",
        contexto_topicos_anteriores=CONTEXTO_ANTERIOR,
        foco=(
            "Juntar tudo (grounding, tokens, janela de contexto, temperatura, "
            "alucinação) numa visão de arquitetura: como o agente de WhatsApp do "
            "Garden Center deveria ser desenhado — orquestrador, tools obrigatórias "
            "pra fatos, memória de cliente, quando usar temperatura baixa vs alta."
        ),
    )
    n_conteudo = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    n_checkpoints_marcados = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    print(f"   -> {n_conteudo} slides de conteúdo, {n_checkpoints_marcados} checkpoints marcados")

    print("❓ QuizAgent lendo o conteúdo e escrevendo as perguntas...")
    perguntas = await quiz_agent.generate_perguntas(conteudo)
    print(f"   -> checkpoints: {list(perguntas.get('checkpoints', {}).keys())}, avaliação: {list(perguntas.get('avaliacao', {}).keys())}")

    print("🔧 Montando o tópico final (código determinístico, sem IA)...")
    topico = montar_topico(
        conteudo, perguntas,
        proximo_topico_label="a conclusão da Aula 1 — este foi o último tópico dela",
    )

    saida_json = Path("../docs/schema/topico6-gerado.json")
    saida_json.write_text(json.dumps(topico, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ JSON salvo em {saida_json.resolve()}")

    problemas = validar_topico(topico)
    if problemas:
        print(f"⚠️ {len(problemas)} problema(s) encontrado(s) pelo validate.py:")
        for p in problemas:
            print(f"   - {p}")
    else:
        print("✅ validate.py: nenhum problema estrutural encontrado.")

    for tema_id in ["vidro-fume", "estufa-noturna", "console-verde", "aurora-botanica"]:
        html = render_topico(topico, tema_id)
        out = Path(f"_render_topico6_{tema_id}.html")
        out.write_text(html, encoding="utf-8")
        print(f"✅ Renderizado: {out.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
