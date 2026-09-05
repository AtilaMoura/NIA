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
from app.models.models import Course, Module, Lesson, Topico, Progress, TopicoProgress, User
from app.core.auth import get_current_user
from app.agents.pipeline import gerar_estrutura_curso, gerar_e_revisar_topico
from app.agents.tutor_agent import TutorAgent
from app.agents.perfis import resolver_perfil
from app.schemas.topico_progress import AvaliarTopicoRequest, TopicoProgressOut
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
_PERFIL_POR_CURSO: dict[int, str] = {8: "obreiro", 9: "ingles"}


def _perfil_do_curso(db: Session, topico: Topico) -> str:
    lesson = db.query(Lesson).filter(Lesson.id == topico.lesson_id).first()
    module = db.query(Module).filter(Module.id == lesson.module_id).first() if lesson else None
    course_id = module.course_id if module else None
    return _PERFIL_POR_CURSO.get(course_id, "tech")


def _rate_limited(err: Exception) -> bool:
    msg = str(err).lower()
    return "429" in msg or "rate_limit" in msg or "rate limit" in msg


@router.post("/topicos/{topico_id}/avaliar", response_model=TopicoProgressOut)
async def avaliar_resumo_topico(
    topico_id: int,
    data: AvaliarTopicoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Análogo por TÓPICO do POST /pipeline/licoes/{id}/avaliar: o aluno cola o
    '=== RESUMO ===' que o render monta no fim do tópico e o Tutor decide
    dominado/reforço. Grava em TopicoProgress (não em Progress) e NÃO dispara
    gamificação — o Emaús é sem pontos/selos/streak."""
    # Mesma trava de identidade do /topico-progress: ninguém envia avaliação "como"
    # outra pessoa (achado de segurança 2026-09-04).
    if data.user_id != current_user.id:
        raise HTTPException(403, "Só é possível avaliar o próprio progresso.")
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico não encontrado")
    if not topico.content or not topico.is_approved:
        raise HTTPException(400, "Este tópico ainda não está disponível para avaliação.")

    lesson = db.query(Lesson).filter(Lesson.id == topico.lesson_id).first()
    module = db.query(Module).filter(Module.id == lesson.module_id).first() if lesson else None
    contexto = topico.titulo
    if lesson:
        contexto += f" — aula '{lesson.title}'"
    if module:
        contexto += f", módulo {module.module_index}"

    registro = (
        db.query(TopicoProgress)
        .filter(
            TopicoProgress.user_id == data.user_id,
            TopicoProgress.topico_id == topico_id,
        )
        .first()
    )

    historico_txt = ""
    if registro and registro.tutor_analise and registro.tutor_analise.get("historico"):
        historico_txt = "\n".join(
            f"- {h.get('veredito')}: {h.get('resumo_diagnostico')}"
            for h in registro.tutor_analise["historico"]
        )

    perfil_id = _perfil_do_curso(db, topico)

    try:
        resultado = await TutorAgent(_service(data.modelo)).avaliar_resumo(
            data.resumo_texto,
            contexto_topico=contexto,
            historico_reforcos=historico_txt,
            perfil=resolver_perfil(perfil_id),
        )
    except Exception as e:
        if _rate_limited(e):
            raise HTTPException(
                503, "O tutor está sobrecarregado agora. Tente de novo em alguns minutos."
            )
        raise HTTPException(500, f"Erro ao avaliar resumo do tópico: {str(e)}")

    agora = datetime.now(timezone.utc)
    if not registro:
        registro = TopicoProgress(
            user_id=data.user_id, topico_id=topico_id, status="em_andamento"
        )
        db.add(registro)

    historico = (registro.tutor_analise or {}).get("historico", [])
    historico.append(
        {
            "veredito": resultado.get("veredito"),
            "resumo_diagnostico": resultado.get("resumo_diagnostico"),
        }
    )
    registro.tutor_veredito = resultado.get("veredito")
    registro.tutor_analise = {"ultima_avaliacao": resultado, "historico": historico}
    registro.avaliado_em = agora

    if resultado.get("veredito") == "dominado":
        registro.status = "concluido"
        if registro.iniciado_em is None:
            registro.iniciado_em = agora
        if registro.concluido_em is None:
            registro.concluido_em = agora
    elif registro.status != "concluido":
        # reforço: mantém em andamento (não regride um tópico já concluído antes)
        registro.status = "em_andamento"
        if registro.iniciado_em is None:
            registro.iniciado_em = agora

    db.commit()
    db.refresh(registro)
    return registro
