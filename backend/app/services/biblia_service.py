# backend/app/services/biblia_service.py
"""
Busca o texto bíblico real (tradução Almeida, domínio público) via bible-api.com,
pra servir de grounding ao ContentAgent do domínio teológico.

Achado testando o piloto de Filipenses (2026-08-22): pedir pra IA "citar o versículo
exato" sem fornecer o texto de verdade não funciona de forma confiável — o modelo
tenta reproduzir de memória e erra a citação (Reviewer pegou isso: Fp 1:7 e Fp 2:19-24
citados errado, os dois reprovados como bloqueante). É o MESMO problema, e a MESMA
solução, do fio condutor da área de IA: fatos precisam vir de fonte externa
determinística, nunca da memória do modelo — aqui a "tool" é essa busca de texto real.

Generalizado em 2026-08-25 (curso de obreiro — ver memória nia-curso-obreiro): a versão
original só reconhecia UMA referência de Filipenses embutida no TÍTULO da lição — o
curso de obreiro cita dezenas de referências, de vários livros diferentes, espalhadas
nos "topicos" da estrutura, não no título. `_LIVRO_PARA_CODIGO` agora cobre o Novo
Testamento inteiro (+ alguns livros do AT mais citados) e `extrair_referencias()`/
`buscar_todos_textos()` acham e buscam TODAS as referências de um texto livre, não só
uma.
"""

import re

import httpx

# Chave: variante em português (abreviação comum ou nome cheio, minúsculo, sem espaço
# interno) → código OSIS de 3 letras que a bible-api.com espera. Cobre o Novo
# Testamento inteiro (é o que o domínio teológico do NIA usa até agora) + os livros do
# Antigo Testamento mais citados num curso de formação geral.
_LIVRO_PARA_CODIGO = {
    # Antigo Testamento (mais citados)
    "gn": "GEN", "gênesis": "GEN", "genesis": "GEN",
    "êx": "EXO", "ex": "EXO", "êxodo": "EXO", "exodo": "EXO",
    "sl": "PSA", "salmo": "PSA", "salmos": "PSA",
    "pv": "PRO", "provérbios": "PRO", "proverbios": "PRO",
    "is": "ISA", "isaías": "ISA", "isaias": "ISA",
    "jr": "JER", "jeremias": "JER",
    "ne": "NEH", "neemias": "NEH",
    # Evangelhos e Atos
    "mt": "MAT", "mateus": "MAT",
    "mc": "MRK", "marcos": "MRK",
    "lc": "LUK", "lucas": "LUK",
    "jo": "JHN", "joão": "JHN", "joao": "JHN",
    "at": "ACT", "atos": "ACT",
    # Cartas de Paulo
    "rm": "ROM", "romanos": "ROM",
    "1co": "1CO", "1coríntios": "1CO", "1corintios": "1CO",
    "2co": "2CO", "2coríntios": "2CO", "2corintios": "2CO",
    "gl": "GAL", "gálatas": "GAL", "galatas": "GAL",
    "ef": "EPH", "efésios": "EPH", "efesios": "EPH",
    "fp": "PHP", "fl": "PHP", "filipenses": "PHP",
    "cl": "COL", "colossenses": "COL",
    "1ts": "1TH", "1tessalonicenses": "1TH",
    "2ts": "2TH", "2tessalonicenses": "2TH",
    "1tm": "1TI", "1timóteo": "1TI", "1timoteo": "1TI",
    "2tm": "2TI", "2timóteo": "2TI", "2timoteo": "2TI",
    "tt": "TIT", "tito": "TIT",
    "fm": "PHM", "filemom": "PHM",
    # Cartas gerais e Apocalipse
    "hb": "HEB", "hebreus": "HEB",
    "tg": "JAS", "tiago": "JAS",
    "1pe": "1PE", "1pedro": "1PE",
    "2pe": "2PE", "2pedro": "2PE",
    "1jo": "1JN", "1joão": "1JN", "1joao": "1JN",
    "2jo": "2JN", "2joão": "2JN", "2joao": "2JN",
    "3jo": "3JN", "3joão": "3JN", "3joao": "3JN",
    "jd": "JUD", "judas": "JUD",
    "ap": "REV", "apocalipse": "REV",
}

# Alternação construída a partir das chaves acima, mais compridas primeiro (evita
# "tm" casar antes de "1timóteo" ter chance). \b + "\.?\s+" cobre "Mt 5:23", "Mt. 5:23".
_PADRAO_REFERENCIA = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in sorted(_LIVRO_PARA_CODIGO, key=len, reverse=True)) + r")"
    r"\.?\s+(\d{1,3})(?::(\d{1,3})(?:-(\d{1,3}))?)?\b",
    re.IGNORECASE,
)


def extrair_referencias(texto: str) -> list[tuple[str, str]]:
    """Acha TODAS as referências bíblicas reconhecíveis num texto livre (título,
    tópicos, foco — qualquer string). Retorna lista de (codigo_osis, referencia),
    ex: [("1TI", "3:1-13"), ("TIT", "1:6-9")]. Não deduplica (quem chama decide)."""
    encontradas = []
    for m in _PADRAO_REFERENCIA.finditer(texto or ""):
        codigo = _LIVRO_PARA_CODIGO[m.group(1).lower()]
        capitulo, v1, v2 = m.group(2), m.group(3), m.group(4)
        referencia = capitulo if not v1 else (f"{capitulo}:{v1}-{v2}" if v2 else f"{capitulo}:{v1}")
        encontradas.append((codigo, referencia))
    return encontradas


async def _buscar_por_codigo(codigo: str, referencia: str) -> str | None:
    ref_normalizada = (
        referencia.replace("–", "-").replace("—", "-").replace("‑", "-").strip()
    )
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"https://bible-api.com/{codigo}+{ref_normalizada}",
                params={"translation": "almeida"},
            )
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                return None
            texto = (data.get("text") or "").strip()
            return texto or None
    except Exception:
        return None


async def buscar_texto(livro: str, referencia: str) -> str | None:
    """referencia no formato tipo '1:1-11' (aceita variações de traço, normalizadas
    aqui). Retorna o texto real da passagem (Almeida) ou None se não achar/der erro
    — quem chama decide o que fazer na ausência (não é fatal, só significa que essa
    lição não vai ter grounding de texto pra citar)."""
    codigo = _LIVRO_PARA_CODIGO.get(livro.strip().lower())
    if not codigo:
        return None
    return await _buscar_por_codigo(codigo, referencia)


async def buscar_todos_textos(texto: str, limite: int = 8) -> str:
    """Acha TODAS as referências bíblicas em `texto` (título + tópicos da aula, por
    exemplo), busca o texto real de cada uma (sem repetir a mesma referência) e devolve
    tudo formatado, pronto pra virar grounding do ContentAgent. `limite` evita gerar um
    prompt gigante numa aula com referência demais — as primeiras `limite` encontradas
    (ordem de aparição no texto) são buscadas, o resto é ignorado silenciosamente."""
    vistas: set[tuple[str, str]] = set()
    unicas: list[tuple[str, str]] = []
    for ref in extrair_referencias(texto):
        if ref not in vistas:
            vistas.add(ref)
            unicas.append(ref)
        if len(unicas) >= limite:
            break

    blocos = []
    for codigo, referencia in unicas:
        passagem = await _buscar_por_codigo(codigo, referencia)
        if passagem:
            blocos.append(f"[{codigo} {referencia}]\n{passagem}")

    return "\n\n".join(blocos)
