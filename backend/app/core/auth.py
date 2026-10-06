from fastapi import Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# Mesma coisa, mas sem 401 automático quando não vem token — pra rotas de leitura
# que funcionam deslogado e só mudam o que mostram quando há login (2026-10-06).
oauth2_scheme_opcional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
        # Token de escopo curto (o do <iframe>, que fica visível na URL) NÃO vale
        # como sessão — só nos endpoints do próprio escopo (2026-10-06).
        if payload.get("scope") is not None:
            raise HTTPException(status_code=401, detail="Token não é de sessão.")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


def get_topico_resposta_user_id(
    topico_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
) -> int:
    """Valida o token de ESCOPO CURTO emitido por POST /auth/topico-token
    (2026-09-09) — usado pelo <iframe> do render pra salvar/ler respostas de
    exercício. Exige as claims 'scope'=='topico_respostas' e 'topico_id' batendo
    com o tópico da URL — um token vazado só autoriza esse tópico específico,
    não vira um jeito de acessar outros endpoints como se fosse sessão real.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    if payload.get("scope") != "topico_respostas":
        raise HTTPException(status_code=403, detail="Token não tem escopo pra isto.")
    if payload.get("topico_id") != topico_id:
        raise HTTPException(status_code=403, detail="Token não é pra este tópico.")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido.")
    return int(user_id)


def get_avaliacao_resposta_user_id(
    avaliacao_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
) -> int:
    """Valida o token de ESCOPO CURTO emitido por POST /auth/avaliacao-token
    — usado pelo <iframe> do render de avaliação pra salvar/ler respostas de
    exercício. Exige as claims 'scope'=='avaliacao_respostas' e 'avaliacao_id'
    batendo com a avaliação da URL — um token vazado só autoriza essa avaliação
    específica, não vira um jeito de acessar outros endpoints como se fosse
    sessão real.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    if payload.get("scope") != "avaliacao_respostas":
        raise HTTPException(status_code=403, detail="Token não tem escopo pra isto.")
    if payload.get("avaliacao_id") != avaliacao_id:
        raise HTTPException(status_code=403, detail="Token não é pra esta avaliação.")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido.")
    return int(user_id)


def get_topico_anotacao_user_id(
    topico_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
) -> int:
    """Anotação pessoal do aluno por slide (2026-09-10) — aceita DOIS tipos de
    token, porque dois contextos diferentes precisam ler/escrever o mesmo dado:
    (1) o token de ESCOPO CURTO do <iframe> do render (scope='topico_respostas'
    — reaproveitado aqui, não criei um scope novo só pra isto) usado pra
    salvar/carregar a anotação enquanto o aluno estuda; (2) o token de SESSÃO
    real, usado pelo Server Component do Emaús (`page.tsx`) pra montar o painel
    "Minhas anotações" fora do iframe. Mesma trava de identidade dos outros
    endpoints por tópico: o user_id nunca vem do corpo da requisição.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    scope = payload.get("scope")
    if scope == "topico_respostas":
        if payload.get("topico_id") != topico_id:
            raise HTTPException(status_code=403, detail="Token não é pra este tópico.")
    elif scope is not None:
        raise HTTPException(status_code=403, detail="Token não tem escopo pra isto.")
    # scope is None => token de sessão real (ver create_access_token em auth.py,
    # que nunca grava a claim 'scope') — aceito sem checagem de tópico, igual
    # get_current_user faz pros outros endpoints autenticados normalmente.

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido.")
    return int(user_id)


def usuario_do_token(db: Session, token: str | None, aceita_escopo_curto: bool = False) -> User | None:
    """Usuário dono do token, ou None se não veio token / token inválido — nunca
    levanta erro (é pra rota que funciona deslogada). Por padrão só aceita token
    de SESSÃO; `aceita_escopo_curto=True` aceita também o token do <iframe>
    (topico_respostas/avaliacao_respostas), usado pelos /render — o iframe não
    tem o token de sessão, só o curto que veio na própria URL."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    if payload.get("scope") is not None and not aceita_escopo_curto:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    return db.query(User).filter(User.id == int(user_id)).first()


def get_usuario_opcional(
    token: str | None = Depends(oauth2_scheme_opcional), db: Session = Depends(get_db)
) -> User | None:
    """Dependência pras rotas de leitura (cursos, módulos, aulas, tópicos): sem
    login devolve None e a rota mostra só o que é público."""
    return usuario_do_token(db, token)
