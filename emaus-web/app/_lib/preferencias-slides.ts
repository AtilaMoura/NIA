import { cookies } from "next/headers";

// Preferências do aluno que valem também nos slides (2026-09-27): o render do backend
// não enxerga os cookies do Emaús, então elas vão na URL do iframe (?modo=&fonte=).
export async function preferenciasDosSlides(): Promise<{ modo: string; fonte: string }> {
  const jar = await cookies();
  const t = jar.get("tm_theme")?.value;
  const f = jar.get("tm_fontsize")?.value;
  return {
    modo: t === "dark" || t === "auto" ? t : "light",
    fonte: f === "sm" || f === "lg" ? f : "md",
  };
}
