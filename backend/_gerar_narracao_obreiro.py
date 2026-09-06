"""
Fase 3 (Audio Top) do curso de obreiro: gera o campo opcional `narracao` por
slide de tipo "conteudo" dos Topicos 1, 2 e 3 - texto falado, tom de
professor explicando, grounded estritamente no conteudo ja aprovado daquele
slide (sem inventar fato/citacao/data nova). Nao gera nenhum arquivo de
audio - o template ja le esse campo via Web Speech API (topico.html.j2).

Passo 1: gera e salva em _narracoes_obreiro.json pra revisao antes de
aplicar no banco (nao faz PUT sozinho).

Rodar: python _gerar_narracao_obreiro.py
"""
import asyncio
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService

TOPICOS = [1, 2, 3]
BASE_URL = "http://localhost:8100"

SYSTEM_PROMPT = """Voce e um professor de teologia gravando o audio de uma aula, explicando um trecho em voz alta pra um aluno que esta OUVINDO, nao lendo a tela.

Regras obrigatorias:
- Pode reorganizar e conectar as ideias com transicoes naturais de fala, mas NUNCA invente fato, data, nome, citacao ou referencia biblica que nao esteja no texto fornecido.
- Nao repita o texto literalmente - explique com suas proprias palavras, como se estivesse comentando pro aluno, mantendo total fidelidade ao conteudo.
- Nao use emojis, nao use markdown, nao comece com saudacao ("Ola", "Bem-vindo") nem termine com despedida - e o meio de uma aula continua.
- Escreva em portugues do Brasil, entre 80 e 180 palavras, em paragrafo corrido (sem listas)."""


def extrair_texto_bloco(b: dict) -> str:
    t = b.get("tipo")
    if t == "paragrafo":
        return b.get("texto", "")
    if t == "box":
        conteudo = b.get("texto") or b.get("itens") or ""
        if isinstance(conteudo, list):
            conteudo = " ".join(str(x) for x in conteudo)
        label = b.get("label", "")
        return f"{label}: {conteudo}" if label else str(conteudo)
    if t == "quote":
        return f'"{b.get("texto", "")}" ({b.get("referencia", "")})'
    if t == "cards":
        itens = b.get("itens", [])
        return " | ".join(f"{i.get('nome', '')}: {i.get('descricao', '')}" for i in itens)
    if t == "cols2":
        partes = []
        for lado in ("esquerda", "direita"):
            c = b.get(lado, {})
            if c:
                partes.append(f"{c.get('label', '')}: {c.get('texto', '')}")
        return " | ".join(partes)
    if t == "timeline":
        itens = b.get("itens", [])
        return " -> ".join(f"{i.get('titulo', '')}: {i.get('descricao', '')}" for i in itens)
    return ""


def montar_grounding(slide: dict) -> str:
    partes = [extrair_texto_bloco(b) for b in slide.get("blocos", [])]
    return "\n".join(p for p in partes if p.strip())


async def gerar_narracao(service: GroqService, titulo_secao: str, grounding: str) -> str:
    prompt = f"Titulo da secao: {titulo_secao}\n\nConteudo desta secao (a UNICA fonte que voce pode usar):\n{grounding}\n\nEscreva a narracao falada agora."
    resultado = await service.generate(prompt=prompt, system_prompt=SYSTEM_PROMPT, max_tokens=500)
    return resultado.strip()


def get_topico(tid: int) -> dict:
    with urllib.request.urlopen(f"{BASE_URL}/topicos/{tid}") as r:
        return json.load(r)


async def main():
    service = GroqService()
    saida = {}
    for tid in TOPICOS:
        topico = get_topico(tid)
        content = json.loads(topico["content"])
        narracoes = []
        for i, slide in enumerate(content["slides"]):
            if slide.get("tipo") != "conteudo":
                continue
            grounding = montar_grounding(slide)
            if not grounding.strip():
                continue
            titulo = slide.get("titulo_secao") or content.get("titulo", "")
            print(f"[T{tid}] slide {i} - {titulo!r} ...", flush=True)
            narracao = await gerar_narracao(service, titulo, grounding)
            narracoes.append({"slide_idx": i, "titulo_secao": titulo, "narracao": narracao})
            print(f"   -> {narracao[:90]}...", flush=True)
        saida[str(tid)] = narracoes

    out_path = Path(__file__).parent / "_narracoes_obreiro.json"
    out_path.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSalvo em {out_path} - revisar antes de aplicar no banco.")


if __name__ == "__main__":
    asyncio.run(main())
