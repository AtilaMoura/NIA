import Link from "next/link";
import { Logo } from "./Logo";
import type { Papel } from "../_lib/papel";
import { navPrincipal } from "../_lib/nav";

// Rodapé único — mesmos links da barra principal (cientes do papel). `versiculo`
// destaca a citação de Lc 24.32 (usado na landing).
export function Rodape({
  papel,
  logado = true,
  versiculo = false,
}: {
  papel?: Papel | null;
  logado?: boolean;
  versiculo?: boolean;
} = {}) {
  // Visitante (página de visitante, 2026-09-26): rodapé compacto numa linha só —
  // logo + assinatura à esquerda, Entrar/Criar conta à direita. Sem margem no
  // topo porque a página já termina numa faixa de fechamento.
  if (!logado) {
    return (
      <footer className="border-t border-[var(--tm-border)] bg-[var(--tm-bg)]">
        <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-wrap items-center justify-between gap-x-6 gap-y-3 px-[clamp(1rem,4vw,2rem)] py-5">
          <div className="flex items-center gap-3">
            <Logo size={22} />
            <span className="text-[.78rem] text-[var(--tm-ink-muted)]">· plataforma de formação bíblica</span>
          </div>
          <nav className="flex items-center gap-5 text-[.85rem] text-[var(--tm-ink-muted)]">
            <Link href="/entrar" className="hover:text-[var(--tm-accent)]">
              Entrar
            </Link>
            <Link href="/criar-conta" className="hover:text-[var(--tm-accent)]">
              Criar conta
            </Link>
          </nav>
        </div>
      </footer>
    );
  }

  const itens = navPrincipal(papel);

  return (
    <footer className="mt-16 border-t border-[var(--tm-border)] bg-[var(--tm-bg)]">
      <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-12">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex max-w-sm flex-col gap-3">
            <Logo size={26} />
            {versiculo && (
              <p
                className="m-0 text-[.9rem] italic leading-relaxed text-[var(--tm-ink-muted)]"
                style={{ fontFamily: "var(--tm-font-display)" }}
              >
                “Não estava ardendo o nosso coração, quando ele nos falava pelo caminho e nos
                abria as Escrituras?” — Lucas 24.32
              </p>
            )}
          </div>
          <nav className="flex flex-col gap-2 text-[.85rem] text-[var(--tm-ink-muted)]">
            {itens.map((i) => (
              <Link key={i.href} href={i.href} className="hover:text-[var(--tm-accent)]">
                {i.rotulo}
              </Link>
            ))}
          </nav>
        </div>
        <p className="m-0 border-t border-[var(--tm-border)] pt-6 text-[.72rem] text-[var(--tm-ink-muted)]">
          Emaús · plataforma de formação bíblica
        </p>
      </div>
    </footer>
  );
}
