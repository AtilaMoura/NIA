"""Quem pode ver o quê (2026-10-06) — a regra de acesso a curso num lugar só.

O front não decide nada: toda rota que entrega curso, módulo, aula, tópico, prova,
render ou tutor pergunta aqui.

- Curso **privado** (estudo pessoal): só o Master e quem tem Matricula ativa.
  Pra quem não pode, o curso "não existe" (404) — nem o título vaza.
- Curso **público**: o curso aparece pra todos; o CONTEÚDO só abre se estiver
  publicado, ou pra quem revisa (master/admin/professor), que vê a prévia.
"""

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Avaliacao, Course, Lesson, Matricula, Module, Topico, User

PAPEIS_REVISAO = ("master", "admin", "professor")


def tem_matricula_ativa(db: Session, user_id: int, course_id: int) -> bool:
    m = (
        db.query(Matricula)
        .filter(Matricula.user_id == user_id, Matricula.course_id == course_id, Matricula.status == "ativa")
        .first()
    )
    if not m:
        return False
    return m.valida_ate is None or m.valida_ate > datetime.now(timezone.utc)


def pode_ver_curso(db: Session, user: User | None, course: Course) -> bool:
    """O curso aparece na lista / dá pra abrir a página dele."""
    if course.visibilidade == "privado":
        return user is not None and (user.role == "master" or tem_matricula_ativa(db, user.id, course.id))
    return True


def pode_estudar_curso(db: Session, user: User | None, course: Course) -> bool:
    """O conteúdo (módulos, aulas, tópicos, render, prova, tutor) abre."""
    if not pode_ver_curso(db, user, course):
        return False
    if course.visibilidade == "privado":
        return True  # quem foi liberado estuda, o Master controla pela matrícula
    if course.status == "published":
        return True
    return user is not None and user.role in PAPEIS_REVISAO


def cursos_visiveis(db: Session, user: User | None) -> list[Course]:
    return [c for c in db.query(Course).order_by(Course.id).all() if pode_ver_curso(db, user, c)]


def ids_cursos_estudaveis(db: Session, user: User | None) -> set[int]:
    return {c.id for c in db.query(Course).all() if pode_estudar_curso(db, user, c)}


# ---- de onde é este conteúdo? ----

def curso_do_modulo(db: Session, module_id: int) -> Course | None:
    return db.query(Course).join(Module, Module.course_id == Course.id).filter(Module.id == module_id).first()


def curso_da_aula(db: Session, lesson_id: int) -> Course | None:
    return (
        db.query(Course)
        .join(Module, Module.course_id == Course.id)
        .join(Lesson, Lesson.module_id == Module.id)
        .filter(Lesson.id == lesson_id)
        .first()
    )


def curso_do_topico(db: Session, topico_id: int) -> Course | None:
    return (
        db.query(Course)
        .join(Module, Module.course_id == Course.id)
        .join(Lesson, Lesson.module_id == Module.id)
        .join(Topico, Topico.lesson_id == Lesson.id)
        .filter(Topico.id == topico_id)
        .first()
    )


def curso_da_avaliacao(db: Session, avaliacao_id: int) -> Course | None:
    a = db.query(Avaliacao.topico_id).filter(Avaliacao.id == avaliacao_id).first()
    return curso_do_topico(db, a[0]) if a else None


# ---- travas pras rotas ----

def exigir_estudo(db: Session, user: User | None, course: Course | None, oque: str = "Conteúdo") -> None:
    """Levanta 404 quando o curso é privado e a pessoa não foi liberada (não
    revela que existe) e 403 quando é público mas ainda não foi publicado."""
    if course is None:
        return  # conteúdo solto, sem curso — segue a regra antiga (rota decide)
    if not pode_ver_curso(db, user, course):
        raise HTTPException(404, f"{oque} not found")
    if not pode_estudar_curso(db, user, course):
        raise HTTPException(403, "Este curso ainda não foi publicado.")


def exigir_estudo_topico(db: Session, user: User | None, topico_id: int) -> None:
    exigir_estudo(db, user, curso_do_topico(db, topico_id), "Tópico")


def exigir_estudo_avaliacao(db: Session, user: User | None, avaliacao_id: int) -> None:
    exigir_estudo(db, user, curso_da_avaliacao(db, avaliacao_id), "Avaliação")


def exigir_estudo_aula(db: Session, user: User | None, lesson_id: int) -> None:
    exigir_estudo(db, user, curso_da_aula(db, lesson_id), "Aula")
