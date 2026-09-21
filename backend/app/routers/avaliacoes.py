from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Avaliacao, User
from app.renderer.render import render_topico, carregar_temas

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])


@router.get("/{avaliacao_id}/render", response_class=HTMLResponse)
def render_avaliacao_endpoint(
    avaliacao_id: int,
    theme: str | None = Query(None, description="id do tema (ver docs/schema/temas.json); se omitido, usa a preferência do usuário ou o padrão"),
    user_id: int | None = Query(None, description="se informado, usa User.preferred_theme como fallback quando 'theme' não for passado"),
    db: Session = Depends(get_db),
):
    """Renderiza a avaliação (prova final) usando o mesmo template de tópico.
    Constrói um dict 'content' sintético no formato que o template espera a partir
    de Avaliacao.conteudo (JSONB: intro/perguntas/resultado)."""
    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(404, "Avaliação not found")
    if not avaliacao.is_approved:
        raise HTTPException(409, "Esta avaliação ainda não tem conteúdo aprovado.")

    theme_id = theme
    if not theme_id and user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.preferred_theme:
            theme_id = user.preferred_theme
    theme_id = theme_id or "vidro-fume"

    temas_disponiveis = carregar_temas()
    if theme_id not in temas_disponiveis:
        raise HTTPException(400, f"Tema '{theme_id}' não existe. Disponíveis: {list(temas_disponiveis.keys())}")

    intro = avaliacao.conteudo.get("intro", {})
    perguntas = avaliacao.conteudo.get("perguntas", [])
    resultado = avaliacao.conteudo.get("resultado", {})

    content = {
        "topico_id": f"avaliacao-{avaliacao.id}",
        "titulo": f"{avaliacao.topico.titulo} — Prova",
        "numero": avaliacao.topico.topico_index,
        "roteiro": [],
        "badges_capa": [],
        "imagem_capa": None,
        "slides": [
            {"tipo": "avaliacao_intro", "secao": "Avaliação Final", **intro},
            *[
                {"tipo": "avaliacao_pergunta", "secao": "Avaliação Final", "gate_id": p["id"], "pergunta": p}
                for p in perguntas
            ],
            {"tipo": "resultado", "secao": "Resultado", **resultado},
        ],
    }

    html = render_topico(content, theme_id)
    return HTMLResponse(content=html)