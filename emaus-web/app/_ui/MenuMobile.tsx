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

  // Item de menu com ícone num quadrado suave — redesign 2026-09-21 (ver
  // PLANO_REDESIGN_EMAUS.md Fase 5): antes era link plano sem ícone/hierarquia.
  function ItemMenu({ href, rotulo, icone }: { href: string; rotulo: string; icone?: string }) {
    const ativo = pathname === href || (href !== "/" && pathname.startsWith(href));
    return (
      <Link
        href={href}
        className={
          "flex items-center gap-3 rounded-[var(--tm-radius)] px-2 py-2 text-[.92rem] font-semibold " +
          (ativo ? "bg-[color-mix(in_srgb,var(--tm-accent)_10%,transparent)]" : "hover:bg-[var(--tm-surface-2)]")
        }
      >
        <span
          aria-hidden
          className={
            "flex h-[30px] w-[30px] shrink-0 items-center justify-center rounded-[9px] text-[.95rem] " +
            (ativo ? "bg-[var(--tm-accent)] text-[var(--tm-bg)]" : "bg-[var(--tm-surface-2)]")
          }
        >
          {icone}
        </span>
        {rotulo}
      </Link>
    );
  }

  return (
    <div className="sm:hidden">
      <button
        type="button"
        onClick={() => setAberto((v) => !v)}
        aria-label={aberto ? "Fechar menu" : "Abrir menu"}
        aria-expanded={aberto}
        className="inline-flex h-9 w-9 items-center justify-center rounded-[var(--tm-radius)] border border-[var(--tm-border)] text-[var(--tm-ink)]"
      >
        {aberto ? (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
            <path d="M6 6l12 12M18 6L6 18" />
          </svg>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
            <path d="M4 7h16M4 12h16M4 17h16" />
          </svg>
        )}
      </button>

      {/* Painel INLINE embaixo da barra (não é mais um drawer lateral com
          backdrop) — fica claro que é parte da mesma página, mesmo padrão
          aprovado no mockup de 2026-09-21. 'fixed top-14' (não 'absolute') de
          propósito: o botão fica fundo numa pilha de flex containers com
          largura própria, então 'absolute' ficaria preso a essa largura
          estreita em vez de cobrir a tela toda — 'fixed' ancora no viewport,
          independente de onde o botão está aninhado. top-14 = mesma altura
          (h-14) do cabeçalho fixo em CabecalhoApp.tsx. */}
      {aberto && (
        <div className="fixed inset-x-0 top-14 z-50 flex flex-col gap-1 border-b border-[var(--tm-border)] bg-[var(--tm-surface)] p-4 shadow-[var(--tm-shadow)]">
          {logado && (
            <div className="mb-1 flex items-center gap-2 border-b border-[var(--tm-border)] pb-3">
              <Avatar nome={nome!} tamanho="sm" />
              <span className="text-[.9rem] font-semibold">{nome}</span>
              {papel && <Chip tom={INFO_PAPEL[papel].tom}>{INFO_PAPEL[papel].rotulo}</Chip>}
            </div>
          )}

          <nav className="flex flex-col gap-0.5">
            {principal.map((i) => (
              <ItemMenu key={i.href} href={i.href} rotulo={i.rotulo} icone={i.icone} />
            ))}
          </nav>

          {logado && naRevisao && (
            <nav className="flex flex-col gap-0.5 border-t border-[var(--tm-border)] pt-1 text-[.85rem] text-[var(--tm-ink-muted)]">
              {NAV_REVISAO.map((i) => (
                <Link key={i.href} href={i.href} className="rounded-[var(--tm-radius)] px-2 py-2 pl-[2.6rem] hover:bg-[var(--tm-surface-2)]">
                  {i.rotulo}
                </Link>
              ))}
            </nav>
          )}

          {logado ? (
            <>
              <span className="mt-2 px-2 text-[.68rem] font-bold uppercase tracking-wide text-[var(--tm-ink-muted)]">
                Conta
              </span>
              <nav className="flex flex-col gap-0.5">
                {ITENS_AVATAR.map((i) => (
                  <ItemMenu key={i.href} href={i.href} rotulo={i.rotulo} icone={i.icone} />
                ))}
              </nav>
              <button
                type="button"
                onClick={sair}
                disabled={saindo}
                className="mt-2 flex items-center gap-2 rounded-[var(--tm-radius)] border border-[color-mix(in_srgb,var(--tm-danger)_35%,var(--tm-border))] bg-[color-mix(in_srgb,var(--tm-danger)_6%,transparent)] px-3 py-2 text-left text-[.88rem] font-bold text-[var(--tm-danger)] hover:bg-[color-mix(in_srgb,var(--tm-danger)_12%,transparent)] disabled:opacity-50"
              >
                <span aria-hidden>↪</span> {saindo ? "Saindo…" : "Sair"}
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
      )}
    </div>
  );
}
