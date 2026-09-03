"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { Chip } from "../../components/ui/Chip";
import { MOODS, useTheme, type ThemeMode } from "../../components/theme/ThemeProvider";
import { getUser, updateUser, type UserPrefs } from "../../lib/api";
import { MOCK_USER_ID } from "../../lib/constants";

type Layout = UserPrefs["preferred_panel_layout"];

const LAYOUTS: { value: Layout; label: string }[] = [
  { value: "retomar", label: "Retomar" },
  { value: "biblioteca", label: "Biblioteca" },
  { value: "trilha", label: "Trilha" },
];

export default function PreferenciasPage() {
  const { mood, theme, setMood, setTheme } = useTheme();
  const [layout, setLayoutState] = useState<Layout>("retomar");
  const [salvo, setSalvo] = useState(false);

  useEffect(() => {
    getUser(MOCK_USER_ID).then((user) => setLayoutState(user.preferred_panel_layout));
  }, []);

  function escolherLayout(next: Layout) {
    setLayoutState(next);
    setSalvo(false);
    updateUser(MOCK_USER_ID, { preferred_panel_layout: next }).then(() => setSalvo(true));
  }

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials="TF" avatarTitle="Usuário de teste Fase 7" />

      <div className="p-[1.15rem] flex flex-col gap-6 max-w-2xl">
        <div>
          <Link href="/aluno" className="text-[.8rem] font-bold" style={{ color: "var(--nia-accent)" }}>
            ← Voltar ao painel
          </Link>
          <h1 className="text-xl font-bold mt-2 mb-0" style={{ fontFamily: "var(--nia-font-display)" }}>
            Preferências
          </h1>
        </div>

        <section className="flex flex-col gap-2">
          <h2 className="text-[.82rem] font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>
            Humor
          </h2>
          <p className="m-0 text-[.75rem]" style={{ color: "var(--nia-ink-muted)" }}>
            A cor conversa com o tipo de curso.
          </p>
          <div className="flex gap-2 flex-wrap">
            {MOODS.map((m) => (
              <Chip key={m.value} active={mood === m.value} onClick={() => setMood(m.value)}>
                {m.label}
              </Chip>
            ))}
          </div>
        </section>

        <section className="flex flex-col gap-2">
          <h2 className="text-[.82rem] font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>
            Modo
          </h2>
          <div className="flex gap-2">
            {(["light", "dark"] as ThemeMode[]).map((t) => (
              <Chip key={t} active={theme === t} onClick={() => setTheme(t)}>
                {t === "light" ? "Claro" : "Escuro"}
              </Chip>
            ))}
          </div>
        </section>

        <section className="flex flex-col gap-2">
          <h2 className="text-[.82rem] font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>
            Layout do painel
          </h2>
          <div className="flex gap-2">
            {LAYOUTS.map((l) => (
              <Chip key={l.value} active={layout === l.value} onClick={() => escolherLayout(l.value)}>
                {l.label}
              </Chip>
            ))}
          </div>
        </section>

        {salvo && (
          <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-good)" }}>
            Salvo — volte ao painel pra ver o novo layout.
          </p>
        )}
      </div>
    </div>
  );
}
