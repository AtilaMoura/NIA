# backend/app/agents/base_agent.py

import asyncio
import re


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

    async def run_json_com_retry(self, prompt: str, tentativas: int = 3) -> dict:
        """
        Chama service.generate_json com retry em rate limit (HTTP 429) — achado
        real testando o modo "pro" (Fase 2): gerar assunto por assunto multiplica
        chamadas de IA e esbarra fácil no limite de tokens/minuto do tier grátis
        da Groq. Em vez de deixar o pipeline inteiro cair, espera o tempo que a
        própria API pede (ou um fallback) e tenta de novo, algumas vezes.
        """
        ultimo_erro = None
        for tentativa in range(1, tentativas + 1):
            try:
                return await self.service.generate_json(prompt)
            except Exception as e:
                ultimo_erro = e
                msg = str(e)
                if "429" not in msg and "rate_limit" not in msg.lower():
                    raise
                match = re.search(r"try again in ([\d.]+)s", msg)
                espera = float(match.group(1)) + 1.0 if match else 5.0 * tentativa
                if tentativa < tentativas:
                    await asyncio.sleep(espera)
        raise ultimo_erro
