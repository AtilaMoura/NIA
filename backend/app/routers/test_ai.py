# backend/app/routers/test_ai.py
"""
Endpoints de teste para os services de IA
# Testar Groq
curl http://localhost:8000/test-ai/groq

# Testar Gemini
curl http://localhost:8000/test-ai/gemini

# Testar JSON
curl http://localhost:8000/test-ai/groq/json

# Comparar os dois
curl http://localhost:8000/test-ai/compare

# Ou abra no navegador:
# http://localhost:8000/test-ai/groq
# http://localhost:8000/test-ai/gemini
"""

from fastapi import APIRouter, HTTPException
from app.services.groq_service import GroqService
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/test-ai", tags=["🧪 Test AI"])

# ============================================
# TESTE: GROQ (Llama)
# ============================================
@router.get("/groq")
async def test_groq():
    """
    Testa se o Groq está funcionando
    
    Acesse: http://localhost:8000/test-ai/groq
    """
    try:
        service = GroqService()
        
        response = await service.generate(
            prompt="Diga 'Olá, Groq funcionando!' em uma frase",
            system_prompt="Você é um assistente amigável",
            temperature=0.5
        )
        
        return {
            "status": "✅ Groq funcionando!",
            "model": service.model,
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erro: {str(e)}")


@router.post("/groq/custom")
async def test_groq_custom(prompt: str):
    """
    Testa Groq com prompt customizado
    
    Exemplo:
    POST http://localhost:8000/test-ai/groq/custom?prompt=Explique Python
    """
    try:
        service = GroqService()
        
        response = await service.generate(
            prompt=prompt,
            temperature=0.7
        )
        
        return {
            "status": "success",
            "prompt": prompt,
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# TESTE: GEMINI
# ============================================
@router.get("/gemini")
async def test_gemini():
    """
    Testa se o Gemini está funcionando
    
    Acesse: http://localhost:8000/test-ai/gemini
    """
    try:
        service = GeminiService()
        
        response = await service.generate(
            prompt="Diga 'Olá, Gemini funcionando!' em uma frase. E qual é a sua Versão é 2?",
            temperature=0.5
        )
        
        return {
            "status": "✅ Gemini funcionando!",
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erro: {str(e)}")


@router.post("/gemini/custom")
async def test_gemini_custom(prompt: str):
    """
    Testa Gemini com prompt customizado
    """
    try:
        service = GeminiService()
        
        response = await service.generate(
            prompt=prompt,
            temperature=0.7
        )
        
        return {
            "status": "success",
            "prompt": prompt,
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# TESTE: JSON (Groq)
# ============================================
@router.get("/groq/json")
async def test_groq_json():
    """
    Testa geração de JSON com Groq
    """
    try:
        service = GroqService()
        
        response = await service.generate_json(
            prompt="Liste 3 linguagens de programação populares",
            system_prompt="Retorne um JSON com array 'languages'"
        )
        
        return {
            "status": "✅ JSON funcionando!",
            "response": response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================================
# TESTE: Comparação Groq vs Gemini
# ======================================
@router.get("/compare")
async def test_compare():
    """
    Compara resposta do Groq e Gemini para a mesma pergunta
    """
    try:
        prompt = "Explique o que é FastAPI em uma frase"
        
        # Groq
        groq = GroqService()
        groq_response = await groq.generate(prompt=prompt, temperature=0.5)
        
        # Gemini
        gemini = GeminiService()
        gemini_response = await gemini.generate(prompt=prompt, temperature=0.5)
        
        return {
            "prompt": prompt,
            "groq_response": groq_response,
            "gemini_response": gemini_response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))