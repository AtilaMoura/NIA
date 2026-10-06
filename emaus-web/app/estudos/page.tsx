import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { CapaCurso } from "../_ui/CapaCurso";
import { getUser, meusEstudos, resumoEstudo, type ResumoCursoEstudo, type ResumoEstudo } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { cursosDosEstudos, type MeuCurso } from "../_lib/meus-cursos";
import { duracao, quando } from "../_lib/pessoas";

export const metadata: Metadata = { title: "Meus estudos" };

// Meus estudos (redesign 2026-10-04, protótipo 11-estudos.html): painel de quem
// está aprendendo — continuar no slide exato, a semana (tempo por dia, sequência,
// concluídos, reforço) e um cartão por estudo com próximo tópico, tempo e
// anotações. Tempo por dia só existe a partir de 2026-10-04.
// Desde 2026-10-06 vale pra qualquer pessoa: a lista de estudos vem do backend
// (o Master vê todos; os outros, só os que ele liberou). Sem nenhum, 404.
export default async function EstudosPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/estudos");
  const token = await getToken();

  const estudos = await meusEstudos(token).catch(() => []);
  if (estudos.length === 0) notFound();

  const [usuario, cursos, resumo] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    cursosDosEstudos(estudos, sessao, token),
    resumoEstudo(token).catch((): ResumoEstudo | null => null),
  ]);
  const abertos = cursos.filter((c) => c.aberto);
  const doCurso = (c: MeuCurso) => resumo?.cursos.find((r) => r.course_id === c.catalogo.courseId) ?? null;

  // "Continuar de onde parou": o estudo com a atividade mais recente
  const recente = abertos
    .map((c) => ({ c, r: doCurso(c) }))
    .filter((x) => x.r?.ultimo?.atualizado_em)
    .sort((a, b) => (b.r!.ultimo!.atualizado_em! > a.r!.ultimo!.atualizado_em! ? 1 : -1))[0];

  // Semana: só os estudos pessoais (concluídos/reforço); tempo por dia é de tudo
  const resumosPessoais = abertos.map(doCurso).filter((r): r is ResumoCursoEstudo => r != null);
  const reforcos = resumosPessoais.reduce((s, r) => s + r.reforcar.length, 0);
  const maxDia = Math.max(1, ...(resumo?.dias ?? []).map((d) => d.segundos));

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Master"} papel={sessao.role} />

      <main className="mx-auto flex w-full max-w-[1100px] flex-col gap-[clamp(1.5rem,4vw,2.25rem)] px-[clamp(1rem,4vw,2rem)] pb-14 pt-[clamp(1.25rem,4vw,2.25rem)]">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">Meus estudos</h1>
            <p className="m-0 mt-1 text-[var(--tm-ink-muted)]">
              {sessao.role === "master" ? "Você controla quem vê cada estudo em Pessoas." : "Estudos liberados só pra você."}
            </p>
          </div>
          <Link
            href="/anotacoes"
            className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-4 py-2 text-[.9rem] font-semibold hover:border-[var(--tm-accent)]"
          >
            📝 Minhas anotações
          </Link>
        </div>

        {recente && <Continuar curso={recente.c} resumo={recente.r!} />}

        {resumo && (
          <section>
            <h2 className="m-0 mb-3 text-[1.15rem]">Esta semana</h2>
            <div className="grid grid-cols-2 gap-2.5 min-[700px]:grid-cols-4">
              <Numero valor={duracao(resumo.tempo_semana_s)} rotulo="de estudo">
                <div aria-label="Tempo por dia" className="mt-2 flex h-[26px] items-end gap-1">
                  {resumo.dias.map((d) => (
                    <i
                      key={d.dia}
                      title={`${d.dia.slice(8, 10)}/${d.dia.slice(5, 7)}: ${duracao(d.segundos)}`}
                      className={"flex-1 rounded-[3px] " + (d.segundos > 0 ? "bg-[var(--tm-good)]" : "bg-[var(--tm-surface-2)]")}
                      style={{ height: `${Math.max(20, Math.round((d.segundos / maxDia) * 100))}%` }}
                    />
                  ))}
                </div>
              </Numero>
              <Numero valor={String(resumosPessoais.reduce((s, r) => s + r.concluidos_semana, 0))} rotulo="tópicos concluídos" />
              <Numero valor={String(resumo.sequencia_dias)} rotulo={resumo.sequencia_dias === 1 ? "dia seguido estudando" : "dias seguidos estudando"} />
              <Numero valor={String(reforcos)} rotulo="pontos pra reforçar (tutor)" />
            </div>
          </section>
        )}

        <section>
          <h2 className="m-0 mb-3 text-[1.15rem]">Seus estudos</h2>
          <div className="grid gap-4 min-[640px]:grid-cols-2 min-[1000px]:grid-cols-3">
            {cursos.map((c) => (
              <CartaoEstudo key={c.catalogo.slug} curso={c} resumo={doCurso(c)} />
            ))}
          </div>
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}

function Numero({ valor, rotulo, children }: { valor: string; rotulo: string; children?: ReactNode }) {
  return (
    <div className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-3">
      <b className="block text-[1.45rem] leading-tight" style={{ fontFamily: "var(--tm-font-display)" }}>
        {valor}
      </b>
      <span className="text-[.8rem] text-[var(--tm-ink-muted)]">{rotulo}</span>
      {children}
    </div>
  );
}

function Barra({ percent }: { percent: number }) {
  return (
    <span className="block h-1.5 overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
      <i className="block h-full bg-[var(--tm-good)]" style={{ width: `${percent}%` }} />
    </span>
  );
}

// Link pro tópico já no slide onde parou (o render recebe ?slide= 1-based)
function hrefTopico(u: NonNullable<ResumoCursoEstudo["ultimo"]>) {
  return u.ultimo_slide != null && u.ultimo_slide > 0 ? `/topico/${u.topico_id}?slide=${u.ultimo_slide + 1}` : `/topico/${u.topico_id}`;
}

function Continuar({ curso, resumo }: { curso: MeuCurso; resumo: ResumoCursoEstudo }) {
  const u = resumo.ultimo!;
  const slide = u.ultimo_slide != null ? u.ultimo_slide + 1 : null;
  return (
    <article className="grid overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] min-[700px]:grid-cols-[260px_1fr]">
      <div className="relative aspect-[16/7] min-[700px]:aspect-auto min-[700px]:min-h-[150px]">
        <div className="absolute inset-0 [&>div]:h-full">
          <CapaCurso titulo={curso.catalogo.titulo} tom={curso.catalogo.tom} capaUrl={curso.capaUrl} />
        </div>
      </div>
      <div className="flex flex-col gap-2 px-5 py-4">
        <p className="m-0 text-[.72rem] font-bold uppercase tracking-[.12em] text-[var(--tm-accent)]">Continuar de onde parou</p>
        <h3 className="m-0 text-[1.3rem]" style={{ fontFamily: "var(--tm-font-display)" }}>
          {u.titulo}
        </h3>
        <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
          {curso.catalogo.titulo}
          {slide ? ` · parou no slide ${slide}${u.total_slides ? ` de ${u.total_slides}` : ""}` : ""}
          {u.atualizado_em ? ` · ${quando(u.atualizado_em)}` : ""}
        </p>
        <Barra percent={curso.percent} />
        <div className="mt-1 flex flex-wrap gap-2">
          <Link
            href={hrefTopico(u)}
            className="rounded-full bg-[var(--tm-accent)] px-4 py-2 text-[.9rem] font-semibold text-[var(--tm-bg)] hover:bg-[var(--tm-accent-2)]"
          >
            {slide && slide > 1 ? `Continuar no slide ${slide} ▶` : "Continuar ▶"}
          </Link>
          <Link
            href={`/curso/${curso.catalogo.courseId}`}
            className="rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-4 py-2 text-[.9rem] font-semibold hover:border-[var(--tm-accent)]"
          >
            Ver o curso
          </Link>
        </div>
      </div>
    </article>
  );
}

function CartaoEstudo({ curso, resumo }: { curso: MeuCurso; resumo: ResumoCursoEstudo | null }) {
  const proximo = curso.proximo;
  return (
    <article className="flex flex-col overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
      <div className="relative aspect-[16/6]">
        <div className="absolute inset-0 [&>div]:h-full">
          <CapaCurso titulo={curso.catalogo.titulo} tom={curso.catalogo.tom} capaUrl={curso.capaUrl} />
        </div>
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4">
        <h3 className="m-0 text-[1.08rem]" style={{ fontFamily: "var(--tm-font-display)" }}>
          {curso.catalogo.titulo}
        </h3>
        <p className="m-0 flex justify-between text-[.8rem] text-[var(--tm-ink-muted)]">
          <span>
            {curso.concluidos} de {curso.totalTopicos} tópicos
          </span>
          <span>{duracao(resumo?.tempo_s ?? 0)}</span>
        </p>
        <Barra percent={curso.percent} />
        {/* Só o Master recebe esta lista do backend */}
        {curso.liberadoPara.length > 0 && (
          <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">
            Liberado também para: {curso.liberadoPara.map((p) => p.name ?? `#${p.id}`).join(", ")}
          </p>
        )}
        {proximo && (
          <p className="m-0 rounded-[var(--tm-radius)] bg-[var(--tm-surface-2)] px-3 py-2 text-[.88rem]">
            <small className="block text-[.72rem] text-[var(--tm-ink-muted)]">Próximo</small>
            {proximo.titulo}
          </p>
        )}
        <div className="flex flex-wrap gap-1.5">
          {resumo?.reforcar.slice(0, 2).map((t) => (
            <span key={t} className="rounded-full border border-[var(--tm-warn)] px-2 text-[.72rem] font-semibold text-[var(--tm-warn)]">
              Reforçar: {t}
            </span>
          ))}
          {(resumo?.anotacoes ?? 0) > 0 && (
            <Link
              href="/anotacoes"
              className="rounded-full border border-[var(--tm-border)] px-2 text-[.72rem] font-semibold text-[var(--tm-ink-muted)] hover:border-[var(--tm-accent)]"
            >
              📝 {resumo!.anotacoes} {resumo!.anotacoes === 1 ? "anotação" : "anotações"}
            </Link>
          )}
        </div>
        <div className="mt-auto flex gap-2 pt-1.5">
          <Link
            href={proximo ? `/topico/${proximo.id}` : `/curso/${curso.catalogo.courseId}`}
            className="flex-1 rounded-full bg-[var(--tm-accent)] px-3 py-2 text-center text-[.85rem] font-semibold text-[var(--tm-bg)] hover:bg-[var(--tm-accent-2)]"
          >
            {proximo ? "Continuar" : "Ver o curso"}
          </Link>
          {proximo && (
            <Link
              href={`/curso/${curso.catalogo.courseId}`}
              className="flex-1 rounded-full border border-[var(--tm-border)] px-3 py-2 text-center text-[.85rem] font-semibold hover:border-[var(--tm-accent)]"
            >
              Curso
            </Link>
          )}
        </div>
      </div>
    </article>
  );
}
