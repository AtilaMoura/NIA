"""Área de revisão do professor (FASE 5a do front Emaús). Anotação por SLIDE
(sincronizada com o <iframe> do render via postMessage) + checklist de
aprovação/reprovação por tópico. Tudo exige login com papel master/admin/professor —
nunca aluno, nunca sem token (mesmo padrão de app/routers/topico_progress.py).

Regra de aprovação NESTA fase: 1 checklist com aprovado=True de qualquer papel
elevado já libera o tópico pro aluno (Topico.is_approved). A regra de quórum por
curso (vários tutores atribuídos, todos vs. um, master aprova sozinho) é a FASE 5b —
ainda não existe tabela de tutores/curso pra decidir isso de verdade.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Topico, TopicoComment, TopicoChecklist, User
from app.core.auth import get_current_user
from app.schemas.revisao import (
    ComentarioCreate,
    ComentarioUpdate,
    ComentarioOut,
    ChecklistUpsert,
    ChecklistOut,
)

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
        q = q.filter(TopicoComment.topico_id == topico_id)
    return q.order_by(TopicoComment.created_at).all()


@router.post("/topico-comments/", response_model=ComentarioOut)
def criar_comentario(
    data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _exigir_revisor(current_user)
    if not db.query(Topico).filter(Topico.id == data.topico_id).first():
        raise HTTPException(404, "Tópico não encontrado")
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
    return (
        db.query(TopicoChecklist)
        .filter(TopicoChecklist.topico_id == topico_id)
        .order_by(TopicoChecklist.updated_at.desc())
        .all()
    )


def _recalcular_aprovacao(db: Session, topico_id: int, nome_revisor: str):
    """1 aprovação de papel elevado já libera nesta fase — ver docstring do módulo."""
    tem_aprovacao = (
        db.query(TopicoChecklist)
        .filter(TopicoChecklist.topico_id == topico_id, TopicoChecklist.aprovado.is_(True))
        .first()
        is not None
    )
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    topico.is_approved = tem_aprovacao
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
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico não encontrado")
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

    _recalcular_aprovacao(db, topico_id, current_user.name or current_user.email)

    db.refresh(registro)
    return registro
