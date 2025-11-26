# backend/app/agents/specialist_agent.py

from .base_agent import BaseAgent

class SpecialistAgent(BaseAgent):
    """
    Gera o conteúdo bruto do curso:
      - módulos
      - lições
      - estrutura inicial
    """

    async def generate_course_structure(self, topic: str) -> str:
        prompt = f"""
        Você é um especialista em educação online.
        Gere uma estrutura completa de um curso sobre: **{topic}**.

        Formato da resposta:
        - Lista de módulos
        - Lista de aulas dentro de cada módulo
        - Objetivos de aprendizado
        - Conteúdo resumido de cada aula
        """
        return await self.run(prompt)
