"""Bug do NIA-T-026: reprovar no checklist NÃO pode esconder um tópico publicado.
Topico.is_approved = visibilidade (scripts de publicação gravam True); o checklist
não pode mais mexer nele."""
from tests.conftest import como


def _checklist(aprovado):
    return {"profundidade": "raso", "clareza": "confuso", "qualidade_geral": "fraca",
            "observacao_final": "teste", "aprovado": aprovado}


def test_checklist_reprovado_nao_esconde_topico_publicado(api, cenario):
    assert cenario.topico.is_approved is True
    r = api.put(f"/topico-checklists/{cenario.topico.id}", json=_checklist(False), headers=como(cenario.master))
    assert r.status_code == 200, r.text
    cenario.db.refresh(cenario.topico)
    assert cenario.topico.is_approved is True  # continua visível para os alunos


def test_checklist_aprovado_tambem_nao_mexe_na_visibilidade(api, cenario):
    cenario.topico.is_approved = False  # tópico ainda não publicado
    cenario.db.flush()
    r = api.put(f"/topico-checklists/{cenario.topico.id}", json=_checklist(True), headers=como(cenario.master))
    assert r.status_code == 200, r.text
    cenario.db.refresh(cenario.topico)
    assert cenario.topico.is_approved is False  # publicar é outro ato
