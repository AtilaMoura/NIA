"use client";

import { MOODS, useTheme, type ThemeMode } from "../../components/theme/ThemeProvider";
import { Avatar } from "../../components/ui/Avatar";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Chip } from "../../components/ui/Chip";
import { ProgressBar } from "../../components/ui/ProgressBar";

// Página de verificação da Fase 1 — não faz parte da navegação final do produto.
export default function DesignSystemPage() {
  const { mood, theme, setMood, setTheme } = useTheme();

  return (
    <div
      className="min-h-screen p-8 flex flex-col gap-8"
      style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}
    >
      <header className="flex flex-col gap-1">
        <p
          className="text-[.72rem] uppercase tracking-[.14em] m-0"
          style={{ color: "var(--nia-accent)", fontFamily: "var(--nia-font-display)" }}
        >
          NIA — Fase 1
        </p>
        <h1 className="text-2xl font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>
          Design system componentizado
        </h1>
      </header>

      <section className="flex flex-wrap gap-8 p-5 rounded-[var(--nia-radius-lg)] border" style={{ background: "var(--nia-surface)", borderColor: "var(--nia-border)" }}>
        <div className="flex flex-col gap-2">
          <span className="text-[.82rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>Humor</span>
          <div className="flex gap-2 flex-wrap">
            {MOODS.map((m) => (
              <Chip key={m.value} active={mood === m.value} onClick={() => setMood(m.value)}>
                {m.label}
              </Chip>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <span className="text-[.82rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>Modo</span>
          <div className="flex gap-2">
            {(["light", "dark"] as ThemeMode[]).map((t) => (
              <Chip key={t} active={theme === t} onClick={() => setTheme(t)}>
                {t === "light" ? "Claro" : "Escuro"}
              </Chip>
            ))}
          </div>
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>Button</h2>
        <div className="flex gap-3 items-center flex-wrap">
          <Button variant="accent">Continuar estudando</Button>
          <Button variant="ghost">Editar foco</Button>
          <Button variant="accent" size="sm">Continuar</Button>
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>Badge</h2>
        <div className="flex gap-2 items-center flex-wrap">
          <Badge variant="neutral">Em andamento</Badge>
          <Badge variant="good">Aprovado</Badge>
          <Badge variant="bad">Reprovado</Badge>
          <Badge variant="info">Gerando</Badge>
          <Badge variant="new">Sugerido</Badge>
        </div>
      </section>

      <section className="flex flex-col gap-4 max-w-md">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>ProgressBar</h2>
        <ProgressBar value={62} label="62%" />
        <ProgressBar value={30} size="sm" />
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>Avatar</h2>
        <div className="flex gap-3 items-center">
          <Avatar initials="MA" title="Marina" />
          <Avatar initials="AT" title="Atila" size="sm" />
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>Chip</h2>
        <div className="flex gap-2">
          <Chip active>Em andamento</Chip>
          <Chip>Concluídos</Chip>
          <Chip>Sugeridos</Chip>
        </div>
      </section>

      <section className="flex flex-col gap-4 max-w-sm">
        <h2 className="text-lg font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>Card</h2>
        <Card className="flex flex-col gap-2">
          <Badge variant="neutral">Em andamento</Badge>
          <h4 className="m-0 text-[.92rem]" style={{ fontFamily: "var(--nia-font-display)" }}>
            Marketing Digital com IA
          </h4>
          <p className="m-0 text-[.75rem]" style={{ color: "var(--nia-ink-muted)" }}>
            4 módulos · 11 tópicos
          </p>
          <ProgressBar value={30} size="sm" />
        </Card>
      </section>
    </div>
  );
}
