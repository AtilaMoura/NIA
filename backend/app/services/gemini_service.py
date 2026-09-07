# backend/app/services/gemini_service.py
"""
Serviço para comunicação com Google Gemini API.

Migrado em 2026-08-26 do pacote antigo `google-generativeai` (0.3.2) pro SDK
novo unificado `google-genai` — o pacote antigo está descontinuado (repo
renomeado "deprecated-generative-ai-python") e dava `504 Deadline Exceeded`
sempre em ~60s com gemini-2.5-flash, independente do tamanho do prompt (bug
conhecido desse SDK antigo com esse modelo — ver
curso de obreiro/anotação para IA.md pro diagnóstico completo, testado
isolado, sem retry, 2 vezes seguidas). Interface pública da classe (generate/
generate_json/validate_content) mantida idêntica — nada no resto do código
(ia_agent.py, quiz_agent.py, reviewer_agent.py, tutor_agent.py) precisa mudar.
"""

import os
from typing import Optional

from google import genai
from google.genai import types


class GeminiService:
    """
    Service para chamar a API do Google Gemini (SDK novo, google-genai).
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", timeout_ms: int = 90_000):
        """
        Inicializa o service do Gemini

        Args:
            model_name: Modelo a usar
            timeout_ms: Timeout por requisição (o SDK antigo travava sem
                limite nenhum — esse aqui é explícito, mesmo que o SDK novo
                também tenha bugs conhecidos de timeout não 100% respeitado)
        """
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY não encontrada no .env!")

        self.model_name = model_name
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=timeout_ms),
        )

        print(f"✅ Gemini Service inicializado com modelo: {model_name} (SDK google-genai, timeout {timeout_ms}ms)")

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Gera texto usando Gemini

        Args:
            prompt: O prompt/pergunta para a IA
            temperature: Criatividade (0.0 = preciso, 1.0 = criativo)
            max_tokens: Tamanho máximo da resposta

        Returns:
            str: Texto gerado pela IA
        """
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text

        except Exception as e:
            raise Exception(f"❌ Erro ao chamar Gemini: {str(e)}")

    async def generate_audio(
        self,
        texto: str,
        voice_name: str = "Kore",
        tts_model: str = "gemini-2.5-flash-preview-tts",
    ) -> bytes:
        """
        Gera áudio (voz natural, não TTS do navegador) a partir de um texto,
        usando o modelo de TTS do Gemini (response_modalities=["AUDIO"]).

        A API devolve PCM cru (24kHz, mono, 16-bit) em base64 — embrulha num
        WAV válido via o módulo `wave` antes de devolver, pra poder salvar
        direto num arquivo `.wav` e servir como estático.

        Args:
            texto: o que deve ser falado
            voice_name: uma das vozes pré-definidas do Gemini (ex. "Kore")
            tts_model: modelo de TTS (diferente do modelo de texto default)

        Returns:
            bytes: conteúdo de um arquivo .wav pronto pra salvar em disco
        """
        import io
        import wave

        try:
            response = await self.client.aio.models.generate_content(
                model=tts_model,
                contents=texto,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                        )
                    ),
                ),
            )
            pcm_data = response.candidates[0].content.parts[0].inline_data.data

            buffer = io.BytesIO()
            with wave.open(buffer, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(24000)
                wav_file.writeframes(pcm_data)
            return buffer.getvalue()

        except Exception as e:
            raise Exception(f"❌ Erro ao gerar áudio no Gemini: {str(e)}")

    async def generate_json(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 8000
    ) -> dict:
        """
        Gera resposta em formato JSON

        Útil para dados estruturados (quizzes, estruturas de curso)

        max_tokens=8000: um tópico completo (schema de
        docs/schema/schema-conteudo-topico.md, gerado em 1 chamada só no modo
        "comum") passa fácil de 3000-3500 tokens de saída.
        """
        import json
        import re

        full_prompt = f"""{prompt}

IMPORTANTE: Retorne APENAS um JSON válido, sem texto adicional, sem markdown.
Não use ```json, apenas o JSON puro."""

        response = await self.generate(
            prompt=full_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

        response = re.sub(r'```json\n?', '', response)
        response = re.sub(r'```\n?', '', response)
        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    pass

            raise Exception(f"❌ Resposta não é JSON válido: {response[:200]}...")

    async def validate_content(
        self,
        content: str,
        criteria: str
    ) -> dict:
        """
        Valida conteúdo com base em critérios

        Útil para o Reviewer Agent

        Args:
            content: Conteúdo a validar
            criteria: Critérios de validação

        Returns:
            dict: {"score": 8.5, "feedback": "...", "approved": true}
        """
        prompt = f"""Você é um revisor técnico especializado.

CONTEÚDO A VALIDAR:
{content[:2000]}  # Limita tamanho

CRITÉRIOS:
{criteria}

Analise o conteúdo e retorne um JSON com:
{{
  "score": 8.5,  // Nota de 0 a 10
  "approved": true,  // true se score >= 7
  "strengths": ["ponto forte 1", "ponto forte 2"],
  "weaknesses": ["ponto fraco 1"],
  "feedback": "Texto geral sobre a qualidade"
}}"""

        return await self.generate_json(prompt)


# ============================================
# EXEMPLO DE USO
# ============================================
if __name__ == "__main__":
    import asyncio

    async def test():
        service = GeminiService()

        print("\n🧪 Teste 1: Geração de texto")
        response = await service.generate(
            prompt="Explique decorators em Python em 3 linhas"
        )
        print(f"Resposta: {response}\n")

        print("🧪 Teste 2: Geração de JSON")
        quiz = await service.generate_json(
            prompt="""Crie um quiz sobre Python básico com 2 questões.
            Formato: {"questions": [{"question": "...", "options": {...}, "correct": "A"}]}"""
        )
        print(f"Quiz: {quiz}\n")

    asyncio.run(test())
