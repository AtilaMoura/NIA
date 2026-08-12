"""
Teste do modo "pro": gera o Tópico 6 assunto por assunto (várias chamadas de IA,
uma por assunto) em vez de tudo de uma vez, e confirma que o resultado passa pelo
MESMO pipeline (QuizAgent -> montar_topico -> validate -> render) sem nenhuma
adaptação — só o ContentAgent muda de estratégia.

Rodar de dentro de backend/:  python _test_modo_pro.py
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
   que nunca viu a prateleira de hoje, as 3 fases de treino, representações latentes.
4. Geração de resposta — logits, softmax, sampling, temperatura, top-k/top-p.
5. Alucinação — modelo afirmar algo com confiança sem base real, grounding.
""".strip()


async def main():
    service = GroqService()
    content_agent = ContentAgent(service)
    quiz_agent = QuizAgent(service)

    print("📝 [MODO PRO] Gerando o Tópico 6 assunto por assunto...")
    conteudo = await content_agent.generate_conteudo_pro(
        titulo="Aplicação no agente",
        aula=1,
        numero=6,
        topico_id="aula1-topico6-aplicacao-no-agente",
        nivel="básico",
        contexto_topicos_anteriores=CONTEXTO_ANTERIOR,
        foco="orquestrador, tools obrigatórias pra fatos, memória de cliente, quando usar temperatura baixa vs alta",
        pausa_entre_chamadas_s=3.0,
    )
    n_assuntos = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    print(f"   -> {n_assuntos} assuntos gerados, cada um sua própria chamada de IA:")
    for s in conteudo["slides"]:
        if s["tipo"] == "conteudo":
            marca = f" [checkpoint: {s['checkpoint_apos']['gate_id']}]" if s.get("checkpoint_apos") else ""
            print(f"      · {s['titulo_secao']}{marca}")

    print("❓ QuizAgent lendo o conteúdo (mesmo agente do modo comum)...")
    perguntas = await quiz_agent.generate_perguntas(conteudo)

    print("🔧 Montando o tópico final (mesma função do modo comum)...")
    topico = montar_topico(
        conteudo, perguntas,
        proximo_topico_label="a conclusão da Aula 1 — este foi o último tópico dela",
    )

    saida_json = Path("../docs/schema/topico6-gerado-pro.json")
    saida_json.write_text(json.dumps(topico, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ JSON salvo em {saida_json.resolve()}")

    problemas = validar_topico(topico)
    if problemas:
        print(f"⚠️ {len(problemas)} problema(s):")
        for p in problemas:
            print(f"   - {p}")
    else:
        print("✅ validate.py: nenhum problema estrutural encontrado.")

    html = render_topico(topico, "vidro-fume")
    out = Path("_render_topico6_pro_vidro-fume.html")
    out.write_text(html, encoding="utf-8")
    print(f"✅ Renderizado (mesmo render_topico do modo comum): {out.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
