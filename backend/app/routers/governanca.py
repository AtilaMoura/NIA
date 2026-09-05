"""Governança/publicação de curso (FASE 5b do front Emaús). Aprovar um TÓPICO
(routers/revisao.py) é diferente de aprovar a PUBLICAÇÃO do CURSO inteiro — este
router é sobre o curso: quais professores são tutores, se o master aprova sozinho,
se precisa de todos os tutores ou só um, e o botão final de publicar/despublicar.

`Course.status` ('draft'|'published'|'archived') é o estado real que os alunos
enxergam — publicar aqui NÃO mexe em nenhum Topico.is_approved (isso é a FASE 5a).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.models import Course, CourseTutor, CourseAprovacao, User
from app.core.auth import get_current_user
from app.schemas.governanca import (
    ConfigCursoUpdate,
    AprovacaoCursoUpsert,
    GovernancaCursoOut,
    PessoaOut,
    AprovacaoOut,
)

router = APIRouter(prefix="/cursos", tags=["Governança"])

PAPEIS_REVISOR = ("master", "admin", "professor")
PAPEIS_ADMIN = ("master", "admin")


def _exigir_revisor(user: User):
    if user.role not in PAPEIS_REVISOR:
        raise HTTPException(403, "Só master, admin ou professor acessam a área de revisão.")


def _exigir_admin(user: User):
    if user.role not in PAPEIS_ADMIN:
        raise HTTPException(403, "Só master ou admin configuram a governança do curso.")


def _curso_ou_404(db: Session, course_id: int) -> Course:
    curso = db.query(Course).filter(Course.id == course_id).first()
    if not curso:
        raise HTTPException(404, "Curso não encontrado")
    return curso


def _pode_publicar(db: Session, curso: Course, tutor_ids: list[int]) -> bool:
    if curso.aprovacao_master_basta:
        aprovou_master = (
            db.query(CourseAprovacao)
            .join(User, User.id == CourseAprovacao.user_id)
            .filter(
                CourseAprovacao.course_id == curso.id,
                CourseAprovacao.aprovado.is_(True),
                User.role == "master",
            )
            .first()
        )
        if aprovou_master:
            return True

    if not tutor_ids:
        return False

    aprovados_tutores = (
        db.query(CourseAprovacao)
        .filter(
            CourseAprovacao.course_id == curso.id,
            CourseAprovacao.user_id.in_(tutor_ids),
            CourseAprovacao.aprovado.is_(True),
        )
        .count()
    )
    if curso.aprovacao_exige_todos_tutores:
        return aprovados_tutores == len(tutor_ids)
    return aprovados_tutores >= 1


@router.get("/{course_id}/governanca", response_model=GovernancaCursoOut)
def obter_governanca(
    course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    _exigir_revisor(current_user)
    curso = _curso_ou_404(db, course_id)

    tutores_rows = db.query(CourseTutor).filter(CourseTutor.course_id == course_id).all()
    tutor_ids = [t.user_id for t in tutores_rows]
    tutores_users = db.query(User).filter(User.id.in_(tutor_ids)).all() if tutor_ids else []
    professores = db.query(User).filter(User.role == "professor").all()
    aprovacoes_rows = (
        db.query(CourseAprovacao, User.name)
        .join(User, User.id == CourseAprovacao.user_id)
        .filter(CourseAprovacao.course_id == course_id)
        .all()
    )

    return GovernancaCursoOut(
        course_id=curso.id,
        status=curso.status,
        publicado=curso.status == "published",
        published_at=curso.published_at,
        aprovacao_master_basta=curso.aprovacao_master_basta,
        aprovacao_exige_todos_tutores=curso.aprovacao_exige_todos_tutores,
        tutores=[PessoaOut(id=u.id, name=u.name, email=u.email) for u in tutores_users],
        professores_disponiveis=[PessoaOut(id=u.id, name=u.name, email=u.email) for u in professores],
        aprovacoes=[
            AprovacaoOut(
                user_id=a.user_id,
                name=nome,
                papel_no_momento=a.papel_no_momento,
                aprovado=a.aprovado,
                observacao=a.observacao,
                updated_at=a.updated_at,
            )
            for a, nome in aprovacoes_rows
        ],
        pode_publicar=current_user.role == "master" or _pode_publicar(db, curso, tutor_ids),
        sou_tutor=current_user.id in tutor_ids,
    )


@router.put("/{course_id}/config", response_model=GovernancaCursoOut)
def salvar_config(
    course_id: int,
    data: ConfigCursoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_admin(current_user)
    curso = _curso_ou_404(db, course_id)

    if data.tutor_ids:
        professores_validos = (
            db.query(User.id).filter(User.id.in_(data.tutor_ids), User.role == "professor").all()
        )
        if len(professores_validos) != len(set(data.tutor_ids)):
            raise HTTPException(400, "Algum id de tutor não corresponde a um usuário professor.")

    curso.aprovacao_master_basta = data.aprovacao_master_basta
    curso.aprovacao_exige_todos_tutores = data.aprovacao_exige_todos_tutores

    db.query(CourseTutor).filter(CourseTutor.course_id == course_id).delete()
    for uid in set(data.tutor_ids):
        db.add(CourseTutor(course_id=course_id, user_id=uid))

    db.commit()
    return obter_governanca(course_id, db, current_user)


@router.put("/{course_id}/aprovacao", response_model=AprovacaoOut)
def salvar_aprovacao(
    course_id: int,
    data: AprovacaoCursoUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    _curso_ou_404(db, course_id)

    if current_user.role == "professor":
        eh_tutor = (
            db.query(CourseTutor)
            .filter(CourseTutor.course_id == course_id, CourseTutor.user_id == current_user.id)
            .first()
        )
        if not eh_tutor:
            raise HTTPException(403, "Você não é tutor deste curso.")

    registro = (
        db.query(CourseAprovacao)
        .filter(CourseAprovacao.course_id == course_id, CourseAprovacao.user_id == current_user.id)
        .first()
    )
    if not registro:
        registro = CourseAprovacao(course_id=course_id, user_id=current_user.id)
        db.add(registro)

    registro.papel_no_momento = current_user.role
    registro.aprovado = data.aprovado
    registro.observacao = data.observacao
    db.commit()
    db.refresh(registro)

    return AprovacaoOut(
        user_id=registro.user_id,
        name=current_user.name,
        papel_no_momento=registro.papel_no_momento,
        aprovado=registro.aprovado,
        observacao=registro.observacao,
        updated_at=registro.updated_at,
    )


@router.post("/{course_id}/publicar", response_model=GovernancaCursoOut)
def publicar_curso(
    course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    _exigir_revisor(current_user)
    curso = _curso_ou_404(db, course_id)

    if current_user.role != "master":
        tutor_ids = [
            t.user_id for t in db.query(CourseTutor).filter(CourseTutor.course_id == course_id).all()
        ]
        if not _pode_publicar(db, curso, tutor_ids):
            raise HTTPException(403, "As condições de aprovação deste curso ainda não foram atingidas.")

    curso.status = "published"
    curso.published_at = func.now()
    db.commit()
    return obter_governanca(course_id, db, current_user)


@router.post("/{course_id}/despublicar", response_model=GovernancaCursoOut)
def despublicar_curso(
    course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != "master":
        raise HTTPException(403, "Só master pode despublicar um curso.")
    curso = _curso_ou_404(db, course_id)
    curso.status = "draft"
    db.commit()
    return obter_governanca(course_id, db, current_user)
