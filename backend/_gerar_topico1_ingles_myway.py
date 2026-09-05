"""
Gera o conteúdo bruto do Tópico 1 ("História & contexto da música") da Aula 1
("My Way") do curso de Inglês (course_id=9, module_id=33, lesson_id=84), em modo
"pro" (esqueleto + assunto por assunto), UMA VEZ COM CADA PROVEDOR (Groq, depois
Gemini) — pra comparar na mão antes de montar o híbrido final (Passo 2 e 3 do
PROCESSO_CRIACAO_TOPICO.md, adaptado do curso de obreiro).

Não chama QuizAgent nem montar_topico ainda — só o conteúdo (Passo 2).

Rodar de dentro do container: docker exec nia_backend python _gerar_topico1_ingles_myway.py
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
- Origem francesa: "Comme d'habitude" (1967-68), música de Jacques Revaux, letra de
  Claude François e Gilles Thibault — canção sobre um relacionamento que acabou
  (François tinha se separado da cantora France Gall), tom melancólico, cotidiano.
- Paul Anka ouviu a melodia num rádio em Paris, em 1968, não gostou da letra francesa
  mas gostou da melodia, e comprou os direitos de adaptação.
- Sinatra tinha dito a Anka que ia se aposentar e queria "uma última música". Anka
  escreveu a letra inglesa para a voz e a vida de Sinatra — um homem no fim, revisando
  a vida e afirmando que a viveu do seu jeito. Letra em inglês não tem nada a ver com o
  tema francês original.
- Frank Sinatra gravou "My Way" em 1969 (single lançado em março de 1969), supostamente
  em uma única tomada. Virou a música-assinatura dele.
- Curiosidades de cultura: uma das músicas mais tocadas em funerais no mundo anglófono;
  virou padrão de karaokê; cover punk de Sid Vicious (1978) inverte o tom; Elvis também
  gravou uma versão.
- Cite as fontes reais no texto (parafraseado, sem citação em bloco longa): Wikipedia
  ("My Way" e "Comme d'habitude"), paulanka.com ("Behind The Song: 'My Way'"),
  Canadian Songwriters Hall of Fame (cshf.ca/song/my-way).
- IMPORTANTE — não reproduza a letra da música em nenhum idioma (copyright de Paul Anka
  / Warner Chappell). Fale SOBRE a história e o contexto, nunca cite a letra. Ao final,
  oriente o aluno a acompanhar a letra oficial no YouTube ou Genius por conta própria.
- Este é o Tópico 1 de 5 da Aula "My Way" (os próximos tópicos, que NÃO fazem parte
  deste, vão cobrir vocabulário/expressões, gramática, pronúncia e um checkpoint de
  compreensão) — este tópico é só história e contexto, não entre em vocabulário/gramática
  aqui.
""".strip()


async def gerar_com(nome: str, service):
    print(f"\n{'='*60}\n{nome.upper()}\n{'='*60}")
    agent = ContentAgent(service)

    conteudo = await agent.generate_conteudo_pro(
        titulo="História & contexto da música",
        aula=1,
        numero=1,
        topico_id="ingles-modulo1-aula1-topico1-historia",
        nivel="básico",
        contexto_topicos_anteriores="",
        foco=FOCO_OBRIGATORIO,
        pausa_entre_chamadas_s=2.0,
        perfil=PERFIL_INGLES,
    )

    n_assuntos = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    n_checkpoints = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    print(f"-> {n_assuntos} assuntos, {n_checkpoints} checkpoints marcados")

    saida = Path(f"/app/_conteudo_{nome}_ingles_topico1.json")
    saida.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Salvo em {saida}")
    return conteudo


async def main():
    await gerar_com("groq", GroqService())
    await gerar_com("gemini", GeminiService())
    print("\n✅ Concluído. backend/./ é bind mount, então os arquivos já aparecem "
          "no host em backend/_conteudo_groq_ingles_topico1.json e "
          "backend/_conteudo_gemini_ingles_topico1.json.")


if __name__ == "__main__":
    asyncio.run(main())
