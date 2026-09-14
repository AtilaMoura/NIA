"""Anotações pessoais do aluno por tópico/slide (2026-09-10).

Diferente de TopicoComment (ferramenta do revisor/professor, FASE 5a): aqui é
o próprio aluno anotando enquanto estuda. 1 linha por (usuário, tópico, slide)
— upsert, sem DELETE (padrão do projeto). Aceita token de escopo curto do
<iframe> OU token de sessão real (ver get_topico_anotacao_user_id) — os dois
contextos leem/escrevem o mesmo dado.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_topico_anotacao_user_id
from app.database import get_db
from app.models.models import Topico, TopicoAnotacao
from app.schemas.topico_anotacoes import TopicoAnotacaoOut, TopicoAnotacaoUpsert

router = APIRouter(prefix="/topico-anotacoes", tags=["Topico Anotações"])


@router.get("/{topico_id}", response_model=list[TopicoAnotacaoOut])
def listar_anotacoes(
    topico_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_anotacao_user_id),
):
    """Anotações do próprio aluno neste tópico — usado tanto pelo <iframe> (pra
    preencher cada slide ao reabrir) quanto pelo painel "Minhas anotações" do
    Emaús (Server Component, com o token de sessão real)."""
    return (
        db.query(TopicoAnotacao)
        .filter(TopicoAnotacao.user_id == user_id, TopicoAnotacao.topico_id == topico_id)
        .order_by(TopicoAnotacao.slide_index)
        .all()
    )


@router.put("/{topico_id}/{slide_index}", response_model=TopicoAnotacaoOut)
def salvar_anotacao(
    topico_id: int,
    slide_index: int,
    data: TopicoAnotacaoUpsert,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_topico_anotacao_user_id),
):
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico not found")

    def _buscar():
        return (
            db.query(TopicoAnotacao)
            .filter(
                TopicoAnotacao.user_id == user_id,
                TopicoAnotacao.topico_id == topico_id,
                TopicoAnotacao.slide_index == slide_index,
            )
            .first()
        )

    registro = _buscar()
    if registro:
        registro.texto = data.texto
        db.commit()
    else:
        registro = TopicoAnotacao(
            user_id=user_id, topico_id=topico_id, slide_index=slide_index, texto=data.texto,
        )
        db.add(registro)
        try:
            db.commit()
        except IntegrityError:
            # mesma corrida do topico_respostas (2 salvamentos quase simultâneos
            # do mesmo slide) — trata como upsert de verdade.
            db.rollback()
            registro = _buscar()
            if not registro:
                raise
            registro.texto = data.texto
            db.commit()

    db.refresh(registro)
    return registro
