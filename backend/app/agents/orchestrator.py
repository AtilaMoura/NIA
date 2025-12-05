# backend/app/agents/orchestrator.py

from .context_agent import ContextAgent
from .specialist_agent import SpecialistAgent
from .reviewer_agent import ReviewerAgent
from .quiz_agent import QuizAgent

# ✅ IMPORTAR OS MODELS
from app.models.models import Course, Module, Progress, Lesson

from app.services.gemini_service import GeminiService 
from app.services.groq_service import GroqService


class Orchestrator:
    """
    Coordena o fluxo completo de geração
    """

    def __init__(self, model: str = "gemini"):
        if model == "gemini":
            service = GeminiService()
        elif model == "llama":
            service = GroqService()
        else:
            service = GeminiService()

        self.context =  ContextAgent(service)
        self.specialist = SpecialistAgent(service)
        self.reviewer = ReviewerAgent(service)
        self.quiz = QuizAgent(service)

    async def generate_course_structure(
        self, 
        topic: str, 
        goal: str, 
        level: str
    ) -> dict:
        """
        Gera APENAS a estrutura (rápido)
        """
        return await self.specialist.generate_course_structure(
            topic=topic,
            level=level,
            goal=goal
        )
    
    async def generate_module_structure(
        self, 
        course: str, 
        module: str, 
        lessons: str
    ) -> dict:
        """
        Gera APENAS a estrutura (rápido)
        """
        text_prompt = await self.context.json_text(
            course=course,
            module=module,
            lessons=lessons
        )

        #return text_prompt

        #print(f"Prompt do context = {text_prompt}")
    
        return await self.specialist.generate_lesson_content(
            course=course,
            prompt = text_prompt
        )