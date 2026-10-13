"""Qual modelo de IA cada função do NIA usa — num lugar só (2026-10-01).

Antes, cada router/agent criava `GeminiService()`/`GroqService()` com o seu próprio
modelo fixo no código. Agora cada FUNÇÃO tem uma CADEIA de modelos: tenta o primeiro
e, se ele falhar (503 "alta demanda", 429/cota do dia, timeout, resposta inválida),
passa pro próximo automaticamente.

Por que cadeia e não um modelo só: no teste comparativo de 2026-10-01
(docs/modelos/BENCHMARK_2026-10-01.md) os Gemini Flash novos não erraram nenhum fato,
mas deram 503 na maioria das tentativas — e cada um tem só 20 pedidos/dia, com cota
SEPARADA por modelo (docs/modelos/LIMITES_GEMINI.md). Revezando, a soma rende bem mais.
Os modelos do Groq erraram raciocínio numérico, então ficam como segunda opinião.

REGRA DO ATILA (2026-10-05): em TUDO, primeiro Gemini e depois Groq — toda cadeia
começa pelos modelos Gemini e termina com Groq como reserva. Única exceção:
"segunda_opiniao", que existe justamente pra ser OUTRO provedor (o processo híbrido
compara Groq x Gemini); se ela começasse no Gemini, deixaria de ser segunda opinião.

Trocar sem mexer em código: variável de ambiente NIA_MODELOS_<FUNCAO>, ex.
    NIA_MODELOS_CONTEUDO="gemini:gemini-3.7-flash,groq:qwen/qwen3.8-27b"

Uso:
    from app.services.modelos import servico
    agente = ContentAgent(servico("conteudo"))
"""

import inspect
import os
import time

from app.services.gemini_service import GeminiService
from app.services.groq_service import GroqService

# Ordem = preferência. Formato: (provedor, modelo).
CADEIAS: dict[str, list[tuple[str, str]]] = {
    # Gerar conteúdo de curso a partir do dossiê (ContentAgent, pipeline do admin)
    "conteudo": [
        ("gemini", "gemini-3.5-flash"),
        ("gemini", "gemini-3.7-flash"),
        ("gemini", "gemini-2.5-flash"),
        ("gemini", "gemini-3.8-flash"),
        ("gemini", "gemma-4-31b-it"),
        ("groq", "qwen/qwen3.8-27b"),
        ("groq", "openai/gpt-oss-120b"),
    ],
    # Perguntas (QuizAgent) — mesma família, cotas separadas
    "quiz": [
        ("gemini", "gemini-3.5-flash"),
        ("gemini", "gemini-3.7-flash"),
        ("gemini", "gemini-2.5-flash"),
        ("gemini", "gemini-3.5-flash-lite"),
        ("groq", "qwen/qwen3.8-27b"),
        ("groq", "openai/gpt-oss-120b"),
    ],
    # Segunda opinião do processo híbrido (outro provedor de propósito — exceção à regra)
    "segunda_opiniao": [
        ("groq", "qwen/qwen3.8-27b"),
        ("groq", "openai/gpt-oss-120b"),
    ],
    # Texto da narração de cada bloco (volume alto, prompt curto → Gemma 4: 14.400/dia)
    "narracao": [
        ("gemini", "gemma-4-31b-it"),
        ("gemini", "gemini-3.5-flash-lite"),
        ("gemini", "gemini-3.1-flash-lite"),
        ("groq", "qwen/qwen3.8-27b"),
    ],
    # Correção do fim do tópico e da prova (nota + revisão do aluno). Antes caía no Groq
    # (rota com modelo="groq" por padrão) — e o Groq foi quem mais errou fato no teste
    # comparativo; num caso real (T66, 2026-10-01) inventou detalhe bíblico na revisão.
    # Reordenada 2026-10-07 (PENDENCIAS.md item 6): a prova 38 levou ~3 min porque os
    # Flash maiores davam 503 (até 44 s cada) e o JSON quebrava. Com o modo JSON nativo,
    # o 3.5 Flash Lite corrigiu as respostas reais do Atila igual à produção em 19 s
    # (_comparar_modelos_correcao.py) e tem 500/dia → vai primeiro; os Flash maiores
    # (agora com 3.8 e 3.6, cota própria de 20/dia cada) ficam de reserva.
    "correcao": [
        ("gemini", "gemini-3.5-flash-lite"),
        ("gemini", "gemini-3.8-flash"),
        ("gemini", "gemini-3.1-flash-lite"),
        ("gemini", "gemini-3.7-flash"),
        ("gemini", "gemini-3.6-flash"),
        ("gemini", "gemini-3.5-flash"),
        ("gemini", "gemini-2.5-flash"),
        ("groq", "qwen/qwen3.8-27b"),
    ],
    # Caderno da aula (2026-10-05): organiza e CORRIGE as anotações do aluno contra o
    # material — mesma prioridade da correção (fato importa mais que velocidade)
    "caderno": [
        ("gemini", "gemini-3.5-flash"),
        ("gemini", "gemini-3.7-flash"),
        ("gemini", "gemini-2.5-flash"),
        ("gemini", "gemini-3.5-flash-lite"),
        ("groq", "qwen/qwen3.8-27b"),
    ],
    # Tutor ao vivo na plataforma (rápido, muitos pedidos/dia)
    "tutor": [
        ("gemini", "gemini-3.5-flash-lite"),
        ("gemini", "gemini-3.1-flash-lite"),
        ("groq", "qwen/qwen3.8-27b"),
        ("groq", "openai/gpt-oss-120b"),
    ],
}

# Voz (TTS): só Gemini; revezar (10 pedidos/dia por modelo, todos aprovados pelo Atila)
CADEIA_VOZ: list[str] = [
    "gemini-3.8-flash-tts",
    "gemini-3.8-flash-lite-tts",
    "gemini-2.5-flash-preview-tts",
]

# Modelo que estourou a cota do dia (429) fica fora da fila por um tempo,
# pra não gastar uma tentativa nele a cada pedido.
_PAUSA_COTA_S = 15 * 60
# Modelo sobrecarregado (503 "alta demanda") ou que estourou o tempo sai da fila por
# pouco tempo (2026-10-13): a correção faz até 3 chamadas seguidas no mesmo envio e
# cada uma batia de novo nos mesmos modelos em 503 — foi o que deu ~3 min na prova 38.
_PAUSA_SOBRECARGA_S = 2 * 60
_pausados: dict[str, float] = {}

# Tempo máximo de espera por modelo (Gemini), por função. O padrão do GeminiService é
# 90 s; na correção o aluno está esperando na tela e o normal é 19-30 s
# (_comparar_modelos_correcao.py, 2026-10-07) — passou de 45 s, vai pro próximo modelo.
TIMEOUT_MS: dict[str, int] = {"correcao": 45_000}


def _cadeia(funcao: str) -> list[tuple[str, str]]:
    env = os.getenv(f"NIA_MODELOS_{funcao.upper()}")
    if env:
        itens = []
        for parte in env.split(","):
            prov, _, modelo = parte.strip().partition(":")
            if prov and modelo:
                itens.append((prov, modelo))
        if itens:
            return itens
    if funcao not in CADEIAS:
        raise ValueError(f"Função de modelo desconhecida: {funcao}")
    return CADEIAS[funcao]


def _estourou_cota(erro: Exception) -> bool:
    msg = str(erro).lower()
    return "429" in msg or "resource_exhausted" in msg or "quota" in msg


def _sobrecarregado(erro: Exception) -> bool:
    msg = str(erro).lower()
    # O GeminiService embrulha o erro original; o timeout do httpx vem com mensagem vazia,
    # então olha também o tipo da causa.
    causa = type(erro.__context__).__name__.lower() if erro.__context__ else ""
    sinais = ("503", "unavailable", "overloaded", "504", "deadline", "timed out", "timeout")
    return any(s in msg for s in sinais) or "timeout" in causa


def _pausa_por(erro: Exception) -> int:
    """Segundos fora da fila depois desta falha (0 = não pausa)."""
    if _estourou_cota(erro):
        return _PAUSA_COTA_S
    return _PAUSA_SOBRECARGA_S if _sobrecarregado(erro) else 0


def _criar(prov: str, modelo: str, funcao: str = ""):
    if prov == "gemini":
        if funcao in TIMEOUT_MS:
            return GeminiService(model_name=modelo, timeout_ms=TIMEOUT_MS[funcao])
        return GeminiService(model_name=modelo)
    if prov == "groq":
        return GroqService(model=modelo)
    raise ValueError(f"Provedor desconhecido: {prov}")


class ServicoComReserva:
    """Mesma interface do GeminiService/GroqService (generate, generate_json, ...),
    mas tenta a cadeia de modelos em ordem até um responder."""

    def __init__(self, funcao: str):
        self.funcao = funcao
        self.cadeia = _cadeia(funcao)
        self._instancias: dict[str, object] = {}
        self.ultimo_modelo: str | None = None  # quem respondeu de fato (pra log/registro)

    def _servico(self, prov: str, modelo: str):
        chave = f"{prov}:{modelo}"
        if chave not in self._instancias:
            self._instancias[chave] = _criar(prov, modelo, self.funcao)
        return self._instancias[chave]

    def __getattr__(self, nome: str):
        if nome.startswith("_"):
            raise AttributeError(nome)

        async def chamar(*args, **kwargs):
            ultimo_erro: Exception | None = None
            agora = time.time()
            for prov, modelo in self.cadeia:
                chave = f"{prov}:{modelo}"
                if _pausados.get(chave, 0) > agora:
                    continue
                try:
                    metodo = getattr(self._servico(prov, modelo), nome, None)
                except Exception as e:  # ex.: chave de API ausente
                    ultimo_erro = e
                    continue
                if metodo is None:
                    continue
                # Gemini e Groq aceitam parâmetros um pouco diferentes
                # (ex.: generate_json do Groq não tem temperature) — repassa só os aceitos
                aceitos = inspect.signature(metodo).parameters
                kw = {k: v for k, v in kwargs.items() if k in aceitos}
                try:
                    resposta = await metodo(*args, **kw)
                    # Resposta vazia (visto no Gemma 4 em 2026-10-01: text=None) também é falha
                    if resposta is None or (isinstance(resposta, str) and not resposta.strip()):
                        raise RuntimeError("resposta vazia")
                    self.ultimo_modelo = chave
                    return resposta
                except Exception as e:
                    ultimo_erro = e
                    if pausa := _pausa_por(e):
                        _pausados[chave] = time.time() + pausa
                    print(f"[modelos:{self.funcao}] {chave} falhou ({str(e)[:120]}) — tentando o próximo")
            # "503" na mensagem: o endpoint da correção trata como sobrecarga passageira
            raise ultimo_erro or RuntimeError(f"503: todos os modelos de '{self.funcao}' estão em pausa")

        return chamar


def servico(funcao: str) -> ServicoComReserva:
    """Serviço de IA pra uma função ("conteudo", "quiz", "segunda_opiniao", "tutor")."""
    return ServicoComReserva(funcao)


async def gerar_voz(texto: str, voice_name: str = "Kore") -> tuple[bytes, str]:
    """Gera áudio revezando os modelos de voz. Devolve (wav, modelo usado).
    ATENÇÃO: o modelo de voz lê em voz alta TUDO o que recebe — mandar só o texto."""
    gemini = GeminiService()
    ultimo_erro: Exception | None = None
    agora = time.time()
    for modelo in CADEIA_VOZ:
        chave = f"voz:{modelo}"
        if _pausados.get(chave, 0) > agora:
            continue
        try:
            return await gemini.generate_audio(texto, voice_name=voice_name, tts_model=modelo), modelo
        except Exception as e:
            ultimo_erro = e
            if _estourou_cota(e):
                _pausados[chave] = agora + _PAUSA_COTA_S
            print(f"[modelos:voz] {modelo} falhou ({str(e)[:120]}) — tentando o próximo")
    raise ultimo_erro or RuntimeError("Nenhum modelo de voz disponível")
