import Link from "next/link";
import type { ReactNode } from "react";
import { Avatar } from "./Avatar";
import { AlternarTema } from "./AlternarTema";
import { Logo } from "./Logo";

// Cabeçalho fixo. Abaixo de 640px: marca + avatar na 1ª linha, navegação em
// linha própria (scroll horizontal se não couber).
export function CabecalhoApp({
  nomeUsuario,
  hrefMarca = "/inicio",
  children,
}: {
  nomeUsuario?: string | null;
  hrefMarca?: string;
  children?: ReactNode;
}) {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--tm-border)] bg-[var(--tm-bg)]/95 backdrop-blur">
      <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-wrap items-center gap-x-4 gap-y-2 px-[clamp(1rem,4vw,2rem)] py-3">
        <Link href={hrefMarca} aria-label="Emaús — início" className="shrink-0">
          <Logo size={34} />
        </Link>

        <nav className="order-3 -mx-1 flex w-full min-w-0 items-center gap-4 overflow-x-auto px-1 text-[.82rem] text-[var(--tm-ink-muted)] sm:order-2 sm:w-auto sm:flex-1 sm:overflow-visible">
          {children}
        </nav>

        <div className="order-2 ml-auto flex items-center gap-2 sm:order-3 sm:ml-0">
          <AlternarTema />
          {nomeUsuario && (
            <>
              <Avatar nome={nomeUsuario} tamanho="sm" />
              <span className="hidden text-[.82rem] text-[var(--tm-ink-muted)] md:inline">
                {nomeUsuario}
              </span>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
