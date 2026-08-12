"""
Checagens determinísticas sobre o JSON de conteúdo — não usa IA.
É a base pro Reviewer da Fase 5 (que vai adicionar checagens semânticas via IA
em cima destas); estas aqui pegam erros estruturais óbvios que um prompt sozinho
provou não evitar de forma confiável (ver PLANO_IMPLEMENTACAO_ESTUDO_IA.md, Fase 2).
"""

import re

from .render import montar_question_order

_HEX_RE = re.compile(r"^#[0-9a-fA-F]{3,8}$")


def validar_topico(content: dict) -> list[str]:
    """Retorna uma lista de problemas encontrados (vazia = sem problemas)."""
    problemas = []

    # 1. Enunciados duplicados/quase idênticos entre perguntas com gate
    enunciados_vistos = {}
    for slide in content.get("slides", []):
        perguntas = []
        if slide["tipo"] == "checkpoint":
            perguntas = [(slide["gate_id"], p) for p in slide["perguntas"]]
        elif slide["tipo"] == "avaliacao_pergunta":
            perguntas = [(slide["gate_id"], slide["pergunta"])]
        for gate_id, p in perguntas:
            enunciado = (p.get("enunciado") or "").strip().lower()
            if not enunciado:
                continue
            if enunciado in enunciados_vistos:
                problemas.append(
                    f"Enunciado duplicado entre '{enunciados_vistos[enunciado]}' e "
                    f"'{gate_id}' ({p.get('id')}): \"{p['enunciado'][:70]}...\""
                )
            else:
                enunciados_vistos[enunciado] = gate_id

    # 2. gate_id repetido
    gate_ids = [s["gate_id"] for s in content.get("slides", []) if "gate_id" in s]
    for gid in set(gate_ids):
        if gate_ids.count(gid) > 1:
            problemas.append(f"gate_id '{gid}' aparece em mais de um slide.")

    # 3. IDs de pergunta repetidos
    ordem = montar_question_order(content)
    ids = [q["id"] for q in ordem]
    for qid in set(ids):
        if ids.count(qid) > 1:
            problemas.append(f"id de pergunta '{qid}' repetido.")

    # 4. Diagrama sem descrição de mecanismo (heurística: menos de 2 passos encadeados).
    # Bug corrigido aqui mesmo (achado testando o Tópico 6): a versão anterior contava
    # "→" como 1 ponto só não importa quantas vezes aparecesse, então uma descrição com
    # 3 setas de fluxo real (ex: "cliente → orquestrador → tool → resposta") era
    # sinalizada como fraca por engano. Agora conta ocorrências de "→"/"->" separadamente
    # das palavras de conector.
    palavras_conectoras = [" então ", " depois ", " decide ", " consulta ", " retorna "]
    for slide in content.get("slides", []):
        if slide["tipo"] != "conteudo":
            continue
        for bloco in slide.get("blocos", []):
            if bloco["tipo"] == "diagrama":
                desc = bloco.get("descricao", "")
                setas = desc.count("→") + desc.count("->")
                palavras = sum(1 for c in palavras_conectoras if c in desc.lower())
                if setas < 2 and palavras < 2:
                    problemas.append(
                        f"Diagrama '{bloco.get('id')}' parece descritivo demais, "
                        f"não narra um fluxo (só {setas} seta(s) e {palavras} palavra(s) de conector encontradas)."
                    )

    # 5b. "cor" de timeline precisa ser hex — achado testando o modo "pro" (Fase 2):
    # a IA devolveu "azul"/"verde"/"amarelo", que é CSS inválido pro jeito que o
    # renderizador usa isso (style="background:{cor}") — a cor simplesmente some.
    for slide in content.get("slides", []):
        if slide["tipo"] != "conteudo":
            continue
        for bloco in slide.get("blocos", []):
            if bloco["tipo"] == "timeline":
                for item in bloco.get("itens", []):
                    cor = item.get("cor", "")
                    if not _HEX_RE.match(cor):
                        problemas.append(
                            f"Timeline item '{item.get('titulo')}' tem cor '{cor}' que "
                            f"não é hex válido (ex: '#2c7fb8') — vai renderizar sem cor."
                        )

    # 5. Todo checkpoint/avaliação precisa ter pelo menos 1 pergunta
    for slide in content.get("slides", []):
        if slide["tipo"] == "checkpoint" and not slide.get("perguntas"):
            problemas.append(f"Checkpoint '{slide.get('gate_id')}' sem perguntas.")

    # 6. Tipo de pergunta do checkpoint bate com o "tipo" que o ContentAgent pediu
    # (ver montar_topico.py — "tipo_esperado"). Achado testando modo Pro (Fase 2b):
    # sem essa trava os checkpoints saíram todos "open".
    for slide in content.get("slides", []):
        if slide["tipo"] != "checkpoint" or not slide.get("tipo_esperado"):
            continue
        for p in slide.get("perguntas", []):
            if p.get("tipo") != slide["tipo_esperado"]:
                problemas.append(
                    f"Checkpoint '{slide['gate_id']}' pedia tipo '{slide['tipo_esperado']}' "
                    f"mas a pergunta '{p.get('id')}' saiu tipo '{p.get('tipo')}'."
                )

    # 7. Duração dentro da faixa esperada (10-20min) — já tem um clamp em
    # montar_topico.py, isso aqui é só pra sinalizar se algo estranho passou.
    duracao = content.get("duracao_estimada_min")
    if duracao is not None and not (10 <= duracao <= 20):
        problemas.append(f"duracao_estimada_min = {duracao}, fora da faixa esperada (10-20).")

    # 8. Pelo menos 1 diagrama no tópico inteiro (independe de modo Comum ou Pro).
    tem_diagrama = any(
        b["tipo"] == "diagrama"
        for s in content.get("slides", []) if s["tipo"] == "conteudo"
        for b in s.get("blocos", [])
    )
    if not tem_diagrama:
        problemas.append("Nenhum bloco 'diagrama' encontrado no tópico inteiro.")

    return problemas


if __name__ == "__main__":
    import json
    import sys

    caminho = sys.argv[1] if len(sys.argv) > 1 else "../docs/schema/topico6-gerado.json"
    with open(caminho, encoding="utf-8") as f:
        content = json.load(f)
    problemas = validar_topico(content)
    if not problemas:
        print("✅ Nenhum problema estrutural encontrado.")
    else:
        print(f"⚠️ {len(problemas)} problema(s) encontrado(s):")
        for p in problemas:
            print(f" - {p}")
