import Link from "next/link";
import { CapaCurso } from "./CapaCurso";
import type { MeuCurso } from "../_lib/meus-cursos";
import { tituloCurto } from "../_lib/catalogo";

// Cartões da home do aluno (redesign 2026-09-27, protótipo aprovado em
// prototipos-front/03-inicio.html). Substituem Prateleira/PosterCurso/CartaoContinuar.

function BarraProgressoCurso({ percent, rotulo }: { percent: number; rotulo: string }) {
  return (
    <div className="flex items-center gap-3 text-[.82rem] text-[var(--tm-ink-muted)]">
      <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
        <span
          className="block h-full rounded-full bg-[var(--tm-good)]"
          style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
        />
      </span>
      {rotulo}
    </div>
  );
}

/** Cartão grande "Continuar estudando" — capa ao lado (tablet+) ou em cima (celular). */
export function CartaoContinuar({ curso }: { curso: MeuCurso }) {
  const t = curso.proximo!;
  const nomeCurso = tituloCurto(curso.catalogo);
  const detalhe = [t.referencia_biblica, t.aulaTitulo].filter(Boolean).join(" · ");

  return (
    <article className="grid overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] shadow-[var(--tm-shadow)] sm:grid-cols-[300px_1fr]">
      {/* Contêiner fixo em volta da capa: o CapaCurso é w-full + aspecto próprio,
          e classe de largura passada direto nele não vence (bug do cartão antigo). */}
      <div className="relative aspect-[16/7] sm:aspect-auto sm:min-h-[190px]">
        <div className="absolute inset-0 [&>div]:h-full">
          <CapaCurso titulo={curso.catalogo.titulo} tom={curso.catalogo.tom} capaUrl={curso.capaUrl} />
        </div>
      </div>
      <div className="flex flex-col gap-1.5 p-5 sm:justify-center sm:px-7 sm:py-6">
        <p className="m-0 text-[.7rem] font-bold uppercase tracking-[.12em] text-[var(--tm-accent)]">
          {nomeCurso}
          {t.moduloTitulo ? ` · ${t.moduloTitulo}` : ""}
        </p>
        <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 text-[1.25rem] leading-snug">
          {t.titulo}
        </h3>
        {detalhe && <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">{detalhe}</p>}
        <div className="mt-2">
          <BarraProgressoCurso percent={curso.percent} rotulo={`${curso.percent}% do curso`} />
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-4">
          <Link
            href={`/topico/${t.id}`}
            className="inline-flex items-center justify-center rounded-[var(--tm-radius-pill)] bg-[var(--tm-accent)] px-5 py-2.5 text-[.92rem] font-semibold text-[var(--tm-bg)] hover:bg-[var(--tm-accent-2)]"
          >
            Continuar →
          </Link>
          <Link
            href={`/curso/${curso.catalogo.courseId}`}
            className="text-[.85rem] font-semibold text-[var(--tm-accent)] hover:underline"
          >
            Ver o curso
          </Link>
        </div>
      </div>
    </article>
  );
}

/** Cartão de curso aberto (grade "Seus cursos"): capa 16:9, título inteiro, progresso. */
export function CartaoCurso({ curso }: { curso: MeuCurso }) {
  const c = curso.catalogo;
  return (
    <Link
      href={`/curso/${c.courseId}`}
      className="flex flex-col overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] shadow-[var(--tm-shadow)] transition-transform hover:-translate-y-1"
    >
      <div className="relative aspect-[16/9]">
        <div className="absolute inset-0 [&>div]:h-full">
          <CapaCurso titulo={c.titulo} tom={c.tom} capaUrl={curso.capaUrl} />
        </div>
        {curso.soRevisores && (
          <span className="absolute left-3 top-3 rounded-[var(--tm-radius-pill)] bg-black/60 px-2.5 py-1 text-[.7rem] font-semibold text-white">
            Em revisão · só revisores
          </span>
        )}
      </div>
      <div className="flex flex-1 flex-col gap-1 p-4">
        <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 line-clamp-2 text-[1.02rem] leading-snug">
          {c.titulo}
        </h3>
        <p className="m-0 text-[.82rem] font-semibold text-[var(--tm-accent)]">{c.subtitulo}</p>
        <div className="mt-auto pt-3">
          <BarraProgressoCurso
            percent={curso.percent}
            rotulo={curso.percent > 0 ? `${curso.percent}%` : "Não iniciado"}
          />
        </div>
      </div>
    </Link>
  );
}

/** Miniatura de curso "em breve" (fileira compacta). */
export function MiniaturaEmBreve({ curso }: { curso: MeuCurso }) {
  const c = curso.catalogo;
  return (
    <div className="w-[150px] flex-none snap-start" aria-label={`${c.titulo} — em breve`}>
      <div className="relative aspect-[4/3] overflow-hidden rounded-[var(--tm-radius)] border border-[var(--tm-border)] saturate-[.8]">
        <div className="absolute inset-0 [&>div]:h-full">
          <CapaCurso titulo={c.titulo} tom={c.tom} capaUrl={curso.capaUrl} />
        </div>
        <span aria-hidden className="absolute right-1.5 top-1 text-[.7rem]">
          🔒
        </span>
      </div>
      <p className="m-0 mt-1.5 text-[.8rem] font-semibold leading-snug">{c.titulo}</p>
    </div>
  );
}
