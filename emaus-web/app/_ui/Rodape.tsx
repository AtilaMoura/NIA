import Link from "next/link";
import { Logo } from "./Logo";
import { papelPodeRevisar, type Papel } from "../_lib/papel";

export function Rodape({ papel }: { papel?: Papel | null } = {}) {
  return (
    <footer className="mt-16 border-t border-[var(--tm-border)]">
      <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-wrap items-center justify-between gap-3 px-[clamp(1rem,4vw,2rem)] py-7 text-[.75rem] text-[var(--tm-ink-muted)]">
        <Logo size={28} />
        <nav className="flex items-center gap-4">
          <Link href="/" className="hover:text-[var(--tm-accent)]">
            Cursos
          </Link>
          <Link href="/preferencias" className="hover:text-[var(--tm-accent)]">
            Preferências
          </Link>
          {papel && papelPodeRevisar(papel) && (
            <Link href="/revisao" className="hover:text-[var(--tm-accent)]">
              Área de revisão
            </Link>
          )}
        </nav>
      </div>
    </footer>
  );
}
