from fastapi import APIRouter, HTTPException, Depends
from app.models.models import User
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.security import create_access_token, verify_password, hash_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.auth import UserLogin, UserRegister, Token
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
