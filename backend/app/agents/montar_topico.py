# backend/app/agents/montar_topico.py
"""
Montagem determinística (sem IA) do tópico final a partir de:
- conteudo: saída do ContentAgent (specialists/ia_agent.py)
- perguntas: saída do QuizAgent (quiz_agent.py)

Fica aqui, em código, tudo que é padrão fixo entre tópicos (texto da intro de avaliação,
título do slide de resultado, contagem de badges) — não pedimos pra IA "lembrar" desses
padrões toda vez, é exatamente o tipo de coisa que uma geração solta erra (ver Fase 2:
o agente único antigo errou a contagem de checkpoints no badge).
"""


def _inferir_tipo_pergunta(p: dict) -> dict:
    """Rede de segurança: se a IA esqueceu o campo 'tipo' (já aconteceu — ver Fase 2
    no plano), infere pelos campos presentes em vez de deixar o renderizador quebrar."""
    if "tipo" in p and p["tipo"]:
        return p
    if "opcoes" in p and "correta_idx" in p:
        p["tipo"] = "mc"
    elif "correta_bool" in p:
        p["tipo"] = "tf"
    elif "rotulos_opcoes" in p and "itens" in p:
        p["tipo"] = "classify"
    elif "respostas_aceitas" in p:
        p["tipo"] = "lacuna"
    elif "placeholder" in p:
        p["tipo"] = "open"
    return p


def montar_topico(conteudo: dict, perguntas: dict, proximo_topico_label: str) -> dict:
    checkpoints = {
        gate_id: [_inferir_tipo_pergunta(p) for p in lista]
        for gate_id, lista in perguntas.get("checkpoints", {}).items()
    }
    avaliacao = {
        gate_id: _inferir_tipo_pergunta(p)
        for gate_id, p in perguntas.get("avaliacao", {}).items()
    }

    slides = [{"tipo": "capa", **_sem_chave(conteudo["slides"][0], "tipo")}]

    for slide in conteudo["slides"][1:]:
        if slide.get("tipo") != "conteudo":
            continue
        checkpoint_marker = slide.get("checkpoint_apos")
        slide_limpo = {k: v for k, v in slide.items() if k not in ("checkpoint_apos",)}
        slide_limpo["tipo"] = "conteudo"
        slides.append(slide_limpo)

        if checkpoint_marker:
            gate_id = checkpoint_marker["gate_id"]
            checkpoint_slide = {
                "tipo": "checkpoint",
                "secao": "Checkpoint",
                "gate_id": gate_id,
                "titulo_secao": "Checkpoint rápido",
                "perguntas": checkpoints.get(gate_id, []),
            }
            # "tipo_esperado" não é usado pelo renderizador (o template ignora chaves
            # que não conhece) — fica só pro validate.py conferir se o QuizAgent
            # respeitou o tipo que o ContentAgent pediu pra esse checkpoint.
            if checkpoint_marker.get("tipo"):
                checkpoint_slide["tipo_esperado"] = checkpoint_marker["tipo"]
            slides.append(checkpoint_slide)

    total_checkpoints = sum(
        1 for s in slides if s["tipo"] == "checkpoint"
    )

    slides.append({
        "tipo": "avaliacao_intro",
        "secao": "Avaliação Final",
        "titulo": "Avaliação Final",
        "subtitulo": "5 questões — algumas juntam mais de um conceito. Duas são abertas.",
        "instrucoes_box": {
            "label": "📋 Antes de começar",
            "texto": (
                "A correção objetiva já aparece na hora. Mas a avaliação final de "
                "verdade — com feedback honesto e a decisão de seguir ou reforçar — "
                "acontece quando você levar o resumo desta tela pro chat com o Claude."
            ),
        },
    })

    for concept in conteudo.get("avaliacao_conceitos", []):
        gate_id = concept["gate_id"]
        pergunta = avaliacao.get(gate_id)
        if not pergunta:
            continue
        slides.append({
            "tipo": "avaliacao_pergunta",
            "secao": "Avaliação Final",
            "gate_id": gate_id,
            "pergunta": pergunta,
        })

    slides.append({
        "tipo": "resultado",
        "secao": "Resultado",
        "titulo": "Resultado desta sessão",
        "proximo_topico_label": proximo_topico_label,
    })

    # Rede de segurança: já vimos a IA devolver 60min pra um slide deck de ~15 (Fase 2b).
    # O prompt agora pede 10-20 explicitamente, mas isso aqui garante o limite mesmo
    # se a IA ignorar a instrução de novo.
    duracao = max(10, min(20, conteudo.get("duracao_estimada_min", 12)))
    badges_capa = [
        f"⏱ ~{duracao} min",
        "🔊 áudio com controle de velocidade",
        f"✍️ {total_checkpoints} checkpoints + avaliação final",
    ]

    resultado = {
        "topico_id": conteudo["topico_id"],
        "titulo": conteudo["titulo"],
        "aula": conteudo["aula"],
        "numero": conteudo["numero"],
        "duracao_estimada_min": duracao,
        "roteiro": conteudo.get("roteiro", []),
        "badges_capa": badges_capa,
        "slides": slides,
    }
    # Achado real (2026-08-26, Tópico 2 do curso de obreiro): imagem_capa sumia
    # ao passar pelo montar_topico() de verdade — só funcionava antes porque o
    # Tópico 1 tinha sido montado à mão, sem passar por essa função.
    if conteudo.get("imagem_capa"):
        resultado["imagem_capa"] = conteudo["imagem_capa"]
    return resultado


def _sem_chave(d: dict, *chaves: str) -> dict:
    return {k: v for k, v in d.items() if k not in chaves}
