export type EstadoTopico = "concluido" | "atual" | "disponivel" | "em_preparacao";

const cfg: Record<EstadoTopico, { texto: string; icone: string; cls: string }> = {
  concluido: { texto: "Concluído", icone: "✓", cls: "text-[var(--tm-good)] border-[var(--tm-good)]" },
  atual: {
    texto: "Continuar",
    icone: "▸",
    cls: "text-[var(--tm-accent)] border-[var(--tm-accent)] bg-[var(--tm-verse-bg)]",
  },
  disponivel: { texto: "Disponível", icone: "○", cls: "text-[var(--tm-ink-muted)] border-[var(--tm-border)]" },
  em_preparacao: {
    texto: "Em preparação",
    icone: "…",
    cls: "text-[var(--tm-ink-muted)] border-dashed border-[var(--tm-border)]",
  },
};

export function Selo({ estado, className = "" }: { estado: EstadoTopico; className?: string }) {
  const c = cfg[estado];
  return (
    <span
      className={
        "inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] border px-2.5 py-0.5 " +
        "text-[.72rem] font-semibold leading-tight " +
        c.cls +
        " " +
        className
      }
    >
      <span aria-hidden>{c.icone}</span>
      {c.texto}
    </span>
  );
}
