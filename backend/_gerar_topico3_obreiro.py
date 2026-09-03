"""
Gera o conteúdo bruto do Tópico 3 ("Vocação e Ofícios", Ef 4:11-12) do curso de
obreiro, em modo "pro" (esqueleto + assunto por assunto), UMA VEZ COM CADA
PROVEDOR (Groq, depois Gemini) — pra comparar na mão antes de montar o híbrido
final (Passo 2 e 3 do PROCESSO_CRIACAO_TOPICO.md).

Não chama QuizAgent nem montar_topico ainda — só o conteúdo (Passo 2).

Rodar de dentro do container: docker exec nia_backend python _gerar_topico3_obreiro.py
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
from app.agents.perfis import PERFIL_OBREIRO
from app.services.biblia_service import buscar_texto

CONTEXTO_ANTERIOR = """
1. Sacerdócio de Todos os Crentes (1Pe 2:9) — todo crente, sem distinção de função ou
   tempo de conversão, é "geração eleita, sacerdócio real, nação santa, povo adquirido"
   (1Pe 2:9); fundamento em "pedras vivas" edificadas sobre Cristo (1Pe 2:4-8), raiz no
   Antigo Testamento (Êx 19:5-6, Is 61:6), não elimina Jesus como único Mediador
   (1Tm 2:5), e foi resgatado pela Reforma (Lutero, 1520) depois de quase se perder na
   Idade Média com o clero virando classe separada dos leigos.
2. Dons Espirituais (Rm 12:6-8) — cada crente recebeu, pela graça, ao menos um dom
   (chárisma) pra servir o corpo: profecia, ministério, ensino, exortação, repartir,
   presidir, misericórdia — cada um com uma atitude prescrita (fé, dedicação,
   liberalidade, zelo, alegria). O dom não é talento natural, é distribuído pelo
   Espírito "como quer" (1Co 12:11). Já introduziu a ideia de que o dom dá forma ao
   chamado, e citou de passagem Efésios 4:11-12 (dons de liderança que equipam o corpo,
   não o substituem) — o Tópico 3 aprofunda exatamente esse ponto. Fechou com a unidade
   do corpo sem hierarquia (1Co 12:4-6, 12, 21) e o amor como condição de tudo (1Co 13).
""".strip()

FOCO_OBRIGATORIO = """
- Diferença entre DOM (capacitação, dada a todo crente, tema do Tópico 2) e OFÍCIO/
  VOCAÇÃO FORMAL (função pública, reconhecida pela igreja, exercida por alguns) — os
  dois não competem, o ofício é o dom operando dentro de uma responsabilidade
  formalizada diante da comunidade.
- Efésios 4:7-16 como texto central: os dons de liderança (apóstolos, profetas,
  evangelistas, pastores e mestres) existem "tendo em vista o aperfeiçoamento dos
  santos, para a obra do ministério, para edificação do corpo de Cristo" (Ef 4:12) — a
  liderança formal EQUIPA o corpo pra servir, não serve no lugar dele. Conectar
  explicitamente com o sacerdócio universal do Tópico 1: reconhecer um ofício não cria
  uma classe sacerdotal separada.
- O padrão bíblico de RECONHECIMENTO PÚBLICO de um ofício, não autoproclamação: Atos
  6:1-6 (a igreja escolhe, os apóstolos oram e impõem as mãos) como exemplo concreto.
- O critério bíblico pra ofícios de ancião/bispo e diácono é CARÁTER, não talento nem
  carisma: percorrer as listas de qualificação de 1 Timóteo 3:1-13 e Tito 1:5-9
  (irrepreensível, marido de uma só mulher, governa bem a própria casa, não neófito,
  hospitaleiro, sóbrio etc.) e destacar que nenhum item da lista é sobre habilidade -
  são todos sobre vida e testemunho.
- NOTA DE NEUTRALIDADE DOUTRINÁRIA OBRIGATÓRIA (mesmo padrão do Tópico 2, sem tomar
  partido): (a) Tito 1:5-7 usa "ancião" e "bispo" pro mesmo cargo no mesmo parágrafo —
  isso é uma observação textual, não opinião — mas tradições cristãs divergem sobre se
  "bispo/presbítero/pastor" continuam sendo o mesmo ofício hoje ou se desenvolveram em
  ofícios distintos (episcopal vs. presbiteriano vs. congregacional); (b) se apóstolo e
  profeta em Ef 4:11 são ofícios que continuam hoje ou eram só da era fundacional da
  igreja (mesmo debate cessacionismo x continuísmo já sinalizado no Tópico 2); (c) quem
  pode ocupar os ofícios formais de ancião/bispo — tradições cristãs divergem sobre a
  elegibilidade de mulheres para esses cargos especificamente (diferente do dom
  espiritual em si, que Rm 12 e 1Co 12 não restringem por sexo) — o curso não assume
  nenhuma dessas posições, só apresenta o texto e o debate.
""".strip()


async def gerar_com(nome: str, service, texto_biblico_base: str):
    print(f"\n{'='*60}\n{nome.upper()}\n{'='*60}")
    agent = ContentAgent(service)

    conteudo = await agent.generate_conteudo_pro(
        titulo="Vocação e Ofícios",
        aula=1,
        numero=3,
        topico_id="curso8-modulo1-topico3",
        nivel="intermediário",
        contexto_topicos_anteriores=CONTEXTO_ANTERIOR,
        foco=FOCO_OBRIGATORIO,
        pausa_entre_chamadas_s=2.0,
        perfil=PERFIL_OBREIRO,
        texto_biblico_base=texto_biblico_base,
    )

    n_assuntos = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    n_checkpoints = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    print(f"-> {n_assuntos} assuntos, {n_checkpoints} checkpoints marcados")

    # ./backend está montado em /app (bind mount) — salvando aqui, o arquivo já
    # aparece direto no host em backend/_conteudo_{nome}_topico3.json.
    saida = Path(f"/app/_conteudo_{nome}_topico3.json")
    saida.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Salvo em {saida}")
    return conteudo


async def main():
    print("📖 Buscando texto bíblico real (Passo 1 já feito, re-confirmando aqui)...")
    refs = [
        ("ef", "4:7-16"),
        ("1co", "12:28"),
        ("at", "6:1-6"),
        ("1tm", "3:1-13"),
        ("tt", "1:5-9"),
    ]
    blocos = []
    for livro, ref in refs:
        texto = await buscar_texto(livro, ref)
        if texto:
            blocos.append(f"[{livro.upper()} {ref}]\n{texto}")
    texto_biblico_base = "\n\n".join(blocos)
    print(f"-> {len(blocos)} passagens carregadas, {len(texto_biblico_base)} caracteres")

    await gerar_com("groq", GroqService(), texto_biblico_base)
    await gerar_com("gemini", GeminiService(), texto_biblico_base)

    print("\n✅ Concluído. backend/./ é bind mount, então os arquivos já aparecem "
          "no host em backend/_conteudo_groq_topico3.json e "
          "backend/_conteudo_gemini_topico3.json.")


if __name__ == "__main__":
    asyncio.run(main())
