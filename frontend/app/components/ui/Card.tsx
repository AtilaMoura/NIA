import type { HTMLAttributes } from "react";

export function Card({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      {...props}
      className={`bg-[var(--nia-surface)] border border-[var(--nia-border)] rounded-[var(--nia-radius-md)] p-[.95rem] ${className}`}
    />
  );
}
