"use client";

// Troca tema/tamanho de fonte. Grava cookie (lido pelo root layout no próximo
// request, sem flash) e aplica no <html> na hora (sem reload).

export type TmTheme = "light" | "dark";
export type TmFontsize = "sm" | "md" | "lg";

function setCookie(nome: string, valor: string) {
  document.cookie = `${nome}=${valor}; path=/; max-age=31536000; samesite=lax`;
}

export function getTmTheme(): TmTheme {
  return document.documentElement.dataset.tmTheme === "dark" ? "dark" : "light";
}

export function setTmTheme(v: TmTheme) {
  setCookie("tm_theme", v);
  document.documentElement.setAttribute("data-tm-theme", v);
}

export function toggleTmTheme() {
  setTmTheme(getTmTheme() === "dark" ? "light" : "dark");
}

export function getTmFontsize(): TmFontsize {
  const v = document.documentElement.dataset.tmFontsize;
  return v === "sm" || v === "lg" ? v : "md";
}

export function setTmFontsize(v: TmFontsize) {
  setCookie("tm_fontsize", v);
  document.documentElement.setAttribute("data-tm-fontsize", v);
}
