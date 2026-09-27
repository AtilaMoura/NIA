// Iniciais só com letras (antes "Master (Atila)" virava "M(") — ver _lib/nome.ts.
import { iniciais } from "../_lib/nome";

export function Avatar({
  nome,
  tamanho = "md",
  className = "",
}: {
  nome: string;
  tamanho?: "sm" | "md" | "lg";
  className?: string;
}) {
  const dim =
    tamanho === "sm"
      ? "h-7 w-7 text-[.7rem]"
      : tamanho === "lg"
        ? "h-16 w-16 text-[1.4rem]"
        : "h-9 w-9 text-[.8rem]";
  return (
    <span
      title={nome}
      aria-label={nome}
      className={
        "inline-flex shrink-0 items-center justify-center rounded-full font-bold " +
        "bg-[var(--tm-surface-2)] text-[var(--tm-accent)] " +
        dim +
        " " +
        className
      }
    >
      {iniciais(nome)}
    </span>
  );
}
