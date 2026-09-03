import type { ReactNode } from "react";

export function Card({
  children,
  interativo = false,
  className = "",
}: {
  children: ReactNode;
  interativo?: boolean;
  className?: string;
}) {
  return (
    <section
      className={
        "rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] " +
        "shadow-[var(--tm-shadow)] " +
        (interativo ? "transition-transform hover:-translate-y-0.5 focus-within:-translate-y-0.5 " : "") +
        className
      }
    >
      {children}
    </section>
  );
}
