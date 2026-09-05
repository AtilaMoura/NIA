"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Avatar } from "./Avatar";
import { Chip } from "./Chip";
import { INFO_PAPEL, type Papel } from "../_lib/papel";
import { itensUsuario } from "../_lib/nav";

// Dropdown do usuário no desktop. No mobile quem cuida disso é o MenuMobile.
export function MenuUsuario({ nome, papel }: { nome: string; papel?: Papel | null }) {
  const [aberto, setAberto] = useState(false);
  const [saindo, setSaindo] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const pathname = usePathname();
  const router = useRouter();

  async function sair() {
    setSaindo(true);
    try {
      await fetch("/api/sessao", { method: "DELETE" });
      router.push("/entrar");
      router.refresh();
    } finally {
      setSaindo(false);
    }
  }

  useEffect(() => setAberto(false), [pathname]);

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
        <span className="hidden items-center gap-1.5 text-[.82rem] text-[var(--tm-ink-muted)] md:flex">
          {nome}
          {papel && <Chip tom={INFO_PAPEL[papel].tom}>{INFO_PAPEL[papel].rotulo}</Chip>}
        </span>
      </button>

      {aberto && (
        <div
          role="menu"
          className="absolute right-0 z-40 mt-2 flex w-52 max-w-[calc(100vw-2rem)] flex-col overflow-hidden rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] py-1 shadow-[var(--tm-shadow)]"
        >
          {itensUsuario(papel).map((i) => (
            <Link
              key={i.href}
              href={i.href}
              role="menuitem"
              className="px-3.5 py-2 text-[.85rem] hover:bg-[var(--tm-surface-2)]"
            >
              {i.rotulo}
            </Link>
          ))}
          <button
            type="button"
            role="menuitem"
            onClick={sair}
            disabled={saindo}
            className="border-t border-[var(--tm-border)] px-3.5 py-2 text-left text-[.85rem] text-[var(--tm-danger)] hover:bg-[var(--tm-surface-2)] disabled:opacity-50"
          >
            {saindo ? "Saindo…" : "Sair"}
          </button>
        </div>
      )}
    </div>
  );
}
