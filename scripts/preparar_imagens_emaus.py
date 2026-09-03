# -*- coding: utf-8 -*-
"""
Prepara as imagens geradas pelo Gemini pro front do Emaus.

  python scripts/preparar_imagens_emaus.py capas
      imagem/capas/emaus/v1/*.png  ->  emaus-web/public/capas/{slug}.jpg  (3:2, ~1400px, jpg)

  python scripts/preparar_imagens_emaus.py marca emaus-simbolo-b.png
      recorta o fundo claro -> transparente, apara as bordas,
      salva em emaus-web/public/marca/emaus-simbolo.png
"""

import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
CAPAS_SRC = RAIZ / "imagem" / "capas" / "emaus" / "v1"
CAPAS_DST = RAIZ / "emaus-web" / "public" / "capas"
MARCA_SRC = RAIZ / "imagem" / "marca" / "emaus" / "v1"
MARCA_DST = RAIZ / "emaus-web" / "public" / "marca"


def preparar_capas() -> None:
    CAPAS_DST.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(CAPAS_SRC.glob("*.png"))
    if not arquivos:
        print(f"nada em {CAPAS_SRC}")
        return
    LARGURA_MAX = 1600  # o enquadramento 3:2 fica por conta do object-cover no CSS
    for src in arquivos:
        img = Image.open(src).convert("RGB")
        w, h = img.size
        if w > LARGURA_MAX:
            img = img.resize((LARGURA_MAX, round(h * LARGURA_MAX / w)), Image.LANCZOS)
        dst = CAPAS_DST / (src.stem + ".jpg")
        img.save(dst, "JPEG", quality=82, optimize=True)
        print(f"  {dst.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}")
    print(f"{len(arquivos)} capa(s) prontas em {CAPAS_DST.relative_to(RAIZ)}")


def preparar_marca(nome_arquivo: str) -> None:
    MARCA_DST.mkdir(parents=True, exist_ok=True)
    src = MARCA_SRC / nome_arquivo
    if not src.exists():
        print(f"nao achei {src}")
        return
    base = Image.open(src).convert("RGB")
    w, h = base.size
    hsv = base.convert("HSV")
    rgb_px = base.load()
    hsv_px = hsv.load()
    img = Image.new("RGBA", (w, h))
    out = img.load()
    # O pergaminho é claro E dessaturado; a tinta do desenho é escura OU saturada.
    # Alpha = quão "desenho" o pixel é (satura rápido pra manter o traço cheio).
    for y in range(h):
        for x in range(w):
            r, g, b = rgb_px[x, y]
            s = hsv_px[x, y][1]
            v = hsv_px[x, y][2]
            escuridao = max(0, 210 - v) / 210.0        # 0 claro .. 1 escuro
            satur = max(0, s - 28) / 227.0             # ignora ruído de cor do papel
            forca = max(escuridao * 1.4, satur * 1.7)
            alpha = max(0, min(255, int(forca * 255)))
            out[x, y] = (r, g, b, alpha)
    # apara pro bounding box do conteudo (só alpha significativo, ignora franja)
    alpha_forte = img.split()[3].point(lambda p: 255 if p > 35 else 0)
    bbox = alpha_forte.getbbox()
    if bbox:
        margem = 16
        x0 = max(0, bbox[0] - margem)
        y0 = max(0, bbox[1] - margem)
        x1 = min(w, bbox[2] + margem)
        y1 = min(h, bbox[3] + margem)
        img = img.crop((x0, y0, x1, y1))
    dst = MARCA_DST / "emaus-simbolo.png"
    img.save(dst, "PNG", optimize=True)
    print(f"marca salva em {dst.relative_to(RAIZ)}  ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo == "capas":
        preparar_capas()
    elif modo == "marca":
        preparar_marca(sys.argv[2] if len(sys.argv) > 2 else "emaus-simbolo-b.png")
    else:
        print(__doc__)
