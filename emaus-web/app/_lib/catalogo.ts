// Catálogo do Emaús. Hardcoded aqui (não no banco do NIA, que é compartilhado com
// o front de tecnologia). Quando um curso "em breve" sair do papel, ele vira um
// curso real no NIA e o card passa a apontar pro /curso/{id}.

export type TomCurso = "trigo" | "oliveira" | "vinho" | "indigo" | "terracota" | "pedra" | "latao";

export type CursoCatalogo = {
  slug: string;
  titulo: string;
  subtitulo: string;
  descricao: string;
  tom: TomCurso;
  /** courseId real no NIA — só quando `disponivel` */
  courseId?: number;
  disponivel: boolean;
};

// Degradê de fundo da capa quando ainda não há imagem (e véu sobre a foto quando há).
export const GRADIENTE_TOM: Record<TomCurso, string> = {
  trigo: "linear-gradient(135deg, #8a5a2b 0%, #d9a441 100%)",
  oliveira: "linear-gradient(135deg, #3f4a24 0%, #7d8a4a 100%)",
  vinho: "linear-gradient(135deg, #5c1f28 0%, #a3505c 100%)",
  indigo: "linear-gradient(135deg, #2c3350 0%, #5b6a97 100%)",
  terracota: "linear-gradient(135deg, #7a3520 0%, #c9743f 100%)",
  pedra: "linear-gradient(135deg, #4a423a 0%, #8f8377 100%)",
  latao: "linear-gradient(135deg, #6b551f 0%, #c9973f 100%)",
};

export const CATALOGO: CursoCatalogo[] = [
  {
    slug: "ingles",
    titulo: "Inglês",
    subtitulo: "Estudo pessoal, do zero à prática com prompts e tecnologia",
    descricao:
      "Ciclos de 30 dias combinando música, vídeos de conversação e inglês para ler e escrever prompts técnicos — conteúdo gerado e revisado tópico a tópico.",
    tom: "latao",
    courseId: 9,
    disponivel: true,
  },
  {
    slug: "engenharia-agentes-llm",
    titulo: "Engenharia de Agentes LLM",
    subtitulo: "Estudo pessoal — do token ao agente de produção",
    descricao:
      "Como um LLM funciona por dentro (tokens, Transformers, embeddings, attention) até a arquitetura completa de um agente de vendas via WhatsApp para um Garden Center: Context Engineering, RAG, memória, tools, orchestrator, avaliação e sistemas multi-agente. Trabalhado tópico a tópico.",
    tom: "pedra",
    courseId: 5,
    disponivel: true,
  },
  {
    slug: "formacao-novo-obreiro",
    titulo: "Formação Geral do Novo Obreiro Cristão",
    subtitulo: "O primeiro passo de quem começa a servir na igreja",
    descricao:
      "Fundamento bíblico, doutrina básica, caráter e ética, disciplinas espirituais e as áreas práticas de serviço na igreja.",
    tom: "trigo",
    courseId: 8,
    disponivel: true,
  },
  {
    slug: "panorama-da-biblia",
    titulo: "Panorama da Bíblia",
    subtitulo: "A história que une os 66 livros",
    descricao:
      "Uma visão de conjunto das Escrituras — criação, queda, redenção e restauração — para nunca mais se perder entre um livro e outro.",
    tom: "indigo",
    disponivel: false,
  },
  {
    slug: "como-estudar-a-biblia",
    titulo: "Como Estudar a Bíblia",
    subtitulo: "Ferramentas para ler com cuidado",
    descricao:
      "Contexto, gênero literário e a regra de ouro da interpretação: aprender a ouvir o texto antes de aplicá-lo.",
    tom: "oliveira",
    disponivel: false,
  },
  {
    slug: "evangelho-de-joao",
    titulo: "O Evangelho de João",
    subtitulo: "“Para que creiais”",
    descricao:
      "Um estudo capítulo a capítulo do Evangelho que mais se demora em quem Jesus é e no que significa crer nele.",
    tom: "vinho",
    disponivel: false,
  },
  {
    slug: "romanos",
    titulo: "Romanos",
    subtitulo: "O coração do evangelho, carta a carta",
    descricao:
      "Pecado, graça, fé, justificação e vida no Espírito — a exposição mais completa do evangelho no Novo Testamento.",
    tom: "terracota",
    disponivel: false,
  },
  {
    slug: "antigo-testamento-panorama",
    titulo: "O Antigo Testamento em Panorama",
    subtitulo: "Da criação ao exílio",
    descricao:
      "Lei, história, poesia e profetas: como as promessas de Deus atravessam séculos e apontam para Cristo.",
    tom: "pedra",
    disponivel: false,
  },
  {
    slug: "vida-de-oracao",
    titulo: "Vida de Oração",
    subtitulo: "Aprendendo a falar com Deus",
    descricao:
      "Oração pessoal, intercessão e o Pai Nosso como modelo — construir um hábito que sustenta a caminhada.",
    tom: "oliveira",
    disponivel: false,
  },
  {
    slug: "doutrinas-essenciais",
    titulo: "Doutrinas Essenciais da Fé Cristã",
    subtitulo: "O que todo cristão precisa entender",
    descricao:
      "Autoridade da Bíblia, a Trindade, a obra de Cristo, salvação pela graça e a igreja — sem jargão, com base no texto.",
    tom: "indigo",
    disponivel: false,
  },
  {
    slug: "discipulado-primeiros-passos",
    titulo: "Discipulado — Os Primeiros Passos",
    subtitulo: "Para quem acabou de crer",
    descricao:
      "Batismo, comunhão, leitura da Bíblia e as primeiras decisões de uma vida seguindo Jesus.",
    tom: "trigo",
    disponivel: false,
  },
  {
    slug: "salmos",
    titulo: "Salmos",
    subtitulo: "Orações para toda emoção",
    descricao:
      "Alegria, medo, arrependimento, gratidão e lamento: aprender a orar com as palavras que Deus mesmo inspirou.",
    tom: "vinho",
    disponivel: false,
  },
  {
    slug: "carater-cristao",
    titulo: "Caráter Cristão",
    subtitulo: "Ética e integridade no dia a dia",
    descricao:
      "Verdade, respeito, justiça e pureza — coerência entre a vida pública e a privada, no trabalho e em casa.",
    tom: "terracota",
    disponivel: false,
  },
  {
    slug: "missoes-e-evangelismo",
    titulo: "Missões e Evangelismo",
    subtitulo: "A igreja enviada",
    descricao:
      "A Grande Comissão, o testemunho pessoal e como compartilhar o evangelho no cotidiano, sem fórmula pronta.",
    tom: "pedra",
    disponivel: false,
  },
];

/** Slug → caminho da capa em /public, se o arquivo existir (checagem em runtime no server). */
export function caminhoCapa(slug: string): string {
  return `/capas/${slug}.jpg`;
}
