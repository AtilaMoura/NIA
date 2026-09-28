"""Tempo de estudo por tópico/prova (página Pessoas do Master, 2026-09-28).

O render (slide aberto + aba visível) manda um "sinal" a cada minuto. Cada sinal
vale no máximo SINAL_S segundos, e só conta se o anterior foi há pelo menos
INTERVALO_MIN_S — então recarregar a página ou abrir o tópico em duas abas não
multiplica o tempo. Nunca apaga nada, só soma.
"""

from datetime import datetime, timezone

SINAL_S = 60          # quanto cada sinal vale
INTERVALO_MIN_S = 50  # sinal mais rápido que isso é ignorado (folga pro timer do navegador)


def registrar_sinal(registro) -> bool:
    """Soma um sinal em `registro` (TopicoProgress ou AvaliacaoProgress). Devolve
    True se contou. Quem chama faz o commit."""
    agora = datetime.now(timezone.utc)
    anterior = registro.ultimo_sinal_em
    if anterior is not None and (agora - anterior).total_seconds() < INTERVALO_MIN_S:
        return False
    registro.time_spent_s = (registro.time_spent_s or 0) + SINAL_S
    registro.ultimo_sinal_em = agora
    return True
