import type { CSSProperties } from "react";

// Símbolo do Emaús — SVG (crisp em qualquer tamanho, do favicon ao herói).
// Livro aberto + brasa subindo do centro: Lc 24, as Escrituras abertas e o
// coração que arde. O livro usa currentColor; a brasa tem tom âmbar fixo, então
// funciona em claro e escuro. Traço reforçado pra ler bem a ~20px.
export function LogoSimbolo({
  size = 28,
  className = "",
  style,
  decorativo = false,
}: {
  size?: number;
  className?: string;
  style?: CSSProperties;
  /** true = puramente decorativo (sai da árvore de acessibilidade) */
  decorativo?: boolean;
}) {
  const a11y = decorativo
    ? { "aria-hidden": true as const }
    : { role: "img" as const, "aria-label": "Emaús" };

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      className={className}
      style={style}
      {...a11y}
    >
      {/* brasa — dois traços, do quente pro claro */}
      <path
        d="M20 2.6c3 3.4 4.6 6 3.9 9.2-.5 2.2-2 3.5-3.9 3.7-2-.2-3.5-1.5-3.9-3.7-.7-3.2.9-5.8 3.9-9.2z"
        fill="var(--tm-accent-2, #b8763a)"
      />
      <path
        d="M20 6.9c1.5 2 2.3 3.5 1.9 5.2-.3 1.2-1 1.8-1.9 2-1-.2-1.6-.8-1.9-2-.4-1.7.4-3.2 1.9-5.2z"
        fill="var(--tm-gold, #d9a441)"
      />
      {/* livro aberto — duas páginas simétricas */}
      <path
        d="M20 17.4C15.9 14.4 10.8 13.6 5.2 15 4.5 15.2 4 15.9 4 16.6v17.2c0 1.1 1 1.9 2.1 1.7 4.6-1 9-.4 13.9 2.3V17.4z"
        fill="currentColor"
      />
      <path
        d="M20 17.4C24.1 14.4 29.2 13.6 34.8 15c.7.2 1.2.9 1.2 1.6v17.2c0 1.1-1 1.9-2.1 1.7-4.6-1-9-.4-13.9 2.3V17.4z"
        fill="currentColor"
        opacity="0.86"
      />
      {/* vinco central */}
      <path
        d="M20 17.4V38"
        stroke="var(--tm-bg, #faf6ee)"
        strokeWidth="1.6"
        strokeLinecap="round"
        opacity="0.55"
      />
    </svg>
  );
}

// Lockup da marca. `orientacao` horizontal (menu) ou empilhada (herói, rodapé).
export function Logo({
  size = 26,
  texto = true,
  orientacao = "horizontal",
  className = "",
}: {
  size?: number;
  texto?: boolean;
  orientacao?: "horizontal" | "empilhado";
  className?: string;
}) {
  const empilhado = orientacao === "empilhado";
  return (
    <span
      className={
        "inline-flex text-[var(--tm-accent)] " +
        (empilhado ? "flex-col items-center gap-1.5 " : "items-center gap-2 ") +
        className
      }
    >
      <LogoSimbolo size={size} decorativo={texto} />
      {texto && (
        <span
          style={{ fontFamily: "var(--tm-font-display)" }}
          className={
            "font-semibold leading-none tracking-[-0.01em] text-[var(--tm-ink)] " +
            (empilhado ? "text-[1.05rem]" : "text-[1.12rem]")
          }
        >
          Emaús
        </span>
      )}
    </span>
  );
}
