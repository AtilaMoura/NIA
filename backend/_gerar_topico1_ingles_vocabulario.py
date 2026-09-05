"""
Gera o conteúdo bruto do NOVO Tópico 1 ("Vocabulário & expressões") da Aula 1 ("My
Way") do curso de Inglês (course_id=9, module_id=33, lesson_id=84) — SUBSTITUI o
antigo Tópico 1 ("História & contexto"), removido da grade a pedido do Atila: o
foco tem que ser 100% em aprender inglês (frases/vocabulário/escuta), não biografia.

Modo "pro" (esqueleto + assunto por assunto), UMA VEZ COM CADA PROVEDOR (Groq, depois
Gemini) — pra comparar na mão antes de montar o híbrido final.

Rodar: docker exec nia_backend python _gerar_topico1_ingles_vocabulario.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService
from app.services.gemini_service import GeminiService
from app.agents.specialists.ia_agent import ContentAgent
from app.agents.perfis import PERFIL_INGLES

FOCO_OBRIGATORIO = """
Grounding real (pesquisa já feita, não invente vocabulário além disso):

ESTRUTURA DA MÚSICA (6 movimentos, paráfrase — a letra em si NUNCA deve ser reproduzida,
nem em inglês nem em português, por causa de copyright; fale SOBRE o movimento, não cite
o verso):
1. Abertura — o fim: anuncia que o fim chegou, encara "a cortina final" (metáfora de
   teatro = a morte/o fim da vida), vai deixar tudo claro, com certeza do que diz.
2. A afirmação — uma vida cheia: viveu uma vida plena, percorreu todos os caminhos, e fez
   do seu jeito.
3. Arrependimentos: teve alguns, mas poucos demais pra mencionar. Fez o que tinha que
   fazer e levou até o fim.
4. Planejamento: traçou cada rota, cada passo cuidadoso pelos caminhos menores.
5. A ponte — os tropeços: houve horas em que "abraçou mais do que dava conta", na dúvida
   encarou, engoliu e seguiu, de cabeça erguida.
6. O fecho — o que é um homem: um homem que não tem a si mesmo não tem nada, precisa
   dizer o que sente de verdade. Que fique registrado que ele levou todos os golpes — do
   seu jeito.

Use um bloco "fluxo" pra mostrar esses 6 movimentos como estrutura da música (não é
história/biografia, é a ORGANIZAÇÃO INTERNA da letra — ajuda a saber o que escutar).

VOCABULÁRIO-ALVO (use o bloco "vocab" pra CADA UM destes, um por vez — não invente
vocabulário além desta lista, e não deixe nenhum de fora):
- the final curtain = o fim (metáfora de teatro). Ex.: "Every performer fears the final
  curtain."
- to state your case = expor seu argumento/posição. Ex.: "Let me state my case before
  you decide."
- certain (of/about) = certo, seguro. Ex.: "I'm certain I locked the door."
- regret = arrependimento; arrepender-se. Ex.: "He regrets selling the house."
- to mention = mencionar, citar. Ex.: "Too small to mention."
- to see it through = levar até o fim. Ex.: "The project was hard, but we saw it
  through."
- exemption = dispensa de uma obrigação. Ex.: "a tax exemption."
- exception = algo fora da regra. Ex.: "Everyone came, without exception."
- to chart a course = traçar uma rota/um plano. Ex.: "She charted a course from intern
  to director."
- byway = estrada secundária. Ex.: "We took the byways to avoid tolls."
- doubt = dúvida. Ex.: "When in doubt, ask."
- to bite off more than you can chew = assumir mais do que dá conta. Ex.: "I bit off
  more than I could chew with two jobs."
- to stand tall = manter-se firme e digno. Ex.: "They lost the vote but stood tall."
- naught (= nothing) = nada (arcaico/poético). Ex.: "All that effort came to naught."
- to kneel = ajoelhar-se; submeter-se. Ex.: "He refused to kneel to the king."
- the blows = os golpes, os baques. Ex.: "life's hard blows."
- let the record show = que fique registrado (formal). Ex.: "Let the record show that I
  disagreed."

NOTA DE HONESTIDADE (inclua em algum ponto): a linha da estrofe 3 aparece em versões como
"without exemption" e "without exception" — ensine as duas palavras, deixando claro que
são parecidas mas diferentes (falso par, não sinônimos).

REGRA DE COPYRIGHT: em nenhum momento cite a letra da música como frase entre aspas
(nem em inglês nem em português) — os exemplos de cada "vocab" são frases SUAS, não
versos. No fim, oriente o aluno a acompanhar a letra oficial no YouTube ou Genius por
conta própria.
""".strip()


async def gerar_com(nome: str, service):
    print(f"\n{'='*60}\n{nome.upper()}\n{'='*60}")
    agent = ContentAgent(service)

    conteudo = await agent.generate_conteudo_pro(
        titulo="Vocabulário & expressões",
        aula=1,
        numero=1,
        topico_id="ingles-modulo1-aula1-topico1-vocabulario",
        nivel="básico",
        contexto_topicos_anteriores="",
        foco=FOCO_OBRIGATORIO,
        pausa_entre_chamadas_s=2.0,
        perfil=PERFIL_INGLES,
    )

    n_assuntos = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    n_checkpoints = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    print(f"-> {n_assuntos} assuntos, {n_checkpoints} checkpoints marcados")

    saida = Path(f"/app/_conteudo_{nome}_ingles_topico1_vocab.json")
    saida.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Salvo em {saida}")
    return conteudo


async def main():
    await gerar_com("groq", GroqService())
    await gerar_com("gemini", GeminiService())
    print("\n✅ Concluído.")


if __name__ == "__main__":
    asyncio.run(main())
