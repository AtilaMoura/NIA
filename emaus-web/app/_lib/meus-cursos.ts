import { CATALOGO, caminhoCapa, cursoPessoal, type CategoriaCurso, type CursoCatalogo } from "./catalogo";
import { listLessons, listModules } from "./api";
import { capaExiste } from "./capas";
import { montarArvore, type TopicoNo } from "./arvore";
import { papelPodeRevisar, type Papel } from "./papel";

// Cursos de uma categoria do catálogo, do ponto de vista de quem está logado —
// usado pela /inicio (Formação bíblica) e pela /estudos (Estudos pessoais).
export type MeuCurso = {
  catalogo: CursoCatalogo;
  capaUrl: string | null;
  /** aberto pra este usuário (publicado, ou em revisão e o usuário revisa) */
  aberto: boolean;
  /** true quando não está publicado e só aparece porque o usuário revisa */
  soRevisores: boolean;
  percent: number;
  concluidos: number;
  totalTopicos: number;
  /** próximo tópico a estudar, com módulo/aula/referência (pro "Continuar") */
  proximo: TopicoNo | null;
};

export async function meusCursos(
  categoria: CategoriaCurso,
  sessao: { id: number; role: Papel },
  token: string | null,
): Promise<MeuCurso[]> {
  const doCatalogo = CATALOGO.filter((c) => c.categoria === categoria);

  return Promise.all(
    doCatalogo.map(async (c): Promise<MeuCurso> => {
      const capaUrl = capaExiste(c.slug) ? caminhoCapa(c.slug) : null;
      const fechado = { catalogo: c, capaUrl, aberto: false, soRevisores: false, percent: 0, concluidos: 0, totalTopicos: 0, proximo: null };
      if (!c.disponivel || c.courseId == null) return fechado;

      const arvore = await montarArvore(c.courseId, sessao.id, token).catch(() => null);
      if (!arvore) return fechado;

      const publicado = arvore.curso.status === "published";
      const revisa = papelPodeRevisar(sessao.role);
      if (!publicado && !revisa) return fechado;

      return {
        catalogo: c,
        capaUrl,
        aberto: true,
        soRevisores: !publicado,
        percent: arvore.resumo.percent,
        concluidos: arvore.resumo.concluidos,
        totalTopicos: arvore.resumo.totalTopicos,
        proximo: arvore.linhaDoTempo.find((t) => t.estado === "atual") ?? null,
      };
    }),
  );
}

/** Cursos em andamento (começados e não terminados), do mais adiantado pro menos. */
export function emAndamento(cursos: MeuCurso[]): MeuCurso[] {
  return cursos
    .filter((c) => c.aberto && c.proximo && c.percent > 0 && c.percent < 100)
    .sort((a, b) => b.percent - a.percent);
}

/** Tópico pertence a um estudo pessoal? (pra não vazar o título dele na aba de
 * quem não é Master — o título é montado antes do bloqueio da página). */
export async function topicoDeEstudoPessoal(lessonId: number): Promise<boolean> {
  const [lessons, modules] = await Promise.all([listLessons(), listModules()]);
  const aula = lessons.find((l) => l.id === lessonId);
  const modulo = aula ? modules.find((m) => m.id === aula.module_id) : undefined;
  return modulo ? cursoPessoal(modulo.course_id) : false;
}
