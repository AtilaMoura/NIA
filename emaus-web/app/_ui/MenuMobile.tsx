"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Avatar } from "./Avatar";
import { Chip } from "./Chip";
import { INFO_PAPEL, type Papel } from "../_lib/papel";
import { ITENS_AVATAR, NAV_DESLOGADO, NAV_REVISAO, navPrincipal } from "../_lib/nav";

// Menu do mobile: hambúrguer + painel deslizante. Mesma navegação do desktop.
export function MenuMobile({ nome, papel }: { nome?: string | null; papel?: Papel | null }) {
  const [aberto, setAberto] = useState(false);
  const [saindo, setSaindo] = useState(false);
  const pathname = usePathname();
  const router = useRouter();
  const logado = !!nome;

  useEffect(() => setAberto(false), [pathname]);

  useEffect(() => {
    if (!aberto) return;
    function aoTeclar(e: KeyboardEvent) {
      if (e.key === "Escape") setAberto(false);
    }
    document.addEventListener("keydown", aoTeclar);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", aoTeclar);
      document.body.style.overflow = "";
    };
  }, [aberto]);

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

  const principal = logado ? navPrincipal(papel) : NAV_DESLOGADO;
  const naRevisao = pathname.startsWith("/revisao");

  return (
    <div className="sm:hidden">
      <button
        type="button"
        onClick={() => setAberto(true)}
        aria-label="Abrir menu"
        aria-expanded={aberto}
        className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--tm-radius)] border border-[var(--tm-border)] text-[var(--tm-ink)]"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
      </button>

      {aberto && (
        <div className="fixed inset-0 z-50">
          <button
            type="button"
            aria-label="Fechar menu"
            onClick={() => setAberto(false)}
            className="absolute inset-0 bg-black/40 backdrop-blur-[1px]"
          />
          <div className="absolute right-0 top-0 flex h-full w-[min(20rem,86vw)] flex-col gap-1 overflow-y-auto border-l border-[var(--tm-border)] bg-[var(--tm-surface)] p-4 shadow-[var(--tm-shadow)]">
            <div className="mb-2 flex items-center justify-between">
              {logado ? (
                <span className="flex items-center gap-2">
                  <Avatar nome={nome!} tamanho="sm" />
                  <span className="text-[.9rem] font-semibold">{nome}</span>
                  {papel && <Chip tom={INFO_PAPEL[papel].tom}>{INFO_PAPEL[papel].rotulo}</Chip>}
                </span>
              ) : (
                <span className="text-[.9rem] font-semibold">Menu</span>
              )}
              <button
                type="button"
                onClick={() => setAberto(false)}
                aria-label="Fechar"
                className="inline-flex h-8 w-8 items-center justify-center rounded-[var(--tm-radius)] text-[var(--tm-ink-muted)] hover:bg-[var(--tm-surface-2)]"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
                  <path d="M6 6l12 12M18 6L6 18" />
                </svg>
              </button>
            </div>

            <nav className="flex flex-col gap-0.5 border-b border-[var(--tm-border)] pb-2 text-[.9rem]">
              {principal.map((i) => (
                <Link key={i.href} href={i.href} className="rounded-[var(--tm-radius)] px-2 py-2 hover:bg-[var(--tm-surface-2)]">
                  {i.rotulo}
                </Link>
              ))}
            </nav>

            {logado && naRevisao && (
              <nav className="flex flex-col gap-0.5 border-b border-[var(--tm-border)] py-1 pl-2 text-[.85rem] text-[var(--tm-ink-muted)]">
                {NAV_REVISAO.map((i) => (
                  <Link key={i.href} href={i.href} className="rounded-[var(--tm-radius)] px-2 py-2 hover:bg-[var(--tm-surface-2)]">
                    {i.rotulo}
                  </Link>
                ))}
              </nav>
            )}

            {logado ? (
              <>
                <nav className="flex flex-col gap-0.5 pt-1 text-[.9rem]">
                  {ITENS_AVATAR.map((i) => (
                    <Link key={i.href} href={i.href} className="rounded-[var(--tm-radius)] px-2 py-2 hover:bg-[var(--tm-surface-2)]">
                      {i.rotulo}
                    </Link>
                  ))}
                </nav>
                <button
                  type="button"
                  onClick={sair}
                  disabled={saindo}
                  className="mt-auto rounded-[var(--tm-radius)] border border-[var(--tm-border)] px-2 py-2 text-left text-[.9rem] text-[var(--tm-danger)] hover:bg-[var(--tm-surface-2)] disabled:opacity-50"
                >
                  {saindo ? "Saindo…" : "Sair"}
                </button>
              </>
            ) : (
              <Link
                href="/entrar"
                className="mt-2 rounded-[var(--tm-radius-pill)] bg-[var(--tm-accent)] px-3 py-2 text-center text-[.9rem] font-semibold text-[var(--tm-bg)]"
              >
                Entrar
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
