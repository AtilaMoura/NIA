"""Prova do tópico no padrão novo (2026-10-07, docs/processo-topico/PROVA.md).

A prova guarda um BANCO de perguntas maior que a prova e cada rodada sorteia um
conjunto menor — ao refazer, as perguntas mudam (pedido do Atila). O sorteio é
fixo por (prova, pessoa, rodada): recarregar a página mostra as mesmas perguntas,
e a correção (pipeline.py) usa exatamente o mesmo conjunto. Não precisa de tabela
nova: dá pra recalcular a qualquer hora.

Prova antiga (sem "banco") continua como sempre: a lista fixa "perguntas".

Formato novo de Avaliacao.conteudo:
    {
      "versao": 2,
      "intro": {...}, "resultado": {...},
      "banco": [Pergunta + "assunto"],        # 18–24 perguntas
      "por_rodada": 6..8,                     # quantas cada rodada sorteia
      "nota_minima": 0.6 | 0.7,               # fração pra passar (regra do curso)
      "tipos_minimos": {"ditado": 1, ...}     # opcional: garantido em toda rodada
    }
"""

import random
from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.models import Avaliacao, AvaliacaoProgress

NOTA_MINIMA_PADRAO = 0.6  # provas antigas: 3 de 5 (decisão do Atila, 2026-09-23)


def tem_banco(conteudo: dict | None) -> bool:
    return bool((conteudo or {}).get("banco"))


def nota_minima(conteudo: dict | None) -> float:
    """Fração mínima pra passar — vem da própria prova (regra do curso); 60% nas antigas."""
    valor = (conteudo or {}).get("nota_minima")
    return float(valor) if valor else NOTA_MINIMA_PADRAO


def rodada_atual(db: Session, user_id: int | None, avaliacao_id: int) -> int:
    if not user_id:
        return 1
    registro = (
        db.query(AvaliacaoProgress)
        .filter(AvaliacaoProgress.user_id == user_id, AvaliacaoProgress.avaliacao_id == avaliacao_id)
        .first()
    )
    return (registro.rodada_atual or 1) if registro else 1


def _sortear(banco: list[dict], n: int, tipos_minimos: dict, evitar: set[str], rng: random.Random) -> list[dict]:
    """Escolhe n perguntas do banco: primeiro os tipos obrigatórios, depois um
    rodízio entre os assuntos (cada assunto aparece antes de algum repetir),
    preferindo um tipo de pergunta ainda não escolhido. Perguntas da rodada
    anterior (evitar) só entram se faltar pergunta nova."""
    n = min(n, len(banco))
    escolhidas: list[dict] = []
    ids_escolhidos: set[str] = set()

    def candidatas(filtro) -> list[dict]:
        livres = [p for p in banco if p["id"] not in ids_escolhidos and filtro(p)]
        novas = [p for p in livres if p["id"] not in evitar]
        rng.shuffle(novas)
        repetidas = [p for p in livres if p["id"] in evitar]
        rng.shuffle(repetidas)
        return novas + repetidas

    def escolher(p: dict) -> None:
        escolhidas.append(p)
        ids_escolhidos.add(p["id"])

    # 1. Tipos garantidos em toda rodada (ex.: Inglês = 1 ditado + 1 escrita)
    for tipo, qtd in sorted(tipos_minimos.items()):
        for p in candidatas(lambda q, t=tipo: q.get("tipo") == t)[:qtd]:
            if len(escolhidas) < n:
                escolher(p)

    # 2. Equilíbrio entre assuntos, variando o tipo de pergunta. A cada passo entra o
    # assunto com MENOS perguntas já escolhidas — inclusive as do passo 1 (antes era
    # um rodízio cego, e a aberta obrigatória deixava a rodada 2/1/3 em vez de 2/2/2;
    # achado no piloto T33/T66, 2026-10-07). Empate: a ordem sorteada dos assuntos.
    assuntos = sorted({p.get("assunto") or "" for p in banco})
    rng.shuffle(assuntos)
    while len(escolhidas) < n:
        contagem = {a: 0 for a in assuntos}
        for p in escolhidas:
            contagem[p.get("assunto") or ""] += 1
        escolheu = False
        for assunto in sorted(assuntos, key=lambda a: contagem[a]):  # sort estável
            cands = candidatas(lambda q, a=assunto: (q.get("assunto") or "") == a)
            if not cands:
                continue
            tipos_ja = {p.get("tipo") for p in escolhidas}
            cands.sort(key=lambda q: (q["id"] in evitar, q.get("tipo") in tipos_ja))  # sort estável
            escolher(cands[0])
            escolheu = True
            break
        if not escolheu:
            break

    # Mantém a ordem em que o banco foi escrito (segue a ordem do tópico)
    ordem = {p["id"]: i for i, p in enumerate(banco)}
    return sorted(escolhidas, key=lambda p: ordem[p["id"]])


def perguntas_da_rodada(conteudo: dict | None, avaliacao_id: int, user_id: int | None, rodada: int) -> list[dict]:
    """As perguntas que esta pessoa vê nesta rodada (determinístico)."""
    conteudo = conteudo or {}
    if not tem_banco(conteudo):
        return list(conteudo.get("perguntas", []))
    banco = conteudo["banco"]
    n = int(conteudo.get("por_rodada") or len(banco))
    tipos_minimos = conteudo.get("tipos_minimos") or {}
    anterior: set[str] = set()
    atual: list[dict] = []
    # Recalcula da rodada 1 até a atual, pra cada uma evitar a anterior
    for r in range(1, max(1, rodada) + 1):
        rng = random.Random(f"prova:{avaliacao_id}:{user_id or 0}:{r}")
        atual = _sortear(banco, n, tipos_minimos, anterior, rng)
        anterior = {p["id"] for p in atual}
    return atual


def perguntas_para(db: Session, avaliacao: Avaliacao, user_id: int | None) -> list[dict]:
    return perguntas_da_rodada(avaliacao.conteudo, avaliacao.id, user_id,
                               rodada_atual(db, user_id, avaliacao.id))


def gravar_prova(db: Session, topico_id: int, conteudo: dict, aprovada: bool) -> Avaliacao:
    """Cria ou atualiza a prova do tópico (1:1). Nada é apagado: as respostas
    antigas continuam no banco, ligadas à rodada delas."""
    avaliacao = db.query(Avaliacao).filter(Avaliacao.topico_id == topico_id).first()
    if avaliacao:
        avaliacao.conteudo = conteudo
        avaliacao.is_approved = aprovada
    else:
        avaliacao = Avaliacao(topico_id=topico_id, conteudo=conteudo, is_approved=aprovada)
        db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    return avaliacao
