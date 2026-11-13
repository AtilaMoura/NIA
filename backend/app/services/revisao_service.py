"""Regras da revisão de conteúdo no tópico (NIA-T-026).

Estados: pendente -> (revisor pontua) -> enviado_ia -> (IA corrige e marca) -> pendente -> aprovado.
`Topico.is_approved` é VISIBILIDADE e NUNCA é alterado aqui; o estado da revisão é `Topico.revisao_status`.
Permissão: master/admin em qualquer curso; professor só se for CourseTutor do curso do tópico.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import (
    CourseTutor, Lesson, Module, Topico, TopicoAnotacao, TopicoAnotacaoTratada,
    TopicoComment, TopicoRevisaoEvento, User,
)
from app.schemas.revisao import (
    AnotacaoRevisaoOut, EventoRevisaoOut, IaRevisouIn, PontoRevisaoOut, RevisaoTopicoOut,
)

PAPEIS_ADMIN = ("master", "admin")
PAPEIS_REVISOR = ("master", "admin", "professor")


# ---- Permissão ----

def curso_do_topico(db: Session, topico_id: int) -> int | None:
    """topico -> lesson -> module.course_id."""
    return (
        db.query(Module.course_id)
        .join(Lesson, Lesson.module_id == Module.id)
        .join(Topico, Topico.lesson_id == Lesson.id)
        .filter(Topico.id == topico_id)
        .scalar()
    )


def pode_revisar_curso(db: Session, user: User, course_id: int | None) -> bool:
    if user.role in PAPEIS_ADMIN:
        return True
    if user.role != "professor" or course_id is None:
        return False
    return (
        db.query(CourseTutor.id)
        .filter(CourseTutor.course_id == course_id, CourseTutor.user_id == user.id)
        .first()
        is not None
    )


def exigir_revisor_topico(db: Session, user: User, topico_id: int) -> Topico:
    """404 se o tópico não existe; 403 se o usuário não pode revisar o curso dele."""
    topico = db.query(Topico).filter(Topico.id == topico_id).first()
    if not topico:
        raise HTTPException(404, "Tópico não encontrado")
    if user.role not in PAPEIS_REVISOR:
        raise HTTPException(403, "Só master, admin ou professor acessam a área de revisão.")
    if not pode_revisar_curso(db, user, curso_do_topico(db, topico_id)):
        raise HTTPException(403, "Você não é tutor do curso deste tópico.")
    return topico


# ---- Eventos e estado ----

def _evento(db: Session, topico_id: int, user_id: int, acao: str, observacao: str | None = None):
    db.add(TopicoRevisaoEvento(topico_id=topico_id, user_id=user_id, acao=acao, observacao=observacao))


def reabrir_se_aprovado(db: Session, topico: Topico, user: User):
    """Ponto novo num tópico já aprovado: volta para pendente (com evento 'reabrir').
    Quem chama faz o commit."""
    if topico.revisao_status == "aprovado":
        topico.revisao_status = "pendente"
        _evento(db, topico.id, user.id, "reabrir", "Novo ponto de revisão")


def _revisores_do_curso(db: Session, course_id: int | None) -> list[int]:
    """Ids dos usuários que podem revisar o curso (master/admin + professores tutores)."""
    ids = [u for (u,) in db.query(User.id).filter(User.role.in_(PAPEIS_ADMIN)).all()]
    if course_id is not None:
        ids += [u for (u,) in db.query(CourseTutor.user_id).filter(CourseTutor.course_id == course_id).all()]
    return list(set(ids))


def _carimbo(a: TopicoAnotacao):
    return a.updated_at or a.created_at


def _anotacao_tratada(a: TopicoAnotacao) -> bool:
    """Tratada só se existe tratamento e a anotação não foi editada depois do que a IA viu."""
    t = a.tratamento[0] if a.tratamento else None
    if t is None or t.updated_at_visto is None:
        return False
    carimbo = _carimbo(a)
    return carimbo is None or carimbo <= t.updated_at_visto


def _anotacoes_de_revisores(db: Session, topico: Topico) -> list[TopicoAnotacao]:
    ids = _revisores_do_curso(db, curso_do_topico(db, topico.id))
    if not ids:
        return []
    return (
        db.query(TopicoAnotacao)
        .filter(TopicoAnotacao.topico_id == topico.id, TopicoAnotacao.user_id.in_(ids))
        .order_by(TopicoAnotacao.slide_index, TopicoAnotacao.id)
        .all()
    )


def _anotacoes_pendentes(db: Session, topico: Topico) -> list[TopicoAnotacao]:
    # anotação esvaziada (texto vazio) some da UI e não conta como ponto
    return [a for a in _anotacoes_de_revisores(db, topico) if (a.texto or "").strip() and not _anotacao_tratada(a)]


def _pontos_abertos(db: Session, topico_id: int) -> list[TopicoComment]:
    return (
        db.query(TopicoComment)
        .filter(TopicoComment.topico_id == topico_id, TopicoComment.resolvido.isnot(True))
        .all()
    )


# ---- Leitura ----

def obter_revisao(db: Session, user: User, topico_id: int) -> RevisaoTopicoOut:
    topico = exigir_revisor_topico(db, user, topico_id)
    nomes: dict[int, str | None] = {}

    def nome(uid):
        if uid not in nomes:
            u = db.query(User).filter(User.id == uid).first()
            nomes[uid] = (u.name or u.email) if u else None
        return nomes[uid]

    comentarios = (
        db.query(TopicoComment).filter(TopicoComment.topico_id == topico_id)
        .order_by(TopicoComment.created_at, TopicoComment.id).all()
    )
    pontos = [
        PontoRevisaoOut(
            id=c.id, user_id=c.user_id, autor=nome(c.user_id), slide_index=c.slide_index, texto=c.texto,
            reacao=c.reacao, resolvido=bool(c.resolvido), resposta_ia=c.resposta_ia, created_at=c.created_at,
        )
        for c in comentarios
    ]
    anotacoes = [
        AnotacaoRevisaoOut(
            id=a.id, user_id=a.user_id, autor=nome(a.user_id), slide_index=a.slide_index, texto=a.texto or "",
            tratada=_anotacao_tratada(a), resposta_ia=(a.tratamento[0].resposta_ia if a.tratamento else None),
            updated_at=_carimbo(a),
        )
        for a in _anotacoes_de_revisores(db, topico) if (a.texto or "").strip()
    ]
    eventos_db = (
        db.query(TopicoRevisaoEvento).filter(TopicoRevisaoEvento.topico_id == topico_id)
        .order_by(TopicoRevisaoEvento.created_at, TopicoRevisaoEvento.id).all()
    )
    eventos = [
        EventoRevisaoOut(id=e.id, user_id=e.user_id, autor=nome(e.user_id), acao=e.acao,
                         observacao=e.observacao, created_at=e.created_at)
        for e in eventos_db
    ]
    aprovado_por = aprovado_em = None
    if topico.revisao_status == "aprovado":
        ultimo = next((e for e in reversed(eventos_db) if e.acao == "aprovar"), None)
        if ultimo:
            aprovado_por, aprovado_em = nome(ultimo.user_id), ultimo.created_at

    abertos = sum(1 for p in pontos if not p.resolvido) + sum(1 for a in anotacoes if not a.tratada)
    return RevisaoTopicoOut(
        topico_id=topico_id, status=topico.revisao_status or "pendente", pode_revisar=True,
        aprovado_por=aprovado_por, aprovado_em=aprovado_em, abertos=abertos,
        pontos=pontos, anotacoes=anotacoes, eventos=eventos,
    )


# ---- Ações ----

def aprovar(db: Session, user: User, topico_id: int, observacao: str | None) -> RevisaoTopicoOut:
    topico = exigir_revisor_topico(db, user, topico_id)
    topico.revisao_status = "aprovado"
    _evento(db, topico.id, user.id, "aprovar", observacao)
    db.commit()
    return obter_revisao(db, user, topico_id)


def enviar_ia(db: Session, user: User, topico_id: int) -> RevisaoTopicoOut:
    topico = exigir_revisor_topico(db, user, topico_id)
    if not _pontos_abertos(db, topico_id) and not _anotacoes_pendentes(db, topico):
        raise HTTPException(400, "Não há ponto aberto nem anotação de revisor pendente para enviar à IA.")
    topico.revisao_status = "enviado_ia"
    _evento(db, topico.id, user.id, "enviar_ia")
    db.commit()
    return obter_revisao(db, user, topico_id)


def ia_revisou(db: Session, user: User, topico_id: int, data: IaRevisouIn) -> RevisaoTopicoOut:
    """Marca pontos como resolvidos e anotações como tratadas; o status volta a 'pendente'
    para o revisor conferir. Valida tudo antes de gravar qualquer coisa."""
    topico = exigir_revisor_topico(db, user, topico_id)

    comentarios = []
    for p in data.pontos:
        c = db.query(TopicoComment).filter(TopicoComment.id == p.comment_id).first()
        if not c or c.topico_id != topico_id:
            raise HTTPException(400, f"Ponto {p.comment_id} não pertence a este tópico.")
        comentarios.append((c, p.resposta_ia))

    validas = {a.id: a for a in _anotacoes_de_revisores(db, topico)}
    anotacoes = []
    for t in data.anotacoes:
        a = validas.get(t.anotacao_id)
        if not a:
            raise HTTPException(400, f"Anotação {t.anotacao_id} não é de revisor deste tópico.")
        anotacoes.append((a, t.resposta_ia))

    for c, resposta in comentarios:
        c.resolvido = True
        c.resposta_ia = resposta
    for a, resposta in anotacoes:
        if a.tratamento:
            a.tratamento[0].updated_at_visto = _carimbo(a)
            a.tratamento[0].resposta_ia = resposta
        else:
            db.add(TopicoAnotacaoTratada(anotacao_id=a.id, updated_at_visto=_carimbo(a), resposta_ia=resposta))

    topico.revisao_status = "pendente"
    _evento(db, topico.id, user.id, "ia_revisou",
            f"{len(comentarios)} ponto(s) e {len(anotacoes)} anotação(ões) tratados pela IA")
    db.commit()
    return obter_revisao(db, user, topico_id)
