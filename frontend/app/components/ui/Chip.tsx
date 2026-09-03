import type { ButtonHTMLAttributes } from "react";

type ChipProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  active?: boolean;
};

export function Chip({ active = false, className = "", ...props }: ChipProps) {
  const stateClasses = active
    ? "bg-[var(--nia-accent)] text-[var(--nia-accent-ink)] border-[var(--nia-accent)]"
    : "bg-[var(--nia-surface)] text-[var(--nia-ink-muted)] border-[var(--nia-border)]";
  return (
    <button
      type="button"
      {...props}
      className={`font-[family-name:var(--nia-font-body)] text-[.79rem] px-[.85rem] py-[.4rem] rounded-[var(--nia-radius-pill)] border cursor-pointer ${stateClasses} ${className}`}
    />
  );
}
