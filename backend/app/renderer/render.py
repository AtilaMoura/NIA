"""
Fase 1 — Renderizador: JSON estruturado (schema em docs/schema/) + tema → HTML interativo.

Não usa IA. É código determinístico: o mesmo par (conteúdo, tema) sempre produz
o mesmo HTML. A camada de IA (Fase 2) só produz o JSON de conteúdo; quem decide
como isso vira slide/CSS/JS é este módulo.
"""

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
SCHEMA_DIR = BASE_DIR.parent.parent.parent / "docs" / "schema"  # renderer -> app -> backend -> NIA

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "j2"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def carregar_temas() -> dict:
    with open(SCHEMA_DIR / "temas.json", encoding="utf-8") as f:
        data = json.load(f)
    return {t["id"]: t for t in data["temas"]}


def _label_pergunta(secao: str, texto: str, limite: int = 52) -> str:
    texto = texto.strip().replace("\n", " ")
    if len(texto) > limite:
        texto = texto[:limite].rstrip() + "..."
    return f"{secao} — {texto}"


def montar_question_order(content: dict) -> list[dict]:
    """
    Varre os slides na ordem em que aparecem e monta a lista de perguntas
    (achatando os itens de classify) que o JS usa pra montar o resumo final.
    Substitui os arrays `order`/`labels` que antes eram escritos à mão por tópico.
    """
    ordem = []
    for slide in content["slides"]:
        if slide["tipo"] == "checkpoint":
            for pergunta in slide["perguntas"]:
                ordem.extend(_perguntas_para_ordem(slide["secao"], pergunta))
        elif slide["tipo"] == "avaliacao_pergunta":
            ordem.extend(_perguntas_para_ordem(slide["secao"], slide["pergunta"]))
    return ordem


def _perguntas_para_ordem(secao: str, pergunta: dict) -> list[dict]:
    if pergunta["tipo"] in ("classify", "associar"):
        out = []
        for item in pergunta["itens"]:
            out.append({
                "id": item["id"],
                "label": _label_pergunta(secao, "item: " + item["texto"]),
                "tipo": pergunta["tipo"] + "_item",
            })
        return out
    return [{
        "id": pergunta["id"],
        "label": _label_pergunta(secao, pergunta["enunciado"]),
        "tipo": pergunta["tipo"],
    }]


def render_topico(content: dict, theme_id: str = "vidro-fume") -> str:
    temas = carregar_temas()
    if theme_id not in temas:
        raise ValueError(
            f"Tema '{theme_id}' não encontrado. Disponíveis: {list(temas.keys())}"
        )
    tema = temas[theme_id]

    question_order = montar_question_order(content)
    open_total = sum(1 for q in question_order if q["tipo"] == "open")

    template = _env.get_template("topico.html.j2")
    return template.render(
        content=content,
        tema=tema,
        question_order_json=json.dumps(question_order, ensure_ascii=False),
        open_total=open_total,
    )


def render_topico_de_arquivo(caminho_json: str, theme_id: str = "vidro-fume") -> str:
    with open(caminho_json, encoding="utf-8") as f:
        content = json.load(f)
    return render_topico(content, theme_id)


if __name__ == "__main__":
    import sys

    caminho = sys.argv[1] if len(sys.argv) > 1 else str(SCHEMA_DIR / "schema-conteudo-topico.example.json")
    tema_id = sys.argv[2] if len(sys.argv) > 2 else "vidro-fume"
    html = render_topico_de_arquivo(caminho, tema_id)
    saida = Path(f"_render_teste_{tema_id}.html")
    saida.write_text(html, encoding="utf-8")
    print(f"Gerado: {saida.resolve()} ({len(html)} caracteres)")
