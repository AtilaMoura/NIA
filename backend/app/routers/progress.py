from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Progress

router = APIRouter(prefix="/progress", tags=["Progress"])

# Criar progresso
@router.post("/")
def create_progress(data: dict, db: Session = Depends(get_db)):
    progress = Progress(**data)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

# Listar todo progresso
@router.get("/")
def list_progress(db: Session = Depends(get_db)):
    return db.query(Progress).all()

# Buscar progresso por ID
@router.get("/{progress_id}")
def get_progress(progress_id: int, db: Session = Depends(get_db)):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(404, "Progress not found")
    return progress

# Atualizar progresso
@router.put("/{progress_id}")
def update_progress(progress_id: int, data: dict, db: Session = Depends(get_db)):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(404, "Progress not found")
    for key, value in data.items():
        setattr(progress, key, value)
    db.commit()
    return progress

# Deletar progresso
@router.delete("/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db)):
    progress = db.query(Progress).filter(Progress.id == progress_id).first()
    if not progress:
        raise HTTPException(404, "Progress not found")
    db.delete(progress)
    db.commit()
    return {"status": "deleted"}
