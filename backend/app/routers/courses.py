# backend/app/routers/courses.py
import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

# ✅ IMPORTAR OS MODELS
from app.models.models import Course, Module, Progress, Lesson  # ← ADICIONE Module!

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
    FASE 1: Gera APENAS a estrutura do curso (títulos de módulos e lições)
    e salva as entidades Course, Module e Lesson no banco de dados.
    """
    try:
        print("🔹 Iniciando geração da estrutura...")
        
        # Inicializa o Orchestrator (Agente que interage com o LLM)
        orchestrator = Orchestrator()
        
        # 1. ✅ Gera ESTRUTURA (Course -> Modules -> Lessons) via LLM
        # A estrutura retornada é um dicionário Python (dict)
        structure = await orchestrator.generate_course_structure(
            topic=data.topic,
            goal=data.goal,
            level=data.level
        )
        
        modules_data = structure.get('modules', [])
        print(f"✅ Estrutura gerada: {structure.get('title')}")
        print(f"   Módulos: {len(modules_data)}")
        
        # 2. ✅ Salva ENTIDADE COURSE no banco
        course = Course(
            title=structure.get("title", data.topic),
            description=structure.get("description", ""),
            level=data.level,
            duration_hours=len(modules_data) * 3,  # Estimativa
            modules_count=len(modules_data),
            structure=structure,  # JSON completo
            status="draft",
            prerequisites=[],
            learning_outcomes=[],
            generated_by={"orchestrator": "gemini", "timestamp": str(datetime.now())}
        )
        db.add(course)
        db.flush()  # Garante que o course.id seja gerado antes de salvar os módulos/lições
        
        print(f"✅ Curso salvo no banco com ID: {course.id}")
        
        # Lista para armazenar o número total de lições
        total_lessons_saved = 0
        
        # 3. ✅ Itera e Salva MÓDULOS e LIÇÕES no banco
        for mod_index, mod_data in enumerate(modules_data, start=1):
            lessons_data = mod_data.get("lessons", [])
            lesson_count = len(lessons_data)
            total_lessons_saved += lesson_count
            
            # 3.1. Salva o MÓDULO (com o contador de lições)
            module = Module(
                course_id=course.id,
                module_index=mod_data.get("index", mod_index), # Usa o index do LLM ou o índice de iteração
                title=mod_data.get("title", f"Módulo {mod_index}"),
                description=mod_data.get("description", ""),
                
                # NOVOS CAMPOS: 
                content_generated=False,
                exam_generated=False,
                lessons_count=lesson_count, # ✅ ATUALIZADO
                
                duration_hours=3,
                examples=[],
                exercises=[],
                resources={},
                quiz={},
                is_published=False,
                generated_by="pending"
            )
            db.add(module)
            db.flush() # Garante que o module.id seja gerado antes de salvar as lições
            
            # 3.2. Salva as LIÇÕES associadas a este módulo
            for lesson_index, lesson_item in enumerate(lessons_data, start=1):
                lesson = Lesson(
                    module_id=module.id,
                    lesson_index=lesson_index,
                    title=lesson_item.get("title", f"Lição {lesson_index}"),
                    
                    # O conteúdo e o status de aprovação serão preenchidos na FASE 2
                    content="",
                    is_approved=False,
                    estimated_read_time_minutes=15, # Placeholder
                )
                db.add(lesson)

        # 4. ✅ COMMIT FINAL
        db.commit()
        
        print(f"✅ Estrutura completa salva. Módulos: {len(modules_data)}, Lições: {total_lessons_saved}")
        
        # 5. ✅ Retorno
        db.refresh(course) # Atualiza o objeto course para garantir consistência
        return CourseStructureResponse(
            id=course.id,
            topic=data.topic,
            title=course.title,
            description=course.description,
            modules=structure.get("modules", []), # Retorna a estrutura JSON original
            total_modules=course.modules_count,
            created_at=course.created_at
        )
    
    except Exception as e:
        # A instrução traceback.print_exc() é importante para ver a pilha de erros completa no console.
        traceback.print_exc()
        db.rollback() # ✅ O rollback é CRUCIAL em caso de erro para não ter dados parciais
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar estrutura: {str(e)}"
        )


# ====================================================================
# GERAÇÃO COM IA - FASE 2: CONTEÚDO DO MÓDULO
# ====================================================================

def is_lesson_complete(lesson: Lesson):
    return (
        lesson.content is not None and
        lesson.is_approved is True and
        lesson.generated_by is not None and
        lesson.estimated_read_time_minutes is not None
    )

@router.post("/generate-module/{course_id}/{module_index}")
async def generate_module_content(
    course_id: int,
    module_index: int,
    db: Session = Depends(get_db),
):
    """
    FASE 2: Gera o conteúdo detalhado para todas as lições de um módulo
    e atualiza a tabela Module.
    """
    print(f"🔹 Iniciando FASE 2: Geração de conteúdo para Módulo {module_index} do Curso {course_id}")
    try:
        # 1. Encontra o Módulo e o Curso
        module = db.query(Module).filter(
            Module.course_id == course_id,
            Module.module_index == module_index
        ).first()
        
        if not module:
            raise HTTPException(status_code=404, detail="Módulo não encontrado")
        
        # ADICIONADO: Buscar o objeto Course pai para fornecer contexto global ao Orchestrator
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            # Isso só deve acontecer se houver um problema de integridade referencial no DB
            raise HTTPException(status_code=500, detail="Curso pai não encontrado para o módulo.")
        
        # 2. Verifica se o conteúdo já foi gerado
        if module.content_generated:
            return {
                "message": "Módulo já teve o conteúdo gerado anteriormente",
                "module_id": module.id,
                "title": module.title,
                "content_generated": True
            }
        
        # 3. Busca a lista de Lições (o Specialist Agent precisará disso)
        lessons = db.query(Lesson).filter(Lesson.module_id == module.id).order_by(Lesson.lesson_index).all()
        
        if not lessons:
             raise HTTPException(status_code=404, detail="Nenhuma lição encontrada para este módulo.")
        
        # 3. Encontrar a próxima lesson incompleta
        next_lesson = next((l for l in lessons if not is_lesson_complete(l)), None)

        if not next_lesson:
            return {
                "message": "Todas as lições já estão completas",
                "module_id": module.id
            }
        
        # 4. Inicializa o Orchestrator
        orchestrator = Orchestrator()#model = "llama")
        
        # 5. Gera o conteúdo chamando o Orchestrator com todo o contexto
        # O Orchestrator será responsável por limpar o contexto, chamar os agentes e salvar o Lesson.content
        
        print("⚙️ Enviando Curso, Módulo e Lições para o Orchestrator...")
        print(f"Curso = {course}")
        print(f"Módulo = {module}")
        print(f"Lições = {lessons}")
        
        result = await orchestrator.generate_module_structure(
            course= course.title,
            module= module.title,
            lessons= next_lesson.title
        )
        return (result)
        print(f"Conteudo = {result}")
        
        # 6. Atualiza o Módulo com status de geração e metadados
        module.content_generated = False # Marca a conclusão da geração
        #module.ai_model_used = result.get('model_used', 'N/A')
        #module.review_score = result.get('review_score', 0)
        #
        db.commit()
        db.refresh(module)
        
        return {

            #"message": "Módulo e Lições gerados com sucesso",
            #"module_id": module.id,
            #"title": module.title,
            #"content": result.content
            #"content_generated": module.content_generated,
            #"lessons_processed": len(lessons),
            #"model_used": module.ai_model_used
        }
    
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar módulo: {str(e)}"
        )