type AvatarSize = "md" | "sm";

type AvatarProps = {
  initials: string;
  title?: string;
  size?: AvatarSize;
  className?: string;
};

const SIZE_CLASSES: Record<AvatarSize, string> = {
  md: "w-8 h-8 text-[.76rem]",
  sm: "w-[26px] h-[26px] text-[.66rem]",
};

export function Avatar({ initials, title, size = "md", className = "" }: AvatarProps) {
  return (
    <div
      title={title}
      className={`rounded-full bg-[var(--nia-accent)] text-[var(--nia-accent-ink)] flex items-center justify-center font-[family-name:var(--nia-font-display)] font-bold shrink-0 ${SIZE_CLASSES[size]} ${className}`}
    >
      {initials}
    </div>
  );
}
