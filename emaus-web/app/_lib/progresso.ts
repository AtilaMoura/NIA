import { CATALOGO, caminhoCapa, type CursoCatalogo } from "./catalogo";
import { capaExiste } from "./capas";
import { montarArvore, type ArvoreCurso } from "./arvore";
import { listAvaliacaoProgress, type AvaliacaoProgress } from "./api";
import type { Papel } from "./papel";
import { papelVeEstudosPessoais } from "./papel";

// Progresso de TODOS os cursos em que o aluno já estudou algo (redesign 2026-09-27,
// protótipo 07-progresso.html) — antes a /progresso era fixa no 1º curso do código.
export type ProgressoCurso = {
  catalogo: CursoCatalogo;
  capaUrl: string | null;
  arvore: ArvoreCurso;
};

export type ResumoGeral = {
  concluidos: number;
  dominados: number;
  provasFeitas: number;
  tempoMin: number;
};

export async function progressoDoAluno(
  userId: number,
  papel: Papel,
  token: string | null,
): Promise<{ cursos: ProgressoCurso[]; provas: Map<number, AvaliacaoProgress>; resumo: ResumoGeral }> {
  // Estudos pessoais só entram pro Master (mesma regra da /inicio e da /estudos)
  const candidatos = CATALOGO.filter(
    (c) =>
      c.disponivel &&
      c.courseId != null &&
      (c.categoria !== "Estudos pessoais" || papelVeEstudosPessoais(papel)),
  );

  const [arvores, progressoProvas] = await Promise.all([
    Promise.all(candidatos.map((c) => montarArvore(c.courseId!, userId, token).catch(() => null))),
    listAvaliacaoProgress(userId, token).catch((): AvaliacaoProgress[] => []),
  ]);

  const cursos: ProgressoCurso[] = [];
  candidatos.forEach((c, i) => {
    const arvore = arvores[i];
    if (!arvore) return;
    // Só aparece curso em que o aluno já mexeu (começou ou concluiu algum tópico)
    const mexeu = arvore.linhaDoTempo.some((t) => t.iniciado_em || t.concluido_em);
    if (!mexeu) return;
    cursos.push({ catalogo: c, capaUrl: capaExiste(c.slug) ? caminhoCapa(c.slug) : null, arvore });
  });

  const provas = new Map(progressoProvas.map((p) => [p.avaliacao_id, p]));
  const topicos = cursos.flatMap((c) => c.arvore.linhaDoTempo);
  const resumo: ResumoGeral = {
    concluidos: topicos.filter((t) => t.estado === "concluido").length,
    dominados: topicos.filter((t) => t.tutor_veredito === "dominado").length,
    provasFeitas: progressoProvas.filter((p) => p.status === "concluido").length,
    tempoMin: cursos.reduce((soma, c) => soma + c.arvore.resumo.tempoTotalMin, 0),
  };

  return { cursos, provas, resumo };
}

/** "3h 20min", "45min" ou "—" */
export function formatarTempo(min: number): string {
  if (min <= 0) return "—";
  const h = Math.floor(min / 60);
  const m = min % 60;
  return h > 0 ? `${h}h ${m}min` : `${m}min`;
}
