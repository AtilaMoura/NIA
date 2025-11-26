# backend/app/agents/base_agent.py

class BaseAgent:
    """
    Classe base para qualquer agente de IA.
    Cada agente recebe:
      - Um service (Gemini, Groq etc.)
      - Um método: run(prompt)
    """

    def __init__(self, service):
        self.service = service

    async def run(self, prompt: str) -> str:
        """
        Envia um prompt para o service (Gemini, Llama, etc.)
        """
        response = await self.service.generate(prompt)
        return response
