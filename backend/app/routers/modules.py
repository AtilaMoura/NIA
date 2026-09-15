from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Module, User
from app.core.auth import get_current_user

router = APIRouter(prefix="/modules", tags=["Modules"])

# Escrita exige admin/master — leitura continua pública (ver topicos.py, mesmo padrão).
PAPEIS_ADMIN = ("master", "admin")


def _exigir_admin(user: User):
    if user.role not in PAPEIS_ADMIN:
        raise HTTPException(403, "Só master ou admin podem criar/editar/apagar módulos.")


# Criar módulo
@router.post("/")
def create_module(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
    module = Module(**data)
    db.add(module)
    db.commit()
    db.refresh(module)
    return module

# Listar todos os módulos
@router.get("/")
def list_modules(db: Session = Depends(get_db)):
    return db.query(Module).all()

# Buscar módulo por ID
@router.get("/{module_id}")
def get_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    return module

# Atualizar módulo
@router.put("/{module_id}")
def update_module(module_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    for key, value in data.items():
        setattr(module, key, value)
    db.commit()
    return module

# Deletar módulo
@router.delete("/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _exigir_admin(current_user)
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    db.delete(module)
    db.commit()
    return {"status": "deleted"}
