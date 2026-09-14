from fastapi import APIRouter, HTTPException, Depends
from app.models.models import Topico, User
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.security import create_access_token, verify_password, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.auth import get_current_user
from app.schemas.auth import TopicoTokenRequest, UserLogin, UserRegister, Token, UserMe
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
def register(data: UserRegister, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == data.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    new_user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": str(new_user.id)})
    return Token(access_token=access_token)

@router.get("/me", response_model=UserMe)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/topico-token", response_model=Token)
def emitir_topico_token(
    data: TopicoTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Token de escopo curto pro <iframe> do render de tópico salvar respostas
    (2026-09-09). NÃO é o token de sessão real — esse nunca sai do servidor
    Next.js (ver emaus-web/app/_lib/sessao.ts: "nunca em JS do navegador").
    Este aqui autoriza só 'salvar resposta deste usuário, neste tópico', por
    2h — mesmo que vaze (fica visível na URL do iframe), o estrago é bem menor
    que o token de sessão de 30 dias com acesso a tudo.
    """
    if not db.query(Topico).filter(Topico.id == data.topico_id).first():
        raise HTTPException(404, "Tópico not found")

    access_token = create_access_token(
        {"sub": str(current_user.id), "topico_id": data.topico_id, "scope": "topico_respostas"},
        expires_delta=timedelta(hours=2),
    )
    return Token(access_token=access_token)

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    access_token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=access_token)
