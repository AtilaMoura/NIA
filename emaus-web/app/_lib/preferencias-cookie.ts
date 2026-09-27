import type { NextResponse } from "next/server";
import { getUser } from "./api";

// No login, os cookies de tema/fonte (fast-path do SSR, lidos no root layout)
// passam a ser os da conta que entrou. Antes eles ficavam os da conta anterior
// no mesmo navegador — ex.: Master voltava em tema escuro depois de o Aluno
// usar escuro (2026-09-27). Sem preferência salva, volta pro padrão.
export async function gravarCookiesPreferencias(
  res: NextResponse,
  userId: number,
  token: string,
): Promise<void> {
  const usuario = await getUser(userId, token).catch(() => null);
  const tema = usuario?.preferred_panel_mode === "dark" ? "dark" : "light";
  const fs = usuario?.preferred_font_size;
  const fonte = fs === "sm" || fs === "lg" ? fs : "md";

  // Mesmas opções que _lib/theme.ts usa no cliente (não é httpOnly: o botão de
  // tema no navegador precisa reescrever o mesmo cookie)
  const opts = { path: "/", maxAge: 31536000, sameSite: "lax" as const };
  res.cookies.set("tm_theme", tema, opts);
  res.cookies.set("tm_fontsize", fonte, opts);
}
