// Monta a fila de revisão de um curso — visão do revisor (master/admin/professor),
// diferente de montarArvore (visão de progresso do aluno). Server-side.

import { getCourse, listModules, listLessons, listTopicos, listTopicoComments, type Course } from "./api";

export type StatusRevisao = "rascunho" | "em_revisao" | "aprovado";

export type TopicoRevisaoNo = {
  id: number;
  titulo: string;
  referencia_biblica: string | null;
  topico_index: number;
  status: StatusRevisao;
  reviewed_by: string | null;
  comentariosAbertos: number;
  moduloTitulo: string;
  aulaTitulo: string;
};

export type FilaRevisao = {
  curso: Course;
  topicos: TopicoRevisaoNo[];
};

export async function montarFilaRevisao(courseId: number, token: string | null): Promise<FilaRevisao> {
  const [curso, modules, lessons, topicos, comentarios] = await Promise.all([
    getCourse(courseId),
    listModules(),
    listLessons(),
    listTopicos(),
    listTopicoComments(undefined, token),
  ]);

  const abertosPorTopico = new Map<number, number>();
  for (const c of comentarios) {
    if (!c.resolvido) abertosPorTopico.set(c.topico_id, (abertosPorTopico.get(c.topico_id) ?? 0) + 1);
  }

  const modsDoCurso = modules
    .filter((m) => m.course_id === courseId)
    .sort((a, b) => a.module_index - b.module_index);
  const idsModulos = new Set(modsDoCurso.map((m) => m.id));
  const moduloPorId = new Map(modsDoCurso.map((m) => [m.id, m]));

  const aulasDoCurso = lessons
    .filter((l) => idsModulos.has(l.module_id))
    .sort((a, b) => a.lesson_index - b.lesson_index);
  const aulaPorId = new Map(aulasDoCurso.map((l) => [l.id, l]));
  const idsAulas = new Set(aulasDoCurso.map((l) => l.id));

  const topicosDoCurso = topicos
    .filter((t) => idsAulas.has(t.lesson_id))
    .sort((a, b) => {
      const la = aulaPorId.get(a.lesson_id)!;
      const lb = aulaPorId.get(b.lesson_id)!;
      return la.lesson_index - lb.lesson_index || a.topico_index - b.topico_index;
    });

  const lista: TopicoRevisaoNo[] = topicosDoCurso.map((t) => {
    const aula = aulaPorId.get(t.lesson_id)!;
    const modulo = moduloPorId.get(aula.module_id)!;
    let status: StatusRevisao;
    if (!t.content) status = "rascunho";
    else if (!t.is_approved) status = "em_revisao";
    else status = "aprovado";
    return {
      id: t.id,
      titulo: t.titulo,
      referencia_biblica: t.referencia_biblica,
      topico_index: t.topico_index,
      status,
      reviewed_by: t.reviewed_by,
      comentariosAbertos: abertosPorTopico.get(t.id) ?? 0,
      moduloTitulo: modulo.title,
      aulaTitulo: aula.title,
    };
  });

  return { curso, topicos: lista };
}
