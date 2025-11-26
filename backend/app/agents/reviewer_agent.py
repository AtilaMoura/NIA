# backend/app/agents/reviewer_agent.py

from .base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    """
    Revisa e melhora o conteúdo do curso.
    """

    async def review(self, content: str) -> str:
        prompt = f"""
        Você é um revisor pedagógico.
        Melhore o conteúdo abaixo mantendo o significado,
        mas deixando mais claro, mais didático e organizado.

        Conteúdo:
        {content}

        Responda apenas com o texto melhorado.
        """
        return await self.run(prompt)
