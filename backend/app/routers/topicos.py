import json

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Avaliacao, Topico, Lesson, User
from app.renderer.render import render_topico, carregar_temas
from app.core.auth import get_current_user

router = APIRouter(prefix="/topicos", tags=["Topicos"])

# Escrita (criar/editar/apagar conteúdo) exige admin/master — leitura (GET, /render)
# continua pública, é o que o site usa pros alunos. Achado real 2026-09-15: esses
# endpoints ficaram sem nenhuma auth desde sempre, só notado depois do deploy público
# (ver [[nia-infra-gotchas]]). Mesmo padrão de app/routers/governanca.py.
PAPEIS_ADMIN = ("master", "admin")


def _exigir_admin(user: User):
    if user.role not in PAPEIS_ADMIN:
        raise HTTPException(403, "Só master ou admin podem criar/editar/apagar tópicos.")


# Nível novo (2026-08-26): Lesson passa a representar a AULA; cada aula pode
# ter vários Tópicos, cada um com seu próprio conteúdo/geração/revisão —
# mesmo padrão de CRUD+render que já existia em lessons.py, um nível abaixo.

def _com_avaliacao_id(topicos: list[Topico], db: Session) -> list[Topico]:
    """Anexa 'avaliacao_id' (não é coluna do model — atributo solto, o FastAPI
    serializa do jeito que for) em cada Topico, só quando existe uma Avaliacao
    vinculada E aprovada (2026-09-16 — front usa isso pra mostrar/travar o link
    'Prova deste tópico' na árvore do curso)."""
    ids = [t.id for t in topicos]
    aprovadas = (
        db.query(Avaliacao.topico_id, Avaliacao.id)
        .filter(Avaliacao.topico_id.in_(ids), Avaliacao.is_approved.is_(True))
        .all()
    )
    mapa = dict(aprovadas)
    for t in topicos:
        t.avaliacao_id = mapa.get(t.id)
    return topicos


@router.get("/")
def list_topicos(lesson_id: int | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Topico)
    if lesson_id is not None:
        query = query.filter(Topico.lesson_id == lesson_id)
    topicos = query.order_by(Topico.lesson_id, Topico.topico_index).all()
    return _com_avaliacao_id(topicos, db)


@router.post("/")
def create_topico(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
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
    return _com_avaliacao_id([topico], db)[0]


@router.put("/{topico_id}")
def update_topico(topico_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
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
def delete_topico(topico_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
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
