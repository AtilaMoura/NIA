# -*- coding: utf-8 -*-
"""
Script pra gerar imagens do curso pelo Gemini (gemini.google.com),
usando um perfil de Chrome ISOLADO + Patchright (stealth).

Suporta modo individual (prompt fixo) ou modo lote (JSON).

Pre-requisito: rodar `python scripts/configurar_perfil_gemini.py` primeiro,
uma unica vez, pra criar esse perfil isolado e logar no Google nele.

Uso:
    # Modo lote (recomendado):
    python scripts/gerar_imagem_gemini.py scripts/imagens_para_gerar.json

    # Modo individual (usa PROMPT fixo do script):
    python scripts/gerar_imagem_gemini.py
"""

import json
import sys
import re
from pathlib import Path
from pathlib import Path as _Path

from patchright.sync_api import sync_playwright

# ============================================================
# CONFIGURACAO
# ============================================================

CHROME_USER_DATA_DIR = str(_Path.home() / ".nia-playwright-profile")

# URL da conversa existente no Gemini (pra reusar uma conversa).
# Deixe vazio ou None pra abrir conversa nova.
GEMINI_CONVERSATION_URL = None

# Prompt padrao (modo individual)
PROMPT_PADRAO = (
    "Generate an image. Documentary-style editorial photography, warm "
    "golden-hour natural light, warm wheat and amber tones. Diverse "
    "real-looking people in everyday modest clothing. Generic evangelical/"
    "Christian community setting, no specific denominational symbols. "
    "Candid, unposed composition, shallow depth of field, focus on human "
    "gesture and interaction. No text or logos. Avoid overly polished "
    "corporate stock-photo look or obvious AI-generated artifacts. A small "
    "group of church volunteers of different ages working together on a "
    "practical task (arranging chairs, packing food donations, setting up "
    "for an event) inside a modest church hall, each person visibly doing "
    "something different, conveying that different gifts serve one shared "
    "purpose."
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def carregar_json(caminho_json: str) -> list[dict]:
    """Carrega a lista de imagens do JSON."""
    with open(caminho_json, "r", encoding="utf-8") as f:
        return json.load(f)


def fase1_gerar_imagem(page, prompt: str, pasta_debug: Path) -> bytes:
    """Abre o Gemini (conversa nova ou existente), manda o prompt, espera a imagem."""
    if GEMINI_CONVERSATION_URL:
        print(f"[FASE 1] Abrindo conversa existente: {GEMINI_CONVERSATION_URL}")
        page.goto(GEMINI_CONVERSATION_URL, wait_until="domcontentloaded")
    else:
        print("[FASE 1] Abrindo Gemini (conversa nova)...")
        page.goto("https://gemini.google.com/app", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    # Caixa de prompt
    try:
        caixa = page.get_by_role(
            "textbox", name=re.compile("Enter a prompt|Digite uma solicitacao", re.I)
        )
        caixa.wait_for(timeout=8000)
    except Exception:
        caixa = page.locator('div[contenteditable="true"]').first
        caixa.wait_for(timeout=8000)

    print("[FASE 1] Digitando o prompt...")
    caixa.click()
    caixa.type(prompt, delay=8)
    page.wait_for_timeout(500)

    # Conta imagens que ja existem antes de enviar o prompt
    ids_antes = set()
    for img in page.locator("img").all():
        try:
            # Usa uma combinacao de src + posicao como identificador
            src = img.get_attribute("src") or ""
            box = img.bounding_box()
            chave = f"{src}:{box['x']:.0f}:{box['y']:.0f}" if box else src
            ids_antes.add(chave)
        except Exception:
            continue
    print(f"[FASE 1] Imagens na pagina antes do prompt: {len(ids_antes)}")

    caixa.press("Enter")

    print("[FASE 1] Esperando a imagem ser gerada (pode levar ~30-60s)...")
    imagem = None

    for tentativa in range(24):  # ate ~2 minutos
        page.wait_for_timeout(5000)

        candidatos = page.locator("img").all()

        for img in reversed(candidatos):  # comeca pelas mais recentes
            try:
                src = img.get_attribute("src") or ""

                # ignora avatar e imagens pequenas de UI
                if "default-user" in src or "s64-c" in src or "s32-c" in src:
                    continue
                if not any(
                    x in src for x in ["googleusercontent", "blob:", "data:image"]
                ):
                    continue

                # so aceita imagens razoavelmente grandes (geradas)
                box = img.bounding_box()
                if not box or box["width"] < 200 or box["height"] < 200:
                    continue

                # Verifica se e uma imagem NOVA (nao existia antes)
                chave = f"{src}:{box['x']:.0f}:{box['y']:.0f}"
                if chave in ids_antes:
                    continue  # imagem ja existia, pula

                imagem = img
                break
            except Exception:
                continue

        if imagem:
            break

        print(f"  ainda esperando... ({tentativa + 1}/24)")

    if imagem is None:
        pasta_debug.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(pasta_debug / "_debug_sem_imagem.png"))
        raise RuntimeError(
            "Nao achei nenhuma imagem gerada depois de ~2min. Screenshot de "
            f"debug salvo em {pasta_debug / '_debug_sem_imagem.png'} — "
            "abre esse print pra ver o que a pagina mostrou."
        )

    src = imagem.get_attribute("src")
    print(f"[FASE 1] Imagem encontrada: {src[:80]}...")

    if src.startswith("data:"):
        import base64

        _, b64data = src.split(",", 1)
        return base64.b64decode(b64data)

    if src.startswith("blob:"):
        import base64

        # Usa JavaScript pra extrair o blob via canvas
        b64data = page.evaluate("""async (imgSelector) => {
            const img = document.querySelector(imgSelector);
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            return canvas.toDataURL('image/png').split(',')[1];
        }""", f'img[src="{src}"]')
        return base64.b64decode(b64data)

    # URL normal — baixa com o contexto autenticado
    resposta = page.request.get(src)
    return resposta.body()


def fase2_salvar(imagem_bytes: bytes, destino: Path) -> Path:
    """Salva a imagem no caminho especificado."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(imagem_bytes)
    print(f"[FASE 2] Salvo em {destino}")
    return destino


def main():
    print(f"Perfil isolado: {CHROME_USER_DATA_DIR}")
    if not _Path(CHROME_USER_DATA_DIR).exists():
        raise SystemExit(
            "Perfil isolado ainda nao existe — rode primeiro "
            "`python scripts/configurar_perfil_gemini.py`"
        )

    # Determina se esta em modo lote ou individual
    modo_lote = len(sys.argv) > 1
    itens = []

    if modo_lote:
        caminho_json = sys.argv[1]
        itens = carregar_json(caminho_json)
        print(f"[MODO LOTE] {len(itens)} imagem(ns) pra gerar")
    else:
        # Modo individual com prompt fixo
        itens = [
            {
                "descricao": PROMPT_PADRAO,
                "modulo": "modulo1",
                "aula": "aula1",
                "topico": "topico2",
                "arquivo": "voluntarios-equipe.png",
            }
        ]
        print("[MODO INDIVIDUAL] Usando prompt fixo do script")

    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_USER_DATA_DIR,
            channel="chrome",
            headless=False,
            no_viewport=True,
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
        )

        page = contexto.pages[0] if contexto.pages else contexto.new_page()

        try:
            for i, item in enumerate(itens):
                modulo = item["modulo"]
                aula = item["aula"]
                topico = item["topico"]
                arquivo = item["arquivo"]
                descricao = item["descricao"]

                destino = REPO_ROOT / "imagem" / modulo / aula / topico / arquivo
                pasta_debug = REPO_ROOT / "imagem" / modulo / aula / topico

                # Pula se ja existe
                if destino.exists():
                    print(f"\n[{i+1}/{len(itens)}] {destino.name} ja existe, pulando...")
                    continue

                print(f"\n[{i+1}/{len(itens)}] Gerando: {modulo}/{aula}/{topico}/{arquivo}")
                imagem_bytes = fase1_gerar_imagem(page, descricao, pasta_debug)
                fase2_salvar(imagem_bytes, destino)
        finally:
            contexto.close()

    print(f"\nPronto! {len(itens)} imagem(ns) processada(s).")


if __name__ == "__main__":
    main()
