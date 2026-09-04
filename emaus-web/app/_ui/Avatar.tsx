function iniciais(nome: string): string {
  const p = nome.trim().split(/\s+/).filter(Boolean);
  if (p.length === 0) return "?";
  if (p.length === 1) return p[0].slice(0, 2).toUpperCase();
  return (p[0][0] + p[p.length - 1][0]).toUpperCase();
}

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
