# backend/app/services/groq_service.py    .
"""
Serviço para comunicação com Groq API.

Achado em 2026-08-22: o modelo antigo (llama-3.3-70b-versatile) foi descontinuado pela
Groq — a conta não tem mais nenhum modelo Llama 3.x disponível, só a nova leva
(gpt-oss-120b/20b, qwen3.6, compound). Trocado pro maior disponível (gpt-oss-120b).
"""

import asyncio
import httpx
import os
from typing import Optional

class GroqService:

    
    def __init__(self, model: str = "openai/gpt-oss-120b"):
       
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
            # gpt-oss é um modelo de "raciocínio" — sem isso ele gasta boa parte do
            # max_tokens pensando (campo "reasoning" separado) e pode devolver
            # "content" vazio/truncado (visto na prática: max_tokens=50 sem isso
            # voltou content="", finish_reason="length"). "low" mantém raciocínio
            # mínimo e sobra orçamento pro JSON de verdade.
            "reasoning_effort": "low",
        }
        
        # Headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Retry com backoff pro rate limit de 8000 tokens/min do tier gratuito (ver
        # nia-infra-gotchas): "Rate limit reached" (já tem uso recente na janela) e
        # "Request too large" (esse pedido sozinho passa do teto) são os dois erros
        # reais vistos gerando o curso de obreiro — ambos passageiros, uma nova
        # tentativa alguns segundos depois costuma passar porque a janela de 1 min
        # esvazia. Não faz sentido tentar de novo em erro que não é de rate limit
        # (ex: chave inválida), por isso só entra no retry quando o code é esse.
        max_tentativas = 4
        espera_s = 8

        for tentativa in range(1, max_tentativas + 1):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        json=payload,
                        headers=headers
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response else str(e)
                code = (error_detail.get("error") or {}).get("code") if isinstance(error_detail, dict) else None

                if code == "rate_limit_exceeded" and tentativa < max_tentativas:
                    await asyncio.sleep(espera_s)
                    espera_s *= 2
                    continue

                raise Exception(f"❌ Erro na API do Groq: {error_detail}")

            except Exception as e:
                raise Exception(f"❌ Erro ao chamar Groq: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 6000
    ) -> dict:
        """
        Gera resposta em formato JSON

        Útil para quando queremos dados estruturados

        max_tokens=6000 (era 8000): achado em 2026-08-22 trocando o modelo pra
        gpt-oss-120b (ver __init__) — a conta free tier da Groq tem um teto de
        8000 tokens/minuto POR REQUISIÇÃO (prompt + max_tokens reservado, não só
        o que é de fato gerado). Com max_tokens=8000 uma chamada com prompt de
        ~1700 tokens já estourava ("Requested 9678"). 6000 deixa folga pro prompt
        e ainda cobre os ~3000-3500 tokens que um tópico "comum" de fato usa.
        """

        # Adiciona instrução para retornar JSON
        full_prompt = f"{prompt}\n\nRETORNE APENAS JSON VÁLIDO, SEM TEXTO ADICIONAL."

        # Gera o texto
        response = await self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Menos criativo para JSON
            max_tokens=max_tokens
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