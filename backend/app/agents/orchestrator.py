# backend/app/agents/orchestrator.py

from .specialist_agent import SpecialistAgent
from .reviewer_agent import ReviewerAgent
from .quiz_agent import QuizAgent

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