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

    async def generate_lesson_content(self, prompt: str, course: str) -> dict:
      """
      Gera o conteúdo COMPLETO de uma aula (Lesson) em JSON compatível com o banco.
      """
      final_prompt_old = f"""
        You are the SpecialistAgent {course}.

        Your task is to generate the full content of a lesson based on the following instructions:

        ---------------------
        {prompt}
        ---------------------

        ⚠️ OUTPUT RULES — FOLLOW STRICTLY:
        1. Return ONLY a valid JSON object. Do NOT add text before or after the JSON.
        2. The lesson MUST be written entirely in Brazilian Portuguese.
        3. "content" must contain a COMPLETE Markdown lesson — detailed, structured, and not short.
        4. The JSON must contain EXACTLY these fields:

        {{
          "title": "...",
          "content": "...",
          "estimated_read_time_minutes": 0,
          "generated_by": "SpecialistAgent"
        }}

        5. "estimated_read_time_minutes" must be based on length (~200 palavras = 1 minuto).
        6. Do NOT add any extra fields under ANY circumstance.
        7. Do NOT wrap the JSON in code blocks.
        8. Ensure the JSON produced is valid, properly escaped, and without Markdown fences.
        """
      
      final_prompt = f"""
      You are the SpecialistAgent.

      Your task is to generate the complete lesson content based on the instructions below.

      ---------------------
      {prompt}
      ---------------------

      ⚠️ OUTPUT RULES — FOLLOW THEM STRICTLY:

      1. Return ONLY a Markdown lesson (no JSON, no code blocks, no backticks).
      2. The lesson MUST be written entirely in Brazilian Portuguese.
      3. The lesson MUST be complete, detailed, well-structured, and written for humans — not summarized.
      4. The Markdown must include:
        - Título da lição
        - Seções e subseções organizadas
        - Exemplos, explicações e conclusões
      5. At the very end of the output, add this line:
        estimated_read_time_minutes: X
        Where X is the estimated reading time based on text length 
        (approximately 200 words = 1 minute).
      6. Do NOT include any other metadata, JSON, keys, wrappers or comments.
      7. Do NOT wrap anything in ``` or any Markdown code delimiters.

      Your output must be ONLY the Markdown lesson followed by the time estimate.
      """

      



      if hasattr(self.service, 'generate_json'):
          try:
              return await self.run(final_prompt)
          except Exception:
              text = await self.run(final_prompt)
              return self._extract_json(text)
      text = await self.run(final_prompt)
      return self._extract_json(text)
  