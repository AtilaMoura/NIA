import Link from "next/link";
import { Logo } from "./Logo";

export function Rodape() {
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
        </nav>
      </div>
    </footer>
  );
}
