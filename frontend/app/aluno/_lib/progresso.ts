import type { Course, Lesson, Module, Progress } from "../../lib/api";
import type { Mood } from "../../components/theme/ThemeProvider";
import type { TrilhaItem } from "../_layouts/types";

const MOODS: Mood[] = ["musgo", "ambar", "mare", "framboesa", "lavanda"];

// Provisório: Course.category não existe populado no backend ainda (ver
// backlog "nia-curso-categoria-nicho"), então o humor do pôster de cada curso
// é um hash determinístico do id — mesmo curso sempre cai no mesmo humor,
// mas não representa uma categoria real ainda. Trocar por Course.category
// quando esse campo existir de verdade.
export function humorDoCurso(courseId: number): Mood {
  return MOODS[courseId % MOODS.length];
}

// Imagem do pôster por humor — pool fixo de 5 fotos (uma por humor), free
// license (domínio público / CC BY / CC BY-SA, ver créditos no rodapé do
// painel). Provisório como humorDoCurso() acima: não é foto do curso de
// verdade, é só o humor. Trocar quando existir upload/geração de capa real.
export const IMAGEM_DO_HUMOR: Record<Mood, string> = {
  musgo: "/course-images/musgo.jpg",
  ambar: "/course-images/ambar.jpg",
  mare: "/course-images/mare.jpg",
  framboesa: "/course-images/framboesa.jpg",
  lavanda: "/course-images/lavanda.jpg",
};

export function modulosDoCurso(course: Course, modules: Module[]) {
  return modules.filter((m) => m.course_id === course.id).sort((a, b) => a.module_index - b.module_index);
}

export function percentDoCurso(course: Course, modules: Module[], progress: Progress | undefined) {
  const modulosOrdenados = modulosDoCurso(course, modules);
  const totalLicoes = modulosOrdenados.reduce((soma, m) => soma + m.lessons_count, 0);
  if (!progress || totalLicoes === 0) return 0;
  const moduloAtual = modulosOrdenados.find((m) => m.id === progress.module_id);
  if (!moduloAtual) return 0;
  const licoesAntes = modulosOrdenados
    .filter((m) => m.module_index < moduloAtual.module_index)
    .reduce((soma, m) => soma + m.lessons_count, 0);
  const posicao = licoesAntes + (progress.current_lesson_index - 1);
  return Math.max(0, Math.min(100, Math.round((posicao / totalLicoes) * 100)));
}

// Lição pra abrir ao clicar num curso: a atual se estiver pronta, senão recua
// até a última lição já aprovada — só fica sem link se o curso não tem NADA gerado.
export function melhorLicaoParaAbrir(course: Course, modules: Module[], lessons: Lesson[], progress: Progress | undefined) {
  const sequencia = modulosDoCurso(course, modules).flatMap((m) =>
    lessons.filter((l) => l.module_id === m.id).sort((a, b) => a.lesson_index - b.lesson_index)
  );
  if (sequencia.length === 0) return null;

  const posicaoAtual = progress
    ? sequencia.findIndex((l) => l.module_id === progress.module_id && l.lesson_index === progress.current_lesson_index)
    : 0;
  const inicio = posicaoAtual === -1 ? sequencia.length - 1 : posicaoAtual;

  for (let i = inicio; i >= 0; i--) {
    if (sequencia[i].is_approved && sequencia[i].content) return sequencia[i].id;
  }
  return null;
}

export function trilhaDoCurso(course: Course, modules: Module[], lessons: Lesson[], progress: Progress): TrilhaItem[] {
  const modulosOrdenados = modulosDoCurso(course, modules);
  const sequencia = modulosOrdenados.flatMap((m) =>
    lessons.filter((l) => l.module_id === m.id).sort((a, b) => a.lesson_index - b.lesson_index)
  );
  const posicaoAtual = sequencia.findIndex(
    (l) => l.module_id === progress.module_id && l.lesson_index === progress.current_lesson_index
  );

  return sequencia.map((lesson, i) => {
    let situacao: TrilhaItem["situacao"];
    if (posicaoAtual === -1) situacao = "bloqueado";
    else if (i < posicaoAtual) situacao = "done";
    else if (i === posicaoAtual) situacao = "current";
    else if (i === posicaoAtual + 1) situacao = lesson.is_approved && lesson.content ? "proximo" : "preparando";
    else situacao = "bloqueado";
    return { lessonId: lesson.id, titulo: lesson.title, situacao };
  });
}

// Um curso pode ter mais de um Progress (é criado por módulo — ver
// backend/app/routers/pipeline.py). Pra qualquer cálculo "onde o aluno está
// nesse curso" precisa do mais avançado, não de um qualquer.
export function progressoMaisAvancado(course: Course, modules: Module[], progressos: Progress[]) {
  const modulosDoCursoIds = new Set(modulosDoCurso(course, modules).map((m) => m.id));
  const doCurso = progressos.filter((p) => modulosDoCursoIds.has(p.module_id));
  if (doCurso.length === 0) return undefined;

  const moduleIndexDe = (p: Progress) => modules.find((m) => m.id === p.module_id)?.module_index ?? 0;
  return doCurso.reduce((maisAvancado, atual) => {
    const idxAtual = moduleIndexDe(atual);
    const idxMaisAvancado = moduleIndexDe(maisAvancado);
    if (idxAtual > idxMaisAvancado) return atual;
    if (idxAtual === idxMaisAvancado && atual.current_lesson_index > maisAvancado.current_lesson_index) return atual;
    return maisAvancado;
  });
}
