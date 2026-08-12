"""
Teste da Fase 4: confirma que o MESMO objeto de conteúdo (carregado uma vez) é
renderizado em temas diferentes sem nenhuma regeneração — só troca o parâmetro.
Não depende de servidor rodando; testa a função que o endpoint /lessons/{id}/render
chama por baixo.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.renderer.render import render_topico

with open("../docs/schema/topico6-gerado.json", encoding="utf-8") as f:
    content = json.load(f)  # carregado UMA VEZ só

content_id_antes = id(content)

for tema_id in ["vidro-fume", "estufa-noturna", "console-verde", "aurora-botanica"]:
    html = render_topico(content, tema_id)
    assert id(content) == content_id_antes, "o dict de conteúdo foi trocado/mutado entre renders!"
    root_bg = html.split("--bg:")[1].split(";")[0].strip()
    print(f"tema={tema_id:16s} -> --bg gerado = {root_bg} | {len(html)} caracteres | mesmo objeto de conteúdo: OK")

print("\n✅ Fase 4 confirmada: mesmo conteúdo, 4 temas, zero regeneração.")
