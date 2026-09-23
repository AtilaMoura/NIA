"""Segunda checagem das lacunas em resposta ABERTA (2026-09-23).

Achado real (Tópico 19 em produção): mesmo recebendo o material e a resposta
esperada, o tutor às vezes (1 em ~9 chamadas nos testes) marca como lacuna
"real" uma resposta que diz a mesma coisa que o material — o gpt-oss varia de
uma chamada pra outra num julgamento geral. Aqui, SÓ quando o veredito é
"reforco" por causa de resposta aberta, uma chamada pequena e focada responde
uma pergunta de sim/não: a resposta do aluno CONTRADIZ a resposta esperada?
Se não contradiz, a lacuna vira "superficial" e, sem nenhuma lacuna real
sobrando, o veredito vira "dominado".

Na dúvida (erro na chamada, pergunta não identificada), mantém o resultado
original — nunca aprova por falha técnica.
"""

import re
import unicodedata

from app.renderer.render import _label_pergunta


def _norm(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", texto.lower())).strip()


def montar_abertas_do_aluno(slides: list[dict], respostas: dict[str, str]) -> list[dict]:
    """Perguntas abertas do material + o que o aluno respondeu em cada uma."""
    abertas = []
    for slide in slides:
        if slide.get("tipo") == "checkpoint":
            perguntas = slide.get("perguntas", [])
        elif slide.get("tipo") == "avaliacao_pergunta":
            perguntas = [slide.get("pergunta") or {}]
        else:
            continue
        for p in perguntas:
            if p.get("tipo") != "open" or not respostas.get(p.get("id")):
                continue
            abertas.append({
                "id": p["id"],
                "label": _label_pergunta(slide.get("secao", ""), p.get("enunciado", "")),
                "enunciado": p.get("enunciado", ""),
                "cenario": p.get("cenario") or "",
                "esperado": p.get("resposta_modelo") or p.get("explicacao") or "",
                "resposta": respostas[p["id"]],
            })
    return abertas


def _aberta_da_lacuna(lacuna: dict, abertas: list[dict]) -> dict | None:
    """Acha qual pergunta aberta a lacuna está citando (pelo trecho da resposta
    do aluno citado na evidência, ou pelo enunciado)."""
    alvo = _norm(f"{lacuna.get('tema', '')} {lacuna.get('evidencia', '')}")
    for a in abertas:
        trecho_resposta = _norm(a["resposta"])[:40]
        trecho_enunciado = _norm(a["enunciado"])[:30]
        if (trecho_resposta and trecho_resposta in alvo) or (trecho_enunciado and trecho_enunciado in alvo):
            return a
    return None


async def revisar_lacunas_abertas(agente, resultado: dict, abertas: list[dict], perfil) -> dict:
    if resultado.get("veredito") != "reforco" or not abertas:
        return resultado

    verificacoes: dict[str, dict] = {}
    revisou_alguma = False
    for lacuna in resultado.get("lacunas") or []:
        if lacuna.get("gravidade") != "real":
            continue
        aberta = _aberta_da_lacuna(lacuna, abertas)
        if not aberta or not aberta["esperado"]:
            continue  # lacuna de questão objetiva, ou sem gabarito: fica como está
        if aberta["id"] not in verificacoes:
            try:
                verificacoes[aberta["id"]] = await agente.verificar_resposta_aberta(aberta, perfil=perfil)
            except Exception as e:  # falha técnica nunca aprova ninguém
                print(f"⚠️ revisão de lacuna aberta falhou ({aberta['id']}): {e}")
                verificacoes[aberta["id"]] = {"contradiz": True}
        verificacao = verificacoes[aberta["id"]]
        if verificacao.get("contradiz") is False:
            lacuna["gravidade"] = "superficial"
            lacuna["revisao"] = verificacao.get("explicacao", "Não contradiz o material.")
            revisou_alguma = True

    if revisou_alguma and not any(l.get("gravidade") == "real" for l in resultado.get("lacunas") or []):
        explicacoes = [v.get("explicacao") for v in verificacoes.values() if v.get("contradiz") is False and v.get("explicacao")]
        resultado["veredito"] = "dominado"
        resultado["resumo_diagnostico"] = (
            explicacoes[0] if explicacoes else "Respostas alinhadas ao material do tópico."
        )
        resultado["reforco_sugerido"] = {"necessario": False, "foco": "", "instrucao_para_gerar": ""}
        resultado["revisao_automatica"] = True  # rastro: veredito corrigido pela 2ª checagem
    return resultado
