"""
Teste da Fase 3: gera a estrutura de 3 cursos diferentes (mesmo assunto em 2 níveis,
e um assunto bem diferente) e confere se a quantidade de módulos/tópicos varia de
forma sensata — não trava num número fixo.

Rodar de dentro de backend/:  python _test_estrutura.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService
from app.agents.estrutura_agent import EstruturaAgent

CASOS = [
    {
        "nome": "llm_basico",
        "assunto": "Fundamentos de LLM aplicado a um agente de vendas via WhatsApp para um Garden Center",
        "nivel": "básico",
        "objetivo": "Entender como funciona por dentro pra desenhar um agente de vendas confiável, sem inventar fatos.",
    },
    {
        "nome": "llm_especialista",
        "assunto": "Fundamentos de LLM aplicado a um agente de vendas via WhatsApp para um Garden Center",
        "nivel": "especialista",
        "objetivo": "Revisão de arquitetura pra quem já trabalha com LLMs em produção e vai desenhar o pipeline de grounding.",
    },
    {
        "nome": "marketing_basico",
        "assunto": "Marketing digital para pequenos negócios locais",
        "nivel": "básico",
        "objetivo": "Aprender a divulgar um pequeno negócio local nas redes sociais do zero.",
    },
]


async def main():
    service = GroqService()
    agent = EstruturaAgent(service)

    resultados = []
    for caso in CASOS:
        print(f"\n🏗️  Gerando estrutura: {caso['nome']} (nível: {caso['nivel']})")
        estrutura = await agent.gerar_estrutura(
            assunto=caso["assunto"], nivel=caso["nivel"], objetivo=caso["objetivo"]
        )
        n_modulos = len(estrutura.get("modulos", []))
        n_licoes = sum(len(m.get("licoes", [])) for m in estrutura.get("modulos", []))
        print(f"   -> título: {estrutura.get('titulo')}")
        print(f"   -> {n_modulos} módulo(s), {n_licoes} tópico(s) no total")
        for m in estrutura.get("modulos", []):
            print(f"      · {m['titulo']} ({len(m.get('licoes', []))} tópicos)")

        saida = Path(f"../docs/schema/estrutura-{caso['nome']}.json")
        saida.write_text(json.dumps(estrutura, ensure_ascii=False, indent=2), encoding="utf-8")
        resultados.append((caso["nome"], n_modulos, n_licoes))

    print("\n📊 Resumo comparativo:")
    for nome, nm, nl in resultados:
        print(f"   {nome}: {nm} módulos, {nl} tópicos")


if __name__ == "__main__":
    asyncio.run(main())
