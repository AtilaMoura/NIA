"""
Gera cópias leves (.otim.webp) das imagens de curso — 2026-09-27.

Por quê: as imagens dos tópicos vêm direto da câmera ou da IA (PNG/JPG de 1 a 4 MB,
até 4032x3024) e um tópico chegava a ~11 MB só de imagem. O renderizador
(app/renderer/render.py, filtro `imagem_web`) usa a cópia leve quando ela existe
ao lado da original; a original nunca é alterada nem apagada.

Idempotente: pula quem já tem cópia mais nova que a original.

Uso (precisa de Pillow — o container do backend não tem):
    pip install pillow
    python backend/scripts/otimizar_imagens.py            # backend/static/course-images
    python backend/scripts/otimizar_imagens.py --pasta X  # outra pasta
Em produção: rodar o mesmo comando no servidor, na pasta do repositório.
"""
import argparse
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent / "static" / "course-images"
SUFIXO = ".otim.webp"
LARGURA_MAX = 1600
QUALIDADE = 80
EXTENSOES = {".png", ".jpg", ".jpeg"}


def otimizar(original: Path) -> tuple[int, int] | None:
    destino = original.with_name(original.name + SUFIXO)
    if destino.exists() and destino.stat().st_mtime >= original.stat().st_mtime:
        return None
    with Image.open(original) as im:
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > LARGURA_MAX:
            altura = round(im.height * LARGURA_MAX / im.width)
            im = im.resize((LARGURA_MAX, altura), Image.LANCZOS)
        im.save(destino, "WEBP", quality=QUALIDADE, method=6)
    return original.stat().st_size, destino.stat().st_size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pasta", type=Path, default=RAIZ)
    args = ap.parse_args()

    antes = depois = feitas = puladas = 0
    for arq in sorted(args.pasta.rglob("*")):
        if arq.suffix.lower() not in EXTENSOES or arq.name.endswith(SUFIXO):
            continue
        r = otimizar(arq)
        if r is None:
            puladas += 1
            continue
        feitas += 1
        antes += r[0]
        depois += r[1]
        print(f"{r[0] // 1024:>6} KB -> {r[1] // 1024:>4} KB  {arq.relative_to(args.pasta)}")

    print(f"\n{feitas} otimizadas, {puladas} já estavam em dia")
    if feitas:
        print(f"Total: {antes / 1048576:.1f} MB -> {depois / 1048576:.1f} MB")


if __name__ == "__main__":
    main()
