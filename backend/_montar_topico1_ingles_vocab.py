"""
Monta o conteúdo final do NOVO Tópico 1 ("Vocabulário & expressões") do curso de
Inglês — À MÃO, não pega o Groq/Gemini como base direto.

Motivo (achado real comparando os dois, 2026-09-04): o prompt pedia explicitamente
"não invente vocabulário além desta lista, e não deixe nenhum de fora" (17 palavras
de `_pesquisa.md`) — NENHUM dos dois respeitou:
- Groq cobriu só 7 das 17 palavras (parou no meio) e ainda testou, na avaliação
  final, 2 palavras que nunca chegou a ensinar ("bite off more than you can chew",
  "let the record show") — bug de coerência.
- Gemini cobriu outras poucas do grounding real, mas COMPLETOU a lição inventando
  16 palavras que não estavam na lista (end, over, declare, full, wish, persist,
  plan, strategy, overcome, struggle, dignity, legacy, speak out, truth...) e
  deixou de fora 9 das 17 palavras reais.

Decisão: aproveitar o texto do Groq pras 7 palavras que ele cobriu direito (boa
qualidade, sem invenção), e escrever as 9 que faltaram à mão, com base direto em
`estudo-ingles/unidades/01-my-way/_pesquisa.md` (exemplos já são meus, de uma
sessão anterior — não são as palavras da letra, não tem risco de copyright). O
"fluxo" dos 6 movimentos também é reescrito à mão — os dois provedores substituíram
por estrutura genérica de música pop (intro/verse/chorus/bridge), ignorando o
grounding real dos movimentos temáticos da letra.

Rodar: docker exec nia_backend python _montar_topico1_ingles_vocab.py
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_service import GroqService
from app.agents.quiz_agent import QuizAgent
from app.agents.montar_topico import montar_topico


def vocab(termo, classe, traducao, en, pt, cuidado=None):
    d = {
        "tipo": "vocab", "termo": termo, "classe_gramatical": classe,
        "traducao": traducao, "exemplo_en": en, "exemplo_pt": pt,
    }
    if cuidado:
        d["cuidado"] = cuidado
    return d


def montar_conteudo() -> dict:
    slides = [
        {
            "tipo": "capa", "secao": "Início",
            "titulo": "Vocabulário & Expressões — My Way",
            "subtitulo": "17 palavras e expressões reais da música, organizadas pela estrutura da letra",
            "instrucoes_box": {
                "label": "📋 Como funciona este estudo",
                "texto": "Use as setas ← → ou os botões embaixo para navegar. Alguns slides são checkpoints — pedem uma resposta antes de liberar o próximo.",
            },
        },
        # Assunto 1 — estrutura real da música (fluxo temático, não genérico)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "A estrutura da letra, em 6 movimentos",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "\"My Way\" se organiza em 6 movimentos temáticos — saber essa estrutura "
                    "ajuda a acompanhar a letra de verdade quando você for ouvir a música. "
                    "Não vamos citar a letra aqui (direitos autorais) — só o que cada parte "
                    "faz na história."
                )},
                {"tipo": "fluxo", "passos": [
                    {"texto": "Abertura: anuncia que o fim chegou, encara \"a cortina final\"", "decisao": False},
                    {"texto": "Afirmação: viveu uma vida cheia, fez do seu jeito", "decisao": False},
                    {"texto": "Arrependimentos: teve alguns, poucos demais pra mencionar", "decisao": False},
                    {"texto": "Planejamento: traçou cada rota, cada passo cuidadoso", "decisao": False},
                    {"texto": "A ponte: tropeços — assumiu mais do que dava conta, mas seguiu de cabeça erguida", "decisao": True},
                    {"texto": "Fecho: um homem precisa dizer o que sente de verdade — que fique registrado", "decisao": False},
                ]},
                {"tipo": "imagem_sugerida", "descricao": "Um microfone em um palco vazio, com um único foco de luz quente — sem rosto de pessoa real, remetendo à ideia de 'luz de palco' e 'cortina final'.", "legenda": "A luz do palco, antes da cortina final."},
            ],
            "checkpoint_apos": None,
        },
        # Assunto 2 — abertura/certeza (Groq, bom)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "Abertura: o fim e a certeza",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "A abertura da música fala do fim chegando, com certeza do que está sendo dito. "
                    "Duas peças de vocabulário centrais pra esse movimento:"
                )},
                vocab("the final curtain", "expressão idiomática", "o último ato, o fim definitivo",
                      "After thirty years of teaching, she felt it was time for the final curtain.",
                      "Depois de trinta anos ensinando, ela sentiu que era hora do último ato.",
                      "Vem do teatro (a última cortina que fecha marca o fim da peça). Sempre traz a ideia de encerramento definitivo, não é só \"a cortina\" física."),
                vocab("certain of / certain about", "adjetivo + preposição", "certo de / certo sobre",
                      "I'm certain of the facts, but not certain about what happens next.",
                      "Tenho certeza dos fatos, mas não tenho certeza sobre o que acontece depois.",
                      "Use \"certain of\" com substantivo/pronome direto; \"certain about\" com assunto mais abstrato, gerúndio ou cláusula. Não confundir com \"right\" (que é sobre não ter errado, não sobre convicção)."),
                {"tipo": "box", "variante": "error", "label": "Erro comum",
                 "texto": "Muita gente omite a preposição: \"I am certain the exam.\" O correto é sempre \"certain OF/ABOUT + algo\"."},
            ],
            "checkpoint_apos": {"gate_id": "ck1", "tipo": "tf",
                "testar": "\"The final curtain\" é uma expressão usada só literalmente, para falar de cortinas de teatro de verdade."},
        },
        # Assunto 3 — argumentos e arrependimentos (Groq, bom)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "Afirmação e arrependimentos",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "Depois da abertura, a música afirma uma vida cheia e reconhece alguns "
                    "arrependimentos — poucos demais pra mencionar."
                )},
                vocab("to state your case", "verbo frasal + objeto", "expor seu argumento / apresentar sua posição",
                      "During the meeting, she will state her case for a higher budget.",
                      "Durante a reunião, ela vai expor seu argumento por um orçamento maior.",
                      "\"Case\" aqui não é \"caso\" (situação legal) — é \"argumento/posição\". Não confundir com \"to make a case\" (mais formal, sem o possessivo)."),
                vocab("regret", "verbo / substantivo", "arrepender-se / arrependimento",
                      "I regret not finishing college when I had the chance.",
                      "Eu me arrependo de não ter terminado a faculdade quando tive a chance.",
                      "Como verbo: \"regret + gerúndio\" (arrependimento de algo já feito) ou \"regret + infinitivo\" (lamentar ter que fazer algo agora, ex: \"we regret to inform you...\"). Como substantivo, precisa de artigo: \"a regret\", \"my regret\"."),
                vocab("to mention", "verbo", "citar, mencionar, referir",
                      "It's too small to mention.",
                      "É pequeno demais pra mencionar.",
                      "Implica trazer o assunto à tona sem detalhar — não confundir com \"say\" (dizer) ou \"tell\" (contar)."),
            ],
            "checkpoint_apos": {"gate_id": "ck2", "tipo": "open",
                "testar": "Formule uma frase em inglês usando \"to state your case\" ou \"regret\"."},
        },
        # Assunto 4 — planejamento e caminhos (2 do Groq + 2 novas)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "Planejamento e caminhos",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "A música fala de traçar cada rota, cada passo cuidadoso pelos caminhos "
                    "menores — e de levar tudo até o fim, mesmo com dúvida no caminho."
                )},
                vocab("to chart a course", "verbo + objeto", "traçar uma rota / um plano",
                      "She charted a course from intern to director.",
                      "Ela traçou uma rota de estagiária a diretora.",
                      "Usado tanto pra navegação literal quanto pra planos de vida/carreira — sempre no sentido de decidir o caminho com cuidado."),
                vocab("byway", "substantivo", "estrada secundária",
                      "We took the byways to avoid tolls.",
                      "Pegamos as estradas secundárias pra evitar pedágios.",
                      "Contraste com \"highway\" (rodovia principal) — \"byway\" é sempre o caminho menos óbvio, mais devagar."),
                vocab("doubt", "substantivo / verbo", "dúvida / duvidar",
                      "When in doubt, ask.",
                      "Na dúvida, pergunte.",
                      "\"When in doubt\" é uma expressão fixa muito comum — não traduza como \"quando em dúvida\", em português soa mais natural \"na dúvida\"."),
                vocab("to see it through", "phrasal verb", "levar até o fim, concluir algo",
                      "The project was hard, but we saw it through.",
                      "O projeto foi difícil, mas nós levamos até o fim.",
                      "Não tem nada a ver com visão física — é sobre persistência. O \"it\" sempre se refere a algo já mencionado antes."),
            ],
            "checkpoint_apos": {"gate_id": "ck3", "tipo": "associar",
                "testar": "Associe cada expressão ao significado certo (chart a course / byway / doubt / see it through)."},
        },
        # Assunto 5 — a ponte: tropeços e firmeza (novas)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "A ponte: tropeços e firmeza",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "Na ponte da música, o eu-lírico admite ter assumido mais do que dava conta "
                    "— mas encarou, engoliu e seguiu de cabeça erguida, mesmo sem ter certeza."
                )},
                vocab("to bite off more than you can chew", "expressão idiomática", "assumir mais do que dá conta",
                      "I bit off more than I could chew with two jobs.",
                      "Eu assumi mais do que dava conta com dois empregos.",
                      "Imagem literal: morder um pedaço grande demais pra mastigar. Sempre no sentido de compromisso/tarefa maior do que a pessoa consegue lidar."),
                vocab("to stand tall", "expressão verbal", "manter-se firme e digno",
                      "They lost the vote but stood tall.",
                      "Eles perderam a votação, mas se mantiveram firmes e dignos.",
                      "Não é sobre altura física — é sobre dignidade mesmo perdendo ou passando por dificuldade."),
                vocab("naught", "substantivo (arcaico/poético)", "nada",
                      "All that effort came to naught.",
                      "Todo aquele esforço não deu em nada.",
                      "Forma antiga de \"nothing\" — hoje só aparece em contextos formais, poéticos ou em frases fixas como \"came to naught\". Não use em conversa comum."),
                vocab("to kneel", "verbo", "ajoelhar-se; submeter-se",
                      "He refused to kneel to the king.",
                      "Ele se recusou a se ajoelhar diante do rei.",
                      "Verbo irregular: kneel–knelt–knelt (ou kneeled, também aceito). Sentido literal e figurado (submeter-se)."),
            ],
            "checkpoint_apos": {"gate_id": "ck4", "tipo": "mc",
                "testar": "O que significa \"to bite off more than you can chew\"?"},
        },
        # Assunto 6 — exemption vs exception (Groq, ótimo) + honestidade
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "Duas palavras parecidas: exemption vs. exception",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "Nota de honestidade: a linha da 3ª estrofe aparece em versões diferentes da "
                    "música como \"without exemption\" e \"without exception\" — vale a pena "
                    "aprender as duas, já que são bem parecidas mas não são sinônimos."
                )},
                vocab("exemption", "substantivo", "dispensa, isenção",
                      "Students with a medical condition may apply for an exemption from the physical education requirement.",
                      "Estudantes com condição médica podem solicitar uma dispensa da exigência de educação física.",
                      "\"Exemption\" é ser liberado de algo que normalmente seria obrigatório (ex.: isenção de imposto)."),
                vocab("exception", "substantivo", "exceção",
                      "Everyone came, without exception.",
                      "Todo mundo veio, sem exceção.",
                      "\"Exception\" é algo que foge da regra geral — a regra continua existindo pros outros, só aquele caso é diferente."),
                {"tipo": "box", "variante": "summary", "label": "Resumo da distinção",
                 "texto": "\"Exemption\" = permissão pra NÃO seguir uma regra. \"Exception\" = um caso que a regra simplesmente não cobre. Não são intercambiáveis."},
            ],
            "checkpoint_apos": None,
        },
        # Assunto 7 — fecho: golpes e legado (novas)
        {
            "tipo": "conteudo", "secao": "Vocabulário & Expressões",
            "titulo_secao": "Fecho: os golpes e o que fica registrado",
            "blocos": [
                {"tipo": "paragrafo", "texto": (
                    "No fecho, a música fala de levar os golpes da vida — e de deixar registrado "
                    "que isso foi feito do seu próprio jeito."
                )},
                vocab("the blows", "substantivo (plural)", "os golpes, os baques",
                      "Life's hard blows taught her resilience.",
                      "Os golpes duros da vida ensinaram resiliência a ela.",
                      "Sempre no plural nesse sentido figurado (dificuldades da vida); \"a blow\" no singular também existe (um golpe específico)."),
                vocab("let the record show", "expressão formal", "que fique registrado",
                      "Let the record show that I disagreed with this decision.",
                      "Que fique registrado que eu discordei dessa decisão.",
                      "Expressão fixa e formal (usada em atas, tribunais) — não muda a ordem das palavras nem o \"the\"."),
                {"tipo": "audio_video", "midia_tipo": "audio", "legenda": "Pronúncia de \"let the record show\"",
                 "descricao": "Áudio curto com a pronúncia da expressão \"let the record show\", destacando o linking entre as palavras."},
            ],
            "checkpoint_apos": {"gate_id": "ck5", "tipo": "lacuna",
                "testar": "Complete: 'Let the record ___ that I tried my best.'"},
        },
    ]

    avaliacao_conceitos = [
        {"gate_id": "ef1", "tipo": "mc", "testar": "Qual expressão significa \"o fim definitivo\"?"},
        {"gate_id": "ef2", "tipo": "tf", "testar": "\"Exemption\" e \"exception\" são sinônimos intercambiáveis em qualquer contexto."},
        {"gate_id": "ef3", "tipo": "classify", "testar": "Classifique cada expressão como relacionada a 'planejamento' ou a 'persistência diante de dificuldade': to chart a course, to see it through, to bite off more than you can chew, to stand tall."},
        {"gate_id": "ef4", "tipo": "open", "testar": "Escolha 2 expressões desta aula e escreva uma frase sua com cada uma, ligando ao sentido da música (sem citar a letra)."},
        {"gate_id": "ef5", "tipo": "mc", "testar": "\"Let the record show\" é uma expressão de registro: (a) informal, usada entre amigos (b) formal, usada em atas/registros oficiais (c) só usada em música (d) arcaica, não usada hoje"},
    ]

    return {
        "topico_id": "ingles-modulo1-aula1-topico1-vocabulario",
        "titulo": "Vocabulário & Expressões — My Way",
        "aula": 1,
        "numero": 1,
        "duracao_estimada_min": 16,
        "roteiro": [
            "A estrutura da letra em 6 movimentos",
            "Abertura: o fim e a certeza",
            "Afirmação e arrependimentos",
            "Planejamento e caminhos",
            "A ponte: tropeços e firmeza",
            "Exemption vs. exception",
            "Fecho: os golpes e o legado",
        ],
        "slides": slides,
        "avaliacao_conceitos": avaliacao_conceitos,
    }


async def main():
    conteudo = montar_conteudo()
    n_assuntos = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo")
    n_checkpoints = sum(1 for s in conteudo["slides"] if s.get("checkpoint_apos"))
    n_vocab = sum(1 for s in conteudo["slides"] if s["tipo"] == "conteudo" for b in s["blocos"] if b["tipo"] == "vocab")
    print(f"{n_assuntos} assuntos, {n_checkpoints} checkpoints, {n_vocab} blocos vocab (esperado 17)")

    quiz_agent = QuizAgent(GroqService())
    perguntas = await quiz_agent.generate_perguntas(conteudo)
    print("Checkpoints gerados:", list(perguntas.get("checkpoints", {}).keys()))
    print("Avaliação gerada:", list(perguntas.get("avaliacao", {}).keys()))

    topico_final = montar_topico(conteudo, perguntas, proximo_topico_label="Gramática em foco")

    saida = Path("/app/_topico1_ingles_vocab_final.json")
    saida.write_text(json.dumps(topico_final, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Salvo em {saida}")


if __name__ == "__main__":
    asyncio.run(main())
