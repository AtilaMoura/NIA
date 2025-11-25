# backend/app/services/groq_service.py    .
"""
Serviço para comunicação com Groq API (Llama 3.3)
"""

import httpx
import os
from typing import Optional

class GroqService:

    
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
       
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY não encontrada no .env!")
        
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = model
        
        print(f"✅ Groq Service inicializado com modelo: {model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        
        # Monta as mensagens
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Payload da requisição
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        # Headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Faz a chamada HTTP
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                
                # Verifica se deu erro
                response.raise_for_status()
                
                # Extrai o texto da resposta
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                return content
        
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json() if e.response else str(e)
            raise Exception(f"❌ Erro na API do Groq: {error_detail}")
        
        except Exception as e:
            raise Exception(f"❌ Erro ao chamar Groq: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> dict:
        """
        Gera resposta em formato JSON
        
        Útil para quando queremos dados estruturados
        """
        
        # Adiciona instrução para retornar JSON
        full_prompt = f"{prompt}\n\nRETORNE APENAS JSON VÁLIDO, SEM TEXTO ADICIONAL."
        
        # Gera o texto
        response = await self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Menos criativo para JSON
        )
        
        # Remove possíveis markdown ```json
        import re
        response = re.sub(r'```json\n?', '', response)
        response = re.sub(r'```\n?', '', response)
        response = response.strip()
        
        # Converte para dict
        import json
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise Exception(f"❌ Resposta não é JSON válido: {response[:200]}...")


# ============================================
# EXEMPLO DE USO
# ============================================
if __name__ == "__main__":
    import asyncio
    
    async def test():
        service = GroqService()
        
        # Teste 1: Texto simples
        print("\n🧪 Teste 1: Geração de texto")
        response = await service.generate(
            prompt="Explique o que é Python em 2 frases",
            system_prompt="Você é um professor didático"
        )
        print(f"Resposta: {response}\n")
        
        # Teste 2: JSON
        print("🧪 Teste 2: Geração de JSON")
        json_response = await service.generate_json(
            prompt="Liste 3 conceitos básicos de Python",
            system_prompt="Retorne um JSON com array 'conceitos'"
        )
        print(f"Resposta JSON: {json_response}")
    
    asyncio.run(test())