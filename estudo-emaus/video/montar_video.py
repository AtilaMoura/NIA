# -*- coding: utf-8 -*-
"""
Monta um vídeo curto (narração TTS + ilustrações com Ken Burns + legenda) a partir de
um JSON de roteiro. Áudio: Gemini TTS (mesma chave do backend). Vídeo: ffmpeg.

Uso:
    python estudo-emaus/video/montar_video.py estudo-emaus/video/piloto_partir_do_pao.json

Saída: <mesmo nome do json>.mp4 na pasta do json, e os intermediários em _work/.
"""
import base64, json, os, re, struct, subprocess, sys, time, wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import google.genai as genai
from google.genai import types

RAIZ = Path(__file__).resolve().parents[2]
IMG_DIR = RAIZ / "imagem" / "emaus" / "cenas" / "v1"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FONTS = {
    "serif": r"C:\Windows\Fonts\georgia.ttf",
    "serif_it": r"C:\Windows\Fonts\georgiai.ttf",
    "sans": r"C:\Windows\Fonts\segoeui.ttf",
    "sans_b": r"C:\Windows\Fonts\segoeuib.ttf",
}
# paleta do estudo
INK = (244, 239, 226)
BOX = (22, 21, 27)
CLAY = (224, 144, 108)


def _key():
    env = (RAIZ / "backend" / ".env").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^GEMINI_API_KEY=(.+)$", env, re.M)
    return m.group(1).strip().strip('"')


def tts(client, texto, voz, estilo, destino: Path):
    if destino.exists():
        return
    prompt = f"{estilo}\n\n{texto}"
    ult = None
    for tent in range(4):
        try:
            r = client.models.generate_content(
                model="models/gemini-2.5-flash-preview-tts",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voz)
                        )
                    ),
                ),
            )
            pcm = r.candidates[0].content.parts[0].inline_data.data
            with wave.open(str(destino), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
                w.writeframes(pcm)
            return
        except Exception as e:  # noqa
            ult = e
            print(f"   TTS tentativa {tent+1} falhou: {str(e)[:120]}")
            time.sleep(8 * (tent + 1))
    raise RuntimeError(f"TTS falhou de vez: {ult}")


def dur_wav(p: Path) -> float:
    with wave.open(str(p), "rb") as w:
        return w.getnframes() / w.getframerate()


def _font(path, size):
    return ImageFont.truetype(path, size)


def legenda_png(texto, largura, destino: Path):
    """Renderiza a legenda como PNG transparente (caixa arredondada + texto)."""
    fnt = _font(FONTS["serif_it"], 46)
    linhas = texto.split("\n")
    pad_x, pad_y, gap = 46, 34, 12
    tmp = Image.new("RGBA", (10, 10)); d = ImageDraw.Draw(tmp)
    lh = max(d.textbbox((0, 0), "Ay", font=fnt)[3] for _ in [0])
    tw = max(d.textbbox((0, 0), l, font=fnt)[2] for l in linhas)
    box_w = min(largura - 80, tw + pad_x * 2)
    box_h = lh * len(linhas) + gap * (len(linhas) - 1) + pad_y * 2
    im = Image.new("RGBA", (largura, box_h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (largura - box_w) // 2
    d.rounded_rectangle([x0, 4, x0 + box_w, 4 + box_h], radius=22, fill=BOX + (190,))
    y = 4 + pad_y
    for l in linhas:
        w = d.textbbox((0, 0), l, font=fnt)[2]
        d.text(((largura - w) // 2, y), l, font=fnt, fill=INK + (255,))
        y += lh + gap
    im.save(destino)
    return im.size[1]


def card_titulo(titulo, subtitulo, tamanho, destino: Path):
    W, H = tamanho
    im = Image.new("RGB", (W, H), (26, 24, 32))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 6], fill=CLAY)
    f_kick = _font(FONTS["sans_b"], 30)
    f_tit = _font(FONTS["serif"], 92 if W < H else 108)
    f_sub = _font(FONTS["serif_it"], 40)
    kick = "ESTUDO EM VÍDEO"
    kw = d.textbbox((0, 0), kick, font=f_kick)[2]
    d.text(((W - kw) // 2, H * 0.34), kick, font=f_kick, fill=(231, 201, 140))
    # título (pode quebrar)
    palavras = titulo.split()
    linhas, cur = [], ""
    for p in palavras:
        t = (cur + " " + p).strip()
        if d.textbbox((0, 0), t, font=f_tit)[2] > W - 160 and cur:
            linhas.append(cur); cur = p
        else:
            cur = t
    linhas.append(cur)
    y = H * 0.40
    for l in linhas:
        w = d.textbbox((0, 0), l, font=f_tit)[2]
        d.text(((W - w) // 2, y), l, font=f_tit, fill=(253, 250, 241))
        y += f_tit.size * 1.12
    sw = d.textbbox((0, 0), subtitulo, font=f_sub)[2]
    d.text(((W - sw) // 2, y + 18), subtitulo, font=f_sub, fill=(217, 205, 176))
    im.save(destino)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERRO:\n", r.stderr[-2500:])
        raise SystemExit(1)


_CACHE = {}


def _bg_plate(img: Path, tamanho, work: Path) -> Path:
    """Placa de fundo estática: imagem preenchendo o quadro, borrada e escurecida. 1x por imagem."""
    W, H = tamanho
    out = work / f"_bg_{img.stem}_{W}x{H}.png"
    if not out.exists():
        run([
            FFMPEG, "-y", "-i", str(img),
            "-vf", (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                    f"boxblur=40:4,eq=brightness=-0.12:saturation=0.72"),
            "-frames:v", "1", str(out),
        ])
    return out


def _vignette_png(tamanho, work: Path) -> Path:
    """Vinheta radial estática (RGBA). 1x por tamanho."""
    W, H = tamanho
    out = work / f"_vig_{W}x{H}.png"
    if not out.exists():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = W / 2, H / 2
        maxr = (cx ** 2 + cy ** 2) ** 0.5
        step = 6
        for r in range(int(maxr), 0, -step):
            p = r / maxr
            a = int(150 * max(0.0, (p - 0.55) / 0.45) ** 1.7)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, a))
        im = im.filter(ImageFilter.GaussianBlur(40))
        im.save(out)
    return out


def _dust_clip(tamanho, assets: Path) -> Path:
    """Loop de ~8s de poeira/brilho flutuante. 1x por tamanho."""
    W, H = tamanho
    key = f"dust{W}x{H}"
    if key in _CACHE:
        return _CACHE[key]
    assets.mkdir(parents=True, exist_ok=True)
    out = assets / f"dust_{W}x{H}.mp4"
    if not out.exists():
        dw, dh = W // 2, H // 2
        run([
            FFMPEG, "-y", "-f", "lavfi", "-i",
            (f"color=c=black:s={dw}x{dh}:d=8:r=24,format=gray,"
             f"noise=alls=60:allf=t+u,curves=all='0/0 0.9/0 0.965/0.5 1/1',"
             f"gblur=sigma=1.3,scroll=horizontal=0.0004:vertical=0.0010"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
            "-pix_fmt", "yuv420p", "-an", str(out),
        ])
    _CACHE[key] = out
    return out


def _kenburns(mov, T, zbase=1.10):
    """Expressões de zoompan por modo de movimento (E = progresso linear 0..1)."""
    E = f"(on/{T})"
    cx = "iw/2-(iw/zoom/2)"
    cy = "ih/2-(ih/zoom/2)"
    if mov == "out":
        return f"z='{1.0+ (zbase-1.0)*1.3:.3f}-{(zbase-1.0)*1.3:.3f}*{E}':x='{cx}':y='{cy}'"
    if mov == "left":
        return f"z='{zbase}':x='(iw-iw/zoom)*(1-{E})':y='(ih-ih/zoom)/2'"
    if mov == "right":
        return f"z='{zbase}':x='(iw-iw/zoom)*{E}':y='(ih-ih/zoom)/2'"
    if mov == "up":
        return f"z='{zbase}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*(1-{E})'"
    if mov == "down":
        return f"z='{zbase}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*{E}'"
    # "in" (padrão)
    return f"z='1.0+{(zbase-1.0)*1.3:.3f}*{E}':x='{cx}':y='{cy}'"


def segmento_mp4(img: Path, wav: Path, cap_png: Path, cap_h, tamanho, saida: Path,
                 mov="in", luz=None, movimento=True):
    W, H = tamanho
    work = saida.parent
    d = dur_wav(wav) + 0.5
    T = max(2, int(d * 30))
    vertical = H > W
    if vertical:
        pic_w, pic_h = W, 604
        y_pic = 548
        y_cap = y_pic + pic_h + 46
    else:
        pic_h = 940
        pic_w = int(pic_h * 16 / 9)
        y_pic = 60
        y_cap = H - cap_h - 56
    up = pic_w + 260
    kb = _kenburns(mov, T)

    bg_png = _bg_plate(img, tamanho, work)
    vig_png = _vignette_png(tamanho, work) if movimento else None
    dust = _dust_clip(tamanho, saida.parents[2] / "_assets") if movimento else None

    # inputs: 0 bg  1 fg-img  2 wav  3 cap  [4 vig] [5 dust]
    inputs = [
        "-loop", "1", "-framerate", "30", "-t", f"{d:.2f}", "-i", str(bg_png),
        "-loop", "1", "-framerate", "30", "-t", f"{d:.2f}", "-i", str(img),
        "-i", str(wav),
        "-loop", "1", "-t", f"{d:.2f}", "-i", str(cap_png),
    ]
    idx = 4
    vig_i = dust_i = None
    if vig_png:
        inputs += ["-loop", "1", "-t", f"{d:.2f}", "-i", str(vig_png)]; vig_i = idx; idx += 1
    if dust:
        inputs += ["-stream_loop", "-1", "-t", f"{d:.2f}", "-i", str(dust)]; dust_i = idx; idx += 1

    steps = [
        f"[1:v]scale={up}:-1:flags=lanczos,zoompan={kb}:d=1:fps=30:s={pic_w}x{pic_h},"
        f"setsar=1,pad={pic_w+6}:{pic_h+6}:3:3:color=0xEFE6D0@0.55[fg]",
        f"[0:v][fg]overlay=(W-w)/2:{y_pic}[s1]",
    ]
    last = "s1"
    if dust_i is not None:
        steps.append(f"[{dust_i}:v]scale={W}:{H},format=gbrp[dst]")
        steps.append(f"[{last}][dst]blend=all_mode=screen:all_opacity=0.12,format=yuv420p[s2]")
        last = "s2"
    steps.append(f"[{last}][3:v]overlay=(W-w)/2:{y_cap}[s3]")
    last = "s3"
    if vig_i is not None:
        steps.append(f"[{last}][{vig_i}:v]overlay=0:0[s4]")
        last = "s4"
    flick = ""
    if movimento and luz == "quente":
        flick = ("eq=brightness='0.012*sin(2*PI*t*1.6)+0.006*sin(2*PI*t*5.1)':"
                 "saturation='1+0.02*sin(2*PI*t*1.6)',")
    grain = "noise=alls=5:allf=t," if movimento else ""
    steps.append(f"[{last}]{flick}{grain}format=yuv420p[v]")
    fc = ";".join(steps)

    run([
        FFMPEG, "-y", *inputs,
        "-filter_complex", fc,
        "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-t", f"{d:.2f}", str(saida),
    ])


def card_mp4(card_png: Path, tamanho, saida: Path, seg=2.6):
    run([
        FFMPEG, "-y", "-loop", "1", "-t", f"{seg}", "-i", str(card_png),
        "-f", "lavfi", "-t", f"{seg}", "-i", "anullsrc=r=48000:cl=mono",
        "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", str(saida),
    ])


def main():
    roteiro = Path(sys.argv[1])
    cfg = json.loads(roteiro.read_text(encoding="utf-8"))
    work = roteiro.parent / "_work" / roteiro.stem
    work.mkdir(parents=True, exist_ok=True)
    tamanho = (1080, 1920) if cfg.get("formato", "9:16") == "9:16" else (1920, 1080)

    client = genai.Client(api_key=_key())

    partes = []

    card_png = work / "card.png"
    card_titulo(cfg["titulo"], cfg["subtitulo"], tamanho, card_png)
    card_v = work / "00_card.mp4"
    card_mp4(card_png, tamanho, card_v)
    partes.append(card_v)

    for i, s in enumerate(cfg["segmentos"], 1):
        print(f"[{i}/{len(cfg['segmentos'])}] {s['imagem']}")
        wav = work / f"{i:02d}.wav"
        tts(client, s["narracao"], cfg["voz"], cfg["estilo"], wav)
        cap_png = work / f"{i:02d}_cap.png"
        cap_h = legenda_png(s["legenda"], tamanho[0], cap_png)
        seg_v = work / f"{i:02d}.mp4"
        movs = ["in", "left", "out", "right", "up"]
        segmento_mp4(
            IMG_DIR / s["imagem"], wav, cap_png, cap_h, tamanho, seg_v,
            mov=s.get("mov", movs[(i - 1) % len(movs)]),
            luz=s.get("luz"),
            movimento=cfg.get("movimento", True),
        )
        partes.append(seg_v)

    lista = work / "concat.txt"
    lista.write_text(
        "".join(f"file '{p.resolve().as_posix()}'\n" for p in partes), encoding="utf-8"
    )
    saida = roteiro.with_suffix(".mp4")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c", "copy", "-movflags", "+faststart", str(saida)])
    print("\nOK ->", saida)


if __name__ == "__main__":
    main()
