"use client";

import { useState } from "react";

// Input de senha com botão Mostrar/Ocultar (telas de acesso). `autoComplete`
// diferencia login (current-password) de cadastro (new-password) — é isso que
// impede o navegador de preencher o cadastro com a senha salva.
export function CampoSenha({
  valor,
  aoMudar,
  autoComplete,
  minLength,
}: {
  valor: string;
  aoMudar: (v: string) => void;
  autoComplete: "current-password" | "new-password";
  minLength?: number;
}) {
  const [visivel, setVisivel] = useState(false);
  return (
    <span className="relative block">
      <input
        type={visivel ? "text" : "password"}
        name="password"
        required
        minLength={minLength}
        autoComplete={autoComplete}
        value={valor}
        onChange={(e) => aoMudar(e.target.value)}
        // padding à direita pro texto não passar por baixo do botão (inline pra vencer .acesso-cartao input)
        style={{ paddingRight: "5rem" }}
      />
      <button
        type="button"
        onClick={() => setVisivel((v) => !v)}
        aria-label={visivel ? "Ocultar senha" : "Mostrar senha"}
        className="vidro-destaque absolute right-1.5 top-1/2 -translate-y-1/2 px-2 py-1.5 text-[.78rem] font-semibold"
      >
        {visivel ? "Ocultar" : "Mostrar"}
      </button>
    </span>
  );
}
