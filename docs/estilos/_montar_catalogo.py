# -*- coding: utf-8 -*-
"""
Monta docs/estilos/catalogo-estilos.html a partir de catalogo.json.

- Converte cada imagem de exemplo pra JPEG leve (960px, q78) em docs/estilos/img/<id>.jpg
- Injeta o catálogo (com o campo "img" relativo) no _template_catalogo.html
- Estilo sem imagem ainda gerada aparece com placeholder na página

Rodar da raiz do repo:  python docs/estilos/_montar_catalogo.py
"""
import json
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
PASTA = Path(__file__).resolve().parent
PASTA_IMG = PASTA / "img"
PASTA_IMG.mkdir(exist_ok=True)

catalogo = json.loads((PASTA / "catalogo.json").read_text(encoding="utf-8"))

faltando = []
for estilo in catalogo["estilos"]:
    origem = RAIZ / estilo["imagem"]
    destino = PASTA_IMG / f"{estilo['id']}.jpg"
    if not origem.exists():
        estilo["img"] = None
        faltando.append(estilo["id"])
        continue
    with Image.open(origem) as im:
        im = im.convert("RGB")
        im.thumbnail((960, 960))
        im.save(destino, "JPEG", quality=78, optimize=True)
    estilo["img"] = f"img/{destino.name}"

# Temas renderizados por _montar_temas.py (rodar antes)
catalogo["temas"] = json.loads((PASTA / "temas.json").read_text(encoding="utf-8"))

template = (PASTA / "_template_catalogo.html").read_text(encoding="utf-8")
html = template.replace("/*__CATALOGO__*/null", json.dumps(catalogo, ensure_ascii=False))
(PASTA / "catalogo-estilos.html").write_text(html, encoding="utf-8")

print(f"OK: {len(catalogo['estilos'])} estilos, {len(faltando)} sem imagem: {faltando}")
