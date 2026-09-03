// Monta a árvore navegável de um curso (módulo → aula → tópico) já com o
// estado de cada tópico anexado. Server-side — usa o cliente de _lib/api.

import type { EstadoTopico } from "../_ui/Selo";
import { ALUNO_USER_ID } from "./config";
import {
  getCourse,
  listModules,
  listLessons,
  listTopicos,
  listTopicoProgress,
  type Course,
} from "./api";

export type TopicoNo = {
  id: number;
  titulo: string;
  referencia_biblica: string | null;
  topico_index: number;
  estado: EstadoTopico;
};

export type AulaNo = {
  id: number;
  titulo: string;
  lesson_index: number;
  topicos: TopicoNo[];
};

export type ModuloNo = {
  id: number;
  titulo: string;
  descricao: string | null;
  module_index: number;
  aulas: AulaNo[];
};

export type ArvoreCurso = {
  curso: Course;
  modulos: ModuloNo[];
  resumo: { totalTopicos: number; concluidos: number; percent: number };
  proximoTopico: { id: number; titulo: string } | null;
};

export async function montarArvore(courseId: number): Promise<ArvoreCurso> {
  const [curso, modules, lessons, topicos, progresso] = await Promise.all([
    getCourse(courseId),
    listModules(),
    listLessons(),
    listTopicos(),
    listTopicoProgress(ALUNO_USER_ID),
  ]);

  const statusPorTopico = new Map(progresso.map((p) => [p.topico_id, p.status]));

  const modsDoCurso = modules
    .filter((m) => m.course_id === courseId)
    .sort((a, b) => a.module_index - b.module_index);

  const idsModulos = new Set(modsDoCurso.map((m) => m.id));
  const aulasDoCurso = lessons
    .filter((l) => idsModulos.has(l.module_id))
    .sort((a, b) => a.lesson_index - b.lesson_index);

  const topicosPorAula = new Map<number, typeof topicos>();
  for (const t of topicos) {
    if (!topicosPorAula.has(t.lesson_id)) topicosPorAula.set(t.lesson_id, []);
    topicosPorAula.get(t.lesson_id)!.push(t);
  }
  for (const lista of topicosPorAula.values()) {
    lista.sort((a, b) => a.topico_index - b.topico_index);
  }

  // 1ª passada: classifica em concluido / em_preparacao / pendente (na ordem do curso).
  let totalTopicos = 0;
  let concluidos = 0;
  let jaMarcouAtual = false;
  let proximoTopico: { id: number; titulo: string } | null = null;

  const modulos: ModuloNo[] = modsDoCurso.map((m) => {
    const aulas: AulaNo[] = aulasDoCurso
      .filter((l) => l.module_id === m.id)
      .map((l) => {
        const tps = topicosPorAula.get(l.id) ?? [];
        const topicosNo: TopicoNo[] = tps.map((t) => {
          totalTopicos++;
          const emPreparacao = !t.content || !t.is_approved;
          let estado: EstadoTopico;
          if (emPreparacao) {
            estado = "em_preparacao";
          } else if (statusPorTopico.get(t.id) === "concluido") {
            estado = "concluido";
            concluidos++;
          } else if (!jaMarcouAtual) {
            estado = "atual";
            jaMarcouAtual = true;
            proximoTopico = { id: t.id, titulo: t.titulo };
          } else {
            estado = "disponivel";
          }
          return {
            id: t.id,
            titulo: t.titulo,
            referencia_biblica: t.referencia_biblica,
            topico_index: t.topico_index,
            estado,
          };
        });
        return { id: l.id, titulo: l.title, lesson_index: l.lesson_index, topicos: topicosNo };
      });
    return {
      id: m.id,
      titulo: m.title,
      descricao: m.description,
      module_index: m.module_index,
      aulas,
    };
  });

  const percent = totalTopicos === 0 ? 0 : Math.round((concluidos / totalTopicos) * 100);

  return { curso, modulos, resumo: { totalTopicos, concluidos, percent }, proximoTopico };
}

// Contagem concluídos/total de um módulo — pro cabeçalho do accordion.
export function contarModulo(m: ModuloNo): { concluidos: number; total: number } {
  let concluidos = 0;
  let total = 0;
  for (const a of m.aulas) {
    for (const t of a.topicos) {
      total++;
      if (t.estado === "concluido") concluidos++;
    }
  }
  return { concluidos, total };
}
