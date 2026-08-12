# backend/app/agents/quiz_agent.py
"""
QuizAgent (reescrito) — lê um tópico de CONTEÚDO já pronto (gerado pelo ContentAgent,
ver specialists/ia_agent.py) e escreve as perguntas: uma pra cada "checkpoint_apos"
marcado no conteúdo, e uma pra cada item de "avaliacao_conceitos".

Diferença chave pro QuizAgent antigo: ele via só um texto solto e "chutava" 10 perguntas
sem gabarito estruturado. Este vê o conteúdo real (JSON) e escreve em cima dele — evita
pergunta desalinhada com o que foi ensinado, e como é uma chamada só vendo todas as
perguntas que ele mesmo vai escrever, fica mais fácil não se repetir (ver Fase 2 no
PLANO_IMPLEMENTACAO_ESTUDO_IA.md — o agente único antigo repetia pergunta entre rodadas).
"""

import json

from .base_agent import BaseAgent

SCHEMA_PERGUNTAS = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "checkpoints": {
    "ck1": [ Pergunta, ... ],
    "ck2": [ Pergunta, ... ]
  },
  "avaliacao": {
    "ef1": Pergunta,
    "ef2": Pergunta,
    "ef3": Pergunta,
    "ef4": Pergunta,
    "ef5": Pergunta
  }
}

As chaves de "checkpoints" devem ser exatamente os gate_ids marcados em "checkpoint_apos"
no conteúdo (uma lista de 1 a 2 perguntas cada). As chaves de "avaliacao" devem ser
exatamente ef1..ef5, seguindo o "tipo" e o "testar" de cada item em "avaliacao_conceitos".

REGRA CRÍTICA DE TIPO: cada "checkpoint_apos" no conteúdo já vem com um campo "tipo"
(mc/tf/classify/open) — a pergunta que você escrever pra aquele gate_id TEM que usar
EXATAMENTE esse tipo, não escolha livremente. Isso existe porque, sem essa trava, os
checkpoints tendem a sair todos do mesmo tipo (geralmente todos "open") — já aconteceu
numa geração real (ver Fase 2b no plano) e deixa a avaliação desbalanceada, com mais
digitação pro aluno do que o necessário.

Cada objeto Pergunta é um desses 4 formatos — e TODOS OS QUATRO exigem o campo
"tipo" LITERALMENTE ESCRITO DENTRO DO OBJETO (não é só a categoria, é uma chave
de verdade: {"tipo": "mc", "id": ..., ...}). Um objeto Pergunta sem a chave "tipo"
é inválido, mesmo que todos os outros campos estejam certos:
- "tipo":"mc": {tipo, id, enunciado, cenario:null, opcoes:[string,string,string], correta_idx, explicacao}
- "tipo":"tf": {tipo, id, enunciado, cenario:null, correta_bool, explicacao}
- "tipo":"classify": {tipo, id, enunciado, cenario:null, rotulos_opcoes:[{valor,rotulo},{valor,rotulo}], itens:[{id,texto,correta}] (3 a 5 itens), explicacao}
- "tipo":"open": {tipo, id, enunciado, cenario (string ou null — use pra cenários de checkpoint aplicado), placeholder, explicacao: null}

REGRA CRÍTICA: nenhum "enunciado" pode se repetir nem ser muito parecido com outro
enunciado em NENHUM outro lugar deste mesmo JSON de saída — releia todas as perguntas
que você mesmo escreveu antes de finalizar e reescreva qualquer uma parecida demais com
outra. Cada pergunta testa um ângulo diferente do "testar"/"checkpoint_apos" pedido.

IDs de pergunta devem seguir o padrão do gate: ck1 com 1 pergunta -> id "ck1_1"; ck2 com
2 perguntas -> "ck2_1","ck2_2"; classify usa itens "ck1_1_1","ck1_1_2",...; avaliação usa
"ef1_1", "ef2_1" etc. Todo texto em português do Brasil.
""".strip()


class QuizAgent(BaseAgent):
    """Gera as perguntas de um tópico a partir do conteúdo já escrito."""

    async def generate_perguntas(self, conteudo: dict) -> dict:
        conteudo_resumido = {
            "titulo": conteudo.get("titulo"),
            "slides": [
                {
                    "secao": s.get("secao"),
                    "titulo_secao": s.get("titulo_secao"),
                    "blocos": s.get("blocos"),
                    "checkpoint_apos": s.get("checkpoint_apos"),
                }
                for s in conteudo.get("slides", [])
                if s.get("tipo") == "conteudo"
            ],
            "avaliacao_conceitos": conteudo.get("avaliacao_conceitos", []),
        }

        prompt = f"""
Você é o especialista em avaliação pedagógica. Abaixo está o conteúdo JÁ ESCRITO de um
tópico de estudo (não é seu trabalho editar o conteúdo, só escrever perguntas sobre ele).

CONTEÚDO DO TÓPICO:
{json.dumps(conteudo_resumido, ensure_ascii=False, indent=2)}

{SCHEMA_PERGUNTAS}
"""
        return await self.run_json_com_retry(prompt)
