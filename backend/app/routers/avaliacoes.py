from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Avaliacao, Topico, User
from app.renderer.render import render_topico, carregar_temas
from app.renderer.validate import validar_prova
from app.core.auth import get_current_user, usuario_do_token
from app.schemas.avaliacao import ProvaOut, ProvaUpsert
from app.services import acesso_service, prova_service

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])

# Criar/editar prova é só de master/admin (mesmo padrão de lessons.py/topicos.py)
PAPEIS_ADMIN = ("master", "admin")


def _exigir_admin(user: User):
    if user.role not in PAPEIS_ADMIN:
        raise HTTPException(403, "Só master ou admin podem ver ou editar a prova inteira.")


@router.get("/topico/{topico_id}", response_model=ProvaOut)
def obter_prova_do_topico(topico_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """A prova inteira (com o banco e o gabarito) — pro /criar-provas-topicos fazer
    backup antes de trocar. Aluno nunca recebe isso: ele só vê o render da rodada."""
    _exigir_admin(current_user)
    avaliacao = db.query(Avaliacao).filter(Avaliacao.topico_id == topico_id).first()
    if not avaliacao:
        raise HTTPException(404, "Este tópico ainda não tem prova.")
    return avaliacao


@router.put("/topico/{topico_id}", response_model=ProvaOut)
def gravar_prova_do_topico(
    topico_id: int,
    data: ProvaUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cria ou troca a prova do tópico no padrão novo (banco + sorteio,
    docs/processo-topico/PROVA.md). Só grava se o validar_prova() não achar nada."""
    _exigir_admin(current_user)
    if not db.query(Topico).filter(Topico.id == topico_id).first():
        raise HTTPException(404, "Tópico não encontrado.")
    conteudo = {"versao": 2, **data.model_dump(exclude={"aprovada"})}
    problemas = validar_prova(conteudo)
    if problemas:
        raise HTTPException(422, {"mensagem": "A prova não passou na validação.", "problemas": problemas})
    return prova_service.gravar_prova(db, topico_id, conteudo, data.aprovada)


@router.get("/{avaliacao_id}/render", response_class=HTMLResponse)
def render_avaliacao_endpoint(
    avaliacao_id: int,
    theme: str | None = Query(None, description="id do tema (ver docs/schema/temas.json); se omitido, usa a preferência do usuário ou o padrão"),
    user_id: int | None = Query(None, description="se informado, usa User.preferred_theme como fallback quando 'theme' não for passado"),
    token: str | None = Query(None, description="token de escopo curto do iframe (ou de sessão) — exigido em curso privado/não publicado"),
    db: Session = Depends(get_db),
):
    """Renderiza a avaliação (prova final) usando o mesmo template de tópico.
    Constrói um dict 'content' sintético no formato que o template espera a partir
    de Avaliacao.conteudo (JSONB: intro/perguntas/resultado)."""
    avaliacao = db.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(404, "Avaliação not found")
    usuario = usuario_do_token(db, token, aceita_escopo_curto=True)
    acesso_service.exigir_estudo_avaliacao(db, usuario, avaliacao_id)
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
    # Padrão novo: as perguntas sorteadas pra esta pessoa nesta rodada (as mesmas que a
    # correção vai usar); prova antiga: a lista fixa de sempre.
    perguntas = prova_service.perguntas_para(db, avaliacao, usuario.id if usuario else None)
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