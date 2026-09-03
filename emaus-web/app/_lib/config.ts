// Config do Emaús. Front puro cliente da API do NIA.

// Escopo de catálogo — cursos da frente de teologia. Hardcoded até existir Tenant no NIA.
export const TEOLOGIA_COURSE_IDS = [8] as const;

// Tema do render de slides do backend (GET /topicos/{id}/render?theme=...).
export const THEME_TOPICO = "trigo-maduro";

// Sem login ainda: um usuário fixo no NIA identifica o progresso.
// Trocar por sessão real numa fase futura sem refazer o resto.
export const ALUNO_USER_ID = 1;

// Server Components rodam no servidor (dentro de container, se houver) — usam
// API_URL_INTERNAL. Browser usa a URL pública.
export const API_URL =
  typeof window === "undefined"
    ? process.env.API_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100"
    : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100";

// SEMPRE a URL pública: usada em src de <iframe> que o navegador carrega.
export const API_URL_PUBLICA = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100";
