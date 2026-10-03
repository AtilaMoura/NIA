// Config do Emaús. Front puro cliente da API do NIA.

// Escopo de catálogo — cursos navegáveis no Emaús hoje. Hardcoded até existir
// Tenant no NIA. Nome ficou de teologia (curso 8), mas os cursos 9 (Inglês), 5
// (Engenharia de Agentes LLM) e 11 (Redes e Câmeras) são estudos PESSOAIS do
// Atila, incluídos aqui provisoriamente — sem Tenant/liberação por perfil
// ainda, não dá pra isolar catálogo por audiência de verdade. Quando a regra
// de liberação por perfil existir, os estudos pessoais saem daqui e viram
// "pessoal", não catálogo público. Ver PLANO_CURSO_IA_EMAUS.md.
// Curso 12 = parte II do curso de obreiro (8 virou a parte I em 2026-09-22).
export const TEOLOGIA_COURSE_IDS = [8, 12, 9, 5, 11] as const;

// Tema do render de slides do backend (GET /topicos/{id}/render?theme=...).
// Default do sistema; cursos com identidade visual própria entram no mapa abaixo
// (mesmo padrão do `_PERFIL_POR_CURSO` no backend).
export const THEME_TOPICO = "trigo-maduro";
// Escolhido no catálogo visual (docs/estilos/, 2026-10-01) — cursos 8/12 seguem no default.
export const TEMA_POR_CURSO: Record<number, string> = {
  9: "caderno-escolar", // Inglês (antes: papel-latao)
  5: "azul-petroleo", // Engenharia de Agentes LLM (catálogo 2026-10-03; antes vinho-ouro, vidro-fume)
  11: "alto-contraste", // Redes e Câmeras (antes: default trigo-maduro)
};

// FASE 1 (auth) trocou isto pela sessão de verdade (`_lib/sessao.ts`, getSessao().id) em
// toda página. Só sobrevive como fallback default de `montarArvore` — não importar direto.
export const ALUNO_USER_ID = 1;

// Server Components rodam no servidor (dentro de container, se houver) — usam
// API_URL_INTERNAL. Browser usa a URL pública.
export const API_URL =
  typeof window === "undefined"
    ? process.env.API_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100"
    : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100";

// SEMPRE a URL pública: usada em src de <iframe> que o navegador carrega.
export const API_URL_PUBLICA = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100";
