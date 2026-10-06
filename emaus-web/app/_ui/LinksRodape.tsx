"use client";

import Link from "next/link";
import type { Papel } from "../_lib/papel";
import { navPrincipal } from "../_lib/nav";
import { useTemEstudos } from "./useTemEstudos";

// Links do rodapé de quem está logado — os mesmos da barra principal, incluindo
// "Meus estudos" quando o backend diz que a pessoa tem algum (2026-10-06).
export function LinksRodape({ papel }: { papel?: Papel | null }) {
  const temEstudos = useTemEstudos(true);
  return (
    <>
      {navPrincipal(papel, temEstudos).map((i) => (
        <Link key={i.href} href={i.href} className="hover:text-[var(--tm-accent)]">
          {i.rotulo}
        </Link>
      ))}
    </>
  );
}
