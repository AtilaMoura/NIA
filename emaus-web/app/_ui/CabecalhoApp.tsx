import Link from "next/link";
import type { ReactNode } from "react";
import { AlternarTema } from "./AlternarTema";
import { MenuUsuario } from "./MenuUsuario";
import { MenuMobile } from "./MenuMobile";
import { Logo } from "./Logo";
import type { Papel } from "../_lib/papel";

// Cabeçalho fixo. Desktop: barra única (marca · navegação · tema+avatar).
// Mobile (<640px): marca · tema · hambúrguer que abre um drawer com a navegação.
// `children` = links de navegação contextuais da página (renderizados nos dois).
export function CabecalhoApp({
  nomeUsuario,
  papel,
  hrefMarca = "/inicio",
  children,
}: {
  nomeUsuario?: string | null;
  papel?: Papel | null;
  hrefMarca?: string;
  children?: ReactNode;
}) {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--tm-border)] bg-[var(--tm-bg)]/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-[var(--tm-maxw)] items-center gap-5 px-[clamp(1rem,4vw,2rem)]">
        <Link href={hrefMarca} aria-label="Emaús — início" className="shrink-0">
          <Logo size={30} />
        </Link>

        <nav className="hidden min-w-0 flex-1 items-center gap-5 text-[.85rem] text-[var(--tm-ink-muted)] sm:flex [&_a:hover]:text-[var(--tm-accent)] [&_a]:transition-colors">
          {children}
        </nav>

        <div className="ml-auto flex items-center gap-2 sm:ml-0">
          <AlternarTema />
          {nomeUsuario && (
            <span className="hidden sm:block">
              <MenuUsuario nome={nomeUsuario} papel={papel ?? null} />
            </span>
          )}
          {!nomeUsuario && (
            <Link
              href="/entrar"
              className="hidden rounded-[var(--tm-radius-pill)] border border-[var(--tm-border)] px-3.5 py-1.5 text-[.82rem] font-semibold hover:border-[var(--tm-accent)] hover:text-[var(--tm-accent)] sm:inline-block"
            >
              Entrar
            </Link>
          )}
          <MenuMobile nome={nomeUsuario} papel={papel ?? null}>
            {children}
          </MenuMobile>
        </div>
      </div>
    </header>
  );
}
