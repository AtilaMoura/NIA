# backend/app/agents/quiz_agent.py

from .base_agent import BaseAgent

class QuizAgent(BaseAgent):
    """
    Gera quizzes e exercícios baseado no conteúdo final do curso.
    """

    async def generate_quiz(self, content: str) -> str:
        prompt = f"""
        Gere 10 perguntas de quiz sobre o conteúdo abaixo.
        Inclua:
        - Pergunta
        - 4 alternativas
        - Uma alternativa correta

        Conteúdo:
        {content}
        """
        return await self.run(prompt)
