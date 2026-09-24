"""Correção + revisão personalizada do fim do tópico e da prova (2026-09-23).

Substitui o veredito geral "dominado/reforço" do avaliar_resumo nesses dois
fluxos (achado real: o julgamento geral do gpt-oss variava e reprovava
resposta certa). Agora:

1. Cada pergunta vale 1 ponto. mc/tf: o gabarito decide (não a IA).
   Classify/associar: 1 se acertou todos os itens, 0,5 se acertou metade ou
   mais. Lacuna/ditado: bate com uma resposta aceita (normalizada) = certa;
   senão a IA julga a FRASE INTEIRA (2026-09-24 — "don’t" com apóstrofo curvo
   e "Brasil" com s viravam erro). Aberta: a IA classifica contra o gabarito
   DELA. Certa 1, parcial 0,5, errada 0 (decisão do Atila).
2. A nota é calculada aqui, no código. Na PROVA, passa com >= 60% (3 de 5,
   decisão do Atila); no TÓPICO não trava nada.
3. Tudo que não foi "certa" vira cartão de revisão, e a IA organiza as
   dificuldades por ASSUNTO + as palavras/termos que o aluno não sabia.

O endpoint (routers/pipeline.py) decide o que fazer com o resultado: salvar
dificuldades e termos, gerar a "revisão de tudo", reiniciar a prova.
"""

import re
import unicodedata

NOTA_MINIMA_PROVA = 0.6  # 3 de 5
PONTOS = {"certa": 1.0, "parcial": 0.5, "errada": 0.0}

# Apóstrofos/aspas "tipográficos" que teclado de celular e ABNT soltam no
# lugar do reto. Em escape de propósito: colados direto no código-fonte já se
# perderam uma vez (viraram ' comum e a normalização do front nunca funcionou).
_APOSTROFOS = re.compile("[‘’‚‛′´`]")
_ASPAS = re.compile("[“”„″]")


def normalizar_resposta(texto) -> str:
    """Mesma regra do normalizarResposta() do render: minúsculas, sem acento,
    apóstrofo/aspas unificados, sem pontuação e com espaços colapsados."""
    s = unicodedata.normalize("NFD", str(texto or "").strip().lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = _ASPAS.sub('"', _APOSTROFOS.sub("'", s))
    s = re.sub(r"[.,!?;:\"]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# Palavras cuja troca é erro de gramática, nunca de grafia (inglês e português).
_PALAVRAS_GRAMATICAIS = {
    "does", "were", "have", "this", "that", "these", "those", "their", "there", "they", "them",
    "your", "yours", "what", "when", "where", "which", "with", "from", "into", "been", "being",
    "will", "would", "could", "should", "sera", "seja", "esta", "este", "essa", "esse", "isso",
    "aquele", "aquela", "estao", "sao", "somos", "tinha", "tenho",
}


def _distancia(a: str, b: str) -> int:
    """Levenshtein simples (palavras curtas — custo irrelevante)."""
    ant = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        atual = [i]
        for j, cb in enumerate(b, 1):
            atual.append(min(ant[j] + 1, atual[j - 1] + 1, ant[j - 1] + (ca != cb)))
        ant = atual
    return ant[-1]


def palavra_com_erro_de_grafia(resposta: str, aceitas: list[str]) -> str | None:
    """Se a resposta só difere de uma aceita por UMA palavra escrita errada
    (até 2 letras, palavra de 4+ letras), devolve a palavra certa — ex.:
    "I live in Brasil" → "brazil". Não vale pra diferença gramatical: se uma
    palavra é a outra + sufixo (like/likes, work/worked), é erro de regra, não
    de grafia. Decidido no código pra não depender da IA (ela dava "parcial")."""
    r = normalizar_resposta(resposta).split()
    for aceita in aceitas:
        a = normalizar_resposta(aceita).split()
        if len(a) != len(r):
            continue
        dif = [(x, y) for x, y in zip(r, a) if x != y]
        if len(dif) != 1:
            continue
        errada, certa = dif[0]
        curta, longa = sorted((errada, certa), key=len)
        # Contração (don't/doesn't) ou palavra gramatical (is/are, this/these)
        # trocada é erro de REGRA — é justamente o que o exercício cobra.
        gramatical = "'" in errada or "'" in certa or errada in _PALAVRAS_GRAMATICAIS or certa in _PALAVRAS_GRAMATICAIS
        if len(certa) >= 4 and not gramatical and not longa.startswith(curta) and _distancia(errada, certa) <= 2:
            return certa
    return None


def _perguntas_dos_slides(slides: list[dict]) -> list[dict]:
    perguntas = []
    for slide in slides:
        if slide.get("tipo") == "checkpoint":
            perguntas.extend(slide.get("perguntas", []))
        elif slide.get("tipo") == "avaliacao_pergunta":
            perguntas.append(slide.get("pergunta") or {})
    return [p for p in perguntas if p.get("id")]


def _tf_texto(valor) -> str:
    return "Verdadeiro" if str(valor).lower() in ("verdadeiro", "true") else "Falso"


def _item_classify(p: dict, respostas: dict, base: dict) -> dict:
    rotulo = {str(o.get("valor")): o.get("rotulo", o.get("valor")) for o in p.get("rotulos_opcoes", [])}
    itens = p.get("itens", [])
    certos, erros, gabarito = 0, [], []
    for it in itens:
        r = respostas.get(it.get("id"))
        certo_txt = rotulo.get(str(it.get("correta")), it.get("correta"))
        if r is not None and r["correta"]:
            certos += 1
            continue
        # Só os itens que ele errou — com o gabarito de cada um. Achado real:
        # mandar só "0 de 4 itens certos" fazia a IA inventar o gabarito.
        marcado = "não respondido" if r is None else f"você marcou {rotulo.get(str(r['resposta']), r['resposta'])}"
        erros.append(f'{it.get("texto")} → {marcado}')
        gabarito.append(f'{it.get("texto")} → {certo_txt}')
    total = len(itens) or 1
    if certos == total:
        classificacao = "certa"
    elif certos * 2 >= total:
        classificacao = "parcial"
    else:
        classificacao = "errada"
    return {**base, "classificacao": classificacao,
            "sua_resposta": "\n".join(erros) if erros else "Todos os itens certos",
            "resposta_certa": "\n".join(gabarito) if gabarito else f"{certos} de {total} itens certos"}


def _item_objetivo(p: dict, respostas: dict) -> dict:
    """mc/tf/classify: o gabarito do material decide, sem IA."""
    tipo = p.get("tipo")
    base = {"id": p["id"], "tipo": tipo, "enunciado": p.get("enunciado", ""), "explicacao": p.get("explicacao") or ""}
    if tipo in ("classify", "associar"):
        return _item_classify(p, respostas, base)

    r = respostas.get(p["id"])
    if tipo == "mc":
        opcoes = p.get("opcoes", [])
        certa = opcoes[p["correta_idx"]] if 0 <= p.get("correta_idx", -1) < len(opcoes) else ""
        marcada = opcoes[r["resposta"]] if r and isinstance(r["resposta"], int) and 0 <= r["resposta"] < len(opcoes) else None
    else:  # tf
        certa = _tf_texto(p.get("correta_bool"))
        marcada = _tf_texto(r["resposta"]) if r else None

    if r is None:
        return {**base, "classificacao": "errada", "sua_resposta": "(não respondida)", "resposta_certa": certa}
    return {**base, "classificacao": "certa" if r["correta"] else "errada",
            "sua_resposta": marcada or str(r["resposta"]), "resposta_certa": certa}


def _para_ia(p: dict, resposta: str, tipo: str) -> dict:
    aceitas = p.get("respostas_aceitas") or []
    return {"id": p["id"], "tipo": tipo, "enunciado": p.get("enunciado", ""), "cenario": p.get("cenario") or "",
            "esperado": p.get("resposta_modelo") or (aceitas[0] if aceitas else "") or p.get("explicacao") or "",
            "aceitas": aceitas[1:4] if tipo == "frase" else [],
            "resposta": resposta}


async def corrigir_e_revisar(agente, slides: list[dict], respostas: dict, material: str, perfil) -> dict:
    """respostas = {question_id: {"resposta": ..., "correta": bool|None}} da rodada atual.

    Levanta exceção se a correção pela IA falhar — sem ela não dá pra
    calcular a nota, e o aluno tenta de novo (503 no endpoint). Nunca chuta
    nota por falha técnica."""
    itens: list[dict] = []
    para_ia: list[dict] = []

    for p in _perguntas_dos_slides(slides):
        tipo = p.get("tipo")
        if tipo in ("open", "lacuna", "ditado"):
            r = respostas.get(p["id"])
            texto = str(r["resposta"]).strip() if r else ""
            aceitas = p.get("respostas_aceitas") or []
            item = {"id": p["id"], "tipo": tipo, "enunciado": p.get("enunciado", ""),
                    "sua_resposta": texto or "(não respondida)", "explicacao": p.get("explicacao") or "",
                    "resposta_certa": p.get("resposta_modelo") or (aceitas[0] if aceitas else "")}
            if not texto:
                item["classificacao"] = "errada"
            elif tipo != "open" and normalizar_resposta(texto) in {normalizar_resposta(a) for a in aceitas}:
                # Recalculado aqui (não confia no "correta" gravado pelo front).
                item["classificacao"] = "certa"
            elif tipo != "open" and (grafia := palavra_com_erro_de_grafia(texto, aceitas)):
                item["classificacao"] = "certa"
                item["aviso"] = f'Atenção à grafia: "{grafia}" (você escreveu "{texto}")'
            else:
                para_ia.append(_para_ia(p, texto, "aberta" if tipo == "open" else "frase"))
            itens.append(item)
        else:
            itens.append(_item_objetivo(p, respostas))

    por_id = {i["id"]: i for i in itens}

    # 1) Abertas + frases que não bateram exato: a IA julga contra o gabarito (1 chamada)
    if para_ia:
        resultado = await agente.corrigir_abertas(para_ia, material, perfil=perfil)
        devolvidos = {str(x.get("id")): x for x in (resultado.get("itens") or [])}
        for a in para_ia:
            x = devolvidos.get(a["id"])
            if not x or x.get("classificacao") not in PONTOS:
                # IA "esqueceu" o item (achado conhecido do Groq): falha técnica
                raise RuntimeError(f"correção de {a['id']} não veio da IA")
            por_id[a["id"]].update({
                "classificacao": x["classificacao"],
                "resposta_certa": x.get("ponto_certo") or por_id[a["id"]]["resposta_certa"],
                "explicacao": x.get("o_que_faltou") or por_id[a["id"]]["explicacao"],
                "exemplo": x.get("exemplo") or "",
                "slide": x.get("slide") if isinstance(x.get("slide"), int) else None,
            })
            if x["classificacao"] == "certa" and x.get("o_que_faltou"):
                # Certa com ressalva (ex.: "Atenção à grafia: Brazil") — não vira
                # cartão de erro, mas o aviso aparece na revisão.
                por_id[a["id"]]["aviso"] = x["o_que_faltou"]

    # 2) Revisão organizada por assunto + termos que faltaram + exemplo/slide de
    # cada questão. Opcional — se falhar, ficam só os cartões por questão.
    pendentes = dificuldades_do_resultado(itens)
    revisao = None
    if pendentes:
        try:
            org = await agente.organizar_revisao(pendentes, material, perfil=perfil)
            for x in org.get("itens") or []:
                alvo = por_id.get(str(x.get("id")))
                if not alvo:
                    continue
                # A explicação escrita no material/IA de correção tem prioridade.
                if not alvo.get("exemplo"):
                    alvo["exemplo"] = x.get("exemplo") or ""
                if not alvo.get("slide") and isinstance(x.get("slide"), int):
                    alvo["slide"] = x["slide"]
            blocos = [b for b in org.get("blocos") or [] if b.get("titulo") and b.get("regra")]
            termos = [t for t in org.get("termos") or [] if t.get("termo") and t.get("significado")]
            revisao = {"blocos": blocos[:4], "termos": termos[:12]}
        except Exception as e:
            print(f"⚠️ organizar revisão falhou (segue só com os cartões): {e}")

    nota = sum(PONTOS[i["classificacao"]] for i in itens)
    return {
        "itens": itens,
        "nota": nota,
        "total": len(itens),
        "certas": sum(1 for i in itens if i["classificacao"] == "certa"),
        "revisao_dificuldades": revisao,
    }


def dificuldades_do_resultado(itens: list[dict]) -> list[dict]:
    return [i for i in itens if i["classificacao"] in ("errada", "parcial")]
