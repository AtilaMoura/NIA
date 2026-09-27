"use client";

import { useRef, type ReactNode } from "react";

// Fileira horizontal com setas (desktop) e deslize (touch). Sem barra de rolagem
// aparente; a borda direita esmaece pra indicar que tem mais itens.
export function FileiraRolavel({ titulo, children }: { titulo: string; children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const rolar = (dir: 1 | -1) =>
    ref.current?.scrollBy({ left: dir * ref.current.clientWidth * 0.8, behavior: "smooth" });

  const seta =
    "grid h-[30px] w-[30px] place-items-center rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] text-[var(--tm-ink)] hover:border-[var(--tm-accent)]";

  return (
    <section>
      <div className="mb-3.5 flex items-center justify-between gap-4">
        <h2 className="m-0 text-[1.15rem]">{titulo}</h2>
        <div className="hidden gap-1.5 sm:flex">
          <button type="button" className={seta} onClick={() => rolar(-1)} aria-label="Anteriores">
            ‹
          </button>
          <button type="button" className={seta} onClick={() => rolar(1)} aria-label="Próximos">
            ›
          </button>
        </div>
      </div>
      <div
        ref={ref}
        className="flex snap-x snap-mandatory gap-3 overflow-x-auto pb-1 [mask-image:linear-gradient(90deg,#000_88%,transparent)] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      >
        {children}
      </div>
    </section>
  );
}
