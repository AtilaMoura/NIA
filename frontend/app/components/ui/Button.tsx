import type { ButtonHTMLAttributes } from "react";

type ButtonVariant = "accent" | "ghost";
type ButtonSize = "md" | "sm";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  size?: ButtonSize;
};

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  accent: "bg-[var(--nia-accent)] text-[var(--nia-accent-ink)] border-transparent",
  ghost: "bg-transparent text-[var(--nia-ink)] border-[var(--nia-border)]",
};

const SIZE_CLASSES: Record<ButtonSize, string> = {
  md: "px-5 py-[.62rem] text-[.84rem]",
  sm: "px-[.85rem] py-[.4rem] text-[.74rem]",
};

export function Button({ variant = "accent", size = "md", className = "", ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`font-[family-name:var(--nia-font-display)] font-bold rounded-[var(--nia-radius-pill)] border cursor-pointer ${VARIANT_CLASSES[variant]} ${SIZE_CLASSES[size]} ${className}`}
    />
  );
}
