from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Course

from app.schemas.courses import CourseGenerateRequest, CourseGenerateResponse
from app.agents.orchestrator import Orchestrator

router = APIRouter(prefix="/courses", tags=["Courses"])

# Criar curso
@router.post("/")
def create_course(data: dict, db: Session = Depends(get_db)):
    course = Course(**data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

# Listar cursos
@router.get("/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# Buscar curso
@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    return course

# Atualizar curso
@router.put("/{course_id}")
def update_course(course_id: int, data: dict, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    for key, value in data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

# Deletar curso
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    db.delete(course)
    db.commit()
    return {"status": "deleted"}

@router.post("/generate", response_model=CourseGenerateResponse)
async def generate_course(
    data: CourseGenerateRequest,
    db: Session = Depends(get_db),
):
    """
    Gera um curso completo usando IA (Gemini + Llama + outros).
    """

    try:
        orchestrator = Orchestrator()
        course = await orchestrator.generate_course(
            topic=data.topic,
            goal=data.goal,
            level=data.level,
            num_modules=data.num_modules,
            quizzes=data.quizzes
        )

        return CourseGenerateResponse(
            topic=course["topic"],
            summary=course["content"],
            modules=course["modules"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar curso: {str(e)}")