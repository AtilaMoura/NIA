import type { ReactNode } from "react";
import Link from "next/link";

// Fileira horizontal estilo streaming (redesign 2026-09-21, ver
// PLANO_REDESIGN_EMAUS.md Fase 2) — usada tanto pra "Continuar estudando"
// quanto pras prateleiras por categoria na home.
export function Prateleira({
  titulo,
  hrefVerTudo,
  children,
}: {
  titulo: string;
  hrefVerTudo?: string;
  children: ReactNode;
}) {
  return (
    <section className="flex flex-col gap-3">
      <div className="flex items-center justify-between gap-3">
        <h2 className="m-0 text-[.95rem] font-bold">{titulo}</h2>
        {hrefVerTudo && (
          <Link href={hrefVerTudo} className="text-[.76rem] font-semibold text-[var(--tm-accent)] hover:underline">
            Ver categoria →
          </Link>
        )}
      </div>
      <div className="flex gap-3 overflow-x-auto pb-2">{children}</div>
    </section>
  );
}
