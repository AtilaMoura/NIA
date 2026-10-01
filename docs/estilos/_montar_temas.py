# -*- coding: utf-8 -*-
"""
Renderiza o MESMO tópico real (Redes T1 "O que é um endereço IP") em cada tema de
docs/schema/temas.json, pra comparar temas lado a lado no catálogo visual.

- Usa o renderizador do backend direto (sem Docker/API)
- Troca as URLs http://localhost:8100/static/... por caminhos relativos e copia
  as imagens usadas (versão leve .otim.webp) pra docs/estilos/temas/img/
- Saída: docs/estilos/temas/<tema>.html + docs/estilos/temas.json (lista pro catálogo)

Rodar da raiz do repo:  python docs/estilos/_montar_temas.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "backend"))

from app.renderer.render import render_topico, carregar_temas  # noqa: E402

TOPICO_JSON = RAIZ / "backend" / "_topico1_redes_final.json"
STATIC = RAIZ / "backend" / "static"
SAIDA = Path(__file__).resolve().parent / "temas"
SAIDA_IMG = SAIDA / "img"
SAIDA_IMG.mkdir(parents=True, exist_ok=True)

content = json.loads(TOPICO_JSON.read_text(encoding="utf-8"))
temas = carregar_temas()
# carregar_temas() devolve {id: tema}
lista = list(temas.values()) if isinstance(temas, dict) else temas

resumo = []
padrao_url = re.compile(r"https?://[^\"')\s]+?/static/([^\"')\s?]+)")

for tema in lista:
    html = render_topico(content, theme_id=tema["id"])

    def trocar(m):
        rel = m.group(1)
        origem = STATIC / rel
        if origem.is_file():
            destino = SAIDA_IMG / origem.name
            if not destino.exists():
                shutil.copy2(origem, destino)
            return f"img/{origem.name}"
        return m.group(0)

    html = padrao_url.sub(trocar, html)
    (SAIDA / f"{tema['id']}.html").write_text(html, encoding="utf-8")
    sobra = re.findall(r"https?://localhost[^\"'\s]*", html)
    # Tema com 'coresDark' tem as duas versões (o render aceita ?modo=light|dark);
    # sem ele, é versão única — clara ou escura conforme a luminância do fundo
    bg = tema["cores"]["bg"].lstrip("#")
    fundo_escuro = sum(int(bg[i:i + 2], 16) for i in (0, 2, 4)) < 3 * 128
    versoes = ["claro", "escuro"] if tema.get("coresDark") else (["escuro"] if fundo_escuro else ["claro"])
    resumo.append({"id": tema["id"], "nome": tema["nome"], "descricao": tema.get("descricao", ""),
                   "arquivo": f"temas/{tema['id']}.html", "versoes": versoes})
    print(f"{tema['id']}: ok, {len(sobra)} referência(s) a localhost restantes")

(Path(__file__).resolve().parent / "temas.json").write_text(
    json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(resumo)} temas renderizados")
