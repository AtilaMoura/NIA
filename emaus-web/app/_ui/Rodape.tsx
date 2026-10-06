import Link from "next/link";
import { Logo } from "./Logo";
import type { Papel } from "../_lib/papel";
import { LinksRodape } from "./LinksRodape";

// Rodapé único, numa linha só (2026-09-28, protótipo 10-pessoas.html): logo +
// assinatura à esquerda, links à direita. Logado mostra os links da barra
// principal (cientes do papel); visitante, Entrar/Criar conta.
export function Rodape({
  papel,
  logado = true,
}: {
  papel?: Papel | null;
  logado?: boolean;
} = {}) {
  const itensVisitante = [
    { href: "/entrar", rotulo: "Entrar" },
    { href: "/criar-conta", rotulo: "Criar conta" },
  ];

  // Visitante sem margem no topo: a página já termina numa faixa de fechamento
  return (
    <footer className={(logado ? "mt-12 " : "") + "border-t border-[var(--tm-border)] bg-[var(--tm-bg)]"}>
      <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-wrap items-center justify-between gap-x-6 gap-y-3 px-[clamp(1rem,4vw,2rem)] py-5">
        <div className="flex items-center gap-3">
          <Logo size={22} />
          <span className="text-[.78rem] text-[var(--tm-ink-muted)]">· plataforma de formação bíblica</span>
        </div>
        <nav className="flex flex-wrap items-center gap-x-5 gap-y-1.5 text-[.85rem] text-[var(--tm-ink-muted)]">
          {logado ? (
            <LinksRodape papel={papel} />
          ) : (
            itensVisitante.map((i) => (
              <Link key={i.href} href={i.href} className="hover:text-[var(--tm-accent)]">
                {i.rotulo}
              </Link>
            ))
          )}
        </nav>
      </div>
    </footer>
  );
}
