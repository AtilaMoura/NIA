# -*- coding: utf-8 -*-
"""
Gera TEXTO pelo Gemini web (gemini.google.com) no navegador — mesmo perfil isolado e
mesmo jeito do gerar_imagem_gemini.py (2026-10-01). Serve de reserva quando a API do
Gemini está com 503/cota: o site não usa a cota da API.

Uso:
    python scripts/gerar_texto_gemini_web.py <arquivo_prompt.txt> <arquivo_saida.md>

Espera a resposta parar de crescer (texto igual por ~12s) e salva o texto puro.
"""
import re
import sys
from pathlib import Path

from patchright.sync_api import sync_playwright

CHROME_USER_DATA_DIR = str(Path.home() / ".nia-playwright-profile")


def fechar_dialogos(page):
    for _ in range(3):
        overlay = page.locator(".cdk-overlay-backdrop-showing, .cdk-overlay-pane")
        if overlay.count() == 0:
            return
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)


def resposta_atual(page) -> str:
    """Texto da última resposta do modelo na conversa."""
    for seletor in ("model-response", "message-content", ".model-response-text"):
        loc = page.locator(seletor)
        if loc.count():
            try:
                return loc.last.inner_text(timeout=3000).strip()
            except Exception:
                continue
    return ""


def gerar(prompt: str) -> str:
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_USER_DATA_DIR, channel="chrome", headless=False, no_viewport=True,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--disable-infobars"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto("https://gemini.google.com/app", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            fechar_dialogos(page)
            try:
                caixa = page.get_by_role("textbox", name=re.compile("Enter a prompt|Digite|Peça ao Gemini", re.I))
                caixa.wait_for(timeout=8000)
            except Exception:
                caixa = page.locator('div[contenteditable="true"]').first
                caixa.wait_for(timeout=8000)
            caixa.click()
            page.keyboard.insert_text(prompt)
            page.wait_for_timeout(800)
            caixa.press("Enter")
            print("Prompt enviado; esperando a resposta terminar...", flush=True)

            anterior, estavel = "", 0
            for _ in range(120):  # até ~10 min
                page.wait_for_timeout(5000)
                atual = resposta_atual(page)
                if atual and atual == anterior:
                    estavel += 1
                    if estavel >= 3:  # ~15s sem mudar = terminou
                        return atual
                else:
                    estavel = 0
                anterior = atual
                print(f"  ... {len(atual)} caracteres", flush=True)
            page.screenshot(path="_debug_texto_gemini.png")
            raise RuntimeError("A resposta não terminou em ~10 min (screenshot em _debug_texto_gemini.png)")
        finally:
            ctx.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    texto = gerar(Path(sys.argv[1]).read_text(encoding="utf-8"))
    Path(sys.argv[2]).write_text(texto, encoding="utf-8")
    print(f"OK: {len(texto)} caracteres em {sys.argv[2]}")
