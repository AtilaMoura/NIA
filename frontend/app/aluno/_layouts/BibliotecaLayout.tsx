"use client";

import { useState } from "react";
import Link from "next/link";
import { Avatar } from "../../components/ui/Avatar";
import { Badge } from "../../components/ui/Badge";
import { Card } from "../../components/ui/Card";
import { Chip } from "../../components/ui/Chip";
import { ProgressBar } from "../../components/ui/ProgressBar";
import type { CursoComStatus, LayoutProps } from "./types";

const BADGE_VARIANT = { completed: "good", in_progress: "neutral", new: "new" } as const;
const BADGE_LABEL = { completed: "Concluído", in_progress: "Em andamento", new: "Sugerido" } as const;

const FILTROS = [
  { valor: "in_progress", label: "Em andamento" },
  { valor: "completed", label: "Concluídos" },
  { valor: "new", label: "Sugeridos" },
] as const;

function SidebarLink({ label, href, ativo, disabled }: { label: string; href?: string; ativo?: boolean; disabled?: boolean }) {
  const classe = "text-[.85rem] px-[.7rem] py-[.55rem] rounded-[var(--nia-radius-sm)]";
  const estilo = ativo
    ? { background: "color-mix(in srgb, var(--nia-accent) 14%, var(--nia-surface))", color: "var(--nia-accent)", fontWeight: 700 }
    : { color: disabled ? "var(--nia-border)" : "var(--nia-ink-muted)" };
  if (disabled) {
    return (
      <span className={classe} style={estilo} title="Em breve">
        {label}
      </span>
    );
  }
  return (
    <Link href={href ?? "#"} className={classe} style={estilo}>
      {label}
    </Link>
  );
}

// Layout alternativo (escolhido em /aluno/preferencias): sidebar + grade filtrável.
export function BibliotecaLayout({ avatarInitials, avatarTitle, cursos }: LayoutProps) {
  const [filtro, setFiltro] = useState<CursoComStatus["status"]>("in_progress");
  const filtrados = cursos.filter((c) => c.status === filtro);

  return (
    <div className="min-h-screen flex" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <aside
        className="w-[206px] shrink-0 border-r p-[1.1rem_.9rem] flex flex-col gap-6"
        style={{ borderColor: "var(--nia-border)", background: "var(--nia-surface)" }}
      >
        <div className="flex items-center gap-2 font-bold text-[1.02rem]" style={{ fontFamily: "var(--nia-font-display)" }}>
          <span aria-hidden className="w-5 h-5 rounded-[7px] inline-block" style={{ background: "var(--nia-accent)" }} />
          NIA
        </div>
        <nav className="flex flex-col gap-1">
          <SidebarLink label="Meus cursos" href="/aluno" ativo />
          <SidebarLink label="Explorar" href="/aluno/explorar" />
          <SidebarLink label="Progresso" href="/aluno/progresso" />
          <SidebarLink label="Perfil" href="/aluno/perfil" />
        </nav>
        <div className="mt-auto flex flex-col gap-2">
          <div className="flex items-center gap-2 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
            <Avatar initials={avatarInitials} title={avatarTitle} size="sm" />
            <span>{avatarTitle}</span>
          </div>
          <Link href="/aluno/preferencias" className="text-[.75rem]" style={{ color: "var(--nia-ink-muted)" }}>
            Preferências
          </Link>
        </div>
      </aside>

      <main className="flex-1 min-w-0 p-[1.1rem_1.2rem] flex flex-col gap-4">
        <div className="flex items-center gap-2 flex-wrap">
          {FILTROS.map((f) => (
            <Chip key={f.valor} active={filtro === f.valor} onClick={() => setFiltro(f.valor)}>
              {f.label}
            </Chip>
          ))}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-[.85rem]">
          {filtrados.length === 0 && (
            <p className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
              Nenhum curso nesse filtro.
            </p>
          )}
          {filtrados.map(({ course, percent, status, linkLicaoId }) => {
            const conteudo = (
              <>
                <Badge variant={BADGE_VARIANT[status]}>{BADGE_LABEL[status]}</Badge>
                <h4 className="m-0 text-[.92rem] leading-[1.25]" style={{ fontFamily: "var(--nia-font-display)" }}>
                  {course.title}
                </h4>
                <p className="m-0 text-[.75rem]" style={{ color: "var(--nia-ink-muted)" }}>
                  {linkLicaoId ? `${percent}% · ${course.modules_count} módulos` : "Nenhuma lição gerada ainda"}
                </p>
                <ProgressBar value={percent} size="sm" />
              </>
            );
            return linkLicaoId ? (
              <Link key={course.id} href={`/aluno/licoes/${linkLicaoId}`}>
                <Card className="flex flex-col gap-2 h-full hover:border-[var(--nia-accent)] transition-colors">{conteudo}</Card>
              </Link>
            ) : (
              <Card key={course.id} className="flex flex-col gap-2 opacity-70">
                {conteudo}
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
}
