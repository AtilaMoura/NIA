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


PERFIS: dict[str, PerfilDominio] = {
    PERFIL_TECH.id: PERFIL_TECH,
    PERFIL_TEOLOGIA.id: PERFIL_TEOLOGIA,
    PERFIL_OBREIRO.id: PERFIL_OBREIRO,
}


def resolver_perfil(perfil_id: str) -> PerfilDominio:
    return PERFIS.get(perfil_id, PERFIL_TECH)
