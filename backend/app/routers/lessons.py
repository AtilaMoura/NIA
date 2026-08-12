import json

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lesson, User
from app.renderer.render import render_topico, carregar_temas

router = APIRouter(prefix="/lessons", tags=["Lessons"])


# Criar lição (content é o JSON estruturado — ver docs/schema/ — guardado como texto)
@router.post("/")
def create_lesson(data: dict, db: Session = Depends(get_db)):
    if isinstance(data.get("content"), dict):
        data = {**data, "content": json.dumps(data["content"], ensure_ascii=False)}
    lesson = Lesson(**data)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson


@router.get("/{lesson_id}/render", response_class=HTMLResponse)
def render_lesson(
    lesson_id: int,
    theme: str | None = Query(None, description="id do tema (ver docs/schema/temas.json); se omitido, usa a preferência do usuário ou o padrão"),
    user_id: int | None = Query(None, description="se informado, usa User.preferred_theme como fallback quando 'theme' não for passado"),
    db: Session = Depends(get_db),
):
    """
    Fase 4 — mesma lição, tema escolhido na hora, sem regenerar conteúdo:
    o JSON salvo em Lesson.content nunca muda, só o parâmetro de tema passado
    pro renderizador (Fase 1).
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

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
        content = json.loads(lesson.content)
    except (TypeError, json.JSONDecodeError):
        raise HTTPException(500, "Lesson.content não é um JSON válido do schema de tópico.")

    html = render_topico(content, theme_id)
    return HTMLResponse(content=html)


@router.put("/{lesson_id}")
def update_lesson(lesson_id: int, data: dict, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    if isinstance(data.get("content"), dict):
        data = {**data, "content": json.dumps(data["content"], ensure_ascii=False)}
    for key, value in data.items():
        setattr(lesson, key, value)
    db.commit()
    return lesson


@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"status": "deleted"}


@router.get("/temas/catalogo")
def listar_temas():
    """Catálogo de temas disponíveis (docs/schema/temas.json) — pro frontend montar o seletor."""
    return carregar_temas()
