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
  cover_image_url: string | null;
};

export type Module = {
  id: number;
  course_id: number;
  module_index: number;
  title: string;
  description: string | null;
  lessons_count: number;
  cover_image_url: string | null;
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
  // id da Avaliacao (prova) vinculada, só quando existe E está aprovada
  // (2026-09-19 — backend anexa isso em GET /topicos, não é coluna real do Topico).
  avaliacao_id: number | null;
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
  ultimo_slide: number | null;
  rodada_atual: number;
};

// Progresso da PROVA (Avaliacao) — mesmos campos de TopicoProgress, trocando
// topico_id por avaliacao_id (2026-09-19, ver PLANO_AVALIACAO_SEPARADA.md).
export type AvaliacaoProgress = {
  id: number;
  user_id: number;
  avaliacao_id: number;
  status: StatusTopico;
  iniciado_em: string | null;
  concluido_em: string | null;
  tutor_veredito: VeredictoTutor | null;
  tutor_analise: TutorAnalise | null;
  avaliado_em: string | null;
  ultimo_slide: number | null;
  rodada_atual: number;
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

// ---- Anotação pessoal do aluno por slide (2026-09-10) ----
export type Anotacao = {
  id: number;
  user_id: number;
  topico_id: number;
  slide_index: number;
  texto: string;
  updated_at: string | null;
};

// GET /topico-anotacoes/{id} aceita token de sessão real (é o caso aqui, chamado
// server-side pro painel "Minhas anotações") OU o token de escopo curto do
// <iframe> — ver get_topico_anotacao_user_id no backend.
export function listAnotacoes(token: string | null | undefined, topicoId: number) {
  if (!token) return Promise.resolve<Anotacao[]>([]);
  return fetchJson<Anotacao[]>(`/topico-anotacoes/${topicoId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// ---- Revisão (FASE 5a) ----
export type Reacao = "positivo" | "negativo";
export type ImagemSugerida = "antes" | "depois";

export type TopicoComment = {
  id: number;
  topico_id: number;
  user_id: number;
  slide_index: number | null;
  reacao: Reacao | null;
  imagem_sugerida: ImagemSugerida | null;
  sobre_imagem: boolean;
  texto: string | null;
  resolvido: boolean;
  created_at: string;
};

export type Profundidade = "raso" | "adequado" | "aprofundado";
export type Clareza = "confuso" | "parcialmente_claro" | "claro";
export type QualidadeGeral = "fraca" | "regular" | "boa" | "excelente";

export type ChecklistTopico = {
  id: number;
  topico_id: number;
  user_id: number;
  profundidade: Profundidade;
  clareza: Clareza;
  qualidade_geral: QualidadeGeral;
  observacao_final: string | null;
  aprovado: boolean;
  updated_at: string | null;
};

// ---- Governança de publicação do curso (FASE 5b) ----
export type Pessoa = { id: number; name: string | null; email: string };

export type AprovacaoCurso = {
  user_id: number;
  name: string | null;
  papel_no_momento: string;
  aprovado: boolean;
  observacao: string | null;
  updated_at: string | null;
};

export type GovernancaCurso = {
  course_id: number;
  status: string;
  publicado: boolean;
  published_at: string | null;
  aprovacao_master_basta: boolean;
  aprovacao_exige_todos_tutores: boolean;
  tutores: Pessoa[];
  professores_disponiveis: Pessoa[];
  aprovacoes: AprovacaoCurso[];
  pode_publicar: boolean;
  sou_tutor: boolean;
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

export function topicoRenderUrl(
  id: number,
  opts: {
    userId: number;
    theme?: string;
    contexto?: "revisao";
    pdf?: boolean;
    respostasToken?: string;
    avaliacaoInicial?: AvaliacaoTutor | null;
    concluido?: boolean;
    temProximo?: boolean;
    avaliacaoId?: number | null;
    slide?: number;
  },
) {
  const params = new URLSearchParams({
    user_id: String(opts.userId),
    theme: opts.theme ?? THEME_TOPICO,
  });
  // "revisao" faz o render nunca sair do modo Slide (some o toggle Corrido/Slide) —
  // a fila de revisão depende de saber "qual slide está na tela" (postMessage
  // emaus:slide) pra sincronizar os comentários por slide.
  if (opts.contexto) params.set("contexto", opts.contexto);
  // "pdf=1" faz aparecer o botão "📄 PDF" no topo do render (imprimir → salvar
  // como PDF, texto corrido). Passado só pra quem revisa (professor/admin/master).
  if (opts.pdf) params.set("pdf", "1");
  // Token de escopo curto (getTopicoToken) — sem ele o render não salva resposta
  // de exercício nenhuma (fica só no estado da página, como sempre foi).
  if (opts.respostasToken) params.set("token", opts.respostasToken);
  // Avisa o render que este Tópico tem Prova separada (2026-09-22) — o slide
  // "Resultado" usa isso pra oferecer o botão "Fazer a prova" quando o aluno
  // domina o conteúdo, além de "Próximo tópico".
  if (opts.avaliacaoId != null) params.set("avaliacao", "1");
  // Abre direto nesse slide (1-based) em vez do último onde o aluno parou.
  if (opts.slide) params.set("slide", String(opts.slide));
  // Estado inicial da avaliação do tutor (2026-09-11) — reabrir um tópico já
  // concluído já mostra o resultado no slide "Resultado", sem precisar clicar
  // em "Fim" de novo. Só o essencial pro slide renderizar (não manda lacunas).
  if (opts.concluido && opts.avaliacaoInicial) {
    params.set("concluido", "1");
    params.set("veredito", opts.avaliacaoInicial.veredito);
    params.set("resumo", opts.avaliacaoInicial.resumo_diagnostico ?? "");
    if (opts.temProximo) params.set("proximo", "1");
  }
  return `${API_URL_PUBLICA}/topicos/${id}/render?${params.toString()}`;
}

// URL de render da PROVA (Avaliacao) — mesmo padrão de topicoRenderUrl, sem
// tema por curso (a prova herda o tema do próprio backend, "vidro-fume" por
// padrão) nem PDF (não faz sentido pra prova nesta 1ª versão).
export function avaliacaoRenderUrl(
  id: number,
  opts: {
    userId: number;
    theme?: string;
    respostasToken?: string;
    avaliacaoInicial?: AvaliacaoTutor | null;
    concluido?: boolean;
  },
) {
  const params = new URLSearchParams({
    user_id: String(opts.userId),
    theme: opts.theme ?? THEME_TOPICO,
  });
  if (opts.respostasToken) params.set("token", opts.respostasToken);
  if (opts.concluido && opts.avaliacaoInicial) {
    params.set("concluido", "1");
    params.set("veredito", opts.avaliacaoInicial.veredito);
    params.set("resumo", opts.avaliacaoInicial.resumo_diagnostico ?? "");
  }
  return `${API_URL_PUBLICA}/avaliacoes/${id}/render?${params.toString()}`;
}

// ---- Usuário / progresso ----
// GET /users/{id} exige login desde 2026-09-23 (achado de segurança: ficava aberto,
// qualquer um enumerava user_id e lia dado pessoal de qualquer conta). `token` vem de
// getToken() (_lib/sessao.ts, server-only) — sem ele, devolve null em vez de tentar.
export function getUser(id: number, token: string | null | undefined) {
  if (!token) return Promise.resolve<UserPrefs | null>(null);
  return fetchJson<UserPrefs>(`/users/${id}`, comAuth(token));
}

// Token de ESCOPO CURTO (2h, só "salvar resposta deste usuário, neste tópico")
// pro <iframe> do render — 2026-09-09. Chamado só server-side, com o token de
// sessão de verdade (getToken() em _lib/sessao.ts, nunca vai pro cliente). O
// token curto devolvido aqui é o único que entra na URL do iframe.
export async function getTopicoToken(token: string, topicoId: number) {
  const { access_token } = await fetchJson<{ access_token: string }>("/auth/topico-token", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ topico_id: topicoId }),
  });
  return access_token;
}

// Token de ESCOPO CURTO pro <iframe> do render da PROVA salvar resposta —
// mesmo padrão de getTopicoToken, endpoint diferente (backend valida o
// GATING aqui: só emite se o tópico vinculado estiver concluído).
export async function getAvaliacaoToken(token: string, avaliacaoId: number) {
  const { access_token } = await fetchJson<{ access_token: string }>("/auth/avaliacao-token", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ avaliacao_id: avaliacaoId }),
  });
  return access_token;
}

// GET /users/ exige login com papel master/admin/professor (área de revisão) —
// usado só server-side com o token da sessão (ver getToken() em _lib/sessao.ts).
export function listUsers(token: string | null | undefined) {
  if (!token) return Promise.resolve<UserPrefs[]>([]);
  return fetchJson<UserPrefs[]>("/users/", { headers: { Authorization: `Bearer ${token}` } });
}

// PUT /users/{id} agora exige login (FASE 1 + correção de segurança 2026-09-04) — um
// Client Component não tem como anexar o Bearer (o token é httpOnly), então não existe
// mais um updateUser() genérico aqui. Ver salvarPerfil()/salvarPreferencia() no fim
// deste arquivo — passam pelo proxy autenticado do próprio Emaús
// (app/api/perfil, app/api/preferencias), que é quem fala com o NIA com o token.

export function listProgress() {
  return fetchJson<Progress[]>("/progress/");
}

// ---- Progresso por tópico (FASE 2) ----
// GET /topico-progress/ exige login desde 2026-09-23 (mesmo achado de segurança do
// getUser acima). Sem token, devolve lista vazia em vez de tentar.
export function listTopicoProgress(userId: number, token: string | null | undefined) {
  if (!token) return Promise.resolve<TopicoProgress[]>([]);
  return fetchJson<TopicoProgress[]>(`/topico-progress/?user_id=${userId}`, comAuth(token));
}

// ---- Progresso da prova (2026-09-19) ----
// GET /avaliacao-progress/ exige login desde 2026-09-23, mesmo padrão acima.
export function listAvaliacaoProgress(userId: number, token: string | null | undefined) {
  if (!token) return Promise.resolve<AvaliacaoProgress[]>([]);
  return fetchJson<AvaliacaoProgress[]>(`/avaliacao-progress/?user_id=${userId}`, comAuth(token));
}

// PUT /topico-progress/{id} também exige login e valida user_id contra o token —
// mesma razão do updateUser acima. Usar marcarProgresso() (client-safe) abaixo.

// ---- Leituras autenticadas de SERVER COMPONENT (área de revisão) ----
// Só master/admin/professor — o backend confere de novo (403 se não for). `token` vem
// de getToken() (_lib/sessao.ts, server-only). Sem token, devolve lista vazia (a
// página decide o que fazer — normalmente nem chega aqui, o middleware já bloqueou).
function comAuth(token: string | null | undefined): RequestInit | undefined {
  return token ? { headers: { Authorization: `Bearer ${token}` } } : undefined;
}

// topicoId omitido = todos os comentários (fila de revisão contando abertos por tópico).
export function listTopicoComments(topicoId: number | undefined, token: string | null | undefined) {
  if (!token) return Promise.resolve<TopicoComment[]>([]);
  const q = topicoId != null ? `?topico_id=${topicoId}` : "";
  return fetchJson<TopicoComment[]>(`/topico-comments/${q}`, comAuth(token));
}

export function listChecklistsTopico(topicoId: number, token?: string | null) {
  if (!token) return Promise.resolve<ChecklistTopico[]>([]);
  return fetchJson<ChecklistTopico[]>(`/topico-checklists/?topico_id=${topicoId}`, comAuth(token));
}

export function getGovernancaCurso(courseId: number, token: string | null | undefined) {
  if (!token) return Promise.resolve<GovernancaCurso | null>(null);
  return fetchJson<GovernancaCurso>(`/cursos/${courseId}/governanca`, comAuth(token));
}

// ============================================================
// Escritas autenticadas de CLIENT COMPONENT — nunca chamam o NIA direto (o token é
// httpOnly, só o servidor do Emaús o vê). Passam pelas rotas em app/api/*, que leem
// o cookie, confirmam a sessão e anexam Authorization: Bearer. O id de quem está
// agindo nunca é parâmetro aqui — é sempre o dono da sessão, ponto final.
// ============================================================

async function chamarMesmaOrigem<T>(
  path: string,
  method: "PUT" | "POST",
  body: unknown,
): Promise<T> {
  const res = await fetch(path, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.erro ?? `Erro ${res.status}`);
  return data as T;
}

export function salvarPerfil(name: string) {
  return chamarMesmaOrigem<{ ok: true }>("/api/perfil", "PUT", { name });
}

export function salvarPreferencia(
  campo: "preferred_panel_mode" | "preferred_font_size",
  valor: string,
) {
  return chamarMesmaOrigem<{ ok: true }>("/api/preferencias", "PUT", { [campo]: valor });
}

export function marcarProgresso(topicoId: number, status: StatusTopico) {
  return chamarMesmaOrigem<TopicoProgress>("/api/topico-progress", "PUT", { topicoId, status });
}

// Recomeçar o tópico (2026-09-15) — pro aluno que testou/espiou exercícios e
// quer refazer valendo de verdade. Não apaga nada (ver POST
// /topico-progress/{id}/reiniciar no backend); só abre uma rodada nova.
export function reiniciarTopico(topicoId: number) {
  return chamarMesmaOrigem<TopicoProgress>("/api/topico-progress/reiniciar", "POST", { topicoId });
}

// Devolve o TopicoProgress atualizado; a avaliação em si fica em
// `.tutor_analise.ultima_avaliacao`, o novo status em `.status`.
export function enviarAvaliacaoTutor(topicoId: number, resumoTexto: string) {
  return chamarMesmaOrigem<TopicoProgress>("/api/tutor", "POST", { topicoId, resumoTexto });
}

// ---- Escritas da prova (2026-09-19) — mesmo padrão de proxy autenticado ----
export function marcarProgressoAvaliacao(avaliacaoId: number, status: StatusTopico) {
  return chamarMesmaOrigem<AvaliacaoProgress>("/api/avaliacao-progress", "PUT", { avaliacaoId, status });
}

// Recomeçar a prova — mesmo princípio do reiniciarTopico (nunca apaga nada,
// só abre uma rodada nova em AvaliacaoResposta/AvaliacaoProgress).
export function reiniciarAvaliacao(avaliacaoId: number) {
  return chamarMesmaOrigem<AvaliacaoProgress>("/api/avaliacao-progress/reiniciar", "POST", { avaliacaoId });
}

export function enviarAvaliacaoTutorProva(avaliacaoId: number, resumoTexto: string) {
  return chamarMesmaOrigem<AvaliacaoProgress>("/api/avaliacao-tutor", "POST", { avaliacaoId, resumoTexto });
}

// ---- Escritas da área de revisão (FASE 5a) — mesmo padrão de proxy autenticado ----
export type NovoComentario = {
  topicoId: number;
  slideIndex: number | null;
  reacao?: Reacao | null;
  imagemSugerida?: ImagemSugerida | null;
  sobreImagem?: boolean;
  texto?: string | null;
};

export function criarComentarioSlide(data: NovoComentario) {
  return chamarMesmaOrigem<TopicoComment>("/api/revisao/comentario", "POST", data);
}

export function resolverComentario(id: number, resolvido: boolean) {
  return chamarMesmaOrigem<TopicoComment>("/api/revisao/comentario", "PUT", { id, resolvido });
}

export type NovoChecklist = {
  topicoId: number;
  profundidade: Profundidade;
  clareza: Clareza;
  qualidadeGeral: QualidadeGeral;
  observacaoFinal: string | null;
  aprovado: boolean;
};

export function salvarChecklist(data: NovoChecklist) {
  return chamarMesmaOrigem<ChecklistTopico>("/api/revisao/checklist", "PUT", data);
}

// ---- Escritas de governança do curso (FASE 5b) ----
export type NovaConfigCurso = {
  courseId: number;
  aprovacaoMasterBasta: boolean;
  aprovacaoExigeTodosTutores: boolean;
  tutorIds: number[];
};

export function salvarConfigCurso(data: NovaConfigCurso) {
  return chamarMesmaOrigem<GovernancaCurso>("/api/revisao/curso-config", "PUT", data);
}

export function salvarAprovacaoCurso(courseId: number, aprovado: boolean, observacao: string | null) {
  return chamarMesmaOrigem<AprovacaoCurso>("/api/revisao/curso-aprovacao", "PUT", {
    courseId,
    aprovado,
    observacao,
  });
}

export function publicarCurso(courseId: number) {
  return chamarMesmaOrigem<GovernancaCurso>("/api/revisao/curso-publicar", "POST", { courseId });
}

export function despublicarCurso(courseId: number) {
  return chamarMesmaOrigem<GovernancaCurso>("/api/revisao/curso-publicar", "PUT", { courseId });
}
