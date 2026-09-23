"""Monta o contexto de texto de um tópico pro tira-dúvida em chat (2026-09-23).

O content do tópico é um JSON grande (narração de áudio, prompts de imagem,
gabarito...) — tópico real chega a 55 mil caracteres. O Groq tem teto de
8000 tokens/minuto POR REQUISIÇÃO (prompt + max_tokens), então aqui só sobra
o texto que o aluno de fato lê na tela, com teto de tamanho.

Reaproveitável pro chat fora do curso (ainda não existe): lá a ideia é mandar
só o resumo do tópico/módulo/curso, não o texto inteiro — decisão do Atila.
"""

import json

# Chaves que nunca são texto de leitura do aluno (áudio, imagem, ids, rótulos
# de estilo). "explicacao" é o gabarito comentado do checkpoint — fica de fora
# pra IA não entregar a resposta de um exercício que o aluno ainda vai fazer.
_CHAVES_IGNORADAS = {
    "narracao", "tipo", "id", "gate_id", "tipo_esperado", "correta_idx",
    "imagem", "imagem_capa", "imagem_sugerida", "prompt", "url", "src", "alt",
    "proximo_topico_label", "audio", "variante", "secao", "explicacao",
}

TETO_TOPICO = 9000  # ~2.500 tokens em português
TETO_SLIDE = 3000


def _coletar_textos(valor, saida: list[str]) -> None:
    """Percorre o JSON do slide e junta as strings de leitura, em ordem."""
    if isinstance(valor, str):
        texto = valor.strip()
        if texto:
            saida.append(texto)
    elif isinstance(valor, list):
        for item in valor:
            _coletar_textos(item, saida)
    elif isinstance(valor, dict):
        for chave, item in valor.items():
            if chave in _CHAVES_IGNORADAS or chave.startswith("imagem"):
                continue
            _coletar_textos(item, saida)


def texto_do_slide(slide: dict) -> str:
    partes: list[str] = []
    _coletar_textos(slide, partes)
    return "\n".join(partes)


def carregar_content(topico) -> dict:
    return topico.content if isinstance(topico.content, dict) else json.loads(topico.content or "{}")


def montar_contexto_duvida(content: dict, slide_index: int, teto_topico: int = TETO_TOPICO) -> tuple[str, str]:
    """Devolve (texto do tópico inteiro, texto do slide em foco).

    O tópico inteiro vai numerado por slide pra IA conseguir ligar a dúvida a
    outras partes do material; se passar do teto, corta os slides mais
    distantes do slide atual primeiro (o entorno importa mais)."""
    slides = content.get("slides", [])
    blocos = [
        (i, f"[Slide {i + 1}]\n{texto_do_slide(s)}")
        for i, s in enumerate(slides)
        if s.get("tipo") not in ("capa", "resultado")
    ]

    slide_foco = ""
    if 0 <= slide_index < len(slides):
        slide_foco = texto_do_slide(slides[slide_index])[:TETO_SLIDE]

    # Mais perto do slide atual primeiro, até estourar o teto
    escolhidos: list[tuple[int, str]] = []
    total = 0
    for i, bloco in sorted(blocos, key=lambda b: abs(b[0] - slide_index)):
        if total + len(bloco) > teto_topico:
            continue
        escolhidos.append((i, bloco))
        total += len(bloco)
    texto_topico = "\n\n".join(b for _, b in sorted(escolhidos))
    return texto_topico, slide_foco


def montar_gabarito_abertas(slides: list[dict]) -> str:
    """Resposta esperada de cada pergunta ABERTA, com o MESMO rótulo que o
    resumo do aluno usa (render.montar_question_order) — pra IA que avalia o
    fim do tópico/prova comparar com o material, não com o "achismo" dela.

    Achado real (2026-09-23, Tópico 19): sem isso o tutor marcou como erro
    conceitual uma resposta que repetia quase literalmente o material
    ("IDs atribuídos por frequência/ordem de descoberta")."""
    from app.renderer.render import _label_pergunta

    linhas: list[str] = []
    for slide in slides:
        if slide.get("tipo") == "checkpoint":
            perguntas = slide.get("perguntas", [])
        elif slide.get("tipo") == "avaliacao_pergunta":
            perguntas = [slide.get("pergunta") or {}]
        else:
            continue
        for p in perguntas:
            if p.get("tipo") != "open":
                continue
            item = f"- {_label_pergunta(slide.get('secao', ''), p.get('enunciado', ''))}"
            if p.get("cenario"):
                item += f"\n  Cenário: {p['cenario']}"
            esperado = p.get("resposta_modelo") or p.get("explicacao")
            if esperado:
                item += f"\n  Resposta esperada (do próprio material): {esperado}"
            linhas.append(item)
    return "\n".join(linhas)
