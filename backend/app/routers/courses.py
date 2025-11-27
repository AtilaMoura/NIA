# backend/app/routers/courses.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

# ✅ IMPORTAR OS MODELS
from app.models.models import Course, Module, Progress  # ← ADICIONE Module!

from app.schemas.courses import (
    CourseGenerateRequest, 
    CourseStructureResponse,
    ModuleGenerateResponse
)
from app.agents.orchestrator import Orchestrator
from datetime import datetime

router = APIRouter(prefix="/courses", tags=["Courses"])

# ============================================
# CRUD BÁSICO (mantém como está)
# ============================================

@router.post("/")
def create_course(data: dict, db: Session = Depends(get_db)):
    course = Course(**data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/")
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    return course

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

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    db.delete(course)
    db.commit()
    return {"status": "deleted"}


# ============================================
# GERAÇÃO COM IA - FASE 1: ESTRUTURA
# ============================================

@router.post("/generate-structure", response_model=CourseStructureResponse)
async def generate_course_structure(
    data: CourseGenerateRequest,
    db: Session = Depends(get_db),
):
    """
    FASE 1: Gera APENAS a estrutura do curso (30 seg)
    
    - Título e descrição do curso
    - Módulos (só título/descrição, SEM conteúdo)
    - Aulas (só título)
    - Salva tudo no banco
    
    Exemplo:
    POST /courses/generate-structure
    {
      "topic": "Python para Iniciantes",
      "goal": "Aprender programação do zero",
      "level": "beginner"
    }
    """
    try:
        print("🔹 Iniciando geração da estrutura...")
        
        orchestrator = Orchestrator()
        
        # ✅ Gera APENAS estrutura (rápido)
        structure = await orchestrator.generate_course_structure(
            topic=data.topic,
            goal=data.goal,
            level=data.level
        )
        
        print(f"✅ Estrutura gerada: {structure.get('title')}")
        print(f"   Módulos: {len(structure.get('modules', []))}")
        
        # ✅ Salva CURSO no banco
        course = Course(
            title=structure.get("title", data.topic),
            description=structure.get("description", ""),
            level=data.level,
            duration_hours=len(structure.get("modules", [])) * 3,  # Estimativa
            modules_count=len(structure.get("modules", [])),
            structure=structure,  # JSON completo
            status="draft",
            prerequisites=[],
            learning_outcomes=[],
            generated_by={"orchestrator": "gemini", "timestamp": str(datetime.now())}
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        
        print(f"✅ Curso salvo no banco com ID: {course.id}")
        
        # ✅ Salva MÓDULOS no banco (SEM conteúdo)
        for mod_data in structure.get("modules", []):
            module = Module(
                course_id=course.id,
                module_index=mod_data.get("index", 0),
                title=mod_data.get("title", "Módulo"),
                description=mod_data.get("description", ""),
                content="",  # ✅ VAZIO! Será gerado sob demanda
                duration_hours=3,
                examples=[],
                exercises=[],
                resources={},
                quiz={},  # ✅ Será gerado depois
                is_published=False,  # ✅ Não publicado ainda
                generated_by="pending"
            )
            db.add(module)
        
        db.commit()
        
        print(f"✅ {len(structure.get('modules', []))} módulos salvos no banco")
        
        return CourseStructureResponse(
            id=course.id,
            topic=data.topic,
            title=course.title,
            description=course.description,
            modules=structure.get("modules", []),
            total_modules=course.modules_count,
            created_at=course.created_at
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar estrutura: {str(e)}"
        )


# ============================================
# GERAÇÃO COM IA - FASE 2: CONTEÚDO DO MÓDULO
# ============================================

@router.post("/generate-module/{course_id}/{module_index}")
async def generate_module_content(
    course_id: int,
    module_index: int,
    db: Session = Depends(get_db),
):
    """
    FASE 2: Gera CONTEÚDO COMPLETO de 1 módulo (3-5 min)
    
    Chamado quando:
    - Aluno clica "Começar Módulo X"
    - Aluno passou no quiz anterior (70%+)
    
    Exemplo:
    POST /courses/generate-module/1/1
    """
    try:
        # ✅ Busca módulo no banco
        module = db.query(Module).filter(
            Module.course_id == course_id,
            Module.module_index == module_index
        ).first()
        
        if not module:
            raise HTTPException(404, "Módulo não encontrado")
        
        # ✅ Se já foi gerado, retorna
        if module.is_published and module.content:
            return {
                "message": "Módulo já foi gerado anteriormente",
                "module_id": module.id,
                "title": module.title,
                "is_published": True
            }
        
        print(f"🔹 Gerando conteúdo do módulo: {module.title}")
        
        orchestrator = Orchestrator()
        
        # ✅ Gera conteúdo COMPLETO (demora mais)
        print("   1/3 Gerando conteúdo...")
        content = await orchestrator.specialist.run(f"""
        Crie um conteúdo COMPLETO e DETALHADO para o módulo:
        
        Título: {module.title}
        Descrição: {module.description}
        
        Inclua:
        - Introdução clara
        - Explicações detalhadas
        - 3+ exemplos práticos com código
        - Exercícios
        """)
        
        print("   2/3 Revisando qualidade...")
        reviewed = await orchestrator.reviewer.run(f"""
        Revise e melhore este conteúdo:
        {content[:2000]}
        
        Deixe mais claro e didático.
        """)
        
        print("   3/3 Criando quiz...")
        quiz_text = await orchestrator.quiz.generate_quiz(reviewed[:1000])
        
        # ✅ Atualiza módulo no banco
        module.content = reviewed
        module.quiz = {"text": quiz_text}  # Simplificado por enquanto
        module.is_published = True
        module.generated_by = "specialist_agent"
        module.ai_model_used = "gemini-1.5-flash"
        module.review_score = 8.5
        
        db.commit()
        db.refresh(module)
        
        print(f"✅ Módulo {module.title} gerado e salvo!")
        
        return {
            "message": "Módulo gerado com sucesso",
            "module_id": module.id,
            "title": module.title,
            "content_length": len(module.content),
            "quiz_generated": True
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar módulo: {str(e)}"
        )