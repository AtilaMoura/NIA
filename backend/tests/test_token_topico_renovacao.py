"""Renovação do token curto do render (NIA-T-030): o iframe pede token novo ao pai ao tomar 401."""
from app.renderer.render import render_topico


def _html():
    conteudo = {
        "titulo": "Tópico de teste", "numero": 1, "duracao_estimada_min": 12, "topico_id": 1,
        "slides": [
            {"tipo": "conteudo", "titulo": "Slide", "secao": "S", "blocos": [{"tipo": "paragrafo", "texto": "oi"}]},
            {"tipo": "resultado", "titulo": "Fim", "secao": "Fim", "proximo_topico_label": "Próximo"},
        ],
    }
    return render_topico(conteudo, "vidro-fume")


def test_helper_pede_token_novo_ao_pai():
    html = _html()
    assert "function fetchComToken" in html
    assert "emaus:token-renovar" in html
    assert "emaus:token-novo" in html
    assert "emaus:token-falhou" in html
    assert "var RESPOSTAS_TOKEN" in html and "const RESPOSTAS_TOKEN" not in html


def test_mensagem_de_sessao_expirada():
    assert "Sua sessão expirou" in _html()


def test_nenhum_fetch_monta_bearer_fora_do_helper():
    html = _html()
    assert html.count("'Bearer ' + RESPOSTAS_TOKEN") == 1
    assert html.count("fetchComToken(") >= 14
