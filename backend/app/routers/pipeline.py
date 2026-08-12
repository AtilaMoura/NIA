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
from app.models.models import Course, Module, Lesson, Progress
from app.agents.pipeline import gerar_estrutura_curso, gerar_e_revisar_topico
from app.agents.tutor_agent import TutorAgent
from app.services.groq_service import GroqService
from app.services.gemini_service import GeminiService

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


def _foco_da_licao(course: Course, module: Module, lesson: Lesson) -> str:
    """O 'foco' de cada tópico só existe no JSON de estrutura (Course.structure) —
    não vale a pena criar coluna nova só pra isso (não há Alembic; ALTER TABLE em
    produção fica pra quando o container for atualizado)."""
    try:
        modulos = course.structure.get("modulos", [])
        licoes = modulos[module.module_index - 1].get("licoes", [])
        return licoes[lesson.lesson_index - 1].get("foco", "")
    except (IndexError, AttributeError, KeyError):
        return ""


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
        else:
            progress.can_advance = False

        db.commit()
        return {"lesson_id": lesson.id, "avaliacao": resultado, "can_advance": progress.can_advance}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Erro ao avaliar resumo: {str(e)}")
