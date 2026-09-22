import Link from "next/link";
import { CapaCurso } from "./CapaCurso";
import type { TomCurso } from "../_lib/catalogo";

// Cartão horizontal "continue estudando", 1 por curso em andamento — vira a
// prateleira de topo da home (redesign 2026-09-21, ver
// PLANO_REDESIGN_EMAUS.md Fase 2), no lugar do hero de tela cheia antigo.
export function CartaoContinuar({
  nomeCurso,
  tituloTopico,
  percent,
  tom,
  capaUrl,
  href,
}: {
  nomeCurso: string;
  tituloTopico: string;
  percent: number;
  tom: TomCurso;
  capaUrl: string | null;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="flex w-[280px] shrink-0 items-center gap-3 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-2.5 hover:border-[var(--tm-accent)]"
    >
      <CapaCurso
        titulo={tituloTopico}
        tom={tom}
        capaUrl={capaUrl}
        aspecto="1/1"
        className="h-16 w-16 shrink-0 rounded-[10px]"
      />
      <div className="min-w-0 flex-1">
        <div className="truncate text-[.68rem] font-bold uppercase tracking-wide text-[var(--tm-accent)]">
          {nomeCurso}
        </div>
        <div className="truncate text-[.86rem] font-bold text-[var(--tm-ink)]">{tituloTopico}</div>
        <div className="mt-1 h-1 overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
          <div className="h-full rounded-full bg-[var(--tm-good)]" style={{ width: `${percent}%` }} />
        </div>
      </div>
    </Link>
  );
}
