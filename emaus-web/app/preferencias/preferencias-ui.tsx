"use client";

import { useState } from "react";
import { setTmFontsize, setTmTheme, type TmFontsize, type TmTheme } from "../_lib/theme";
import { salvarPreferencia } from "../_lib/api";

// Preferências (redesign 2026-09-27, protótipo 09-preferencias.html): aparência com
// "Automático", tamanho do texto numa linha, prévia ao vivo. As escolhas também
// valem pros slides (o Emaús passa ?modo=&fonte= pro render).

// Persiste no banco em paralelo à aplicação imediata no <html>. Fire-and-forget:
// a UI já respondeu; se o PUT falhar, o cookie ainda segura a preferência.
function salvar(campo: "preferred_panel_mode" | "preferred_font_size", valor: string) {
  salvarPreferencia(campo, valor).catch((e) => console.error(`falha ao salvar ${campo}`, e));
}

const MODOS: { valor: TmTheme; rotulo: string; dica: string; amostra: string }[] = [
  { valor: "light", rotulo: "Claro", dica: "Fundo creme", amostra: "linear-gradient(90deg,#faf6ee 60%,#8a5a2b 60% 70%,#faf6ee 70%)" },
  { valor: "dark", rotulo: "Escuro", dica: "Melhor à noite", amostra: "linear-gradient(90deg,#1b1610 60%,#d79b5b 60% 70%,#1b1610 70%)" },
  { valor: "auto", rotulo: "Automático", dica: "Segue o aparelho", amostra: "linear-gradient(90deg,#faf6ee 50%,#1b1610 50%)" },
];

const FONTES: { valor: TmFontsize; rotulo: string; px: number }[] = [
  { valor: "sm", rotulo: "Pequeno", px: 18 },
  { valor: "md", rotulo: "Médio", px: 22 },
  { valor: "lg", rotulo: "Grande", px: 26 },
];

const OPCAO =
  "grid content-start justify-items-start gap-1.5 rounded-[var(--tm-radius)] border p-3 text-left transition-colors";
const OPCAO_ATIVA =
  "border-[var(--tm-accent)] bg-[var(--tm-verse-bg)] shadow-[0_0_0_3px_color-mix(in_srgb,var(--tm-accent)_15%,transparent)]";
const OPCAO_INATIVA = "border-[var(--tm-border)] bg-[var(--tm-surface)] hover:border-[var(--tm-accent)]";

export function Preferencias({ modoInicial, fonteInicial }: { modoInicial: TmTheme; fonteInicial: TmFontsize }) {
  const [modo, setModo] = useState<TmTheme>(modoInicial);
  const [fonte, setFonte] = useState<TmFontsize>(fonteInicial);

  function trocarModo(v: TmTheme) {
    setModo(v);
    setTmTheme(v);
    salvar("preferred_panel_mode", v);
  }

  function trocarFonte(v: TmFontsize) {
    setFonte(v);
    setTmFontsize(v);
    salvar("preferred_font_size", v);
  }

  const cartao = "rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-5";

  return (
    <div className="flex flex-col gap-4">
      <section className={cartao}>
        <h2 className="m-0 text-[1.05rem]">Aparência</h2>
        <p className="m-0 mt-0.5 text-[.88rem] text-[var(--tm-ink-muted)]">Vale pro site e pros slides dos cursos.</p>
        <div role="group" aria-label="Aparência" className="mt-3.5 grid grid-cols-3 gap-2.5">
          {MODOS.map((m) => (
            <button
              key={m.valor}
              type="button"
              aria-pressed={modo === m.valor}
              onClick={() => trocarModo(m.valor)}
              className={`${OPCAO} ${modo === m.valor ? OPCAO_ATIVA : OPCAO_INATIVA}`}
            >
              <span aria-hidden className="h-[34px] w-full rounded-lg border border-[var(--tm-border)]" style={{ background: m.amostra }} />
              <b className="text-[.88rem]">{m.rotulo}</b>
              <small className="hidden text-[.75rem] text-[var(--tm-ink-muted)] min-[421px]:block">{m.dica}</small>
            </button>
          ))}
        </div>
      </section>

      <section className={cartao}>
        <h2 className="m-0 text-[1.05rem]">Tamanho do texto</h2>
        <p className="m-0 mt-0.5 text-[.88rem] text-[var(--tm-ink-muted)]">Nos slides e em todo o site.</p>
        <div role="group" aria-label="Tamanho do texto" className="mt-3.5 grid grid-cols-3 gap-2.5">
          {FONTES.map((f) => (
            <button
              key={f.valor}
              type="button"
              aria-pressed={fonte === f.valor}
              onClick={() => trocarFonte(f.valor)}
              className={`${OPCAO} ${fonte === f.valor ? OPCAO_ATIVA : OPCAO_INATIVA}`}
            >
              <span aria-hidden style={{ fontFamily: "var(--tm-font-display)", fontSize: f.px }} className="leading-none">
                Aa
              </span>
              <b className="text-[.88rem]">{f.rotulo}</b>
            </button>
          ))}
        </div>

        {/* Prévia: usa o tamanho do site (--tm-fs muda com a escolha, na hora) */}
        <div aria-label="Prévia" className="mt-4 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-bg)] px-4 py-3.5">
          <p className="m-0 text-[.7em] font-bold uppercase tracking-[.14em] text-[var(--tm-accent)]">Prévia de um slide</p>
          <p style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 mb-2 mt-1 text-[1.25em] font-semibold">
            Pedras Vivas, Casa Espiritual
          </p>
          <p className="m-0">Pedro vinha construindo uma imagem que explica por que ele chama pessoas comuns de sacerdotes.</p>
          <p
            style={{ fontFamily: "var(--tm-font-display)" }}
            className="m-0 mt-2.5 rounded-r-[10px] border-l-[3px] border-[var(--tm-verse-border)] bg-[var(--tm-verse-bg)] px-3 py-2 text-[.95em] italic"
          >
            “…vós também, quais pedras vivas, sois edificados casa espiritual…” — 1Pe 2.5
          </p>
        </div>
      </section>

      <p className="m-0 text-center text-[.82rem] text-[var(--tm-ink-muted)]">
        ✓ Salvo na sua conta — aparece igual em qualquer aparelho.
      </p>
    </div>
  );
}
