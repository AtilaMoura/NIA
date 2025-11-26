# backend/app/agents/orchestrator.py

from .specialist_agent import SpecialistAgent
from .reviewer_agent import ReviewerAgent
from .quiz_agent import QuizAgent

from app.services.gemini_service import GeminiService
from app.services.groq_service import GroqService


class Orchestrator:
    """
    Coordena o fluxo completo:
        1. Gera conteúdo (SpecialistAgent)
        2. Revisa (ReviewerAgent)
        3. Cria quizzes (QuizAgent)
        4. Retorna o pacote completo
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

    async def generate_course(self, topic: str, goal: str, level: str, num_modules: int, quizzes: bool 
        ) -> dict:
        print("🔹 Gerando estrutura inicial...")
        raw_content = await self.specialist.generate_course_structure(topic)

        print("🔹 Revisando conteúdo...")
        improved_content = await self.reviewer.review(raw_content)

        print("🔹 Criando quizzes...")
        quiz = await self.quiz.generate_quiz(improved_content)

        return {
            "topic": topic,
            "content": improved_content,
            "quiz": quiz,
            "modules": [] 
        }
