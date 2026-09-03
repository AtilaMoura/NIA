type ProgressBarSize = "md" | "sm";

type ProgressBarProps = {
  value: number;
  size?: ProgressBarSize;
  label?: string;
  className?: string;
};

const TRACK_HEIGHT: Record<ProgressBarSize, string> = {
  md: "h-2",
  sm: "h-1.5",
};

export function ProgressBar({ value, size = "md", label, className = "" }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={`flex items-center gap-[.6rem] ${className}`}>
      <div
        className={`flex-1 ${TRACK_HEIGHT[size]} rounded-[var(--nia-radius-pill)] bg-[var(--nia-surface2)] border border-[var(--nia-border)] overflow-hidden`}
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div className="h-full rounded-[inherit] bg-[var(--nia-accent)]" style={{ width: `${clamped}%` }} />
      </div>
      {label && (
        <span className="font-[family-name:var(--nia-font-mono)] text-[.76rem] text-[var(--nia-ink-muted)] tabular-nums">
          {label}
        </span>
      )}
    </div>
  );
}
