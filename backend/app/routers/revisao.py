"""Área de revisão do professor (FASE 5a do front Emaús). Anotação por SLIDE
(sincronizada com o <iframe> do render via postMessage) + checklist de
aprovação/reprovação por tópico. Tudo exige login com papel master/admin/professor —
nunca aluno, nunca sem token (mesmo padrão de app/routers/topico_progress.py).

Permissão (NIA-T-026): master/admin em qualquer curso; professor só se for tutor
(CourseTutor) do curso do tópico — regra em services/revisao_service.py.

O checklist NÃO mexe mais em Topico.is_approved: esse campo é a VISIBILIDADE do tópico
(scripts de publicação gravam True) e reprovar não pode escondê-lo dos alunos. O estado
da revisão de conteúdo é Topico.revisao_status (endpoints /topicos/{id}/revisao...).
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import CourseTutor, Lesson, Module, Topico, TopicoComment, TopicoChecklist, User
from app.core.auth import get_current_user
from app.schemas.revisao import (
    ComentarioCreate,
    ComentarioUpdate,
    ComentarioOut,
    ChecklistUpsert,
    ChecklistOut,
    AprovarTopicoIn,
    IaRevisouIn,
    RevisaoTopicoOut,
)
from app.services import revisao_service

router = APIRouter(tags=["Revisão"])

PAPEIS_REVISOR = ("master", "admin", "professor")


def _exigir_revisor(user: User):
    if user.role not in PAPEIS_REVISOR:
        raise HTTPException(403, "Só master, admin ou professor acessam a área de revisão.")


# ---- Comentários por slide ----

@router.get("/topico-comments/", response_model=list[ComentarioOut])
def listar_comentarios(
    topico_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    q = db.query(TopicoComment)
    if topico_id is not None:
        revisao_service.exigir_revisor_topico(db, current_user, topico_id)
        q = q.filter(TopicoComment.topico_id == topico_id)
    elif current_user.role == "professor":
        # sem filtro de tópico, o professor só enxerga os cursos em que é tutor
        q = (
            q.join(Topico, Topico.id == TopicoComment.topico_id)
            .join(Lesson, Lesson.id == Topico.lesson_id)
            .join(Module, Module.id == Lesson.module_id)
            .join(CourseTutor, CourseTutor.course_id == Module.course_id)
            .filter(CourseTutor.user_id == current_user.id)
        )
    return q.order_by(TopicoComment.created_at).all()


@router.post("/topico-comments/", response_model=ComentarioOut)
def criar_comentario(
    data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    topico = revisao_service.exigir_revisor_topico(db, current_user, data.topico_id)  # 404/403
    if not data.texto and not data.reacao and not data.imagem_sugerida:
        raise HTTPException(400, "Comentário vazio — mande reação, texto ou pedido de imagem.")

    comentario = TopicoComment(
        topico_id=data.topico_id,
        user_id=current_user.id,  # sempre quem está logado — nunca vem do cliente
        slide_index=data.slide_index,
        reacao=data.reacao,
        imagem_sugerida=data.imagem_sugerida,
        sobre_imagem=data.sobre_imagem,
        texto=data.texto,
    )
    db.add(comentario)
    revisao_service.reabrir_se_aprovado(db, topico, current_user)  # ponto novo reabre tópico aprovado
    db.commit()
    db.refresh(comentario)
    return comentario


@router.put("/topico-comments/{comment_id}", response_model=ComentarioOut)
def atualizar_comentario(
    comment_id: int,
    data: ComentarioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    comentario = db.query(TopicoComment).filter(TopicoComment.id == comment_id).first()
    if not comentario:
        raise HTTPException(404, "Comentário não encontrado")
    revisao_service.exigir_revisor_topico(db, current_user, comentario.topico_id)

    if data.texto is not None:
        if comentario.user_id != current_user.id:
            raise HTTPException(403, "Só quem escreveu o comentário pode editar o texto.")
        comentario.texto = data.texto
    if data.resolvido is not None:
        comentario.resolvido = data.resolvido  # qualquer revisor pode marcar resolvido

    db.commit()
    db.refresh(comentario)
    return comentario


# ---- Checklist (aprovação por tópico) ----

@router.get("/topico-checklists/", response_model=list[ChecklistOut])
def listar_checklists(
    topico_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    revisao_service.exigir_revisor_topico(db, current_user, topico_id)
    return (
        db.query(TopicoChecklist)
        .filter(TopicoChecklist.topico_id == topico_id)
        .order_by(TopicoChecklist.updated_at.desc())
        .all()
    )


def _registrar_revisor(db: Session, topico_id: int, nome_revisor: str):
    """Guarda quem revisou por último. NÃO altera Topico.is_approved (visibilidade) — ver docstring do módulo."""
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    topico.reviewed_by = nome_revisor
    db.commit()


@router.put("/topico-checklists/{topico_id}", response_model=ChecklistOut)
def salvar_checklist(
    topico_id: int,
    data: ChecklistUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    topico = revisao_service.exigir_revisor_topico(db, current_user, topico_id)
    if not topico.content:
        raise HTTPException(400, "Este tópico ainda não tem conteúdo pra revisar.")

    registro = (
        db.query(TopicoChecklist)
        .filter(TopicoChecklist.topico_id == topico_id, TopicoChecklist.user_id == current_user.id)
        .first()
    )
    if not registro:
        registro = TopicoChecklist(topico_id=topico_id, user_id=current_user.id)
        db.add(registro)

    registro.profundidade = data.profundidade
    registro.clareza = data.clareza
    registro.qualidade_geral = data.qualidade_geral
    registro.observacao_final = data.observacao_final
    registro.aprovado = data.aprovado
    db.commit()

    _registrar_revisor(db, topico_id, current_user.name or current_user.email)

    db.refresh(registro)
    return registro


# ---- Revisão no próprio tópico (NIA-T-026) ----

@router.get("/topicos/{topico_id}/revisao", response_model=RevisaoTopicoOut)
def obter_revisao(
    topico_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return revisao_service.obter_revisao(db, current_user, topico_id)


@router.post("/topicos/{topico_id}/revisao/aprovar", response_model=RevisaoTopicoOut)
def aprovar_topico(
    topico_id: int,
    data: AprovarTopicoIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return revisao_service.aprovar(db, current_user, topico_id, data.observacao)


@router.post("/topicos/{topico_id}/revisao/enviar-ia", response_model=RevisaoTopicoOut)
def enviar_para_ia(
    topico_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return revisao_service.enviar_ia(db, current_user, topico_id)


@router.post("/topicos/{topico_id}/revisao/ia-revisou", response_model=RevisaoTopicoOut)
def ia_revisou(
    topico_id: int,
    data: IaRevisouIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return revisao_service.ia_revisou(db, current_user, topico_id, data)
