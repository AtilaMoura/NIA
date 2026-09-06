"""
Aplica o campo `narracao` (gerado por _gerar_narracao_obreiro.py, salvo em
_narracoes_obreiro.json) no Topico.content de verdade, via PUT /topicos/{id}.
"""
import json
import urllib.request
from pathlib import Path

BASE_URL = "http://localhost:8100"


def get_topico(tid: int) -> dict:
    with urllib.request.urlopen(f"{BASE_URL}/topicos/{tid}") as r:
        return json.load(r)


def put_content(tid: int, topico: dict, content: dict) -> int:
    topico = dict(topico)
    topico["content"] = json.dumps(content, ensure_ascii=False)
    data = json.dumps(topico).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/topicos/{tid}", data=data, method="PUT",
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.status


def main():
    narracoes = json.loads(Path(__file__).parent.joinpath("_narracoes_obreiro.json").read_text(encoding="utf-8"))
    for tid_str, itens in narracoes.items():
        tid = int(tid_str)
        topico = get_topico(tid)
        content = json.loads(topico["content"])
        aplicados = 0
        for item in itens:
            idx = item["slide_idx"]
            content["slides"][idx]["narracao"] = item["narracao"]
            aplicados += 1
        status = put_content(tid, topico, content)
        print(f"Topico {tid}: {aplicados} narracoes aplicadas, PUT -> {status}")


if __name__ == "__main__":
    main()
