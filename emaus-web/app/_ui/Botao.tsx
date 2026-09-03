import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

type Variante = "primario" | "fantasma" | "perigo";
type Tamanho = "sm" | "md";

const BASE =
  "inline-flex items-center justify-center gap-2 font-semibold rounded-[var(--tm-radius-pill)] " +
  "transition-[transform,background-color,border-color] disabled:opacity-50 disabled:pointer-events-none " +
  "active:translate-y-px whitespace-nowrap";

function classes(variante: Variante, tamanho: Tamanho) {
  const size = tamanho === "sm" ? "text-[.8rem] px-3.5 py-1.5" : "text-[.9rem] px-5 py-2.5";
  const look =
    variante === "primario"
      ? "bg-[var(--tm-accent)] text-[var(--tm-bg)] hover:bg-[var(--tm-accent-2)]"
      : variante === "perigo"
        ? "bg-transparent text-[var(--tm-danger)] border border-[var(--tm-danger)] hover:bg-[var(--tm-danger)] hover:text-[var(--tm-bg)]"
        : "bg-transparent text-[var(--tm-ink)] border border-[var(--tm-border)] hover:border-[var(--tm-accent)]";
  return `${BASE} ${size} ${look}`;
}

type BotaoProps = {
  variante?: Variante;
  tamanho?: Tamanho;
  children: ReactNode;
  className?: string;
} & Omit<ComponentProps<"button">, "className" | "children">;

export function Botao({
  variante = "primario",
  tamanho = "md",
  className = "",
  children,
  ...rest
}: BotaoProps) {
  return (
    <button className={`${classes(variante, tamanho)} ${className}`} {...rest}>
      {children}
    </button>
  );
}

type LinkBotaoProps = {
  variante?: Variante;
  tamanho?: Tamanho;
  children: ReactNode;
  className?: string;
  href: string;
} & Omit<ComponentProps<typeof Link>, "className" | "children" | "href">;

export function LinkBotao({
  variante = "primario",
  tamanho = "md",
  className = "",
  children,
  href,
  ...rest
}: LinkBotaoProps) {
  return (
    <Link href={href} className={`${classes(variante, tamanho)} ${className}`} {...rest}>
      {children}
    </Link>
  );
}
