# -*- coding: utf-8 -*-
"""
Acrescenta 12 temas novos (claro + escuro cada) em docs/schema/temas.json.

- Aditivo e idempotente: tema com o mesmo id é substituído, os 6 antigos não mudam.
- Antes de gravar, confere contraste WCAG de cada versão (texto, texto secundário,
  acento sobre o fundo, texto sobre o botão de acento). Falhou = não grava.

Rodar da raiz do repo:  python docs/estilos/_adicionar_temas_novos.py
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ARQ = RAIZ / "docs" / "schema" / "temas.json"


def rgba(hexcor, a):
    h = hexcor.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def paleta(bg, surface, surface2, border, borderSoft, text, textMuted, textDim,
           accent, accentTextOn, bad, blue, amber, violet, good, escuro=False):
    """Monta o dicionário de cores no formato do temas.json (soft = acento translúcido)."""
    return {
        "bg": bg, "surface": surface, "surface2": surface2, "border": border,
        "borderSoft": borderSoft, "text": text, "textMuted": textMuted, "textDim": textDim,
        "accent": accent, "accentSoft": rgba(accent, .18 if escuro else .14),
        "bad": bad, "badSoft": rgba(bad, .14 if escuro else .12),
        "blue": blue, "amber": amber, "violet": violet, "good": good,
        "accentTextOn": accentTextOn,
    }


def fonts(*familias):
    return "https://fonts.googleapis.com/css2?" + "&".join(f"family={f}" for f in familias) + "&display=swap"


SANS = "-apple-system, 'Segoe UI', 'Noto Sans', Roboto, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Consolas, monospace"

TEMAS = [
    {
        "id": "ceu-manha", "nome": "Céu de Manhã",
        "descricao": "Azul-céu claro com acento coral. Leve e acolhedor, bom pra línguas e cursos gerais.",
        "cores": paleta("#f2f7fc", "#ffffff", "#e6f0fa", "#cddcec", "#dde8f4", "#1c2a3a", "#4a5d72", "#66788c",
                        "#c24a35", "#ffffff", "#b3261e", "#2f6fb3", "#a8650a", "#6a4fb3", "#2e7d4f"),
        "coresDark": paleta("#0f1a26", "#172433", "#1d2d40", "#2c3f55", "#223246", "#e8f0f8", "#a3b4c6", "#8395a9",
                            "#ff8a73", "#1a0d09", "#ff7a70", "#7fb8f0", "#f0b050", "#b8a4f5", "#6cc28a", True),
        "radius": "10px", "radiusLg": "16px",
        "fontFamily": f"'Nunito Sans', {SANS}", "fontFamilyDisplay": f"'Nunito', {SANS}",
        "googleFonts": fonts("Nunito:wght@600;800", "Nunito+Sans:wght@400;600;700"),
        "pesoTitulo": "800", "letterSpacingLabel": "0.06em",
    },
    {
        "id": "menta-grafite", "nome": "Menta & Grafite",
        "descricao": "Branco-menta com verde-água e texto grafite. Técnico e calmo, bom pra IA e dados.",
        "cores": paleta("#f1f8f5", "#ffffff", "#e3f1ea", "#c9e0d5", "#d9ebe2", "#1f2a27", "#4c5e58", "#687974",
                        "#0f7a68", "#ffffff", "#b3372e", "#2b6ea8", "#a86b12", "#6650a8", "#2f7d45"),
        "coresDark": paleta("#111816", "#18221f", "#1f2b27", "#2c3b36", "#23302c", "#e6f2ed", "#9fb5ac", "#7f948c",
                            "#4fd1b5", "#0b1a16", "#f07a70", "#7fb4e6", "#e7b25c", "#b3a3ee", "#6fcf8f", True),
        "radius": "8px", "radiusLg": "12px",
        "fontFamily": f"'Source Sans 3', {SANS}", "fontFamilyDisplay": f"'Sora', {SANS}", "fontFamilyLabel": MONO,
        "googleFonts": fonts("Sora:wght@600;700", "Source+Sans+3:wght@400;600;700", "JetBrains+Mono:wght@500"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.08em",
    },
    {
        "id": "oceano", "nome": "Oceano",
        "descricao": "Branco azulado com azul-marinho e turquesa. Sério e limpo, bom pra redes e segurança.",
        "cores": paleta("#eef4f8", "#ffffff", "#e0ebf2", "#c6d7e3", "#d6e4ee", "#0f2233", "#405466", "#5f7284",
                        "#0b4f7a", "#ffffff", "#b3261e", "#0b7a7a", "#a0600a", "#5b4a9e", "#25784a"),
        "coresDark": paleta("#0a1824", "#102232", "#152b3e", "#23405a", "#1a3247", "#e4eef6", "#9db3c6", "#7d96ab",
                            "#3cc8c8", "#04181c", "#ff7b72", "#6fb3ea", "#f2b35e", "#b0a2f0", "#62c98a", True),
        "radius": "8px", "radiusLg": "14px",
        "fontFamily": f"'Lexend', {SANS}", "fontFamilyDisplay": f"'Lexend', {SANS}", "fontFamilyLabel": f"'IBM Plex Mono', {MONO}",
        "googleFonts": fonts("Lexend:wght@400;600;700", "IBM+Plex+Mono:wght@500"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.08em",
    },
    {
        "id": "azul-petroleo", "nome": "Azul Petróleo",
        "descricao": "Petróleo com acento âmbar e creme. Combina com as ilustrações isométricas do curso de Redes.",
        "cores": paleta("#eef3f4", "#ffffff", "#e1eaec", "#c5d4d8", "#d5e1e4", "#13262b", "#43585e", "#61747a",
                        "#1c5d6b", "#ffffff", "#b23a2c", "#2e6f9e", "#a8620a", "#5d4f99", "#2a7a48"),
        "coresDark": paleta("#0f2027", "#152b33", "#1b343d", "#2a4752", "#203a44", "#eef3f1", "#a6bcc0", "#85a0a5",
                            "#f2a541", "#1c1203", "#ff7a6b", "#6fb2d8", "#f2a541", "#b4a6ec", "#6ccb8c", True),
        "radius": "6px", "radiusLg": "10px",
        "fontFamily": f"'Barlow', {SANS}", "fontFamilyDisplay": f"'Barlow Semi Condensed', {SANS}", "fontFamilyLabel": MONO,
        "googleFonts": fonts("Barlow:wght@400;500;600", "Barlow+Semi+Condensed:wght@600;700", "JetBrains+Mono:wght@500"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.08em",
    },
    {
        "id": "por-do-sol", "nome": "Pôr do Sol",
        "descricao": "Pêssego com laranja queimado e roxo. Quente e criativo, bom pra línguas e temas de cultura.",
        "cores": paleta("#fff5ee", "#ffffff", "#fde8dc", "#f0cfbd", "#f6dfd2", "#2d1b24", "#6b4c58", "#856672",
                        "#b8400b", "#ffffff", "#a3202a", "#2f6aa3", "#9a5606", "#6d3fa6", "#2d7a4a"),
        "coresDark": paleta("#1e1220", "#29192b", "#331f35", "#4a2f4c", "#3b263d", "#fbeee8", "#d0b3bd", "#ae919c",
                            "#ff8a4c", "#2a0f02", "#ff7a85", "#8ab8f0", "#ffc15c", "#c9a2ff", "#7fd49a", True),
        "radius": "14px", "radiusLg": "20px",
        "fontFamily": f"'DM Sans', {SANS}", "fontFamilyDisplay": "'DM Serif Display', Georgia, serif",
        "googleFonts": fonts("DM+Serif+Display", "DM+Sans:wght@400;500;700"),
        "pesoTitulo": "400", "letterSpacingLabel": "0.06em",
    },
    {
        "id": "lavanda", "nome": "Lavanda",
        "descricao": "Lilás claro com roxo e mostarda. Suave e moderno, serve pra qualquer curso.",
        "cores": paleta("#f6f3fb", "#ffffff", "#ece6f7", "#d9cfea", "#e5ddf2", "#241d33", "#574c6b", "#766b8a",
                        "#6a3fb5", "#ffffff", "#b02a37", "#2f64a8", "#8a5f00", "#9a3f86", "#2b7a4b"),
        "coresDark": paleta("#16121f", "#1f1a2b", "#272136", "#3a3150", "#2e2740", "#efeaf8", "#b6abcc", "#948aac",
                            "#b89cff", "#1a1030", "#ff7d8a", "#8fb6f0", "#e8c14a", "#f0a3d6", "#74d39a", True),
        "radius": "12px", "radiusLg": "18px",
        "fontFamily": f"'Nunito Sans', {SANS}", "fontFamilyDisplay": f"'Outfit', {SANS}",
        "googleFonts": fonts("Outfit:wght@500;700", "Nunito+Sans:wght@400;600;700"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.06em",
    },
    {
        "id": "terracota-salvia", "nome": "Terracota & Sálvia",
        "descricao": "Off-white com terracota e verde-sálvia. Terroso e sereno, bom pra estudo bíblico e devocional.",
        "cores": paleta("#f8f4ef", "#ffffff", "#efe8df", "#ddd1c3", "#e8ddd1", "#2a221d", "#5f5248", "#7a6c61",
                        "#a8452b", "#ffffff", "#9e2c26", "#3b6679", "#9a600e", "#6a5585", "#4a7445"),
        "coresDark": paleta("#1b1714", "#24201c", "#2d2823", "#423a33", "#352f29", "#f3ece4", "#c2b5a7", "#9c9084",
                            "#e2825f", "#2a1008", "#f08070", "#8fb3c4", "#e6b060", "#bca8dc", "#9cc493", True),
        "radius": "12px", "radiusLg": "18px",
        "fontFamily": f"'Source Sans 3', {SANS}", "fontFamilyDisplay": "'Lora', Georgia, serif",
        "googleFonts": fonts("Lora:wght@500;700", "Source+Sans+3:wght@400;600;700"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.06em",
    },
    {
        "id": "papel-kraft", "nome": "Papel Kraft",
        "descricao": "Papel kraft com verde-oliva e vermelho-tijolo. Rústico, cara de caderno de estudo antigo; bom pra Bíblia e história.",
        "cores": paleta("#efe4d2", "#f8f1e5", "#e6d8c1", "#cfbd9f", "#dccbb0", "#2b2418", "#574a36", "#6f6049",
                        "#4f652b", "#ffffff", "#9e2f23", "#325a6e", "#8a540c", "#5d4a6e", "#3f6b30"),
        "coresDark": paleta("#1c1812", "#252019", "#2e2820", "#463d30", "#383026", "#f1e8d8", "#c4b597", "#a0927a",
                            "#a8c26a", "#1a2008", "#e87a64", "#8cb2c4", "#e3ad5c", "#bba7d2", "#9cc47c", True),
        "radius": "4px", "radiusLg": "8px",
        "fontFamily": f"'Libre Franklin', {SANS}", "fontFamilyDisplay": "'Bitter', Georgia, serif",
        "googleFonts": fonts("Bitter:wght@600;700", "Libre+Franklin:wght@400;500;600"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.08em",
    },
    {
        "id": "vinho-ouro", "nome": "Vinho & Ouro",
        "descricao": "Marfim com bordô no claro; bordô com dourado no escuro. Solene, bom pra teologia e cursos formais.",
        "cores": paleta("#faf6f0", "#ffffff", "#f2eadf", "#e0d2c0", "#eadfd0", "#2a1a1c", "#5e4a4d", "#7a6568",
                        "#7a1f33", "#ffffff", "#b0302a", "#34587a", "#8c6412", "#5b3f7a", "#3b7040"),
        "coresDark": paleta("#1c0f13", "#26151a", "#301b21", "#4a2a33", "#3a2129", "#f6ece4", "#cdb6b0", "#a8938e",
                            "#d9b25f", "#2a1a05", "#ff8078", "#8fb0d6", "#d9b25f", "#c6a8e0", "#86c98a", True),
        "radius": "6px", "radiusLg": "12px",
        "fontFamily": f"'Source Sans 3', {SANS}", "fontFamilyDisplay": "'Cormorant Garamond', Georgia, serif",
        "googleFonts": fonts("Cormorant+Garamond:wght@600;700", "Source+Sans+3:wght@400;600;700"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.1em",
    },
    {
        "id": "floresta", "nome": "Floresta",
        "descricao": "Verde profundo com creme e laranja. Natural e vivo, bom pra IA e temas de natureza.",
        "cores": paleta("#f2f5ef", "#ffffff", "#e5ebdf", "#cad5c1", "#d9e2d1", "#1a261d", "#4a5a4c", "#667568",
                        "#1f5a36", "#ffffff", "#a8302b", "#2d6a8a", "#b0500b", "#5e4d91", "#2e7b45"),
        "coresDark": paleta("#0e1a12", "#152419", "#1b2d20", "#2a4331", "#213728", "#eef3e6", "#a9bba6", "#899d86",
                            "#ff9a4d", "#2a1203", "#ff7a70", "#82bcd8", "#ffb35c", "#b8a8ec", "#7fd08f", True),
        "radius": "10px", "radiusLg": "16px",
        "fontFamily": f"'Figtree', {SANS}", "fontFamilyDisplay": f"'Epilogue', {SANS}",
        "googleFonts": fonts("Epilogue:wght@600;800", "Figtree:wght@400;500;700"),
        "pesoTitulo": "800", "letterSpacingLabel": "0.06em",
    },
    {
        "id": "caderno-escolar", "nome": "Caderno Escolar",
        "descricao": "Folha pautada com caneta azul e marca-texto amarelo. Cara de caderno de aluno, bom pra línguas e estudo.",
        "cores": paleta("#fdfdf8", "#ffffff", "#fff6b8", "#c9d6ea", "#e3eaf5", "#1d2433", "#4a5468", "#687186",
                        "#1f4fbf", "#ffffff", "#c0262d", "#1f4fbf", "#9a6200", "#7b3fa0", "#217a3c"),
        "coresDark": paleta("#141821", "#1b2030", "#2f2c17", "#2e3a55", "#232c40", "#eef1f8", "#aab4c8", "#8a93aa",
                            "#7fa6ff", "#0b1430", "#ff7a80", "#7fa6ff", "#ffd84d", "#cf9bf0", "#6fd08c", True),
        "radius": "6px", "radiusLg": "10px",
        "fontFamily": f"'Atkinson Hyperlegible', {SANS}", "fontFamilyDisplay": "'Kalam', 'Comic Sans MS', cursive",
        "googleFonts": fonts("Kalam:wght@700", "Atkinson+Hyperlegible:wght@400;700"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.05em",
        "extra_css": ".slides{background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 31px,var(--border-soft) 31px,var(--border-soft) 32px);}",
    },
    {
        "id": "alto-contraste", "nome": "Alto Contraste",
        "descricao": "Preto e branco puros, acento azul no claro e amarelo no escuro, fonte grande de leitura fácil. Pra quem enxerga pouco.",
        "cores": paleta("#ffffff", "#ffffff", "#f2f2f2", "#000000", "#555555", "#000000", "#1f1f1f", "#3d3d3d",
                        "#0040c0", "#ffffff", "#b00000", "#0040c0", "#6e5100", "#5a1f99", "#006b21"),
        "coresDark": paleta("#000000", "#0a0a0a", "#141414", "#ffffff", "#9a9a9a", "#ffffff", "#f0f0f0", "#d0d0d0",
                            "#ffd600", "#000000", "#ff6b6b", "#7fc4ff", "#ffd600", "#d7a8ff", "#5cf08a", True),
        "radius": "4px", "radiusLg": "6px",
        "fontFamily": f"'Atkinson Hyperlegible', {SANS}", "fontFamilyDisplay": f"'Atkinson Hyperlegible', {SANS}",
        "googleFonts": fonts("Atkinson+Hyperlegible:wght@400;700"),
        "pesoTitulo": "700", "letterSpacingLabel": "0.04em",
        "extra_css": "body{font-size:1.08em;} a{text-decoration:underline;}",
    },
]


# ---------- contraste WCAG ----------
def _lum(hexcor):
    h = hexcor.lstrip("#")
    canais = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def checar(tema_id, versao, c):
    """Mínimos: texto 7, secundário 4.5, apagado 3.5, acento no fundo 3, texto no botão 4.5."""
    regras = [("text", "bg", 7), ("text", "surface", 7), ("textMuted", "bg", 4.5), ("textMuted", "surface", 4.5),
              ("textDim", "bg", 3.5), ("accent", "bg", 3), ("accentTextOn", "accent", 4.5),
              ("bad", "bg", 3), ("good", "bg", 3), ("blue", "bg", 3), ("amber", "bg", 3), ("violet", "bg", 3)]
    falhas = []
    for fg, bg, minimo in regras:
        r = contraste(c[fg], c[bg])
        if r < minimo:
            falhas.append(f"{tema_id}/{versao}: {fg} sobre {bg} = {r:.2f} (mín {minimo})")
    return falhas


falhas = []
for t in TEMAS:
    falhas += checar(t["id"], "claro", t["cores"])
    falhas += checar(t["id"], "escuro", t["coresDark"])
if falhas:
    print("CONTRASTE REPROVADO — nada gravado:")
    print("\n".join(falhas))
    sys.exit(1)

dados = json.loads(ARQ.read_text(encoding="utf-8"))
ids_novos = {t["id"] for t in TEMAS}
dados["temas"] = [t for t in dados["temas"] if t["id"] not in ids_novos]
for t in TEMAS:
    t.setdefault("padrao_atual", False)
    t.setdefault("extra_css", "")
    dados["temas"].append(t)
ARQ.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"OK: contraste aprovado em {len(TEMAS) * 2} versões; temas.json tem {len(dados['temas'])} temas")
