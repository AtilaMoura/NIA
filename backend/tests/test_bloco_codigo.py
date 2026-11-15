"""Bloco 'codigo' (NIA-T-029): renderização escapada, botão Copiar, validação e não-regressão."""
import re

from app.renderer.render import render_topico
from app.renderer.validate import validar_topico


def _conteudo(blocos):
    return {
        "titulo": "Tópico de teste", "numero": 1, "duracao_estimada_min": 12, "topico_id": 1,
        "slides": [
            {"tipo": "conteudo", "titulo": "Slide", "secao": "S", "blocos": blocos},
            {"tipo": "resultado", "titulo": "Fim", "secao": "Fim", "proximo_topico_label": "Próximo"},
        ],
    }


def _render(blocos, tema="vidro-fume"):
    return render_topico(_conteudo(blocos), tema)


BLOCO = {"tipo": "codigo", "linguagem": "powershell", "titulo": "Criar o repositório",
         "texto": "mkdir C:\treino\ncd C:\treino\ngit init -b main", "nota": "Um comando por vez."}


def test_renderiza_codigo_com_quebras_botao_e_rotulos():
    html = _render([BLOCO])
    assert 'class="codigo-pre"' in html and "codigo-copy-btn" in html
    assert "mkdir C:\treino\ncd C:\treino\ngit init -b main" in html  # quebras preservadas
    assert "Criar o repositório" in html and "powershell" in html and "Um comando por vez." in html


def test_texto_do_codigo_sai_escapado():
    html = _render([{"tipo": "codigo", "texto": "<script>alert(1)</script> & <b>x</b>"}])
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp; &lt;b&gt;x&lt;/b&gt;" in html
    assert "<script>alert(1)</script>" not in html


def test_renderiza_nos_temas_claro_e_escuro():
    from app.renderer.render import carregar_temas
    for tid in list(carregar_temas())[:4]:
        assert "codigo-pre" in _render([BLOCO], tid)


def test_sem_bloco_codigo_nao_cria_elemento_do_bloco():
    html = _render([{"tipo": "paragrafo", "texto": "oi"}])
    assert '<div class="codigo-bloco">' not in html and '<pre class="codigo-pre">' not in html
    # o bloco prompt_externo continua igual
    html2 = _render([{"tipo": "prompt_externo", "titulo": "T", "texto": "abc"}])
    assert "prompt-copy-btn" in html2 and "Copiar prompt" in html2 and '<div class="codigo-bloco">' not in html2


def _problemas_codigo(bloco):
    return [p for p in validar_topico(_conteudo([bloco])) if "codigo" in p]


def test_validacao_acusa_texto_vazio_e_linguagem_invalida():
    assert _problemas_codigo({"tipo": "codigo", "texto": "   "})
    assert _problemas_codigo({"tipo": "codigo"})
    assert _problemas_codigo({"tipo": "codigo", "texto": "ls", "linguagem": "cobol"})
    assert _problemas_codigo({"tipo": "codigo", "texto": "x" * 5001})


def test_validacao_aceita_bloco_correto():
    assert not _problemas_codigo(BLOCO)
    assert not _problemas_codigo({"tipo": "codigo", "texto": "ls"})
