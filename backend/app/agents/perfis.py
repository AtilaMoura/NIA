# backend/app/agents/perfis.py
"""
Perfis de domínio — parametrizam o que antes estava fixo direto na string do
prompt de ContentAgent/ReviewerAgent/TutorAgent (curso "LLM aplicado a um
agente de vendas via WhatsApp para um Garden Center", fio condutor de
LLM/tools/grounding). Sem isso, os três agentes geravam conteúdo da área de IA
não importa o assunto pedido — achado real ao tentar preparar um curso de
teologia (sessão de 2026-08-22).

Isto é a versão MVP do "domain_profile" que a tabela `Tenant` vai carregar
quando o schema multi-tenant existir (ver anotação de memória do projeto) —
por enquanto são só constantes Python, sem tabela nova no banco.
"""

from dataclasses import dataclass

from .specialists.shared import FIO_CONDUTOR_IA, EXEMPLO_DE_PROFUNDIDADE


@dataclass(frozen=True)
class PerfilDominio:
    id: str
    contexto_curso: str       # como o agente se apresenta: "...pro {contexto_curso}"
    fio_condutor: str         # regra pedagógica obrigatória, nunca pode ser contradita
    exemplo_calibracao: str   # exemplo real de bloco já publicado, calibra nível de detalhe (pode ser "")
    exemplo_diagrama: str = ""  # exemplo de bloco "diagrama" (fluxo com setas) calibrado pro domínio —
    # achado gerando o curso de obreiro (2026-08-25): o exemplo genérico embutido no
    # ContentAgent ("cliente pergunta X → sistema decide Y → resultado Z") é de domínio
    # técnico e viesou o modelo a escrever diagramas descritivos sem seta/conector em
    # temas teológicos abstratos (ex: "discernimento"), reprovando 2x seguidas no
    # Reviewer estrutural (validate.py exige ≥2 setas ou ≥2 palavras conectoras).


PERFIL_TECH = PerfilDominio(
    id="tech",
    contexto_curso=(
        'curso "LLM aplicado a um agente de vendas via WhatsApp para um Garden Center" '
        "(loja de plantas fictícia)"
    ),
    fio_condutor=FIO_CONDUTOR_IA,
    exemplo_calibracao=EXEMPLO_DE_PROFUNDIDADE,
)


FIO_CONDUTOR_TEOLOGIA = """
Fio condutor pedagógico obrigatório desta área (nunca contradizer):
O texto bíblico é sempre a fonte central e final — comentário de estudioso, contexto
histórico ou aplicação prática são material de APOIO, nunca equiparados à autoridade do
texto em si. Sem viés denominacional: não apresente como certo/consensual um ponto
disputado entre tradições cristãs (ex: dons espirituais, escatologia, modo de batismo) —
se o tema tocar nisso, deixe explícito que é uma questão interpretativa, não um fato
assentado. Deixe sempre claro quando algo é leitura/interpretação humana (mesmo citando
estudiosos) e quando é o texto bíblico propriamente dito — nunca apresentar os dois com
o mesmo peso.

REGRA DE CITAÇÃO (igual em espírito ao "fatos vêm de tools, nunca de memória" da área
de IA — aqui a fonte de verdade é o texto fornecido, não a sua memória):
- Se um TEXTO BÍBLICO DE REFERÊNCIA for fornecido nesta chamada: toda citação entre
  aspas apresentada como literal TEM que vir exatamente desse texto fornecido — não
  complete, corrija ou invente uma palavra sequer de memória.
- Se NENHUM texto de referência for fornecido: é PROIBIDO colocar qualquer coisa entre
  aspas como se fosse citação literal do texto bíblico (você não tem certeza da palavra
  exata). Em vez disso, descreva/parafraseie o conteúdo do versículo em prosa normal
  (sem aspas de citação) e cite a referência exata (livro capítulo:versículo) pra quem
  quiser conferir o texto original.
""".strip()

EXEMPLO_CALIBRACAO_TEOLOGIA = """
Exemplo real do nível de detalhe esperado num bloco "box" de exposição textual — repare
que cita a referência exata e distingue o que o texto diz do que é leitura/aplicação:

{
  "tipo": "box", "variante": "def", "label": "📖 O texto",
  "texto": "Em Filipenses 1:21, Paulo escreve: 'Porque para mim o viver é Cristo, e o
  morrer é lucro' (Fp 1:21). No grego, 'viver' (zên) e 'Cristo' aparecem lado a lado de
  forma incomum — a construção sugere que a própria identidade de Paulo está fundida à
  pessoa de Cristo, não apenas sua atividade religiosa. É esse ponto específico, e não
  uma leitura genérica de 'devoção a Deus', que o restante do versículo (o contraste com
  'morrer é lucro') desenvolve."
}

PROIBIDO: parafrasear o versículo como se fosse a citação literal, ou fazer uma aplicação
("isso significa que você deveria...") sem antes deixar claro que aquilo é leitura, não
o texto em si.
""".strip()

EXEMPLO_DIAGRAMA_TEOLOGIA = (
    'Exemplo de "descricao" de diagrama bem formada pra esta área: "Convicção do '
    "pecado → arrependimento (2Co 7:10) → confissão (1Jo 1:9) → decide: há alguém a "
    'reparar? → se sim, busca reconciliação (Mt 5:23-24) → restauração".'
)

PERFIL_TEOLOGIA = PerfilDominio(
    id="teologia",
    contexto_curso="curso de estudo bíblico sobre a Carta de Paulo aos Filipenses",
    fio_condutor=FIO_CONDUTOR_TEOLOGIA,
    exemplo_calibracao=EXEMPLO_CALIBRACAO_TEOLOGIA,
    exemplo_diagrama=EXEMPLO_DIAGRAMA_TEOLOGIA,
)


PERFIL_OBREIRO = PerfilDominio(
    id="obreiro",
    contexto_curso="curso de Formação Geral do Novo Obreiro Cristão",
    fio_condutor=FIO_CONDUTOR_TEOLOGIA,
    exemplo_calibracao=EXEMPLO_CALIBRACAO_TEOLOGIA,
    exemplo_diagrama=EXEMPLO_DIAGRAMA_TEOLOGIA,
)


FIO_CONDUTOR_INGLES = """
Fio condutor pedagógico obrigatório desta área (nunca contradizer):
Isto é uma aula de inglês pra um brasileiro adulto em estudo pessoal (nível calibrado por
diagnóstico, entre A1 e B2 — assuma o nível informado no pedido, nunca invente um nível
diferente). Regras inegociáveis:
- NUNCA inventar palavra, expressão idiomática ou exemplo de frase em inglês que não seja
  uso real e comprovado da língua — isso é o equivalente, aqui, de "nunca citar fato de
  memória" na área de teologia/tech. Na dúvida sobre se uma expressão é natural, prefira
  uma mais simples e comprovadamente comum a arriscar uma invenção.
- Todo vocabulário ou estrutura nova PRECISA vir acompanhado de pelo menos 1 frase de
  exemplo completa e natural, usando a palavra em contexto real — nunca só a tradução
  isolada.
- Ser sempre explícito sobre QUAL tempo verbal ou estrutura gramatical está sendo
  ensinado (ex: "present perfect", não só "isso é usado quando..."), nomeando o padrão.
- Quando fizer sentido pedagógico, contrastar com armadilhas comuns de quem fala
  português (falsos cognatos, ordem de palavras, preposições que não têm equivalente
  direto) — isso ajuda mais que só explicar a regra em inglês isolada.
- Nunca reproduzir letra de música, trecho de vídeo com direitos autorais ou texto longo
  protegido por copyright como se fosse citação literal — parafrasear o sentido, comentar
  vocabulário/gramática em cima dele, e indicar a fonte original pra quem quiser conferir
  (mesmo espírito da regra de citação bíblica: nunca "completar de memória").
- Pra palavra/expressão nova, use o bloco "vocab" (campos: termo, classe_gramatical,
  traducao, exemplo_en, exemplo_pt, cuidado opcional) — NÃO o bloco "box" genérico. O
  "box" vira parede de texto (achado real, 2026-09-04: várias palavras espremidas no
  mesmo "texto" saem ilegíveis); "vocab" é um card estruturado, um por palavra.
- Pra fluxo/processo (ex.: passos de como algo aconteceu), use o bloco "fluxo" (campos:
  passos: [{texto, decisao: bool}]) — NÃO peça um "diagrama" com svg_raw pra isso: SVG
  cru escrito por IA sai com coordenadas erradas e texto vazando das caixas (achado real
  testando este curso). "fluxo" desenha em HTML/CSS e nunca quebra.
""".strip()

EXEMPLO_CALIBRACAO_INGLES = """
Exemplo real do nível de detalhe esperado pra uma palavra nova — bloco "vocab", não
"box" (o "box" genérico é só pra explicação em prosa, nunca pra vocabulário):

{
  "tipo": "vocab", "termo": "certain", "classe_gramatical": "adjetivo",
  "traducao": "seguro, convicto de algo",
  "exemplo_en": "I am certain that this will work.",
  "exemplo_pt": "Tenho certeza de que isso vai funcionar.",
  "cuidado": "Em português dizemos 'estou certo' com o verbo 'estar', mas em inglês
  'certain' também vem depois de 'be' — o que muda é que 'sure' é intercambiável aqui
  ('I am sure' = 'I am certain'), mas 'right' NÃO é ('estou certo' no sentido de 'não
  errei' é 'I am right', não 'I am certain')."
}

PROIBIDO: dar só a tradução ("certain = certo") sem exemplo, ou inventar uma frase que
soe não-natural em inglês só pra caber no exemplo. PROIBIDO também amontoar 2+ palavras
num "box" só de texto corrido — cada palavra nova é o seu próprio bloco "vocab".
""".strip()

PERFIL_INGLES = PerfilDominio(
    id="ingles",
    contexto_curso=(
        "curso pessoal de inglês (estudo próprio, nível calibrado por diagnóstico entre "
        "A1 e B2)"
    ),
    fio_condutor=FIO_CONDUTOR_INGLES,
    exemplo_calibracao=EXEMPLO_CALIBRACAO_INGLES,
)


PERFIS: dict[str, PerfilDominio] = {
    PERFIL_TECH.id: PERFIL_TECH,
    PERFIL_TEOLOGIA.id: PERFIL_TEOLOGIA,
    PERFIL_OBREIRO.id: PERFIL_OBREIRO,
    PERFIL_INGLES.id: PERFIL_INGLES,
}


def resolver_perfil(perfil_id: str) -> PerfilDominio:
    return PERFIS.get(perfil_id, PERFIL_TECH)
