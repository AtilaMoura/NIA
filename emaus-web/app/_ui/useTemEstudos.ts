"use client";

import { useEffect, useState } from "react";

// "Esta pessoa tem algum estudo liberado?" (2026-10-06) — quem decide é o backend
// (via /api/estudos). Uma pergunta só por carregamento de página, dividida entre
// cabeçalho, menu mobile e rodapé.
let pergunta: Promise<boolean> | null = null;

function perguntar(): Promise<boolean> {
  pergunta ??= fetch("/api/estudos", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : { tem: false }))
    .then((d: { tem?: boolean }) => d.tem === true)
    .catch(() => false);
  return pergunta;
}

export function useTemEstudos(logado: boolean): boolean {
  const [tem, setTem] = useState(false);
  useEffect(() => {
    if (!logado) return;
    let vivo = true;
    perguntar().then((v) => vivo && setTem(v));
    return () => {
      vivo = false;
    };
  }, [logado]);
  return tem;
}
