import json

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Topico, Lesson, User
from app.renderer.render import render_topico, carregar_temas

router = APIRouter(prefix="/topicos", tags=["Topicos"])


# Nível novo (2026-08-26): Lesson passa a representar a AULA; cada aula pode
# ter vários Tópicos, cada um com seu próprio conteúdo/geração/revisão —
# mesmo padrão de CRUD+render que já existia em lessons.py, um nível abaixo.

@router.get("/")
def list_topicos(lesson_id: int | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Topico)
    if lesson_id is not None:
        query = query.filter(Topico.lesson_id == lesson_id)
    return query.order_by(Topico.lesson_id, Topico.topico_index).all()


@router.post("/")
def create_topico(data: dict, db: Session = Depends(get_db)):
    if isinstance(data.get("content"), dict):
        data = {**data, "content": json.dumps(data["content"], ensure_ascii=False)}
    topico = Topico(**data)
    db.add(topico)
    db.commit()
    db.refresh(topico)
    return topico


@router.get("/{topico_id}")
def get_topico(topico_id: int, db: Session = Depends(get_db)):
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")
    return topico


@router.put("/{topico_id}")
def update_topico(topico_id: int, data: dict, db: Session = Depends(get_db)):
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")
    if isinstance(data.get("content"), dict):
        data = {**data, "content": json.dumps(data["content"], ensure_ascii=False)}
    for key, value in data.items():
        setattr(topico, key, value)
    db.commit()
    return topico


@router.delete("/{topico_id}")
def delete_topico(topico_id: int, db: Session = Depends(get_db)):
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")
    db.delete(topico)
    db.commit()
    return {"status": "deleted"}


@router.get("/{topico_id}/render", response_class=HTMLResponse)
def render_topico_endpoint(
    topico_id: int,
    theme: str | None = Query(None, description="id do tema (ver docs/schema/temas.json); se omitido, usa a preferência do usuário ou o padrão"),
    user_id: int | None = Query(None, description="se informado, usa User.preferred_theme como fallback quando 'theme' não for passado"),
    db: Session = Depends(get_db),
):
    """Mesma lógica de GET /lessons/{id}/render (Fase 4), um nível abaixo: o JSON
    salvo em Topico.content nunca muda, só o tema passado pro renderizador."""
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico not found")
    if not topico.content:
        raise HTTPException(409, "Este tópico ainda não tem conteúdo gerado.")

    theme_id = theme
    if not theme_id and user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.preferred_theme:
            theme_id = user.preferred_theme
    theme_id = theme_id or "vidro-fume"

    temas_disponiveis = carregar_temas()
    if theme_id not in temas_disponiveis:
        raise HTTPException(400, f"Tema '{theme_id}' não existe. Disponíveis: {list(temas_disponiveis.keys())}")

    try:
        content = json.loads(topico.content)
    except (TypeError, json.JSONDecodeError):
        raise HTTPException(500, "Topico.content não é um JSON válido do schema de tópico.")

    html = render_topico(content, theme_id)
    return HTMLResponse(content=html)
