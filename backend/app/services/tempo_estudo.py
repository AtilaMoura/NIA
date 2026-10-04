"""Tempo de estudo por tópico/prova (página Pessoas do Master, 2026-09-28).

O render (slide aberto + aba visível) manda um "sinal" a cada minuto. Cada sinal
vale no máximo SINAL_S segundos, e só conta se o anterior foi há pelo menos
INTERVALO_MIN_S — então recarregar a página ou abrir o tópico em duas abas não
multiplica o tempo. Nunca apaga nada, só soma.
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.dialects.postgresql import insert

from app.models.models import TempoEstudoDia

# Brasil sem horário de verão desde 2019 — offset fixo evita depender do tzdata
FUSO_BRASILIA = timezone(timedelta(hours=-3))
SINAL_S = 60          # quanto cada sinal vale
INTERVALO_MIN_S = 50  # sinal mais rápido que isso é ignorado (folga pro timer do navegador)


def registrar_sinal(db, registro) -> bool:
    """Soma um sinal em `registro` (TopicoProgress ou AvaliacaoProgress) e no
    tempo do dia (TempoEstudoDia). Devolve True se contou. Quem chama faz o commit."""
    agora = datetime.now(timezone.utc)
    anterior = registro.ultimo_sinal_em
    if anterior is not None and (agora - anterior).total_seconds() < INTERVALO_MIN_S:
        return False
    registro.time_spent_s = (registro.time_spent_s or 0) + SINAL_S
    registro.ultimo_sinal_em = agora

    # Upsert atômico do dia (dois sinais ao mesmo tempo não duplicam a linha)
    dia = agora.astimezone(FUSO_BRASILIA).date()
    db.execute(
        insert(TempoEstudoDia)
        .values(user_id=registro.user_id, dia=dia, segundos=SINAL_S)
        .on_conflict_do_update(
            constraint="uq_tempo_estudo_dia_user_dia",
            set_={"segundos": TempoEstudoDia.segundos + SINAL_S},
        )
    )
    return True
