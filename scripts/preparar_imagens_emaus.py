# -*- coding: utf-8 -*-
"""
Prepara as imagens geradas pelo Gemini pro front do Emaus.

  python scripts/preparar_imagens_emaus.py capas
      imagem/capas/emaus/v1/*.png  ->  emaus-web/public/capas/{slug}.jpg (jpg, ~1600px)

  python scripts/preparar_imagens_emaus.py marca <arquivo>
      recorta o fundo claro -> transparente  ->  emaus-web/public/marca/emaus-simbolo.png

  python scripts/preparar_imagens_emaus.py simbolos            (FASE 6)
      imagem/marca/emaus/v2/*.png  -> recorta fundo -> emaus-web/public/marca/v2/{stem}.png
      (as 5 variacoes, pra comparar no navegador antes de escolher)

  python scripts/preparar_imagens_emaus.py heroi               (FASE 6)
      imagem/heroi/emaus/v1/*.png  ->  emaus-web/public/heroi/{stem}.jpg
      (mantem o fundo pergaminho — o tema escuro cuida do resto com mascara)

  python scripts/preparar_imagens_emaus.py como-funciona       (FASE 6)
      imagem/como-funciona/emaus/v1/*.png -> recorta fundo -> emaus-web/public/como-funciona/{stem}.png

  python scripts/preparar_imagens_emaus.py recortar <origem.png> <destino.png>
      recorte de fundo generico (qualquer imagem sobre papel claro -> PNG transparente)
"""

import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
PUB = RAIZ / "emaus-web" / "public"


# ------------------------------------------------------------
# Recorte de fundo (pergaminho claro/dessaturado -> transparente)
# ------------------------------------------------------------
def recortar_fundo(src_img: Image.Image, aparar: bool = True, margem: int = 16) -> Image.Image:
    """O pergaminho e claro E dessaturado; a tinta do desenho e escura OU saturada.
    Alpha = quao 'desenho' o pixel e."""
    base = src_img.convert("RGB")
    w, h = base.size
    hsv = base.convert("HSV")
    rgb_px = base.load()
    hsv_px = hsv.load()
    img = Image.new("RGBA", (w, h))
    out = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = rgb_px[x, y]
            s = hsv_px[x, y][1]
            v = hsv_px[x, y][2]
            escuridao = max(0, 215 - v) / 215.0        # 0 claro .. 1 escuro
            satur = max(0, s - 26) / 229.0             # ignora ruido de cor do papel
            forca = max(escuridao * 1.45, satur * 1.75)
            alpha = max(0, min(255, int(forca * 255)))
            out[x, y] = (r, g, b, alpha)

    if aparar:
        alpha_forte = img.split()[3].point(lambda p: 255 if p > 35 else 0)
        bbox = alpha_forte.getbbox()
        if bbox:
            x0 = max(0, bbox[0] - margem)
            y0 = max(0, bbox[1] - margem)
            x1 = min(w, bbox[2] + margem)
            y1 = min(h, bbox[3] + margem)
            img = img.crop((x0, y0, x1, y1))
    return img


def _pngs(pasta: Path) -> list[Path]:
    return sorted(pasta.glob("*.png"))


# ------------------------------------------------------------
# Modos
# ------------------------------------------------------------
def preparar_capas() -> None:
    src_dir = RAIZ / "imagem" / "capas" / "emaus" / "v1"
    dst_dir = PUB / "capas"
    dst_dir.mkdir(parents=True, exist_ok=True)
    arquivos = _pngs(src_dir)
    if not arquivos:
        print(f"nada em {src_dir}")
        return
    for src in arquivos:
        img = Image.open(src).convert("RGB")
        w, h = img.size
        if w > 1600:
            img = img.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
        dst = dst_dir / (src.stem + ".jpg")
        img.save(dst, "JPEG", quality=82, optimize=True)
        print(f"  {dst.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}")
    print(f"{len(arquivos)} capa(s) prontas")


def preparar_heroi() -> None:
    src_dir = RAIZ / "imagem" / "heroi" / "emaus" / "v1"
    dst_dir = PUB / "heroi"
    dst_dir.mkdir(parents=True, exist_ok=True)
    arquivos = _pngs(src_dir)
    if not arquivos:
        print(f"nada em {src_dir}")
        return
    for src in arquivos:
        img = Image.open(src).convert("RGB")
        w, h = img.size
        lado = min(w, h)  # corta pro quadrado central (o carrossel usa quadrado)
        img = img.crop(((w - lado) // 2, (h - lado) // 2, (w + lado) // 2, (h + lado) // 2))
        if lado > 1200:
            img = img.resize((1200, 1200), Image.LANCZOS)
        dst = dst_dir / (src.stem + ".jpg")
        img.save(dst, "JPEG", quality=84, optimize=True)
        print(f"  {dst.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}")
    print(f"{len(arquivos)} imagem(ns) de herói prontas")


def preparar_simbolos() -> None:
    src_dir = RAIZ / "imagem" / "marca" / "emaus" / "v2"
    dst_dir = PUB / "marca" / "v2"
    dst_dir.mkdir(parents=True, exist_ok=True)
    arquivos = _pngs(src_dir)
    if not arquivos:
        print(f"nada em {src_dir}")
        return
    for src in arquivos:
        img = recortar_fundo(Image.open(src))
        dst = dst_dir / (src.stem + ".png")
        img.save(dst, "PNG", optimize=True)
        print(f"  {dst.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}")
    print(f"{len(arquivos)} símbolo(s) recortados — compare em /marca/v2/")


def preparar_como_funciona() -> None:
    src_dir = RAIZ / "imagem" / "como-funciona" / "emaus" / "v1"
    dst_dir = PUB / "como-funciona"
    dst_dir.mkdir(parents=True, exist_ok=True)
    arquivos = _pngs(src_dir)
    if not arquivos:
        print(f"nada em {src_dir}")
        return
    for src in arquivos:
        img = recortar_fundo(Image.open(src), margem=24)
        dst = dst_dir / (src.stem + ".png")
        img.save(dst, "PNG", optimize=True)
        print(f"  {dst.relative_to(RAIZ)}  {img.size[0]}x{img.size[1]}")
    print(f"{len(arquivos)} spot(s) de 'como funciona' recortados")


def preparar_marca(nome_arquivo: str) -> None:
    src = RAIZ / "imagem" / "marca" / "emaus" / "v1" / nome_arquivo
    if not src.exists():
        print(f"nao achei {src}")
        return
    (PUB / "marca").mkdir(parents=True, exist_ok=True)
    img = recortar_fundo(Image.open(src))
    dst = PUB / "marca" / "emaus-simbolo.png"
    img.save(dst, "PNG", optimize=True)
    print(f"marca salva em {dst.relative_to(RAIZ)}  ({img.size[0]}x{img.size[1]})")


def recortar_generico(origem: str, destino: str) -> None:
    src = Path(origem)
    if not src.is_absolute():
        src = RAIZ / src
    if not src.exists():
        print(f"nao achei {src}")
        return
    dst = Path(destino)
    if not dst.is_absolute():
        dst = RAIZ / dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    img = recortar_fundo(Image.open(src))
    img.save(dst, "PNG", optimize=True)
    print(f"recortado -> {dst}  ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo == "capas":
        preparar_capas()
    elif modo == "heroi":
        preparar_heroi()
    elif modo == "simbolos":
        preparar_simbolos()
    elif modo == "como-funciona":
        preparar_como_funciona()
    elif modo == "marca":
        preparar_marca(sys.argv[2] if len(sys.argv) > 2 else "emaus-simbolo-b.png")
    elif modo == "recortar" and len(sys.argv) >= 4:
        recortar_generico(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
