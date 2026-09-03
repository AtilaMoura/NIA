import type { ReactNode } from "react";
import { Avatar } from "../ui/Avatar";

type AppTopbarProps = {
  avatarInitials: string;
  avatarTitle?: string;
  children?: ReactNode;
};

export function AppTopbar({ avatarInitials, avatarTitle, children }: AppTopbarProps) {
  return (
    <header
      className="flex items-center flex-wrap gap-x-4 gap-y-2 px-[1.15rem] py-[.9rem] border-b"
      style={{ borderColor: "var(--nia-border)", background: "var(--nia-surface)" }}
    >
      <div
        className="flex items-center gap-2 font-bold text-[1.02rem]"
        style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}
      >
        <span
          aria-hidden
          className="w-5 h-5 rounded-[7px] inline-block"
          style={{ background: "var(--nia-accent)" }}
        />
        NIA
      </div>
      <div className="flex-1 flex items-center flex-wrap justify-end gap-x-3 gap-y-2 min-w-0 order-3 sm:order-none basis-full sm:basis-auto">
        {children}
      </div>
      <Avatar initials={avatarInitials} title={avatarTitle} />
    </header>
  );
}
