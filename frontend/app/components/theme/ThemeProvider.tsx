"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getUser, updateUser } from "../../lib/api";
import { MOCK_USER_ID } from "../../lib/constants";

export type Mood = "musgo" | "ambar" | "mare" | "framboesa" | "lavanda";
export type ThemeMode = "light" | "dark";

export const MOODS: { value: Mood; label: string; sub: string }[] = [
  { value: "musgo", label: "Musgo", sub: "Bem-estar & Natureza" },
  { value: "ambar", label: "Âmbar", sub: "Negócios & Carreira" },
  { value: "mare", label: "Maré", sub: "Tecnologia & Dados" },
  { value: "framboesa", label: "Framboesa", sub: "Criativo & Comunicação" },
  { value: "lavanda", label: "Lavanda", sub: "Humanas & Idiomas" },
];

const DEFAULT_MOOD: Mood = "musgo";
const DEFAULT_THEME: ThemeMode = "light";

type ThemeContextValue = {
  mood: Mood;
  theme: ThemeMode;
  setMood: (mood: Mood) => void;
  setTheme: (theme: ThemeMode) => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

// Padrão de fábrica travado para o aluno: Musgo, Claro (ver memória "nia-visual-padroes").
// Fase 4: persiste em User.preferred_mood/preferred_panel_mode no backend (MOCK_USER_ID
// até existir login de verdade) — não é mais só localStorage.
export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mood, setMoodState] = useState<Mood>(DEFAULT_MOOD);
  const [theme, setThemeState] = useState<ThemeMode>(DEFAULT_THEME);

  useEffect(() => {
    getUser(MOCK_USER_ID)
      .then((user) => {
        setMoodState((user.preferred_mood as Mood) ?? DEFAULT_MOOD);
        setThemeState(user.preferred_panel_mode ?? DEFAULT_THEME);
      })
      .catch(() => {
        // sem backend disponível, fica no padrão de fábrica
      });
  }, []);

  useEffect(() => {
    document.documentElement.dataset.mood = mood;
    document.documentElement.dataset.theme = theme;
  }, [mood, theme]);

  const setMood = (next: Mood) => {
    setMoodState(next);
    updateUser(MOCK_USER_ID, { preferred_mood: next }).catch(() => {});
  };

  const setTheme = (next: ThemeMode) => {
    setThemeState(next);
    updateUser(MOCK_USER_ID, { preferred_panel_mode: next }).catch(() => {});
  };

  return (
    <ThemeContext.Provider value={{ mood, theme, setMood, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme precisa estar dentro de um ThemeProvider");
  return ctx;
}
