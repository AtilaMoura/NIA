import type { CSSProperties } from "react";

// Marca ilustrada (aquarela) gerada pelo script do Gemini + recorte de fundo
// (scripts/preparar_imagens_emaus.py) em public/marca/emaus-simbolo.png.
// Trocar pra `false` volta pro símbolo SVG.
const MARCA_ILUSTRADA_PRONTA = true;

// Símbolo do Emaús: livro aberto + brasa subindo do centro (Lc 24 — as Escrituras
// abertas e o coração que arde). Usa currentColor no livro e um tom âmbar fixo na
// brasa, pra funcionar em claro e escuro.
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

  if (MARCA_ILUSTRADA_PRONTA) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src="/marca/emaus-simbolo.png"
        alt={decorativo ? "" : "Emaús"}
        width={size}
        height={size}
        className={className}
        style={style}
        {...(decorativo ? { "aria-hidden": true } : {})}
      />
    );
  }

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
      {/* brasa / chama */}
      <path
        d="M20 3.5c2.4 3 3.9 5.2 3.3 8-.4 1.9-1.7 3-3.3 3.2-1.7-.2-3-1.5-3.3-3.2-.6-2.8 1-5 3.3-8z"
        fill="var(--tm-accent-2, #b8763a)"
      />
      <path
        d="M20 7.6c1.1 1.6 1.7 2.8 1.4 4.2-.2 1-.8 1.5-1.4 1.6-.7-.1-1.2-.6-1.4-1.6-.3-1.4.3-2.6 1.4-4.2z"
        fill="var(--tm-gold, #d9a441)"
      />
      {/* páginas do livro aberto */}
      <path
        d="M20 16.8C16.4 14 11.8 13.2 6.5 14.4 5.6 14.6 5 15.4 5 16.3v16.1c0 1.2 1.1 2 2.3 1.8 4.4-.9 8.5-.3 12.7 2.2V16.8z"
        fill="currentColor"
        opacity="0.92"
      />
      <path
        d="M20 16.8C23.6 14 28.2 13.2 33.5 14.4c.9.2 1.5 1 1.5 1.9v16.1c0 1.2-1.1 2-2.3 1.8-4.4-.9-8.5-.3-12.7 2.2V16.8z"
        fill="currentColor"
      />
      {/* vinco central */}
      <path
        d="M20 16.8v23.2"
        stroke="var(--tm-bg, #faf6ee)"
        strokeWidth="1.4"
        strokeLinecap="round"
        opacity="0.5"
      />
    </svg>
  );
}

export function Logo({
  size = 26,
  texto = true,
  className = "",
}: {
  size?: number;
  texto?: boolean;
  className?: string;
}) {
  return (
    <span className={`inline-flex items-center gap-2 text-[var(--tm-accent)] ${className}`}>
      <LogoSimbolo size={size} decorativo={texto} />
      {texto && (
        <span
          style={{ fontFamily: "var(--tm-font-display)" }}
          className="text-[1.15rem] font-semibold tracking-tight text-[var(--tm-ink)]"
        >
          Emaús
        </span>
      )}
    </span>
  );
}
