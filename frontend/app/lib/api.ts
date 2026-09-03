// Cliente de API mínimo pra Fase 3 (fluxo aluno) — só os endpoints usados aqui.
// Cliente completo/tipado pra todo o backend fica pra Fase 0.

// Achado em 2026-08-22: os Server Components (page.tsx sem "use client") rodam
// DENTRO do container do frontend, onde "localhost" aponta pro próprio container,
// não pro backend — precisam do hostname da rede Docker (API_URL_INTERNAL). Só o
// código client-side (componentes "use client", roda no navegador do usuário)
// deve usar NEXT_PUBLIC_API_URL (porta mapeada no host).
const API_URL =
  typeof window === "undefined"
    ? process.env.API_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
    : process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Course = {
  id: number;
  title: string;
  description: string | null;
  level: string;
  status: string;
  modules_count: number;
  duration_hours: number;
  ai_quality_score: number | null;
};

export type Module = {
  id: number;
  course_id: number;
  module_index: number;
  title: string;
  description: string | null;
  lessons_count: number;
};

export type Lesson = {
  id: number;
  module_id: number;
  lesson_index: number;
  title: string;
  content: string | null;
  is_approved: boolean;
  estimated_read_time_minutes: number | null;
};

export type TutorHistoricoItem = {
  lesson_id: number;
  veredito: string;
  resumo_diagnostico: string;
};

export type Progress = {
  id: number;
  user_id: number;
  course_id: number;
  module_id: number;
  status: string;
  current_lesson_index: number;
  can_advance: boolean;
  tutor_analysis: { historico?: TutorHistoricoItem[] } | null;
};

export type AvaliarResumoResponse = {
  lesson_id: number;
  avaliacao: {
    veredito: string;
    resumo_diagnostico?: string;
    [key: string]: unknown;
  };
  can_advance: boolean;
};

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Erro ${res.status} em ${path}: ${await res.text()}`);
  }
  return res.json();
}

export type UserPrefs = {
  id: number;
  name: string | null;
  preferred_mood: string;
  preferred_panel_mode: "light" | "dark";
  preferred_panel_layout: "retomar" | "biblioteca" | "trilha";
  level: number | null;
  total_points: number | null;
  streak_days: number | null;
  preferred_topics: string[] | null;
  badges: string[] | null;
};

export function getUser(id: number) {
  return fetchJson<UserPrefs>(`/users/${id}`);
}

export function updateUser(id: number, data: Partial<Pick<UserPrefs, "preferred_mood" | "preferred_panel_mode" | "preferred_panel_layout">>) {
  return fetchJson<UserPrefs>(`/users/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export function listCourses() {
  return fetchJson<Course[]>("/courses/");
}

export function getCourse(id: number) {
  return fetchJson<Course>(`/courses/${id}`);
}

export function listModules() {
  return fetchJson<Module[]>("/modules/");
}

export function getModule(id: number) {
  return fetchJson<Module>(`/modules/${id}`);
}

export function listLessons() {
  return fetchJson<Lesson[]>("/lessons/");
}

export function getLesson(id: number) {
  return fetchJson<Lesson>(`/lessons/${id}`);
}

export function listProgress() {
  return fetchJson<Progress[]>("/progress/");
}

export function lessonRenderUrl(lessonId: number, opts: { theme?: string; userId: number }) {
  const params = new URLSearchParams({ user_id: String(opts.userId) });
  if (opts.theme) params.set("theme", opts.theme);
  // SEMPRE a URL pública, nunca API_URL_INTERNAL — mesmo chamada de dentro de um
  // Server Component, o resultado vira o "src" do <iframe> que o NAVEGADOR carrega,
  // e o navegador não resolve o hostname interno do Docker ("backend").
  const publicUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  return `${publicUrl}/lessons/${lessonId}/render?${params.toString()}`;
}

export function avaliarResumo(lessonId: number, data: { userId: number; resumoTexto: string; modelo?: string }) {
  return fetchJson<AvaliarResumoResponse>(`/pipeline/licoes/${lessonId}/avaliar`, {
    method: "POST",
    body: JSON.stringify({
      user_id: data.userId,
      resumo_texto: data.resumoTexto,
      modelo: data.modelo ?? "groq",
    }),
  });
}
