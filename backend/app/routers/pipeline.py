# backend/app/routers/pipeline.py
"""
Fase 7 — glue de banco + HTTP em cima de app/agents/pipeline.py (Fases 0-6). Duas
frentes, como combinado:

- Admin: cria curso com estrutura variável (Fase 3), gera+revisa lição por lição
  (Fase 2 comum/pro + Fase 5) — nunca aprova sozinho, o Reviewer decide, e se
  reprovar o admin vê exatamente o que falta e decide regenerar.
- Aluno: estuda uma lição aprovada (GET /lessons/{id}/render, já existe — Fase 4)
  e no fim cola o resumo aqui, que o Tutor avalia (Fase 6) e libera ou não o avanço.

Geração continua tópico por tópico (não o curso inteiro de uma vez) — o aluno pode
começar a estudar as lições já aprovadas enquanto o admin ainda gera as de trás.
"""

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import (
    AlunoDificuldade, Avaliacao, AvaliacaoProgress, AvaliacaoResposta, Course, Lesson, Module,
    Progress, RevisaoTopico, Topico, TopicoProgress, TopicoResposta, User,
)
from app.core.auth import get_current_user
from app.agents.pipeline import gerar_estrutura_curso, gerar_e_revisar_topico
from app.agents.tutor_agent import TutorAgent
from app.agents.contexto_topico import carregar_content, montar_contexto_duvida
from app.agents.revisao_avaliacao import NOTA_MINIMA_PROVA, corrigir_e_revisar, dificuldades_do_resultado
from app.agents.perfis import resolver_perfil
from app.schemas.topico_progress import AvaliarTopicoRequest, TopicoProgressOut
from app.schemas.avaliacao_progress import AvaliacaoProgressOut
from app.services.groq_service import GroqService
from app.services.gemini_service import GeminiService
from app.services.biblia_service import buscar_todos_textos

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


def _service(modelo: str):
    if modelo == "gemini":
        return GeminiService()
    return GroqService()


# ============================================================
# ADMIN — Fase 3: criar curso com estrutura variável
# ============================================================

class CriarCursoRequest(BaseModel):
    assunto: str
    nivel: str  # básico | intermediário | avançado | especialista
    objetivo: str = ""
    modelo: str = "groq"


@router.post("/cursos")
async def criar_curso(data: CriarCursoRequest, db: Session = Depends(get_db)):
    """Gera só a estrutura (módulos + tópicos, quantidade variável por assunto/nível —
    Fase 3) e salva o esqueleto: Course + Module + Lesson, todas as lições com
    content=None e is_approved=False, prontas pra Fase 2 gerar uma de cada vez."""
    try:
        estrutura = await gerar_estrutura_curso(
            _service(data.modelo), assunto=data.assunto, nivel=data.nivel, objetivo=data.objetivo
        )

        modulos_data = estrutura.get("modulos", [])
        course = Course(
            title=estrutura.get("titulo", data.assunto),
            description=estrutura.get("descricao", ""),
            level=data.nivel,
            duration_hours=max(1, len(modulos_data) * 2),
            modules_count=len(modulos_data),
            structure=estrutura,
            status="draft",
            prerequisites=[],
            learning_outcomes=[],
            generated_by={"agente": "EstruturaAgent", "modelo": data.modelo, "timestamp": str(datetime.now())},
        )
        db.add(course)
        db.flush()

        for mod_index, mod_data in enumerate(modulos_data, start=1):
            licoes_data = mod_data.get("licoes", [])
            module = Module(
                course_id=course.id,
                module_index=mod_data.get("index", mod_index),
                title=mod_data.get("titulo", f"Módulo {mod_index}"),
                description=mod_data.get("descricao", ""),
                content_generated=False,
                exam_generated=False,
                lessons_count=len(licoes_data),
                duration_hours=max(1, len(licoes_data)),
                examples=[], exercises=[], resources={}, quiz={},
                is_published=False,
                generated_by="pending",
            )
            db.add(module)
            db.flush()

            for lesson_index, licao in enumerate(licoes_data, start=1):
                lesson = Lesson(
                    module_id=module.id,
                    lesson_index=lesson_index,
                    title=licao.get("titulo", f"Tópico {lesson_index}"),
                    content=None,
                    is_approved=False,
                )
                db.add(lesson)

        db.commit()
        db.refresh(course)
        return {"course_id": course.id, "titulo": course.title, "estrutura": estrutura}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro ao gerar estrutura do curso: {str(e)}")


# ============================================================
# ADMIN — Fase 2 (comum/pro) + Fase 5: gerar e revisar 1 tópico
# ============================================================

class GerarLicaoRequest(BaseModel):
    modo: str = "comum"  # "comum" | "pro"
    modelo: str = "groq"
    perfil: str = "tech"  # "tech" | "teologia" — ver app/agents/perfis.py


def _licao_data(course: Course, module: Module, lesson: Lesson) -> dict:
    """Dados brutos da lição no JSON de estrutura (Course.structure) — não vale a
    pena criar coluna nova só pra isso (não há Alembic; ALTER TABLE em produção fica
    pra quando o container for atualizado)."""
    try:
        modulos = course.structure.get("modulos", [])
        licoes = modulos[module.module_index - 1].get("licoes", [])
        return licoes[lesson.lesson_index - 1]
    except (IndexError, AttributeError, KeyError):
        return {}


def _foco_da_licao(course: Course, module: Module, lesson: Lesson) -> str:
    return _licao_data(course, module, lesson).get("foco", "")


async def _texto_biblico_da_licao(course: Course, module: Module, lesson: Lesson) -> str:
    """Achado no piloto de Filipenses: pedir citação literal sem fornecer o texto de
    verdade não funciona (IA erra a citação, Reviewer reprova certo). Generalizado pro
    curso de obreiro (2026-08-25, ver memória nia-curso-obreiro): em vez de reconhecer
    só UMA referência de Filipenses no título, varre título + foco + "topicos" da
    lição inteira em busca de QUALQUER referência bíblica (qualquer livro do NT +
    alguns do AT — ver biblia_service.extrair_referencias) e busca o texto real
    (Almeida, domínio público) de cada uma. Sem nenhuma referência reconhecida = ""
    (a lição é contextual/histórica, sem grounding, e o fio condutor cobre esse caso
    proibindo citação literal sem base)."""
    dados = _licao_data(course, module, lesson)
    texto_busca = " ".join([
        lesson.title,
        dados.get("foco", ""),
        " ".join(dados.get("topicos", [])),
    ])
    return await buscar_todos_textos(texto_busca)


def _contexto_topicos_anteriores(db: Session, course_id: int, module: Module, lesson: Lesson) -> str:
    """Lições já APROVADAS (Fase 5 passou) antes desta, na ordem do curso — vira o
    texto que o ContentAgent/Reviewer usam pra checar continuidade (Fase 5,
    checagem 'Continuidade' — é exatamente o tipo de erro que motivou essa checagem:
    o modelo referenciar errado um tópico anterior)."""
    modulos = (
        db.query(Module)
        .filter(Module.course_id == course_id, Module.module_index <= module.module_index)
        .order_by(Module.module_index)
        .all()
    )
    linhas = []
    for mod in modulos:
        licoes = (
            db.query(Lesson)
            .filter(Lesson.module_id == mod.id, Lesson.is_approved == True)  # noqa: E712
            .order_by(Lesson.lesson_index)
            .all()
        )
        for licao in licoes:
            if mod.id == module.id and licao.lesson_index >= lesson.lesson_index:
                continue
            linhas.append(f"- Módulo {mod.module_index}, Tópico {licao.lesson_index}: {licao.title}")
    return "\n".join(linhas)


def _proximo_topico_label(db: Session, course_id: int, module: Module, lesson: Lesson) -> str:
    proxima_na_mesma = (
        db.query(Lesson)
        .filter(Lesson.module_id == module.id, Lesson.lesson_index == lesson.lesson_index + 1)
        .first()
    )
    if proxima_na_mesma:
        return proxima_na_mesma.title

    proximo_modulo = (
        db.query(Module)
        .filter(Module.course_id == course_id, Module.module_index == module.module_index + 1)
        .first()
    )
    if proximo_modulo:
        primeira_licao = (
            db.query(Lesson)
            .filter(Lesson.module_id == proximo_modulo.id)
            .order_by(Lesson.lesson_index)
            .first()
        )
        if primeira_licao:
            return f"{proximo_modulo.title}: {primeira_licao.title}"

    return "conclusão do curso"


def _contexto_topicos_anteriores_na_aula(db: Session, lesson_id: int, topico_index_atual: int) -> str:
    """Mesma ideia de _contexto_topicos_anteriores(), um nível abaixo: continuidade
    entre Tópicos da MESMA aula (Lesson), não entre lições do curso — criado junto
    com a tabela Topico (2026-08-26, curso de obreiro, ver PLANO_IMPLEMENTACAO_ESTUDO_IA.md
    Fase 0b). Só considera tópicos já aprovados, na ordem, antes do atual."""
    topicos_antes = (
        db.query(Topico)
        .filter(
            Topico.lesson_id == lesson_id,
            Topico.is_approved == True,  # noqa: E712
            Topico.topico_index < topico_index_atual,
        )
        .order_by(Topico.topico_index)
        .all()
    )
    linhas = [f"- Tópico {t.topico_index}: {t.titulo}" for t in topicos_antes]
    return "\n".join(linhas)


def _proximo_topico_label_na_aula(db: Session, lesson_id: int, topico_index_atual: int) -> str:
    proximo = (
        db.query(Topico)
        .filter(Topico.lesson_id == lesson_id, Topico.topico_index == topico_index_atual + 1)
        .first()
    )
    return proximo.titulo if proximo else "conclusão desta aula"


@router.post("/topicos/{topico_id}/gerar")
async def gerar_topico(topico_id: int, data: GerarLicaoRequest, db: Session = Depends(get_db)):
    """Mesma coisa que POST /licoes/{id}/gerar (Fase 2 comum/pro + Fase 5), um nível
    abaixo: gera 1 Topico dentro de uma aula (Lesson), com continuidade calculada
    entre os tópicos da mesma aula (não entre aulas do curso — ver
    _contexto_topicos_anteriores_na_aula acima). Texto bíblico vem direto de
    Topico.referencia_biblica, sem precisar escanear título/foco como Lesson fazia."""
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico não encontrado")
    lesson = db.query(Lesson).filter(Lesson.id == topico.lesson_id).first()
    module = db.query(Module).filter(Module.id == lesson.module_id).first()
    course = db.query(Course).filter(Course.id == module.course_id).first()

    if topico.is_approved:
        return {"message": "Tópico já aprovado anteriormente", "topico_id": topico.id, "aprovado": True}

    try:
        resultado = await gerar_e_revisar_topico(
            _service(data.modelo),
            titulo=topico.titulo,
            aula=module.module_index,
            numero=topico.topico_index,
            topico_id=f"curso{course.id}-modulo{module.module_index}-aula{lesson.lesson_index}-topico{topico.topico_index}",
            modo=data.modo,
            nivel=course.level,
            contexto_topicos_anteriores=_contexto_topicos_anteriores_na_aula(db, lesson.id, topico.topico_index),
            foco=f"{lesson.title} — {topico.titulo}" + (f" ({topico.referencia_biblica})" if topico.referencia_biblica else ""),
            proximo_topico_label=_proximo_topico_label_na_aula(db, lesson.id, topico.topico_index),
            perfil=resolver_perfil(data.perfil),
            texto_biblico_base=await buscar_todos_textos(topico.referencia_biblica or ""),
        )

        revisao = resultado["revisao"]
        topico.content = json.dumps(resultado["topico"], ensure_ascii=False)
        topico.generated_by = f"ContentAgent+QuizAgent ({data.modo})"
        topico.reviewed_by = "ReviewerAgent"
        topico.review_feedback = revisao
        topico.is_approved = bool(revisao.get("aprovado"))
        topico.estimated_read_time_minutes = resultado["topico"].get("duracao_estimada_min")
        db.commit()

        avaliacao_row = db.query(Avaliacao).filter(Avaliacao.topico_id == topico.id).first()
        if not avaliacao_row:
            avaliacao_row = Avaliacao(topico_id=topico.id, conteudo=resultado["avaliacao"], is_approved=topico.is_approved)
            db.add(avaliacao_row)
        else:
            avaliacao_row.conteudo = resultado["avaliacao"]
            avaliacao_row.is_approved = topico.is_approved
        db.commit()

        return {
            "topico_id": topico.id,
            "aprovado": topico.is_approved,
            "revisao": revisao,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro ao gerar/revisar tópico: {str(e)}")


@router.post("/licoes/{lesson_id}/gerar")
async def gerar_licao(lesson_id: int, data: GerarLicaoRequest, db: Session = Depends(get_db)):
    """Gera o conteúdo de 1 tópico (Fase 2, modo comum ou pro) e já roda o Reviewer
    (Fase 5) em cima. Só marca is_approved=True se o Reviewer aprovar — se reprovar,
    o feedback fica salvo pro admin decidir (não tenta de novo sozinho, pra não
    gastar chamada de IA numa causa que pode precisar de ajuste no foco/estrutura)."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lição não encontrada")
    module = db.query(Module).filter(Module.id == lesson.module_id).first()
    course = db.query(Course).filter(Course.id == module.course_id).first()

    if lesson.is_approved:
        return {"message": "Lição já aprovada anteriormente", "lesson_id": lesson.id, "aprovado": True}

    try:
        resultado = await gerar_e_revisar_topico(
            _service(data.modelo),
            titulo=lesson.title,
            aula=module.module_index,
            numero=lesson.lesson_index,
            topico_id=f"curso{course.id}-modulo{module.module_index}-topico{lesson.lesson_index}",
            modo=data.modo,
            nivel=course.level,
            contexto_topicos_anteriores=_contexto_topicos_anteriores(db, course.id, module, lesson),
            foco=_foco_da_licao(course, module, lesson),
            proximo_topico_label=_proximo_topico_label(db, course.id, module, lesson),
            perfil=resolver_perfil(data.perfil),
            texto_biblico_base=await _texto_biblico_da_licao(course, module, lesson),
        )

        revisao = resultado["revisao"]
        lesson.content = json.dumps(resultado["topico"], ensure_ascii=False)
        lesson.generated_by = f"ContentAgent+QuizAgent ({data.modo})"
        lesson.reviewed_by = "ReviewerAgent"
        lesson.review_feedback = revisao
        lesson.is_approved = bool(revisao.get("aprovado"))
        lesson.estimated_read_time_minutes = resultado["topico"].get("duracao_estimada_min")
        db.commit()

        if lesson.is_approved:
            todas_aprovadas = all(
                l.is_approved
                for l in db.query(Lesson).filter(Lesson.module_id == module.id).all()
            )
            if todas_aprovadas:
                module.content_generated = True
                db.commit()

        return {
            "lesson_id": lesson.id,
            "aprovado": lesson.is_approved,
            "revisao": revisao,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro ao gerar/revisar lição: {str(e)}")


# ============================================================
# ALUNO — Fase 6: avaliar o resumo colado ao final do tópico
# ============================================================

class AvaliarResumoRequest(BaseModel):
    user_id: int
    resumo_texto: str
    modelo: str = "groq"
    perfil: str = "tech"  # "tech" | "teologia" — ver app/agents/perfis.py


PONTOS_POR_LICAO_DOMINADA = 10


def _curso_ficou_completo(db: Session, user_id: int, course_id: int) -> bool:
    """Um curso não tem status próprio de conclusão — cada Module tem seu
    próprio Progress (ver _foco_da_licao acima). 'Curso completo' aqui
    significa: todos os módulos do curso já têm Progress concluído pra esse
    aluno."""
    modulos_ids = [m.id for m in db.query(Module).filter(Module.course_id == course_id).all()]
    if not modulos_ids:
        return False
    completos = (
        db.query(Progress)
        .filter(Progress.user_id == user_id, Progress.module_id.in_(modulos_ids), Progress.status == "completed")
        .count()
    )
    return completos == len(modulos_ids)


def _conceder_gamificacao(db: Session, user: User, course_id: int) -> None:
    """Chamado só quando o Tutor aprova ('dominado'). Pontos/nível/streak/badges
    não tinham nenhum código escrevendo neles antes disso — eram campos mortos
    no schema desde o início do projeto. Catálogo de badges é intencionalmente
    pequeno e objetivo (não é exaustivo — ver PROMPT_UX_ALUNO.md)."""
    user.total_points = (user.total_points or 0) + PONTOS_POR_LICAO_DOMINADA

    agora = datetime.now(timezone.utc)
    if user.last_activity_date is None:
        user.streak_days = 1
    else:
        dias_diff = (agora.date() - user.last_activity_date.date()).days
        if dias_diff == 1:
            user.streak_days = (user.streak_days or 0) + 1
        elif dias_diff > 1:
            user.streak_days = 1
        # dias_diff == 0 (mesma data): streak não muda, já conta hoje
    user.last_activity_date = agora
    user.level = min(100, max(1, 1 + user.total_points // 100))

    total_dominado = 0
    for p in db.query(Progress).filter(Progress.user_id == user.id).all():
        historico = (p.tutor_analysis or {}).get("historico", [])
        total_dominado += sum(1 for h in historico if h.get("veredito") == "dominado")

    atuais = set(user.badges or [])
    novas = []
    if total_dominado >= 1 and "primeira-licao-dominada" not in atuais:
        novas.append("primeira-licao-dominada")
    if (user.streak_days or 0) >= 3 and "streak-3-dias" not in atuais:
        novas.append("streak-3-dias")
    if (user.streak_days or 0) >= 7 and "streak-7-dias" not in atuais:
        novas.append("streak-7-dias")
    if _curso_ficou_completo(db, user.id, course_id) and "primeiro-curso-concluido" not in atuais:
        novas.append("primeiro-curso-concluido")
    if novas:
        user.badges = list(atuais) + novas


@router.post("/licoes/{lesson_id}/avaliar")
async def avaliar_resumo(lesson_id: int, data: AvaliarResumoRequest, db: Session = Depends(get_db)):
    """Aluno cola o resumo (o mesmo '=== RESUMO ===' que o template já monta —
    Fase 4) e o Tutor decide dominado/reforço (Fase 6). Atualiza Progress —
    can_advance só fica True se o veredito for 'dominado'."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lição não encontrada")
    if not lesson.is_approved:
        raise HTTPException(400, "Esta lição ainda não foi aprovada — não deveria estar disponível pro aluno.")
    module = db.query(Module).filter(Module.id == lesson.module_id).first()

    progress = (
        db.query(Progress)
        .filter(Progress.user_id == data.user_id, Progress.module_id == module.id)
        .first()
    )
    if not progress:
        progress = Progress(
            user_id=data.user_id, course_id=module.course_id, module_id=module.id,
            status="in_progress", current_lesson_index=lesson.lesson_index,
            started_at=datetime.now(timezone.utc),
        )
        db.add(progress)
        db.flush()

    historico = ""
    if progress.tutor_analysis and progress.tutor_analysis.get("historico"):
        historico = "\n".join(
            f"- Tópico {h['lesson_id']}: {h['veredito']} — {h['resumo_diagnostico']}"
            for h in progress.tutor_analysis["historico"]
        )

    try:
        resultado = await TutorAgent(_service(data.modelo)).avaliar_resumo(
            data.resumo_texto,
            contexto_topico=f"{lesson.title} (Módulo {module.module_index}, Tópico {lesson.lesson_index})",
            historico_reforcos=historico,
            perfil=resolver_perfil(data.perfil),
        )

        historico_atualizado = (progress.tutor_analysis or {}).get("historico", [])
        historico_atualizado.append({
            "lesson_id": lesson.id,
            "veredito": resultado.get("veredito"),
            "resumo_diagnostico": resultado.get("resumo_diagnostico"),
        })
        progress.tutor_analysis = {"ultima_avaliacao": resultado, "historico": historico_atualizado}
        progress.last_accessed_at = datetime.now(timezone.utc)

        if resultado.get("veredito") == "dominado":
            progress.can_advance = True
            progress.current_lesson_index = lesson.lesson_index + 1
            proxima = (
                db.query(Lesson)
                .filter(Lesson.module_id == module.id, Lesson.lesson_index == lesson.lesson_index + 1)
                .first()
            )
            if not proxima:
                progress.status = "completed"
                progress.completed_at = datetime.now(timezone.utc)

            usuario = db.query(User).filter(User.id == data.user_id).first()
            if usuario:
                _conceder_gamificacao(db, usuario, module.course_id)
        else:
            progress.can_advance = False

        db.commit()
        return {"lesson_id": lesson.id, "avaliacao": resultado, "can_advance": progress.can_advance}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro ao avaliar resumo: {str(e)}")


# ============================================================
# ALUNO — Tutor por TÓPICO (FASE 4 do front Emaús)
# ============================================================

# Enquanto não existe Tenant/domain_profile no banco, o perfil de domínio do
# Tutor é resolvido pelo curso. Curso 8 = Formação do Novo Obreiro (teologia);
# curso 9 = estudo pessoal de Inglês; o resto cai no perfil "tech" (default de
# resolver_perfil).
_PERFIL_POR_CURSO: dict[int, str] = {8: "obreiro", 9: "ingles", 11: "redes"}


def _perfil_do_curso(db: Session, topico: Topico) -> str:
    lesson = db.query(Lesson).filter(Lesson.id == topico.lesson_id).first()
    module = db.query(Module).filter(Module.id == lesson.module_id).first() if lesson else None
    course_id = module.course_id if module else None
    return _PERFIL_POR_CURSO.get(course_id, "tech")


def _rate_limited(err: Exception) -> bool:
    msg = str(err).lower()
    return "429" in msg or "rate_limit" in msg or "rate limit" in msg


# Teto do texto do tópico (numerado por "[Slide N]") que vai na correção —
# o prompt ainda leva as perguntas + gabaritos, e o teto de ~8000 tokens/min
# do Groq é da conta inteira.
TETO_MATERIAL_AVALIACAO = 5000
# "Revisão de tudo" é gerada uma vez por tópico — pode levar mais material.
TETO_MATERIAL_REVISAO_COMPLETA = 8000


def _material_para_avaliacao(content_topico: dict, teto: int = TETO_MATERIAL_AVALIACAO) -> str:
    slides = content_topico.get("slides", [])
    # Prioriza o fim do tópico (slide de resumo + checkpoints finais).
    material, _ = montar_contexto_duvida(content_topico, len(slides) - 1, teto_topico=teto)
    return material


def _formatar_nota(nota: float) -> str:
    return f"{nota:g}".replace(".", ",")


def _diagnostico(modo: str, aprovado: bool, nota: float, total: int, n_revisar: int) -> str:
    placar = f"{_formatar_nota(nota)} de {total}"
    if modo == "prova" and not aprovado:
        minimo = _formatar_nota(NOTA_MINIMA_PROVA * total)
        return f"Você fez {placar} — precisa de {minimo} pra passar. Releia a revisão e refaça a prova."
    if not n_revisar:
        return f"Você fez {placar}. Acertou tudo!"
    if modo == "prova":
        return f"Você fez {placar} e passou. Revise {'o ponto' if n_revisar == 1 else 'os pontos'} abaixo antes de seguir."
    return f"Você fez {placar}. Revise {'o ponto' if n_revisar == 1 else 'os pontos'} abaixo antes da prova."


def _salvar_dificuldades(db: Session, user_id: int, topico_id: int, avaliacao_id: int | None,
                         origem: str, itens: list[dict], rodada: int) -> None:
    """Histórico do que o aluno errou/acertou parcialmente — só acrescenta."""
    for item in dificuldades_do_resultado(itens):
        db.add(AlunoDificuldade(
            user_id=user_id, topico_id=topico_id, avaliacao_id=avaliacao_id, origem=origem,
            question_id=item["id"], conceito=item["enunciado"] or item["id"],
            resposta_aluno=item.get("sua_resposta"), classificacao=item["classificacao"], rodada=rodada,
        ))


async def _revisao_completa_do_topico(db: Session, agente: TutorAgent, topico: Topico,
                                      content_topico: dict, perfil) -> dict | None:
    """Pontos-chave do tópico inteiro — gerado UMA vez e guardado em
    RevisaoTopico. Se a IA falhar, a prova segue sem essa parte (os cartões
    do que o aluno errou continuam aparecendo)."""
    cache = db.query(RevisaoTopico).filter(RevisaoTopico.topico_id == topico.id).first()
    if cache:
        return cache.conteudo
    try:
        conteudo = await agente.gerar_revisao_topico(
            topico.titulo, _material_para_avaliacao(content_topico, TETO_MATERIAL_REVISAO_COMPLETA), perfil=perfil,
        )
    except Exception as e:
        print(f"⚠️ revisão completa do tópico {topico.id} falhou: {e}")
        return None
    if not conteudo.get("pontos"):
        return None
    db.add(RevisaoTopico(topico_id=topico.id, conteudo=conteudo, gerado_por="groq"))
    return conteudo


def _registrar_analise(registro, analise: dict, agora: datetime) -> None:
    historico = list((registro.tutor_analise or {}).get("historico", []))
    historico.append({
        "veredito": analise["veredito"],
        "resumo_diagnostico": analise["resumo_diagnostico"],
        "rodada": analise["rodada"],
        "nota": analise["nota"],
        "total": analise["total"],
    })
    registro.tutor_veredito = analise["veredito"]
    registro.tutor_analise = {"ultima_avaliacao": analise, "historico": historico}
    registro.avaliado_em = agora


def _erro_de_correcao(e: Exception) -> HTTPException:
    if _rate_limited(e):
        return HTTPException(503, "O tutor está sobrecarregado agora. Tente de novo em alguns minutos.")
    print(f"⚠️ correção falhou: {e}")
    return HTTPException(503, "Não deu pra corrigir agora. Tente de novo em instantes.")


@router.post("/topicos/{topico_id}/avaliar", response_model=TopicoProgressOut)
async def avaliar_resumo_topico(
    topico_id: int,
    data: AvaliarTopicoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fim do TÓPICO (reescrito 2026-09-23): corrige pergunta por pergunta
    (ver agents/revisao_avaliacao.py) e devolve a revisão personalizada do que
    o aluno errou. Não trava: o tópico fica concluído e a prova é liberada — a
    prova é que decide se ele passa (decisão do Atila). Grava em
    TopicoProgress e NÃO dispara gamificação (Emaús é sem pontos/selos).
    O resumo_texto do request não é mais usado (respostas vêm do banco)."""
    # Mesma trava de identidade do /topico-progress (achado de segurança 2026-09-04).
    if data.user_id != current_user.id:
        raise HTTPException(403, "Só é possível avaliar o próprio progresso.")
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico não encontrado")
    if not topico.content or not topico.is_approved:
        raise HTTPException(400, "Este tópico ainda não está disponível para avaliação.")

    registro = (
        db.query(TopicoProgress)
        .filter(TopicoProgress.user_id == data.user_id, TopicoProgress.topico_id == topico_id)
        .first()
    )
    rodada = registro.rodada_atual if registro else 1
    content_topico = carregar_content(topico)
    perfil = resolver_perfil(_perfil_do_curso(db, topico))
    agente = TutorAgent(_service(data.modelo))

    respostas = {
        r.question_id: {"resposta": r.resposta_dada, "correta": r.correta}
        for r in db.query(TopicoResposta).filter(
            TopicoResposta.user_id == data.user_id,
            TopicoResposta.topico_id == topico_id,
            TopicoResposta.rodada == rodada,
        )
    }

    try:
        correcao = await corrigir_e_revisar(
            agente, content_topico.get("slides", []), respostas, _material_para_avaliacao(content_topico), perfil,
        )
    except Exception as e:
        raise _erro_de_correcao(e)

    n_revisar = len(dificuldades_do_resultado(correcao["itens"]))
    analise = {
        "modo": "topico",
        "aprovado": True,
        "veredito": "dominado",
        "nota": correcao["nota"],
        "total": correcao["total"],
        "certas": correcao["certas"],
        "itens": correcao["itens"],
        "revisao_completa": None,
        "rodada": rodada,
        "resumo_diagnostico": _diagnostico("topico", True, correcao["nota"], correcao["total"], n_revisar),
    }

    agora = datetime.now(timezone.utc)
    if not registro:
        registro = TopicoProgress(user_id=data.user_id, topico_id=topico_id, status="em_andamento")
        db.add(registro)

    _salvar_dificuldades(db, data.user_id, topico_id, None, "topico", correcao["itens"], rodada)
    _registrar_analise(registro, analise, agora)
    registro.status = "concluido"
    if registro.iniciado_em is None:
        registro.iniciado_em = agora
    if registro.concluido_em is None:
        registro.concluido_em = agora

    db.commit()
    db.refresh(registro)
    return registro


@router.post("/avaliacoes/{avaliacao_id}/avaliar", response_model=AvaliacaoProgressOut)
async def avaliar_resumo_avaliacao(
    avaliacao_id: int,
    data: AvaliarTopicoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fim da PROVA (reescrito 2026-09-23). Cada pergunta vale 1 (parcial 0,5);
    passa com >= 60% (3 de 5):
    - passou: prova concluída + revisão do que errou/acertou em parte;
    - não passou: revisão do que errou + "revisão de tudo" do tópico, a
      dificuldade fica no histórico (AlunoDificuldade) e a prova é reiniciada
      (rodada nova — respostas antigas ficam no banco, só saem de vista).

    GATING: só permite se o tópico vinculado tiver TopicoProgress concluído.
    """
    # Mesma trava de identidade: ninguém envia avaliação "como" outra pessoa.
    if data.user_id != current_user.id:
        raise HTTPException(403, "Só é possível avaliar o próprio progresso.")

    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")
    if not avaliacao.conteudo or not avaliacao.is_approved:
        raise HTTPException(400, "Esta avaliação ainda não está disponível para avaliação.")

    topico_concluido = (
        db.query(TopicoProgress)
        .filter(
            TopicoProgress.user_id == current_user.id,
            TopicoProgress.topico_id == avaliacao.topico_id,
            TopicoProgress.status == "concluido",
        )
        .first()
    )
    if not topico_concluido:
        raise HTTPException(403, "Termine o conteúdo do tópico antes de fazer a prova.")

    registro = (
        db.query(AvaliacaoProgress)
        .filter(AvaliacaoProgress.user_id == data.user_id, AvaliacaoProgress.avaliacao_id == avaliacao_id)
        .first()
    )
    rodada = registro.rodada_atual if registro else 1
    topico = avaliacao.topico
    content_topico = carregar_content(topico) if topico and topico.content else {"slides": []}
    perfil = resolver_perfil(_perfil_do_curso(db, topico) if topico else "tech")
    agente = TutorAgent(_service(data.modelo))

    # Mesmo formato de slide que o render da prova monta (routers/avaliacoes.py).
    slides_prova = [
        {"tipo": "avaliacao_pergunta", "secao": "Avaliação Final", "pergunta": p}
        for p in (avaliacao.conteudo or {}).get("perguntas", [])
    ]
    respostas = {
        r.question_id: {"resposta": r.resposta_dada, "correta": r.correta}
        for r in db.query(AvaliacaoResposta).filter(
            AvaliacaoResposta.user_id == data.user_id,
            AvaliacaoResposta.avaliacao_id == avaliacao_id,
            AvaliacaoResposta.rodada == rodada,
        )
    }

    try:
        correcao = await corrigir_e_revisar(
            agente, slides_prova, respostas, _material_para_avaliacao(content_topico), perfil,
        )
    except Exception as e:
        raise _erro_de_correcao(e)

    aprovado = correcao["nota"] >= NOTA_MINIMA_PROVA * correcao["total"]
    revisao_completa = None
    if not aprovado and topico:
        revisao_completa = await _revisao_completa_do_topico(db, agente, topico, content_topico, perfil)

    n_revisar = len(dificuldades_do_resultado(correcao["itens"]))
    analise = {
        "modo": "prova",
        "aprovado": aprovado,
        "veredito": "dominado" if aprovado else "reforco",
        "nota": correcao["nota"],
        "total": correcao["total"],
        "certas": correcao["certas"],
        "itens": correcao["itens"],
        "revisao_completa": revisao_completa,
        "rodada": rodada,
        "resumo_diagnostico": _diagnostico("prova", aprovado, correcao["nota"], correcao["total"], n_revisar),
    }

    agora = datetime.now(timezone.utc)
    if not registro:
        registro = AvaliacaoProgress(user_id=data.user_id, avaliacao_id=avaliacao_id, status="em_andamento")
        db.add(registro)

    _salvar_dificuldades(db, data.user_id, avaliacao.topico_id, avaliacao_id, "prova", correcao["itens"], rodada)
    _registrar_analise(registro, analise, agora)
    if registro.iniciado_em is None:
        registro.iniciado_em = agora
    if aprovado:
        registro.status = "concluido"
        if registro.concluido_em is None:
            registro.concluido_em = agora
    else:
        # Reinicia a prova pra ele refazer — mesmo mecanismo do POST
        # /avaliacao-progress/{id}/reiniciar (nada é apagado).
        registro.rodada_atual = rodada + 1
        registro.status = "em_andamento"
        registro.ultimo_slide = None

    db.commit()
    db.refresh(registro)
    return registro
