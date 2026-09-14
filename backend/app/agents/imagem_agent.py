# backend/app/agents/imagem_agent.py
"""
ImagemAgent (2026-09-11) — não gera imagem nenhuma (isso continua sendo o
scripts/gerar_imagem_gemini.py, via browser automation no Gemini web, de
propósito — não trocar por API tipo gpt-image-1/DALL-E, decisão do usuário).
Este agente escreve os PROMPTS: uma identidade visual reutilizável por curso
(pra toda imagem do curso parecer da mesma "família"), e um prompt completo e
específico por peça (capa do curso, capa de cada módulo, imagem de tópico).

Antes disso, cada imagem gerada manualmente reusava o mesmo PROMPT_PADRAO
genérico do script (voluntários de igreja, sempre a mesma composição/estilo)
— funciona como placeholder mas sai repetitivo e sem a qualidade de produção
de referências como um pôster de curso de verdade (fotografia/ilustração
realista, cores vivas, composição variada por peça).
"""

import json

from .base_agent import BaseAgent
from .perfis import PerfilDominio, PERFIL_TECH

SCHEMA_IDENTIDADE_VISUAL = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{
  "estilo": "descrição objetiva da técnica visual (ex: 'fotografia editorial realista' ou
    'ilustração digital aquarela')",
  "paleta_cores": ["#hex", "#hex", "#hex"],
  "iluminacao_mood": "1 frase sobre luz e atmosfera (ex: 'luz dourada de fim de tarde,
    quente e acolhedora')",
  "elementos_recorrentes": ["objeto/cenário/motivo que pode aparecer em mais de uma peça
    do curso, pra dar unidade — 2 a 4 itens"],
  "evitar": ["o que NUNCA deve aparecer nas imagens deste curso — 2 a 4 itens, específico,
    não genérico"]
}

REGRAS:
- Realista, vivo, moderno: nunca genérico/corporativo de banco de imagem, nunca com cara
  óbvia de gerado por IA (mãos estranhas, texto ilegível, simetria artificial demais).
- A paleta tem que ser 3 cores hex reais, escolhidas pelo tema do curso (não um default
  cinza/azul corporativo).
- "evitar" tem que ser específico do risco real deste curso/domínio, não uma lista
  genérica copiada de outro contexto.
- CRÍTICO em "estilo": tem que ser uma descrição TÉCNICA E AUTOCONTIDA da técnica visual —
  meio (fotografia/aquarela/vetor/etc.), tratamento de linha, forma de aplicar cor/luz,
  textura, nível de detalhe. NUNCA vale citar uma referência que o gerador de imagem não
  consegue ver (ex: "igual ao curso X", "mesmo estilo do material Y") — quem lê esse texto
  depois é a IA que gera a imagem, ela não tem acesso a nenhum material do NIA nem sabe o
  que "curso X" significa. Se o pedido de quem chamou mencionar um material de referência,
  sua tarefa é DESCREVER em detalhe o que esse material mostra visualmente (técnica, traço,
  paleta, textura, tratamento de luz) e escrever isso por extenso em "estilo" — nunca só
  citar o nome do material.
""".strip()

SCHEMA_PROMPT_CAPA = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{ "descricao": "o prompt completo, pronto pra mandar pro gerador de imagem" }

Isto é uma CAPA — pôster do curso ou de um módulo, não uma cena solta dentro do conteúdo.
Diferente das imagens de tópico (que NUNCA têm texto), a capa TEM que ter o título escrito
nela, como pôster de verdade. O prompt em "descricao" TEM que:
- Pedir explicitamente ILUSTRAÇÃO (não fotografia) de alta qualidade de produção:
  detalhada, cores vivas e ricas, composição intencional, nível de agência de design,
  NUNCA com cara infantil/simplista/clipart nem estilo "desenho animado" raso. Se o campo
  "estilo" da identidade visual já descrever uma técnica de ilustração específica (ex:
  aquarela, traço a nanquim), USE essa descrição inteira e detalhada — não troque por um
  genérico "digital illustration". Só ignore "estilo" se ele descrever fotografia.
- Descrever EXATAMENTE o texto que deve aparecer na peça, entre aspas, pedindo tipografia
  grande, legível e bem posicionada (ex: 'bold display typography reading "TÍTULO EXATO"
  prominently placed in the upper third') — nunca deixe a IA inventar outro texto.
- Descrever uma cena/composição concreta ao redor do título (não só um fundo liso) —
  elementos do curso, cenário, objetos simbólicos — coerente com a identidade visual.
- Terminar com uma lista curta do que NÃO incluir (herdado de "evitar" da identidade
  visual + clichê infantil, tipografia ilegível, watermark).
- Ter entre 60 e 130 palavras, em inglês (é o que o gerador de imagem entende melhor).
- OBRIGATÓRIO: pedir explicitamente orientação PAISAGEM/horizontal, formato widescreen
  16:9 (ex: "landscape orientation, 16:9 widescreen, wider than tall") — capa nunca pode
  sair em retrato/vertical (achado real: o gerador às vezes ignora e devolve retrato se
  isso não for dito explicitamente no prompt).
""".strip()

SCHEMA_PROMPT_IMAGEM = """
Devolva APENAS um JSON válido (sem markdown), neste formato:

{ "descricao": "o prompt completo, pronto pra mandar pro gerador de imagem" }

O prompt em "descricao" TEM que:
- Ser uma cena concreta e específica pro que foi pedido (nunca "uma imagem sobre X" —
  descreva pessoas/objetos/cenário/ação reais, como se fosse briefing pra um fotógrafo ou
  ilustrador de verdade).
- Incorporar a identidade visual do curso: use o MESMO meio/técnica descrito em "estilo"
  (nunca troque fotografia por ilustração ou vice-versa por conta própria), mesma paleta e
  mood — cite as cores hex e o estilo explicitamente no texto do prompt.
- Pedir explicitamente qualidade de produção alta nesse meio (se for foto: realista, vivo,
  profundidade de campo; se for ilustração: traço/pintura detalhada, cores vivas, nunca
  clipart raso), composição intencional (regra dos terços) — NUNCA composição genérica de
  banco de imagens nem visual óbvio de IA malfeito.
- Ser DIFERENTE em composição/ângulo/cenário das outras peças do mesmo curso (varie:
  plano aberto vs. close, pessoas vs. objeto/cenário só, ângulos diferentes) — nunca
  repetir a mesma pose/enquadramento em toda imagem do curso.
- Terminar com uma lista curta do que NÃO incluir (herdada de "evitar" da identidade
  visual + qualquer coisa específica que atrapalharia esta peça, ex: texto/logo/marca
  d'água, quando a peça é uma foto de cena e não um pôster com tipografia).
- Ter entre 60 e 130 palavras, em inglês (é o que o gerador de imagem entende melhor).
- OBRIGATÓRIO: pedir explicitamente orientação PAISAGEM/horizontal, formato widescreen
  16:9 (ex: "landscape orientation, 16:9 widescreen, wider than tall") — todas as imagens
  do curso têm que sair no mesmo formato, nunca retrato/vertical (achado real: o gerador
  às vezes ignora e devolve retrato se isso não for dito explicitamente no prompt).
""".strip()


class ImagemAgent(BaseAgent):
    """Escreve identidade visual + prompts de imagem — nunca gera a imagem em si."""

    async def gerar_identidade_visual(
        self,
        curso_titulo: str,
        curso_descricao: str,
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> dict:
        prompt = f"""
Você é o diretor de arte responsável pela identidade visual do {perfil.contexto_curso}.
Esta identidade será reutilizada em TODAS as imagens do curso (capa do curso, capa de
cada módulo, imagens de tópico) — pra tudo parecer produzido pela mesma equipe, não um
grab-bag de estilos.

CURSO: {curso_titulo}
DESCRIÇÃO: {curso_descricao or "(sem descrição adicional)"}

Referência de qualidade esperada (não copie o tema, copie o NÍVEL de produção): pôsteres
de curso profissionais têm fotografia/ilustração realista e vívida, paleta de cor
intencional, tipografia e composição de nível editorial — não a estética
"documentário genérico" ou "clipart corporativo".

{SCHEMA_IDENTIDADE_VISUAL}
"""
        return await self.run_json_com_retry(prompt, max_tokens=2500)

    async def gerar_prompt_imagem(
        self,
        identidade_visual: dict,
        contexto: str,
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> str:
        """`contexto` = o que esta peça específica precisa mostrar (ex: "Capa do curso
        'Formação do Novo Obreiro'" ou a descrição curta que o ContentAgent já sugeriu
        pra um bloco 'imagem_sugerida' de um tópico)."""
        prompt = f"""
Você escreve prompts de geração de imagem pro {perfil.contexto_curso}.

IDENTIDADE VISUAL DO CURSO (toda imagem tem que seguir isso):
{json.dumps(identidade_visual, ensure_ascii=False, indent=2)}

O QUE ESTA IMAGEM ESPECÍFICA PRECISA MOSTRAR:
{contexto}

{SCHEMA_PROMPT_IMAGEM}
"""
        resultado = await self.run_json_com_retry(prompt, max_tokens=1600)
        return resultado["descricao"]

    async def gerar_prompt_capa(
        self,
        identidade_visual: dict,
        titulo: str,
        subtitulo: str = "",
        perfil: PerfilDominio = PERFIL_TECH,
    ) -> str:
        """Capa (curso ou módulo) — ilustração com o título escrito na peça, tipo
        pôster de verdade. Diferente de gerar_prompt_imagem (que é pra cena sem
        texto nenhum dentro do conteúdo)."""
        prompt = f"""
Você escreve prompts de geração de imagem pro {perfil.contexto_curso}.

IDENTIDADE VISUAL DO CURSO (paleta de cores tem que seguir isso; estilo/meio é sempre
ilustração pra capa, mesmo que a identidade abaixo fale de fotografia):
{json.dumps(identidade_visual, ensure_ascii=False, indent=2)}

TEXTO EXATO QUE PRECISA APARECER NA CAPA:
Título: "{titulo}"
{f'Subtítulo: "{subtitulo}"' if subtitulo else ""}

{SCHEMA_PROMPT_CAPA}
"""
        resultado = await self.run_json_com_retry(prompt, max_tokens=1600)
        return resultado["descricao"]
