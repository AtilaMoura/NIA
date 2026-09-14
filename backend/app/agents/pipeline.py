# backend/app/agents/pipeline.py
"""
Fase 7 — orquestração que liga as Fases 0-6, sem tocar banco nem HTTP. Recebe um
"service" de IA (Gemini/Groq/FakeService) e devolve dicts prontos — quem chama
(ver routers/pipeline.py) decide o que persistir. Fica separado do router de
propósito: assim dá pra testar o fluxo inteiro com FakeService, sem precisar de
Postgres nem de chamada real de API (mesma técnica de _test_mock_pipeline.py,
_test_reviewer.py, _test_tutor.py).

Duas funções:
- gerar_estrutura_curso(): Fase 3, só decide módulos/tópicos.
- gerar_e_revisar_topico(): Fase 2 (comum ou pro) + Fase 5 num só passo — gera o
  tópico inteiro e já roda o reviewer em cima, pra quem chamar decidir salvar como
  aprovado ou devolver os problemas pro admin (nunca aprova sozinho sem reviewer).
"""

from .estrutura_agent import EstruturaAgent
from .specialists.ia_agent import ContentAgent
from .quiz_agent import QuizAgent
from .montar_topico import montar_topico
from .reviewer_agent import ReviewerAgent
from .perfis import PerfilDominio, PERFIL_TECH


async def gerar_estrutura_curso(service, assunto: str, nivel: str, objetivo: str = "") -> dict:
    return await EstruturaAgent(service).gerar_estrutura(assunto, nivel, objetivo)


async def gerar_e_revisar_topico(
    service,
    *,
    titulo: str,
    aula: int,
    numero: int,
    topico_id: str,
    modo: str = "comum",
    nivel: str = "básico",
    contexto_topicos_anteriores: str = "",
    foco: str = "",
    proximo_topico_label: str = "(fim do módulo)",
    pausa_entre_chamadas_s: float = 2.0,
    perfil: PerfilDominio = PERFIL_TECH,
    texto_biblico_base: str = "",
) -> dict:
    """Gera 1 tópico completo (conteúdo + perguntas + montagem) e já revisa.
    Retorna {"topico": dict, "revisao": dict} — "revisao['aprovado']" decide se
    quem chamou deve salvar como aprovado ou devolver os problemas pro admin.
    "modo" é "comum" (1 chamada, mais rápido) ou "pro" (assunto por assunto, mais
    detalhista e mais chamadas — ver Fase 2b)."""
    if modo not in ("comum", "pro"):
        raise ValueError(f"modo inválido: '{modo}' (use 'comum' ou 'pro')")

    content_agent = ContentAgent(service)
    quiz_agent = QuizAgent(service)
    reviewer = ReviewerAgent(service)

    if modo == "pro":
        conteudo = await content_agent.generate_conteudo_pro(
            titulo=titulo, aula=aula, numero=numero, topico_id=topico_id,
            nivel=nivel, contexto_topicos_anteriores=contexto_topicos_anteriores,
            foco=foco, pausa_entre_chamadas_s=pausa_entre_chamadas_s, perfil=perfil,
            texto_biblico_base=texto_biblico_base,
        )
    else:
        conteudo = await content_agent.generate_conteudo(
            titulo=titulo, aula=aula, numero=numero, nivel=nivel,
            contexto_topicos_anteriores=contexto_topicos_anteriores, foco=foco,
            perfil=perfil, texto_biblico_base=texto_biblico_base,
        )

    # Trava determinística (não confiar na IA pra isso — mesmo motivo que
    # proximo_topico_label já é sempre passado por fora, nunca gerado): o
    # identificador/posição do tópico vêm de quem chamou (o banco), não do texto
    # que a IA decidiu escrever dentro do JSON.
    conteudo = {**conteudo, "topico_id": topico_id, "aula": aula, "numero": numero}

    perguntas = await quiz_agent.generate_perguntas(conteudo, perfil=perfil)
    topico = montar_topico(conteudo, perguntas, proximo_topico_label=proximo_topico_label)
    revisao = await reviewer.revisar_topico(
        topico,
        contexto_topicos_anteriores=contexto_topicos_anteriores,
        foco_esperado=foco,
        perfil=perfil,
    )

    return {"topico": topico, "revisao": revisao}
