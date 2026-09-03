# backend/app/services/image_service.py
"""
Serviço de geração de imagem via API da OpenAI (gpt-image-1), chamado com httpx puro
— mesmo padrão do GroqService, sem lib nova. Usado pra gerar a imagem de capa de cada
aula (e, quando existir, a imagem de blocos "imagem_sugerida" do conteúdo).

gpt-image-1 só devolve base64 (sem "url" temporária como o dall-e-3 antigo) — por isso
o método já devolve os bytes decodificados, prontos pra salvar em disco.
"""

import base64
import httpx
import os


class ImageService:

    def __init__(self, model: str = "gpt-image-1"):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY não encontrada no .env!")

        self.base_url = "https://api.openai.com/v1"
        self.model = model

    async def gerar_imagem(self, prompt: str, size: str = "1536x1024") -> bytes:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "size": size,
            "n": 1,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/images/generations",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
                b64 = data["data"][0]["b64_json"]
                return base64.b64decode(b64)

        except httpx.HTTPStatusError as e:
            error_detail = e.response.json() if e.response else str(e)
            raise Exception(f"❌ Erro na API de imagem da OpenAI: {error_detail}")
        except Exception as e:
            raise Exception(f"❌ Erro ao gerar imagem: {str(e)}")
