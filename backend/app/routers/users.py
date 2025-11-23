from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User

router = APIRouter(prefix="/users", tags=["Users"])

# Criar usuário
@router.post("/")
def create_user(user: dict, db: Session = Depends(get_db)):
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Listar todos usuários
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Buscar usuário por ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

# Atualizar usuário
@router.put("/{user_id}")
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    return user

# Deletar usuário
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}
