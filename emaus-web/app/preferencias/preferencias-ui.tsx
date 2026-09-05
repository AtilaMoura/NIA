"use client";

import { useState } from "react";
import {
  setTmFontsize,
  setTmTheme,
  type TmFontsize,
  type TmTheme,
} from "../_lib/theme";
import { salvarPreferencia } from "../_lib/api";

// Persiste no banco em paralelo à aplicação imediata no <html>. Fire-and-forget:
// a UI já respondeu; se o PUT falhar, o cookie ainda segura a preferência.
function salvar(campo: "preferred_panel_mode" | "preferred_font_size", valor: string) {
  salvarPreferencia(campo, valor).catch((e) => console.error(`falha ao salvar ${campo}`, e));
}

const MODOS: { valor: TmTheme; rotulo: string }[] = [
  { valor: "light", rotulo: "Claro" },
  { valor: "dark", rotulo: "Escuro" },
];

const FONTES: { valor: TmFontsize; rotulo: string }[] = [
  { valor: "sm", rotulo: "Pequeno" },
  { valor: "md", rotulo: "Médio" },
  { valor: "lg", rotulo: "Grande" },
];

const PREVIEW_PX: Record<TmFontsize, string> = { sm: "15px", md: "17px", lg: "19px" };

export function Preferencias({
  modoInicial,
  fonteInicial,
}: {
  modoInicial: TmTheme;
  fonteInicial: TmFontsize;
}) {
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

  return (
    <div className="flex flex-col gap-8">
      <fieldset className="m-0 flex flex-col gap-2 border-0 p-0">
        <legend className="mb-1 p-0 text-[.95rem] font-semibold">Modo de exibição</legend>
        <div className="inline-flex w-fit overflow-hidden rounded-[var(--tm-radius-pill)] border border-[var(--tm-border)]">
          {MODOS.map((m) => (
            <button
              key={m.valor}
              type="button"
              aria-pressed={modo === m.valor}
              onClick={() => trocarModo(m.valor)}
              className={
                "px-4 py-1.5 text-[.85rem] font-semibold transition-colors " +
                (modo === m.valor
                  ? "bg-[var(--tm-accent)] text-[var(--tm-bg)]"
                  : "text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]")
              }
            >
              {m.rotulo}
            </button>
          ))}
        </div>
      </fieldset>

      <fieldset className="m-0 flex flex-col gap-3 border-0 p-0">
        <legend className="mb-1 p-0 text-[.95rem] font-semibold">Tamanho do texto</legend>
        <div className="flex flex-wrap gap-2">
          {FONTES.map((f) => (
            <button
              key={f.valor}
              type="button"
              aria-pressed={fonte === f.valor}
              onClick={() => trocarFonte(f.valor)}
              className={
                "flex flex-col items-start gap-1 rounded-[var(--tm-radius)] border px-3 py-2 text-left transition-colors " +
                (fonte === f.valor
                  ? "border-[var(--tm-accent)] bg-[var(--tm-verse-bg)]"
                  : "border-[var(--tm-border)] hover:border-[var(--tm-accent)]")
              }
            >
              <span className="text-[.8rem] font-semibold">{f.rotulo}</span>
              <span style={{ fontSize: PREVIEW_PX[f.valor] }} className="text-[var(--tm-ink-muted)]">
                Abrindo as Escrituras
              </span>
            </button>
          ))}
        </div>
      </fieldset>
    </div>
  );
}
