"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Avatar } from "./Avatar";

const ITENS = [
  { href: "/perfil", rotulo: "Perfil" },
  { href: "/progresso", rotulo: "Progresso" },
  { href: "/preferencias", rotulo: "Preferências" },
];

export function MenuUsuario({ nome }: { nome: string }) {
  const [aberto, setAberto] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const pathname = usePathname();

  // Fecha ao navegar.
  useEffect(() => setAberto(false), [pathname]);

  // Fecha no Escape / clique fora.
  useEffect(() => {
    if (!aberto) return;
    function aoTeclar(e: KeyboardEvent) {
      if (e.key === "Escape") setAberto(false);
    }
    function aoClicar(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setAberto(false);
    }
    document.addEventListener("keydown", aoTeclar);
    document.addEventListener("mousedown", aoClicar);
    return () => {
      document.removeEventListener("keydown", aoTeclar);
      document.removeEventListener("mousedown", aoClicar);
    };
  }, [aberto]);

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setAberto((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={aberto}
        className="flex items-center gap-2 rounded-[var(--tm-radius-pill)] border border-transparent px-1 py-0.5 hover:border-[var(--tm-border)]"
      >
        <Avatar nome={nome} tamanho="sm" />
        <span className="hidden text-[.82rem] text-[var(--tm-ink-muted)] md:inline">{nome}</span>
      </button>

      {aberto && (
        <div
          role="menu"
          className="absolute right-0 z-40 mt-2 flex w-44 max-w-[calc(100vw-2rem)] flex-col overflow-hidden rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] py-1 shadow-[var(--tm-shadow)]"
        >
          {ITENS.map((i) => (
            <Link
              key={i.href}
              href={i.href}
              role="menuitem"
              className="px-3.5 py-2 text-[.85rem] hover:bg-[var(--tm-surface-2)]"
            >
              {i.rotulo}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
