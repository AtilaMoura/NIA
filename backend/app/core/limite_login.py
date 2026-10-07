"""
Limite de tentativas de login, por conta (e-mail): MAX_ERROS senhas erradas dentro de
JANELA_S segundos e a conta espera até os erros mais antigos saírem da janela.

Por conta e não por IP: quem chama /auth/login é o servidor do Emaús, então todo
aluno chega com o mesmo IP (e a OWASP recomenda por conta).

ponytail: o contador fica na memória do processo. Com 2 workers do uvicorn o teto
real é até 2x MAX_ERROS, e zera quando o backend reinicia. Se o Emaús crescer, virar
coluna na tabela de usuários (erros_login, bloqueado_ate).
"""
import threading
import time

MAX_ERROS = 10
JANELA_S = 15 * 60
_MAX_CONTAS = 5000  # acima disso, limpa as contas sem erro recente (robô variando e-mail)

_erros: dict[str, list[float]] = {}
_trava = threading.Lock()


def _recentes(email: str, agora: float) -> list[float]:
    return [t for t in _erros.get(email, []) if agora - t < JANELA_S]


def bloqueado(email: str, agora: float | None = None) -> bool:
    agora = time.time() if agora is None else agora
    with _trava:
        return len(_recentes(email, agora)) >= MAX_ERROS


def registrar_erro(email: str, agora: float | None = None) -> None:
    agora = time.time() if agora is None else agora
    with _trava:
        if len(_erros) > _MAX_CONTAS:
            for chave in [k for k in _erros if not _recentes(k, agora)]:
                del _erros[chave]
        _erros[email] = _recentes(email, agora) + [agora]


def limpar(email: str) -> None:
    with _trava:
        _erros.pop(email, None)


if __name__ == "__main__":
    # Conferência rápida:  python -m app.core.limite_login
    e = "teste@exemplo"
    for i in range(MAX_ERROS - 1):
        registrar_erro(e, agora=1000 + i)
    assert not bloqueado(e, agora=1010), "9 erros ainda não bloqueiam"
    registrar_erro(e, agora=1010)
    assert bloqueado(e, agora=1011), "10 erros bloqueiam"
    assert not bloqueado("outra@exemplo", agora=1011), "o bloqueio é só daquela conta"
    assert bloqueado(e, agora=1000 + JANELA_S - 1), "segue bloqueado dentro da janela"
    assert not bloqueado(e, agora=1000 + JANELA_S + 1), "libera quando o erro mais antigo sai da janela"
    limpar(e)
    assert not bloqueado(e, agora=1011), "login certo zera"
    print("limite_login ok")
