"""Correção + revisão personalizada do fim do tópico e da prova (2026-09-23).

Substitui o veredito geral "dominado/reforço" do avaliar_resumo nesses dois
fluxos (achado real: o julgamento geral do gpt-oss variava e reprovava
resposta certa). Agora:

1. Cada pergunta vale 1 ponto. Objetiva: o gabarito decide (não a IA).
   Classify/associar: 1 se acertou todos os itens, 0,5 se acertou metade ou
   mais. Aberta: a IA classifica contra o gabarito DELA — certa 1, parcial
   0,5, errada 0 (decisão do Atila).
2. A nota é calculada aqui, no código. Na PROVA, passa com >= 60% (3 de 5,
   decisão do Atila); no TÓPICO não trava nada.
3. Tudo que não foi "certa" vira um cartão de revisão (resposta do aluno,
   ponto certo, exemplo, slide pra reler).

O endpoint (routers/pipeline.py) decide o que fazer com o resultado: salvar
dificuldades, gerar a "revisão de tudo", reiniciar a prova.
"""

NOTA_MINIMA_PROVA = 0.6  # 3 de 5
PONTOS = {"certa": 1.0, "parcial": 0.5, "errada": 0.0}


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


def _item_objetivo(p: dict, respostas: dict) -> dict:
    """Monta o item de uma pergunta objetiva a partir do gabarito do material
    e da resposta salva (TopicoResposta/AvaliacaoResposta da rodada atual)."""
    tipo = p.get("tipo")
    base = {"id": p["id"], "tipo": tipo, "enunciado": p.get("enunciado", ""), "explicacao": p.get("explicacao") or ""}

    if tipo in ("classify", "associar"):
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

    r = respostas.get(p["id"])
    if tipo == "mc":
        opcoes = p.get("opcoes", [])
        certa = opcoes[p["correta_idx"]] if 0 <= p.get("correta_idx", -1) < len(opcoes) else ""
        marcada = opcoes[r["resposta"]] if r and isinstance(r["resposta"], int) and 0 <= r["resposta"] < len(opcoes) else None
    elif tipo == "tf":
        certa = _tf_texto(p.get("correta_bool"))
        marcada = _tf_texto(r["resposta"]) if r else None
    else:  # lacuna | ditado
        aceitas = p.get("respostas_aceitas") or []
        certa = aceitas[0] if aceitas else ""
        marcada = str(r["resposta"]) if r else None

    if r is None:
        return {**base, "classificacao": "errada", "sua_resposta": "(não respondida)", "resposta_certa": certa}
    return {**base, "classificacao": "certa" if r["correta"] else "errada",
            "sua_resposta": marcada or str(r["resposta"]), "resposta_certa": certa}


async def corrigir_e_revisar(agente, slides: list[dict], respostas: dict, material: str, perfil) -> dict:
    """respostas = {question_id: {"resposta": ..., "correta": bool|None}} da rodada atual.

    Levanta exceção se a correção das abertas falhar — sem ela não dá pra
    calcular a nota, e o aluno tenta de novo (503 no endpoint). Nunca chuta
    nota por falha técnica."""
    perguntas = _perguntas_dos_slides(slides)
    itens: list[dict] = []
    abertas: list[dict] = []

    for p in perguntas:
        if p.get("tipo") == "open":
            r = respostas.get(p["id"])
            item = {"id": p["id"], "tipo": "open", "enunciado": p.get("enunciado", ""),
                    "sua_resposta": str(r["resposta"]) if r else "(não respondida)",
                    "resposta_certa": p.get("resposta_modelo") or "", "explicacao": ""}
            if r and str(r["resposta"]).strip():
                abertas.append({"id": p["id"], "enunciado": p.get("enunciado", ""), "cenario": p.get("cenario") or "",
                                "esperado": p.get("resposta_modelo") or p.get("explicacao") or "",
                                "resposta": str(r["resposta"])})
            else:
                item["classificacao"] = "errada"
            itens.append(item)
        else:
            itens.append(_item_objetivo(p, respostas))

    por_id = {i["id"]: i for i in itens}

    # 1) Abertas: a IA classifica contra o gabarito de cada uma (1 chamada)
    if abertas:
        resultado = await agente.corrigir_abertas(abertas, material, perfil=perfil)
        devolvidos = {str(x.get("id")): x for x in (resultado.get("itens") or [])}
        for a in abertas:
            x = devolvidos.get(a["id"])
            if not x or x.get("classificacao") not in PONTOS:
                # IA "esqueceu" o item (achado conhecido do Groq): falha técnica
                raise RuntimeError(f"correção da aberta {a['id']} não veio da IA")
            por_id[a["id"]].update({
                "classificacao": x["classificacao"],
                "resposta_certa": x.get("ponto_certo") or por_id[a["id"]]["resposta_certa"],
                "explicacao": x.get("o_que_faltou") or "",
                "exemplo": x.get("exemplo") or "",
                "slide": x.get("slide") if isinstance(x.get("slide"), int) else None,
            })

    # 2) Objetivas erradas/parciais: exemplo + slide (a resposta certa já é do gabarito).
    # Opcional — se falhar, o cartão sai só com a explicação do próprio material.
    objetivas_erradas = [i for i in itens if i["tipo"] != "open" and i["classificacao"] != "certa"]
    if objetivas_erradas:
        try:
            extra = await agente.enriquecer_objetivas(objetivas_erradas, material, perfil=perfil)
            for x in extra.get("itens") or []:
                alvo = por_id.get(str(x.get("id")))
                if alvo:
                    # A explicação escrita no material tem prioridade — a IA só
                    # preenche quando o material não tem (menos chance de inventar).
                    alvo["explicacao"] = alvo["explicacao"] or x.get("explicacao") or ""
                    alvo["exemplo"] = x.get("exemplo") or ""
                    alvo["slide"] = x.get("slide") if isinstance(x.get("slide"), int) else None
        except Exception as e:
            print(f"⚠️ enriquecer objetivas falhou (segue só com o gabarito): {e}")

    nota = sum(PONTOS[i["classificacao"]] for i in itens)
    return {
        "itens": itens,
        "nota": nota,
        "total": len(itens),
        "certas": sum(1 for i in itens if i["classificacao"] == "certa"),
    }


def dificuldades_do_resultado(itens: list[dict]) -> list[dict]:
    return [i for i in itens if i["classificacao"] in ("errada", "parcial")]
