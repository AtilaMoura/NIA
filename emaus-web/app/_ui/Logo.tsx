import type { CSSProperties } from "react";

// Símbolo do Emaús — logo 1 escolhido em 2026-09-26: o "E" com a estrada laranja
// e o arco do sol (Lc 24, o caminho de Emaús). Recortado da prancha gerada
// (public/marca/originais/logo1-prancha.png) com fundo transparente, em 2 versões:
// E preto (tema claro) e E creme (tema escuro). O CSS em globals.css mostra só a
// versão do tema ativo. Os logos 2 (chama/coração) e 3 (pão/estrada) ficam
// guardados em public/marca/final/ como alternativas.
// O antigo SVG (livro + brasa) está em public/marca/originais/icon-antigo-livro-brasa.svg.

// Proporção do recorte (239 x 203 px) — `size` define a ALTURA.
const PROPORCAO = 239 / 203;

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
  const largura = Math.round(size * PROPORCAO);
  const alt = decorativo ? "" : "Emaús";

  return (
    <span
      className={"inline-flex shrink-0 " + className}
      style={{ width: largura, height: size, ...style }}
      {...(decorativo ? { "aria-hidden": true as const } : {})}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/marca/final/logo1-simbolo.png"
        alt={alt}
        width={largura}
        height={size}
        className="logo-tema-claro h-full w-full object-contain"
      />
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/marca/final/logo1-simbolo-escuro.png"
        alt={alt}
        width={largura}
        height={size}
        className="logo-tema-escuro h-full w-full object-contain"
      />
    </span>
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
