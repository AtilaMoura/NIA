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
  listProgress,
  type Course,
  type VeredictoTutor,
} from "./api";

export type TopicoNo = {
  id: number;
  titulo: string;
  referencia_biblica: string | null;
  topico_index: number;
  estado: EstadoTopico;
  lesson_id: number;
  iniciado_em: string | null;
  concluido_em: string | null;
  tutor_veredito: VeredictoTutor | null;
  // id da Avaliacao (prova) vinculada, só quando aprovada — null = sem prova
  // pra este tópico (2026-09-19). A prova só libera quando estado==="concluido".
  avaliacaoId: number | null;
  // preenchidos só na linhaDoTempo (contexto pra exibir fora da árvore)
  moduloTitulo?: string;
  aulaTitulo?: string;
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
  cover_image_url: string | null;
  aulas: AulaNo[];
};

export type ArvoreCurso = {
  curso: Course;
  modulos: ModuloNo[];
  resumo: { totalTopicos: number; concluidos: number; percent: number; tempoTotalMin: number };
  proximoTopico: { id: number; titulo: string } | null;
  // Todos os tópicos na ordem do curso, com módulo/aula anexados — pra /progresso.
  linhaDoTempo: TopicoNo[];
};

// userId opcional (default = ALUNO_USER_ID) — a partir da FASE 1 (auth), quem chama
// deve sempre passar o id da sessão de verdade; o default fica só de fallback.
export async function montarArvore(
  courseId: number,
  userId: number = ALUNO_USER_ID,
): Promise<ArvoreCurso> {
  const [curso, modules, lessons, topicos, progresso, progressModulos] = await Promise.all([
    getCourse(courseId),
    listModules(),
    listLessons(),
    listTopicos(),
    listTopicoProgress(userId),
    listProgress().catch(() => []),
  ]);

  const progressoPorTopico = new Map(progresso.map((p) => [p.topico_id, p]));
  const statusPorTopico = new Map(progresso.map((p) => [p.topico_id, p.status]));

  const tempoTotalMin = progressModulos
    .filter((p) => p.course_id === courseId && p.user_id === userId)
    .reduce((soma, p) => soma + (p.time_spent_minutes ?? 0), 0);

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
          const prog = progressoPorTopico.get(t.id);
          return {
            id: t.id,
            titulo: t.titulo,
            referencia_biblica: t.referencia_biblica,
            topico_index: t.topico_index,
            estado,
            lesson_id: t.lesson_id,
            iniciado_em: prog?.iniciado_em ?? null,
            concluido_em: prog?.concluido_em ?? null,
            tutor_veredito: prog?.tutor_veredito ?? null,
            avaliacaoId: t.avaliacao_id,
          };
        });
        return { id: l.id, titulo: l.title, lesson_index: l.lesson_index, topicos: topicosNo };
      });
    return {
      id: m.id,
      titulo: m.title,
      descricao: m.description,
      module_index: m.module_index,
      cover_image_url: m.cover_image_url,
      aulas,
    };
  });

  const percent = totalTopicos === 0 ? 0 : Math.round((concluidos / totalTopicos) * 100);

  const linhaDoTempo: TopicoNo[] = modulos.flatMap((m) =>
    m.aulas.flatMap((a) =>
      a.topicos.map((t) => ({ ...t, moduloTitulo: m.titulo, aulaTitulo: a.titulo })),
    ),
  );

  return {
    curso,
    modulos,
    resumo: { totalTopicos, concluidos, percent, tempoTotalMin },
    proximoTopico,
    linhaDoTempo,
  };
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
