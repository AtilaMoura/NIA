"""Área de estudo do próprio usuário (2026-10-04): todas as anotações dele
organizadas por curso/tópico/slide, e o resumo da /estudos (tempo por curso,
onde parou, semana, sequência de dias). Só leitura.
"""

import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.models import (
    Course,
    Lesson,
    Module,
    TempoEstudoDia,
    Topico,
    TopicoAnotacao,
    TopicoProgress,
)
from app.schemas.estudo import (
    AnotacaoMinha,
    DiaEstudo,
    ResumoCurso,
    ResumoEstudo,
    UltimoTopico,
)
from app.services.tempo_estudo import FUSO_BRASILIA


def _slides(conteudo: str | None) -> list:
    if not conteudo:
        return []
    try:
        return json.loads(conteudo).get("slides") or []
    except (ValueError, AttributeError):
        return []


def _info_topicos(db: Session, ids: set[int]) -> dict[int, tuple]:
    """topico_id -> (titulo, content, course_id, curso, module_index, modulo, lesson_index, topico_index, lesson_id, aula)"""
    if not ids:
        return {}
    linhas = (
        db.query(
            Topico.id, Topico.titulo, Topico.content, Course.id, Course.title,
            Module.module_index, Module.title, Lesson.lesson_index, Topico.topico_index,
            Lesson.id, Lesson.title,
        )
        .join(Lesson, Topico.lesson_id == Lesson.id)
        .join(Module, Lesson.module_id == Module.id)
        .join(Course, Module.course_id == Course.id)
        .filter(Topico.id.in_(ids))
        .all()
    )
    return {l[0]: tuple(l[1:]) for l in linhas}


def _anotacoes_com_texto(db: Session, user_id: int) -> list[TopicoAnotacao]:
    # Texto vazio = anotação "apagada" na UI (a linha fica, padrão do projeto)
    notas = db.query(TopicoAnotacao).filter(TopicoAnotacao.user_id == user_id).all()
    return [n for n in notas if (n.texto or "").strip()]


def minhas_anotacoes(db: Session, user_id: int) -> list[AnotacaoMinha]:
    notas = _anotacoes_com_texto(db, user_id)
    info = _info_topicos(db, {n.topico_id for n in notas})

    saida: list[tuple[tuple, AnotacaoMinha]] = []
    for n in notas:
        i = info.get(n.topico_id)
        if not i:
            continue
        titulo, conteudo, course_id, curso, mod_idx, modulo, aula_idx, top_idx, lesson_id, aula = i
        slides = _slides(conteudo)
        slide = slides[n.slide_index] if 0 <= n.slide_index < len(slides) else None
        saida.append((
            (course_id, mod_idx, aula_idx, top_idx, n.slide_index),
            AnotacaoMinha(
                topico_id=n.topico_id,
                topico_titulo=titulo,
                course_id=course_id,
                curso=curso,
                modulo_index=mod_idx,
                modulo_titulo=modulo,
                lesson_id=lesson_id,
                aula_index=aula_idx,
                aula_titulo=aula,
                slide_index=n.slide_index,
                slide_titulo=slide.get("titulo") if isinstance(slide, dict) else None,
                texto=n.texto,
                atualizado_em=n.updated_at or n.created_at,
            ),
        ))
    saida.sort(key=lambda x: x[0])
    return [a for _, a in saida]


def _quando(r: TopicoProgress):
    datas = [d for d in (r.ultimo_sinal_em, r.updated_at, r.concluido_em, r.iniciado_em) if d]
    return max(datas) if datas else None


def resumo_estudo(db: Session, user_id: int) -> ResumoEstudo:
    tps = db.query(TopicoProgress).filter(TopicoProgress.user_id == user_id).all()
    notas = _anotacoes_com_texto(db, user_id)
    info = _info_topicos(db, {r.topico_id for r in tps} | {n.topico_id for n in notas})

    agora = datetime.now(FUSO_BRASILIA)
    limite = agora - timedelta(days=7)
    cursos: dict[int, ResumoCurso] = {}

    def _curso(topico_id: int) -> ResumoCurso | None:
        i = info.get(topico_id)
        if not i:
            return None
        return cursos.setdefault(i[2], ResumoCurso(course_id=i[2]))

    for n in notas:
        c = _curso(n.topico_id)
        if c:
            c.anotacoes += 1

    # Onde parou em cada curso = tópico com a atividade mais recente
    ultimo_por_curso: dict[int, TopicoProgress] = {}
    for r in tps:
        c = _curso(r.topico_id)
        if not c:
            continue
        c.tempo_s += r.time_spent_s or 0
        if r.concluido_em and r.concluido_em >= limite:
            c.concluidos_semana += 1
        if r.tutor_veredito == "reforco":
            c.reforcar.append(info[r.topico_id][0])
        q = _quando(r)
        atual = ultimo_por_curso.get(c.course_id)
        if q and (atual is None or q > _quando(atual)):
            ultimo_por_curso[c.course_id] = r

    for course_id, r in ultimo_por_curso.items():
        titulo, conteudo = info[r.topico_id][0], info[r.topico_id][1]
        cursos[course_id].ultimo = UltimoTopico(
            topico_id=r.topico_id,
            titulo=titulo,
            ultimo_slide=r.ultimo_slide,
            total_slides=len(_slides(conteudo)) or None,
            atualizado_em=_quando(r),
        )

    # Semana (horário de Brasília)
    hoje = agora.date()
    inicio = hoje - timedelta(days=6)
    por_dia = {
        d.dia: d.segundos
        for d in db.query(TempoEstudoDia)
        .filter(TempoEstudoDia.user_id == user_id, TempoEstudoDia.dia >= hoje - timedelta(days=366))
        .all()
    }
    dias = [
        DiaEstudo(dia=inicio + timedelta(days=k), segundos=por_dia.get(inicio + timedelta(days=k), 0))
        for k in range(7)
    ]

    # Sequência: conta pra trás a partir de hoje (ou de ontem, se hoje ainda não estudou)
    sequencia = 0
    dia = hoje if por_dia.get(hoje) else hoje - timedelta(days=1)
    while por_dia.get(dia):
        sequencia += 1
        dia -= timedelta(days=1)

    return ResumoEstudo(
        cursos=list(cursos.values()),
        dias=dias,
        tempo_semana_s=sum(d.segundos for d in dias),
        concluidos_semana=sum(c.concluidos_semana for c in cursos.values()),
        sequencia_dias=sequencia,
    )
