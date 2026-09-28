"""
Corrige o texto da introdução das provas antigas — 2026-09-27.

As provas geradas até aqui nasceram com um texto da época em que o tutor era externo:
"...acontece quando você levar o resumo desta tela pro chat com o Claude." Hoje o tutor
corrige dentro da plataforma. O gerador (app/agents/montar_topico.py) já foi corrigido;
este script atualiza as provas que já estão no banco.

Seguro:
- só mexe em prova cujo intro.instrucoes_box.texto contém "chat com o Claude";
- salva backup JSON de TODAS as provas alteradas antes de gravar (nada é apagado);
- idempotente: rodar de novo não altera nada.

Uso (dentro do container do backend, que já tem acesso ao banco):
    docker exec nia_backend python scripts/corrigir_intro_provas.py            # só mostra
    docker exec nia_backend python scripts/corrigir_intro_provas.py --aplicar  # grava
Em produção: mesmo comando no servidor.
"""
import argparse
import copy
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm.attributes import flag_modified  # noqa: E402

from app.database import SessionLocal  # noqa: E402
from app.models.models import Avaliacao  # noqa: E402

MARCA_ANTIGA = "chat com o Claude"
LABEL_NOVO = "📋 Como funciona"
TEXTO_NOVO = (
    "As questões objetivas mostram a resposta certa na hora. No fim, você envia a prova "
    "e o tutor corrige tudo — inclusive as abertas — e diz se você pode seguir ou o que "
    "vale revisar."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="grava no banco (sem isso só mostra)")
    args = ap.parse_args()

    db = SessionLocal()
    try:
        alvos = []
        for av in db.query(Avaliacao).order_by(Avaliacao.id).all():
            box = ((av.conteudo or {}).get("intro") or {}).get("instrucoes_box") or {}
            if MARCA_ANTIGA in (box.get("texto") or ""):
                alvos.append(av)

        print(f"{len(alvos)} prova(s) com o texto antigo: {[a.id for a in alvos]}")
        if not alvos or not args.aplicar:
            if alvos:
                print("Nada gravado. Rode com --aplicar pra corrigir.")
            return

        backup = Path(__file__).resolve().parent.parent / (
            f"_backup_intro_provas_{datetime.now():%Y-%m-%d_%H%M}.json"
        )
        backup.write_text(
            json.dumps({a.id: a.conteudo for a in alvos}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print(f"Backup: {backup}")

        for av in alvos:
            conteudo = copy.deepcopy(av.conteudo)
            conteudo["intro"]["instrucoes_box"]["label"] = LABEL_NOVO
            conteudo["intro"]["instrucoes_box"]["texto"] = TEXTO_NOVO
            av.conteudo = conteudo
            flag_modified(av, "conteudo")
        db.commit()
        print(f"{len(alvos)} prova(s) corrigida(s).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
