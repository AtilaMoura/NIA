"use client";

import { useEffect } from "react";
import { Logo } from "./_ui/Logo";
import { Botao } from "./_ui/Botao";

// Erro em qualquer rota (ex.: a API do NIA fora do ar, rate limit, 500).
export default function ErroApp({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("[emaus] erro de página:", error);
  }, [error]);

  const pareceApiFora =
    /fetch failed|ECONNREFUSED|NIA 5\d\d|Failed to fetch|network/i.test(error.message);

  return (
    <main className="mx-auto flex min-h-[80vh] max-w-md flex-col items-start justify-center gap-5 px-[clamp(1rem,4vw,2rem)]">
      <Logo size={24} />
      <h1 className="m-0 text-[1.5rem]">
        {pareceApiFora ? "Não conseguimos falar com o servidor" : "Algo deu errado aqui"}
      </h1>
      <p className="m-0 text-[.92rem] leading-relaxed text-[var(--tm-ink-muted)]">
        {pareceApiFora
          ? "O conteúdo é carregado de um servidor que parece estar fora do ar no momento. Tente de novo em instantes."
          : "Foi um problema inesperado ao montar a página. Você pode tentar recarregar."}
      </p>
      <div className="flex flex-wrap gap-3">
        <Botao onClick={reset}>Tentar de novo</Botao>
        <a
          href="/"
          className="inline-flex items-center text-[.85rem] font-semibold text-[var(--tm-accent)] hover:underline"
        >
          Voltar ao início
        </a>
      </div>
    </main>
  );
}
