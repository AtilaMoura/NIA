import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Chip } from "../_ui/Chip";
import { Rodape } from "../_ui/Rodape";
import { TEOLOGIA_COURSE_IDS } from "../_lib/config";
import { CATALOGO } from "../_lib/catalogo";
import { getSessao, getToken } from "../_lib/sessao";
import { papelPodeRevisar } from "../_lib/papel";
import { montarFilaRevisao, type StatusRevisao } from "../_lib/revisao";

const CURSO_ID_PADRAO = TEOLOGIA_COURSE_IDS[0];

// Cursos navegáveis na fila de revisão — mesma lista de `TEOLOGIA_COURSE_IDS`, com
// título pra mostrar no seletor (achado pelo catálogo, que já tem os títulos certos).
function cursosDisponiveis() {
  return (TEOLOGIA_COURSE_IDS as readonly number[]).map((id) => ({
    id,
    titulo: CATALOGO.find((c) => c.courseId === id)?.titulo ?? `Curso ${id}`,
  }));
}

export const metadata: Metadata = { title: "Área de revisão" };

const ROTULO_STATUS: Record<StatusRevisao, { texto: string; tom: "neutro" | "aviso" | "bom" }> = {
  rascunho: { texto: "Rascunho", tom: "neutro" },
  em_revisao: { texto: "Em revisão", tom: "aviso" },
  aprovado: { texto: "Aprovado", tom: "bom" },
};

export default async function RevisaoPage({
  searchParams,
}: {
  searchParams: Promise<{ curso?: string }>;
}) {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/revisao");
  if (!papelPodeRevisar(sessao.role)) redirect("/inicio");

  const { curso: cursoParam } = await searchParams;
  const cursos = cursosDisponiveis();
  const CURSO_ID =
    Number(cursoParam) && cursos.some((c) => c.id === Number(cursoParam))
      ? Number(cursoParam)
      : CURSO_ID_PADRAO;

  const token = await getToken();
  const { curso, topicos } = await montarFilaRevisao(CURSO_ID, token);

  const porAula: { aula: string; modulo: string; topicos: typeof topicos }[] = [];
  for (const t of topicos) {
    const ultima = porAula[porAula.length - 1];
    if (ultima && ultima.aula === t.aulaTitulo) ultima.topicos.push(t);
    else porAula.push({ aula: t.aulaTitulo, modulo: t.moduloTitulo, topicos: [t] });
  }

  const contagem = {
    rascunho: topicos.filter((t) => t.status === "rascunho").length,
    em_revisao: topicos.filter((t) => t.status === "em_revisao").length,
    aprovado: topicos.filter((t) => t.status === "aprovado").length,
  };

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} hrefMarca="/revisao">
        <span className="text-[var(--tm-accent)]">Revisão</span>
        <Link href="/revisao/alunos" className="hover:text-[var(--tm-accent)]">
          Alunos
        </Link>
        <Link href={`/revisao/curso/${CURSO_ID}`} className="hover:text-[var(--tm-accent)]">
          Governança do curso
        </Link>
        <Link href="/inicio" className="hover:text-[var(--tm-accent)]">
          Ver como aluno
        </Link>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        {cursos.length > 1 && (
          <nav className="flex flex-wrap gap-2 text-[.82rem]">
            {cursos.map((c) => (
              <Link
                key={c.id}
                href={`/revisao?curso=${c.id}`}
                className={
                  c.id === CURSO_ID
                    ? "rounded-[var(--tm-radius-pill)] bg-[var(--tm-accent)] px-3 py-1.5 font-semibold text-[var(--tm-accent-ink,#fff)]"
                    : "rounded-[var(--tm-radius-pill)] border border-[var(--tm-border)] px-3 py-1.5 text-[var(--tm-ink-muted)] hover:border-[var(--tm-accent)]"
                }
              >
                {c.titulo}
              </Link>
            ))}
          </nav>
        )}
        <header className="flex flex-col gap-2">
          <h1 className="m-0 text-[1.6rem]">Fila de revisão — {curso.title}</h1>
          <div className="flex flex-wrap gap-2 text-[.8rem] text-[var(--tm-ink-muted)]">
            <Chip tom="neutro">{contagem.rascunho} rascunho</Chip>
            <Chip tom="aviso">{contagem.em_revisao} em revisão</Chip>
            <Chip tom="bom">{contagem.aprovado} aprovado</Chip>
          </div>
        </header>

        <section className="flex flex-col gap-6">
          {porAula.map((grupo, gi) => (
            <div key={gi} className="flex flex-col gap-2">
              <h2 className="m-0 text-[.78rem] font-semibold uppercase tracking-[.1em] text-[var(--tm-ink-muted)]">
                {grupo.modulo} · {grupo.aula}
              </h2>
              <ol className="m-0 flex list-none flex-col gap-2 p-0">
                {grupo.topicos.map((t) => (
                  <li
                    key={t.id}
                    className="flex flex-col gap-1.5 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex min-w-0 flex-wrap items-center gap-x-3 gap-y-1">
                      <Chip tom={ROTULO_STATUS[t.status].tom}>{ROTULO_STATUS[t.status].texto}</Chip>
                      <span className="font-medium">{t.titulo}</span>
                      {t.referencia_biblica && <Chip tom="info">{t.referencia_biblica}</Chip>}
                      {t.comentariosAbertos > 0 && (
                        <span className="text-[.78rem] text-[var(--tm-warn)]">
                          💬 {t.comentariosAbertos} aberto{t.comentariosAbertos > 1 ? "s" : ""}
                        </span>
                      )}
                      {t.reviewed_by && (
                        <span className="text-[.76rem] text-[var(--tm-ink-muted)]">
                          revisado por {t.reviewed_by}
                        </span>
                      )}
                    </div>
                    {t.status !== "rascunho" ? (
                      <Link
                        href={`/revisao/topico/${t.id}`}
                        className="shrink-0 text-[.82rem] font-semibold text-[var(--tm-accent)] hover:underline"
                      >
                        Revisar →
                      </Link>
                    ) : (
                      <span className="shrink-0 text-[.78rem] text-[var(--tm-ink-muted)]">
                        sem conteúdo ainda
                      </span>
                    )}
                  </li>
                ))}
              </ol>
            </div>
          ))}
          {topicos.length === 0 && (
            <p className="text-[.9rem] text-[var(--tm-ink-muted)]">Nenhum tópico neste curso ainda.</p>
          )}
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
