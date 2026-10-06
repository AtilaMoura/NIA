"""Liberação de estudos privados por pessoa (2026-10-06).

O Master libera um curso privado pra alguém (Matricula origem 'master', status
'ativa') ou pausa. Nunca apaga a linha — pausar e liberar de novo só trocam o
status, e `liberada_por` guarda quem mexeu por último.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Course, Matricula, User
from app.schemas.matricula import EstudoMeu, LiberacaoEstudo, PessoaCurta
from app.services import acesso_service


def _cursos_privados(db: Session) -> list[Course]:
    return db.query(Course).filter(Course.visibilidade == "privado").order_by(Course.id).all()


def meus_estudos(db: Session, user: User) -> list[EstudoMeu]:
    """Estudos privados que este usuário abre. Pro Master: todos, com a lista de
    quem mais tem cada um liberado."""
    saida = []
    for c in _cursos_privados(db):
        if not acesso_service.pode_ver_curso(db, user, c):
            continue
        liberado_para: list[PessoaCurta] = []
        if user.role == "master":
            linhas = (
                db.query(User)
                .join(Matricula, Matricula.user_id == User.id)
                .filter(Matricula.course_id == c.id, Matricula.status == "ativa")
                .order_by(User.name)
                .all()
            )
            liberado_para = [PessoaCurta(id=u.id, name=u.name) for u in linhas]
        saida.append(
            EstudoMeu(
                course_id=c.id,
                titulo=c.title,
                descricao=c.description,
                cover_image_url=c.cover_image_url,
                liberado_para=liberado_para,
            )
        )
    return saida


def liberacoes_da_pessoa(db: Session, user_id: int) -> list[LiberacaoEstudo]:
    """Todos os estudos privados, com o status da liberação pra esta pessoa."""
    if not db.get(User, user_id):
        raise HTTPException(404, "Pessoa não encontrada.")
    matriculas = {m.course_id: m for m in db.query(Matricula).filter(Matricula.user_id == user_id).all()}
    return [
        LiberacaoEstudo(
            course_id=c.id,
            titulo=c.title,
            status=matriculas[c.id].status if c.id in matriculas else None,
            atualizada_em=matriculas[c.id].atualizada_em if c.id in matriculas else None,
        )
        for c in _cursos_privados(db)
    ]


def mudar_liberacao(db: Session, master: User, user_id: int, course_id: int, status: str) -> LiberacaoEstudo:
    """Libera ('ativa') ou pausa ('pausada') um estudo privado pra uma pessoa."""
    if not db.get(User, user_id):
        raise HTTPException(404, "Pessoa não encontrada.")
    curso = db.get(Course, course_id)
    if not curso or curso.visibilidade != "privado":
        raise HTTPException(404, "Estudo privado não encontrado.")

    m = db.query(Matricula).filter(Matricula.user_id == user_id, Matricula.course_id == course_id).first()
    if m is None:
        if status != "ativa":
            raise HTTPException(400, "Este estudo nunca foi liberado pra esta pessoa.")
        m = Matricula(user_id=user_id, course_id=course_id, origem="master", status="ativa", liberada_por=master.id)
        db.add(m)
    else:
        m.status = status
        m.liberada_por = master.id
    db.commit()
    db.refresh(m)
    return LiberacaoEstudo(course_id=curso.id, titulo=curso.title, status=m.status, atualizada_em=m.atualizada_em)
