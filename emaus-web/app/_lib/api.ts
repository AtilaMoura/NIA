// Cliente da API do NIA — só os endpoints que o Emaús usa.

import { API_URL, API_URL_PUBLICA, THEME_TOPICO } from "./config";

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

export type Topico = {
  id: number;
  lesson_id: number;
  topico_index: number;
  titulo: string;
  referencia_biblica: string | null;
  content: string | null;
  is_approved: boolean;
  generated_by: string | null;
  reviewed_by: string | null;
  estimated_read_time_minutes: number | null;
};

export type FontSize = "sm" | "md" | "lg";

export type UserPrefs = {
  id: number;
  name: string | null;
  email?: string;
  preferred_panel_mode: "light" | "dark";
  preferred_font_size?: FontSize | null;
  [k: string]: unknown;
};

export type StatusTopico = "nao_iniciado" | "em_andamento" | "concluido";

export type VeredictoTutor = "dominado" | "reforco";

export type TutorLacuna = {
  tema: string;
  evidencia: string;
  gravidade: "superficial" | "real";
};

export type TutorReforco = {
  necessario: boolean;
  foco: string;
  instrucao_para_gerar: string;
};

// O JSON que o TutorAgent devolve (guardado em tutor_analise.ultima_avaliacao).
export type AvaliacaoTutor = {
  veredito: VeredictoTutor;
  resumo_diagnostico: string;
  pontos_fortes: string[];
  lacunas: TutorLacuna[];
  reforco_sugerido: TutorReforco;
};

export type TutorAnalise = {
  ultima_avaliacao: AvaliacaoTutor;
  historico: { veredito: VeredictoTutor; resumo_diagnostico: string }[];
};

export type TopicoProgress = {
  id: number;
  user_id: number;
  topico_id: number;
  status: StatusTopico;
  iniciado_em: string | null;
  concluido_em: string | null;
  tutor_veredito: VeredictoTutor | null;
  tutor_analise: TutorAnalise | null;
  avaliado_em: string | null;
};

// Progress é por MÓDULO (o de tópico é TopicoProgress). Só os campos que o Emaús lê.
export type Progress = {
  id: number;
  user_id: number;
  course_id: number;
  module_id: number;
  status: string;
  time_spent_minutes: number | null;
  last_accessed_at: string | null;
};

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`NIA ${res.status} em ${path}: ${await res.text()}`);
  }
  return res.json() as Promise<T>;
}

// ---- Catálogo / conteúdo ----
export function listCourses() {
  return fetchJson<Course[]>("/courses/");
}

export function getCourse(id: number) {
  return fetchJson<Course>(`/courses/${id}`);
}

export function listModules() {
  return fetchJson<Module[]>("/modules/");
}

export function listLessons() {
  return fetchJson<Lesson[]>("/lessons/");
}

export function listTopicos(lessonId?: number) {
  const q = lessonId != null ? `?lesson_id=${lessonId}` : "";
  return fetchJson<Topico[]>(`/topicos/${q}`);
}

export function getTopico(id: number) {
  return fetchJson<Topico>(`/topicos/${id}`);
}

export function topicoRenderUrl(id: number, opts: { userId: number; theme?: string }) {
  const params = new URLSearchParams({
    user_id: String(opts.userId),
    theme: opts.theme ?? THEME_TOPICO,
  });
  return `${API_URL_PUBLICA}/topicos/${id}/render?${params.toString()}`;
}

// ---- Usuário / progresso ----
export function getUser(id: number) {
  return fetchJson<UserPrefs>(`/users/${id}`);
}

export function updateUser(id: number, data: Record<string, unknown>) {
  return fetchJson<UserPrefs>(`/users/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export function listProgress() {
  return fetchJson<Progress[]>("/progress/");
}

// ---- Progresso por tópico (FASE 2) ----
export function listTopicoProgress(userId: number) {
  return fetchJson<TopicoProgress[]>(`/topico-progress/?user_id=${userId}`);
}

export function setTopicoProgress(topicoId: number, userId: number, status: StatusTopico) {
  return fetchJson<TopicoProgress>(`/topico-progress/${topicoId}`, {
    method: "PUT",
    body: JSON.stringify({ user_id: userId, status }),
  });
}

// ---- Avaliação do Tutor por tópico (FASE 4) ----
// Devolve o TopicoProgress atualizado; a avaliação em si fica em
// `.tutor_analise.ultima_avaliacao`, o novo status em `.status`.
export function avaliarTopico(topicoId: number, userId: number, resumoTexto: string) {
  return fetchJson<TopicoProgress>(`/pipeline/topicos/${topicoId}/avaliar`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId, resumo_texto: resumoTexto }),
  });
}
