from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# Papéis que podem administrar OUTROS usuários (criar, editar quem não é eles mesmos).
# Só 'master' pode conceder papel — evita um admin/professor se autopromover.
_PAPEIS_ADMIN = ("master", "admin")


def _sem_senha(user: User) -> dict:
    """Nunca devolver password_hash numa resposta de API — vazamento real
    encontrado 2026-09-04 (GET /users/{id} expunha o hash bcrypt sem login)."""
    return {
        k: v
        for k, v in user.__dict__.items()
        if k not in ("password_hash", "_sa_instance_state")
    }


# Criar usuário — só quem já é master/admin pode criar outro usuário com papel elevado.
@router.post("/")
def create_user(
    user: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role not in _PAPEIS_ADMIN:
        raise HTTPException(403, "Só master/admin podem criar usuários por aqui.")
    if "password_hash" in user:
        raise HTTPException(400, "Use /auth/register para definir senha (nunca hash cru).")
    if user.get("role") == "master" and current_user.role != "master":
        raise HTTPException(403, "Só master pode conceder o papel master.")
    new_user = User(**user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return _sem_senha(new_user)


# Listar todos usuários — lista com dado pessoal de todo mundo, só papel administrativo.
@router.get("/")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in (*_PAPEIS_ADMIN, "professor"):
        raise HTTPException(403, "Sem permissão pra listar usuários.")
    return [_sem_senha(u) for u in db.query(User).all()]


# Buscar usuário por ID — leitura segue aberta (usada por toda página do Emaús sem
# repassar token ainda; ver nota de segurança 2026-09-04). Nunca devolve password_hash.
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return _sem_senha(user)


# Atualizar usuário — exige login. Só o próprio dono ou master/admin editam; só master
# muda o campo 'role' de alguém (achado real 2026-09-04: sem isso, qualquer requisição
# sem token virava 'master' direto).
@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if current_user.id != user_id and current_user.role not in _PAPEIS_ADMIN:
        raise HTTPException(403, "Só o próprio usuário ou master/admin podem editar este perfil.")
    if "role" in data and current_user.role != "master":
        raise HTTPException(403, "Só master pode alterar o papel de um usuário.")
    if "password_hash" in data:
        raise HTTPException(400, "Use /auth/register ou um fluxo de troca de senha próprio.")
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return _sem_senha(user)


# Deletar usuário — restrito a master (soft delete ainda não existe pra User; documentado
# como pendência, não usado pelo Emaús hoje).
@router.delete("/{user_id}")
def delete_user(
    user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != "master":
        raise HTTPException(403, "Só master pode remover usuários.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}
