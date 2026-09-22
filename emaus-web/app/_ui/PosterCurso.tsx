import Link from "next/link";
import { CapaCurso } from "./CapaCurso";
import type { TomCurso } from "../_lib/catalogo";

// Cartão vertical tipo pôster de streaming, 1 por curso — usado nas
// prateleiras por categoria da home (redesign 2026-09-21, ver
// PLANO_REDESIGN_EMAUS.md Fase 2).
export function PosterCurso({
  titulo,
  subtitulo,
  tom,
  capaUrl,
  href,
  bloqueado = false,
  percentConcluido,
}: {
  titulo: string;
  subtitulo: string;
  tom: TomCurso;
  capaUrl: string | null;
  href?: string;
  bloqueado?: boolean;
  percentConcluido?: number;
}) {
  const capa = (
    <div className="relative">
      <CapaCurso titulo={titulo} tom={tom} capaUrl={capaUrl} aspecto="3/4" className="rounded-[var(--tm-radius-lg)]" />
      {bloqueado ? (
        <span className="absolute right-2 top-2 inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] bg-black/50 px-2 py-0.5 text-[.66rem] font-semibold text-white backdrop-blur">
          🔒 Em breve
        </span>
      ) : (
        percentConcluido != null &&
        percentConcluido > 0 && (
          <span className="absolute bottom-2 left-2 inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] bg-black/50 px-2 py-0.5 text-[.66rem] font-semibold text-white">
            {percentConcluido}%
          </span>
        )
      )}
    </div>
  );

  const legenda = (
    <>
      <div className="mt-2 truncate text-[.8rem] font-bold text-[var(--tm-ink)]">{titulo}</div>
      <div className="truncate text-[.72rem] text-[var(--tm-ink-muted)]">{subtitulo}</div>
    </>
  );

  if (href && !bloqueado) {
    return (
      <Link href={href} className="w-[168px] shrink-0">
        {capa}
        {legenda}
      </Link>
    );
  }
  return (
    <div className="w-[168px] shrink-0 opacity-75">
      {capa}
      {legenda}
    </div>
  );
}
