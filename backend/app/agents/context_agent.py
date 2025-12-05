# backend/app/agents/specialist_agent.py

from .base_agent import BaseAgent
import json
import re

class ContextAgent(BaseAgent):
    """
    Gera texto para o SpecialistAgent
    """

    async def json_text(self, 
                        course: str, 
                        module: str,
                        lessons: str,
                        ) -> dict:
        """
        Gera estrutura JSON do curso
        """
        print("entrei no generate!!!")

        info_json = json.dumps({
                "course": course,
                "module": module,
                "lessons": lessons
            }, ensure_ascii=False, indent=4)

        prompt = f"""
                You are a prompt creation specialist agent, focused on carefully interpreting all the information provided in JSON.
                Your goal is to transform this data into a didactic, coherent, and well-structured prompt for another agent.
                
                The final prompt must be written **in English**, but must instruct the other agent to produce the response **in Brazilian Portuguese**.
                
                Your task is:
                
                1. Read and fully interpret all fields of the JSON.
                
                2. Transform this information into a clear, concise, and well-structured prompt in English.
                
                3. The generated prompt must include:
                
                - Context
                
                - Objective
                - Constraints
                - Expected output format
                
                - Any relevant additional details extracted from the JSON
                
                Ensure that the English prompt explicitly instructs the agent to respond in Brazilian Portuguese.
                
                Here is the information:

                {info_json}            

                only the prompt in the response
                """
        
        
        try:
            return await self.run(prompt)
        except Exception as e:
                print(f"⚠️ Erro ao gerar Prompt: {e}")
                