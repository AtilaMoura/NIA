"""Agregados da página Pessoas do Master (2026-09-28).

Tudo em Python sobre poucas consultas — o volume é de dezenas de pessoas, não
vale uma query agregada complicada. Só leitura.
"""

from sqlalchemy.orm import Session

from app.models.models import (
    Avaliacao,
    AvaliacaoProgress,
    Course,
    Lesson,
    Module,
    Topico,
    TopicoProgress,
    User,
)
from app.schemas.pessoas import PessoaDetalhe, PessoaResumo, TopicoDaPessoa


def _mais_recente(*datas):
    validas = [d for d in datas if d is not None]
    return max(validas) if validas else None


def _datas_de(registro):
    return (
        registro.updated_at,
        registro.iniciado_em,
        registro.concluido_em,
        registro.avaliado_em,
        registro.ultimo_sinal_em,
    )


def _resumo(user: User, tps: list[TopicoProgress], aps: list[AvaliacaoProgress]) -> PessoaResumo:
    ultima = _mais_recente(*(d for r in (*tps, *aps) for d in _datas_de(r)))
    return PessoaResumo(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        cadastro_em=user.created_at,
        ultimo_login=user.last_login,
        ultima_atividade=ultima,
        topicos_iniciados=sum(1 for r in tps if r.status != "nao_iniciado" or r.iniciado_em),
        topicos_concluidos=sum(1 for r in tps if r.status == "concluido"),
        provas_feitas=sum(1 for r in aps if r.status == "concluido"),
        tempo_s=sum((r.time_spent_s or 0) for r in (*tps, *aps)),
    )


def listar_pessoas(db: Session) -> list[PessoaResumo]:
    usuarios = db.query(User).all()
    tps_por_user: dict[int, list[TopicoProgress]] = {}
    for r in db.query(TopicoProgress).all():
        tps_por_user.setdefault(r.user_id, []).append(r)
    aps_por_user: dict[int, list[AvaliacaoProgress]] = {}
    for r in db.query(AvaliacaoProgress).all():
        aps_por_user.setdefault(r.user_id, []).append(r)

    pessoas = [_resumo(u, tps_por_user.get(u.id, []), aps_por_user.get(u.id, [])) for u in usuarios]

    # Mais recente primeiro (atividade ou login); quem nunca fez nada vai pro fim
    def _chave(p: PessoaResumo) -> float:
        d = _mais_recente(p.ultima_atividade, p.ultimo_login)
        return d.timestamp() if d else 0.0

    pessoas.sort(key=_chave, reverse=True)
    return pessoas


def detalhe_pessoa(db: Session, user_id: int) -> PessoaDetalhe | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    tps = db.query(TopicoProgress).filter(TopicoProgress.user_id == user_id).all()
    aps = db.query(AvaliacaoProgress).filter(AvaliacaoProgress.user_id == user_id).all()

    # Prova de cada tópico (Avaliacao.topico_id é único)
    prova_por_topico: dict[int, AvaliacaoProgress] = {}
    if aps:
        ids_av = {a.avaliacao_id for a in aps}
        topico_da_av = dict(
            db.query(Avaliacao.id, Avaliacao.topico_id).filter(Avaliacao.id.in_(ids_av)).all()
        )
        for a in aps:
            tid = topico_da_av.get(a.avaliacao_id)
            if tid is not None:
                prova_por_topico[tid] = a

    # Título do tópico + curso (tópico → aula → módulo → curso)
    info: dict[int, tuple] = {}
    if tps:
        linhas = (
            db.query(Topico.id, Topico.titulo, Course.id, Course.title, Module.module_index, Lesson.lesson_index, Topico.topico_index)
            .join(Lesson, Topico.lesson_id == Lesson.id)
            .join(Module, Lesson.module_id == Module.id)
            .join(Course, Module.course_id == Course.id)
            .filter(Topico.id.in_({r.topico_id for r in tps}))
            .all()
        )
        info = {l[0]: l for l in linhas}

    topicos: list[TopicoDaPessoa] = []
    for r in tps:
        i = info.get(r.topico_id)
        if not i:
            continue
        prova = prova_por_topico.get(r.topico_id)
        topicos.append(
            TopicoDaPessoa(
                topico_id=r.topico_id,
                titulo=i[1],
                course_id=i[2],
                curso=i[3],
                status=r.status,
                iniciado_em=r.iniciado_em,
                concluido_em=r.concluido_em,
                ultimo_slide=r.ultimo_slide,
                tempo_s=(r.time_spent_s or 0) + ((prova.time_spent_s or 0) if prova else 0),
                tutor_veredito=r.tutor_veredito,
                prova_status=prova.status if prova else None,
                prova_veredito=prova.tutor_veredito if prova else None,
            )
        )
    # Ordem do curso: curso, módulo, aula, tópico
    ordem = {tid: (l[2], l[4], l[5], l[6]) for tid, l in info.items()}
    topicos.sort(key=lambda t: ordem.get(t.topico_id, (0, 0, 0, 0)))

    resumo = _resumo(user, tps, aps)
    return PessoaDetalhe(**resumo.model_dump(), topicos=topicos)
