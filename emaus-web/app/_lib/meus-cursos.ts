import { CATALOGO, caminhoCapa, type CategoriaCurso, type CursoCatalogo } from "./catalogo";
import type { EstudoMeu, PessoaCurta } from "./api";
import { capaExiste } from "./capas";
import { montarArvore, type TopicoNo } from "./arvore";
import type { Papel } from "./papel";

// Cursos de uma prateleira, do ponto de vista de quem está logado — usado pela
// /inicio (Formação bíblica) e pela /estudos (estudos privados).
// Quem vê o quê é o BACKEND que decide (2026-10-06): curso sem acesso volta 404
// e conteúdo de curso não publicado não vem pra quem não revisa. Aqui só se monta
// o cartão com o que veio.
export type MeuCurso = {
  catalogo: CursoCatalogo;
  capaUrl: string | null;
  /** o backend entregou o conteúdo (módulos) pra este usuário */
  aberto: boolean;
  /** aberto mas ainda não publicado — só aparece porque o usuário revisa */
  soRevisores: boolean;
  percent: number;
  concluidos: number;
  totalTopicos: number;
  /** próximo tópico a estudar, com módulo/aula/referência (pro "Continuar") */
  proximo: TopicoNo | null;
  /** estudos privados, só pro Master: quem mais tem este estudo liberado */
  liberadoPara: PessoaCurta[];
};

async function montarCartao(
  c: CursoCatalogo,
  sessao: { id: number; role: Papel },
  token: string | null,
  liberadoPara: PessoaCurta[] = [],
): Promise<MeuCurso> {
  const capaUrl = capaExiste(c.slug) ? caminhoCapa(c.slug) : null;
  const fechado = {
    catalogo: c, capaUrl, aberto: false, soRevisores: false, percent: 0, concluidos: 0, totalTopicos: 0,
    proximo: null, liberadoPara,
  };
  if (!c.disponivel || c.courseId == null) return fechado;

  const arvore = await montarArvore(c.courseId, sessao.id, token).catch(() => null);
  if (!arvore || arvore.modulos.length === 0) return fechado;

  return {
    catalogo: c,
    capaUrl,
    aberto: true,
    soRevisores: arvore.curso.status !== "published" && arvore.curso.visibilidade !== "privado",
    percent: arvore.resumo.percent,
    concluidos: arvore.resumo.concluidos,
    totalTopicos: arvore.resumo.totalTopicos,
    proximo: arvore.linhaDoTempo.find((t) => t.estado === "atual") ?? null,
    liberadoPara,
  };
}

export async function meusCursos(
  categoria: CategoriaCurso,
  sessao: { id: number; role: Papel },
  token: string | null,
): Promise<MeuCurso[]> {
  return Promise.all(CATALOGO.filter((c) => c.categoria === categoria).map((c) => montarCartao(c, sessao, token)));
}

/** Estudo que não está no catálogo do Emaús (ex.: um estudo novo criado pra uma
 * pessoa) — o cartão sai com o título/descrição do banco e capa em degradê. */
export function catalogoDoEstudo(e: EstudoMeu): CursoCatalogo {
  return (
    CATALOGO.find((c) => c.courseId === e.course_id) ?? {
      slug: `estudo-${e.course_id}`,
      titulo: e.titulo,
      subtitulo: "",
      descricao: e.descricao ?? "",
      tom: "pedra",
      categoria: "Estudos pessoais",
      courseId: e.course_id,
      disponivel: true,
    }
  );
}

/** Estudos privados liberados pra esta pessoa (lista vem do backend). */
export async function cursosDosEstudos(
  estudos: EstudoMeu[],
  sessao: { id: number; role: Papel },
  token: string | null,
): Promise<MeuCurso[]> {
  return Promise.all(estudos.map((e) => montarCartao(catalogoDoEstudo(e), sessao, token, e.liberado_para)));
}

/** Cursos em andamento (começados e não terminados), do mais adiantado pro menos. */
export function emAndamento(cursos: MeuCurso[]): MeuCurso[] {
  return cursos
    .filter((c) => c.aberto && c.proximo && c.percent > 0 && c.percent < 100)
    .sort((a, b) => b.percent - a.percent);
}
