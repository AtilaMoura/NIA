import type { HTMLAttributes } from "react";

type BadgeVariant = "neutral" | "good" | "bad" | "info" | "new";

type BadgeProps = HTMLAttributes<HTMLSpanElement> & {
  variant?: BadgeVariant;
};

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  neutral: "bg-[color-mix(in_srgb,var(--nia-accent)_16%,var(--nia-surface))] text-[var(--nia-accent)]",
  good: "bg-[color-mix(in_srgb,var(--nia-good)_18%,var(--nia-surface))] text-[var(--nia-good)]",
  bad: "bg-[color-mix(in_srgb,var(--nia-bad)_16%,var(--nia-surface))] text-[var(--nia-bad)]",
  info: "bg-[color-mix(in_srgb,var(--nia-info)_16%,var(--nia-surface))] text-[var(--nia-info)]",
  new: "bg-[color-mix(in_srgb,var(--nia-ink)_8%,var(--nia-surface))] text-[var(--nia-ink-muted)]",
};

export function Badge({ variant = "neutral", className = "", ...props }: BadgeProps) {
  return (
    <span
      {...props}
      className={`inline-block font-[family-name:var(--nia-font-mono)] text-[.65rem] px-[.55rem] py-[.2rem] rounded-[var(--nia-radius-pill)] uppercase tracking-[.04em] ${VARIANT_CLASSES[variant]} ${className}`}
    />
  );
}
