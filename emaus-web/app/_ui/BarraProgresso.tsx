export function BarraProgresso({
  valor,
  rotulo,
  className = "",
}: {
  valor: number;
  rotulo?: string;
  className?: string;
}) {
  const pct = Math.max(0, Math.min(100, Math.round(valor)));
  return (
    <div className={className}>
      {rotulo && (
        <div className="mb-1 flex items-baseline justify-between text-[.78rem] text-[var(--tm-ink-muted)]">
          <span>{rotulo}</span>
          <span className="font-semibold text-[var(--tm-accent)]">{pct}%</span>
        </div>
      )}
      <div
        className="h-2 w-full overflow-hidden rounded-[var(--tm-radius-pill)] bg-[var(--tm-surface-2)]"
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={rotulo ?? "Progresso"}
      >
        <div
          className="h-full rounded-[var(--tm-radius-pill)] bg-[var(--tm-accent)] transition-[width]"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
