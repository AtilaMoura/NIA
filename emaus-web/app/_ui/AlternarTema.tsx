"use client";

import { useEffect, useState } from "react";
import { getTmTheme, setTmTheme, type TmTheme } from "../_lib/theme";

// Botão de modo claro/escuro no cabeçalho. Provisório até a tela /preferencias
// (FASE 4) — mas grava no mesmo cookie `tm_theme` que o layout lê no servidor.
export function AlternarTema({ className = "" }: { className?: string }) {
  const [montado, setMontado] = useState(false);
  const [tema, setTema] = useState<TmTheme>("light");

  useEffect(() => {
    setTema(getTmTheme());
    setMontado(true);
  }, []);

  function trocar() {
    const proximo: TmTheme = tema === "dark" ? "light" : "dark";
    setTmTheme(proximo);
    setTema(proximo);
  }

  const base =
    "inline-flex h-8 w-8 items-center justify-center rounded-full border border-[var(--tm-border)] " +
    "text-[.9rem] text-[var(--tm-ink-muted)] hover:border-[var(--tm-accent)] hover:text-[var(--tm-accent)] " +
    className;

  // Antes de montar: placeholder do mesmo tamanho, sem ícone (evita mismatch de hidratação).
  if (!montado) {
    return <span className={base} aria-hidden />;
  }

  return (
    <button
      type="button"
      onClick={trocar}
      className={base}
      aria-label={tema === "dark" ? "Mudar para o modo claro" : "Mudar para o modo escuro"}
      title={tema === "dark" ? "Modo claro" : "Modo escuro"}
    >
      {tema === "dark" ? "☀" : "☾"}
    </button>
  );
}
