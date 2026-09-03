import type { ReactNode } from "react";

const tons = {
  neutro: "bg-[var(--tm-surface-2)] text-[var(--tm-ink-muted)] border-[var(--tm-border)]",
  info: "bg-[var(--tm-verse-bg)] text-[var(--tm-accent)] border-[var(--tm-verse-border)]",
  bom: "bg-transparent text-[var(--tm-good)] border-[var(--tm-good)]",
  aviso: "bg-transparent text-[var(--tm-warn)] border-[var(--tm-warn)]",
} as const;

export function Chip({
  children,
  tom = "neutro",
  className = "",
}: {
  children: ReactNode;
  tom?: keyof typeof tons;
  className?: string;
}) {
  return (
    <span
      className={
        "inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] border px-2.5 py-0.5 " +
        "text-[.72rem] font-semibold leading-tight " +
        tons[tom] +
        " " +
        className
      }
    >
      {children}
    </span>
  );
}
