# -*- coding: utf-8 -*-
"""
FASE 0 (só roda 1 vez): cria um perfil de Chrome isolado, separado do seu
Chrome do dia a dia, e abre uma janela pra você logar no Google manualmente.
Depois disso, `gerar_imagem_gemini.py` reaproveita essa mesma pasta sem
precisar fechar nada do seu navegador normal.

Uso:
    python scripts/configurar_perfil_gemini.py

A janela do Chrome vai abrir sozinha, com a página de login do Google — faça
login com a conta que você quer usar pro Gemini. Depois de logado (e já
vendo o chat do Gemini funcionando), pode fechar a janela manualmente, ou
esperar o script encerrar sozinho (~5 minutos de folga).
"""
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PERFIL_ISOLADO = Path.home() / ".nia-playwright-profile"
PERFIL_ISOLADO.mkdir(parents=True, exist_ok=True)


def main():
    print(f"Perfil isolado: {PERFIL_ISOLADO}")
    print("Abrindo o Chrome numa janela separada do seu perfil normal...")
    print("Faça login no Google nessa janela. Você tem ~5 minutos.\n")

    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(
            user_data_dir=str(PERFIL_ISOLADO),
            channel="chrome",
            headless=False,
        )
        page = contexto.new_page()
        page.goto("https://gemini.google.com/app", wait_until="domcontentloaded")

        for minuto in range(5):
            print(f"  aguardando login... ({minuto + 1}/5 min)")
            time.sleep(60)

        print("\nTempo esgotado — fechando a janela de configuração.")
        print("Se já logou, pode rodar o gerar_imagem_gemini.py agora.")
        contexto.close()


if __name__ == "__main__":
    main()
