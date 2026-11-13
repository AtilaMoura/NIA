"""Regras da revisão no tópico (NIA-T-026): permissão, aprovar, enviar à IA, reabrir, tratar."""
from datetime import timedelta

from tests.conftest import como


def _ponto(api, cenario, user, topico=None, slide=1, texto="Trocar este exemplo"):
    t = topico or cenario.topico
    return api.post("/topico-comments/", json={"topico_id": t.id, "slide_index": slide, "texto": texto}, headers=como(user))


def _revisao(api, cenario, user, topico=None):
    t = topico or cenario.topico
    return api.get(f"/topicos/{t.id}/revisao", headers=como(user))


# ---- Permissão ----

def test_aluno_recebe_403(api, cenario):
    assert _revisao(api, cenario, cenario.aluno).status_code == 403
    assert api.post(f"/topicos/{cenario.topico.id}/revisao/aprovar", json={}, headers=como(cenario.aluno)).status_code == 403
    assert _ponto(api, cenario, cenario.aluno).status_code == 403


def test_professor_fora_do_curso_recebe_403(api, cenario):
    assert _revisao(api, cenario, cenario.prof_fora).status_code == 403
    assert _ponto(api, cenario, cenario.prof_fora).status_code == 403
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/aprovar", json={}, headers=como(cenario.prof_fora))
    assert r.status_code == 403


def test_professor_tutor_do_curso_pode(api, cenario):
    r = _revisao(api, cenario, cenario.prof_tutor)
    assert r.status_code == 200
    assert r.json()["pode_revisar"] is True and r.json()["status"] == "pendente"
    assert _ponto(api, cenario, cenario.prof_tutor).status_code == 200


def test_master_e_admin_em_qualquer_curso(api, cenario):
    assert _revisao(api, cenario, cenario.master).status_code == 200
    assert _revisao(api, cenario, cenario.admin).status_code == 200


def test_topico_inexistente_404(api, cenario):
    assert api.get("/topicos/99999999/revisao", headers=como(cenario.master)).status_code == 404


# ---- Fluxo de estados ----

def test_aprovar_grava_status_evento_e_nao_mexe_na_visibilidade(api, cenario):
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/aprovar", json={"observacao": "ok"}, headers=como(cenario.prof_tutor))
    assert r.status_code == 200, r.text
    j = r.json()
    assert j["status"] == "aprovado" and j["aprovado_por"] == "Teste professor"
    assert [e["acao"] for e in j["eventos"]] == ["aprovar"]
    cenario.db.refresh(cenario.topico)
    assert cenario.topico.is_approved is True


def test_enviar_ia_sem_ponto_da_400(api, cenario):
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/enviar-ia", headers=como(cenario.master))
    assert r.status_code == 400


def test_enviar_ia_com_ponto_aberto(api, cenario):
    assert _ponto(api, cenario, cenario.master).status_code == 200
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/enviar-ia", headers=como(cenario.master))
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "enviado_ia" and r.json()["abertos"] == 1


def test_enviar_ia_com_anotacao_de_revisor_pendente(api, cenario):
    cenario.nova_anotacao(cenario.master, cenario.topico, slide=2)
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/enviar-ia", headers=como(cenario.master))
    assert r.status_code == 200 and r.json()["status"] == "enviado_ia"


def test_anotacao_de_aluno_nao_conta_como_ponto(api, cenario):
    cenario.nova_anotacao(cenario.aluno, cenario.topico, slide=2)
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/enviar-ia", headers=como(cenario.master))
    assert r.status_code == 400
    assert _revisao(api, cenario, cenario.master).json()["anotacoes"] == []


def test_ponto_novo_reabre_topico_aprovado(api, cenario):
    api.post(f"/topicos/{cenario.topico.id}/revisao/aprovar", json={}, headers=como(cenario.master))
    assert _revisao(api, cenario, cenario.master).json()["status"] == "aprovado"
    assert _ponto(api, cenario, cenario.master).status_code == 200
    j = _revisao(api, cenario, cenario.master).json()
    assert j["status"] == "pendente"
    assert [e["acao"] for e in j["eventos"]] == ["aprovar", "reabrir"]


def test_ia_revisou_volta_a_pendente_e_resolve(api, cenario):
    comentario = _ponto(api, cenario, cenario.master).json()
    api.post(f"/topicos/{cenario.topico.id}/revisao/enviar-ia", headers=como(cenario.master))
    r = api.post(
        f"/topicos/{cenario.topico.id}/revisao/ia-revisou",
        json={"pontos": [{"comment_id": comentario["id"], "resposta_ia": "Troquei o exemplo"}], "anotacoes": []},
        headers=como(cenario.master),
    )
    assert r.status_code == 200, r.text
    j = r.json()
    assert j["status"] == "pendente" and j["abertos"] == 0
    assert j["pontos"][0]["resolvido"] is True and j["pontos"][0]["resposta_ia"] == "Troquei o exemplo"
    assert [e["acao"] for e in j["eventos"]] == ["enviar_ia", "ia_revisou"]


def test_ia_revisou_rejeita_ponto_de_outro_topico(api, cenario):
    outro = cenario.novo_topico(5)
    comentario = _ponto(api, cenario, cenario.master, topico=outro).json()
    r = api.post(f"/topicos/{cenario.topico.id}/revisao/ia-revisou",
                 json={"pontos": [{"comment_id": comentario["id"], "resposta_ia": "x"}]}, headers=como(cenario.master))
    assert r.status_code == 400


def test_anotacao_tratada_e_editada_depois_volta_a_pendente(api, cenario):
    a = cenario.nova_anotacao(cenario.prof_tutor, cenario.topico, slide=3)
    ver = _revisao(api, cenario, cenario.master).json()
    assert ver["anotacoes"][0]["tratada"] is False and ver["abertos"] == 1

    r = api.post(f"/topicos/{cenario.topico.id}/revisao/ia-revisou",
                 json={"anotacoes": [{"anotacao_id": a.id, "resposta_ia": "Ajustado"}]}, headers=como(cenario.master))
    assert r.status_code == 200, r.text
    assert r.json()["anotacoes"][0]["tratada"] is True and r.json()["abertos"] == 0

    # o revisor edita a anotação depois (updated_at passa a ser maior que o visto pela IA)
    cenario.db.refresh(a)
    a.texto = "agora quero outra coisa"
    a.updated_at = a.created_at + timedelta(hours=1)
    cenario.db.flush()
    j = _revisao(api, cenario, cenario.master).json()
    assert j["anotacoes"][0]["tratada"] is False and j["abertos"] == 1


def test_comentario_do_professor_fora_do_curso_nao_pode_ser_resolvido(api, cenario):
    c = _ponto(api, cenario, cenario.master).json()
    r = api.put(f"/topico-comments/{c['id']}", json={"resolvido": True}, headers=como(cenario.prof_fora))
    assert r.status_code == 403
