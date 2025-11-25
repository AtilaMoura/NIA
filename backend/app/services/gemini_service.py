# backend/app/services/gemini_service.py
"""
Serviço para comunicação com Google Gemini API
"""

import google.generativeai as genai
import os
from typing import Optional
import json
import re

class GeminiService:
    """
    Service para chamar a API do Google Gemini
    
    Gemini Pro é GRÁTIS e muito bom para:
    - Análise e validação
    - Geração de quizzes
    - Coordenação (Orchestrator)
    """
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Inicializa o service do Gemini
        
        Args:
            model_name: Modelo a usar (gemini-pro é o padrão)
        """
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY não encontrada no .env!")
        
        # Configura a API
        genai.configure(api_key=api_key)
        
        # Cria o modelo
        self.model = genai.GenerativeModel(model_name)
        
        print(f"✅ Gemini Service inicializado com modelo: {model_name}")
    
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
            # Configurações de geração
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            # Gera o conteúdo (sícrono, mas rápido)
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"❌ Erro ao chamar Gemini: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        temperature: float = 0.3
    ) -> dict:
        """
        Gera resposta em formato JSON
        
        Útil para dados estruturados (quizzes, estruturas de curso)
        """
        
        # Adiciona instrução para retornar JSON
        full_prompt = f"""{prompt}

IMPORTANTE: Retorne APENAS um JSON válido, sem texto adicional, sem markdown.
Não use ```json, apenas o JSON puro."""
        
        # Gera o texto
        response = await self.generate(
            prompt=full_prompt,
            temperature=temperature
        )
        
        # Remove possíveis markdown
        response = re.sub(r'```json\n?', '', response)
        response = re.sub(r'```\n?', '', response)
        response = response.strip()
        
        # Converte para dict
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Tenta encontrar JSON no texto
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
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
        
        # Teste 1: Texto simples
        print("\n🧪 Teste 1: Geração de texto")
        response = await service.generate(
            prompt="Explique decorators em Python em 3 linhas"
        )
        print(f"Resposta: {response}\n")
        
        # Teste 2: JSON
        print("🧪 Teste 2: Geração de JSON")
        quiz = await service.generate_json(
            prompt="""Crie um quiz sobre Python básico com 2 questões.
            Formato: {"questions": [{"question": "...", "options": {...}, "correct": "A"}]}"""
        )
        print(f"Quiz: {quiz}\n")
        
        # Teste 3: Validação
        print("🧪 Teste 3: Validação de conteúdo")
        validation = await service.validate_content(
            content="Python é uma linguagem de programação interpretada...",
            criteria="Clareza, precisão técnica, didática"
        )
        print(f"Validação: {validation}")
    
    asyncio.run(test())