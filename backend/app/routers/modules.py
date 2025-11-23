from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Module

router = APIRouter(prefix="/modules", tags=["Modules"])

# Criar módulo
@router.post("/")
def create_module(data: dict, db: Session = Depends(get_db)):
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
def update_module(module_id: int, data: dict, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    for key, value in data.items():
        setattr(module, key, value)
    db.commit()
    return module

# Deletar módulo
@router.delete("/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(404, "Module not found")
    db.delete(module)
    db.commit()
    return {"status": "deleted"}
