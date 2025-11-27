# backend/app/agents/specialist_agent.py

from .base_agent import BaseAgent
import json
import re

class SpecialistAgent(BaseAgent):
    """
    Gera o conteúdo bruto do curso
    """

    async def generate_course_structure(self, topic: str, level: str, goal: str) -> dict:
        """
        Gera estrutura JSON do curso
        """
        print("entrei no generate!!!")
        prompt = f"""
                  Crie uma estrutura completa de curso para iniciantes.

                  **TÓPICO DO CURSO:** {topic}
                  **NÍVEL DE DIFICULDADE:** {level}
                  **OBJETIVO DO ALUNO:** {goal}

                  Gere {3} módulos com {3} aulas cada.

                  **INSTRUÇÕES CRÍTICAS:**
                  1. Retorne APENAS um objeto JSON válido.
                  2. Não gere o conteúdo detalhado das aulas. O campo "content" dentro de "lessons" deve ser uma **string vazia ("")** ou um **placeholder breve** como "Conteúdo a ser gerado".

                  Retorne o JSON estritamente no seguinte formato:

                  {{
                    "title": "Título do Curso sobre {topic}",
                    "description": "Uma descrição concisa e atraente baseada no objetivo e nível.",
                    "modules": [
                      {{
                        "index": 1,
                        "title": "Título do Módulo 1 (Ex: Fundamentos)",
                        "description": "Breve descrição do que será aprendido neste módulo.",
                        "lessons": [
                          {{"title": "Título da Aula 1.1", "content": ""}}, 
                          {{"title": "Título da Aula 1.2", "content": ""}},
                          {{"title": "Título da Aula 1.3", "content": ""}}
                        ]
                      }},
                      {{
                        "index": 2,
                        "title": "Título do Módulo 2",
                        "description": "Breve descrição do que será aprendido neste módulo.",
                        "lessons": [
                          {{"title": "Título da Aula 2.1", "content": ""}},
                          // ... (Continue para o módulo 3)
                        ]
                      }}
                      // ... (Até o número de módulos desejado)
                    ]
                  }}
                  """
        
        # ✅ Usa generate_json para garantir dict
        if hasattr(self.service, 'generate_json'):
            try:
                return await self.service.generate_json(prompt)
            except Exception as e:
                print(f"⚠️ Erro ao gerar JSON: {e}")
                # Fallback: tenta extrair JSON do texto
                text = await self.run(prompt)
                return self._extract_json(text)
        else:
            # Fallback para services sem generate_json
            text = await self.run(prompt)
            return self._extract_json(text)
    
    def _extract_json(self, text: str) -> dict:
        """
        Extrai JSON de uma string
        """
        try:
            # Remove markdown
            text = re.sub(r'```json\n?', '', text)
            text = re.sub(r'```\n?', '', text)
            
            # Tenta parsear direto
            return json.loads(text.strip())
        except:
            # Tenta encontrar JSON no meio do texto
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
        
        # Fallback: retorna estrutura mínima
        return {
            "title": "Erro ao gerar",
            "description": text[:200],
            "modules": []
        }