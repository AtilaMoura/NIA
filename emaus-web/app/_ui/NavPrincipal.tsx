"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Papel } from "../_lib/papel";
import {
  NAV_DESLOGADO,
  navRevisao,
  itemAtivo,
  navPrincipal,
} from "../_lib/nav";
import { useTemEstudos } from "./useTemEstudos";

// Barra de navegação do desktop. Idêntica em toda tela; só ganha "Revisão" se o
// usuário for revisor. Dentro de /revisao/* aparece uma 2ª linha com a sub-nav.
export function NavPrincipal({
  papel,
  logado,
}: {
  papel?: Papel | null;
  logado: boolean;
}) {
  const pathname = usePathname();
  const temEstudos = useTemEstudos(logado);
  const itens = logado ? navPrincipal(papel, temEstudos) : NAV_DESLOGADO;
  const naRevisao = pathname.startsWith("/revisao");

  return (
    <nav className="hidden min-w-0 flex-1 items-center gap-1 whitespace-nowrap text-[.85rem] sm:flex">
      {itens.map((i) => {
        const ativo = itemAtivo(pathname, i.href);
        return (
          <Link
            key={i.href}
            href={i.href}
            aria-current={ativo ? "page" : undefined}
            className={
              "rounded-full px-3 py-1.5 transition-colors " +
              (ativo
                ? "bg-[var(--tm-surface-2)] font-semibold text-[var(--tm-ink)]"
                : "text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]")
            }
          >
            {i.rotulo}
          </Link>
        );
      })}

      {logado && naRevisao && (
        <span className="ml-2 flex items-center gap-4 border-l border-[var(--tm-border)] pl-5 text-[.82rem]">
          {navRevisao(papel).map((i) => {
            const ativo =
              i.href === "/revisao"
                ? pathname === "/revisao" || pathname.startsWith("/revisao/curso") || pathname.startsWith("/revisao/topico")
                : pathname.startsWith(i.href);
            return (
              <Link
                key={i.href}
                href={i.href}
                aria-current={ativo ? "page" : undefined}
                className={
                  ativo
                    ? "font-semibold text-[var(--tm-ink)]"
                    : "text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]"
                }
              >
                {i.rotulo}
              </Link>
            );
          })}
        </span>
      )}
    </nav>
  );
}
