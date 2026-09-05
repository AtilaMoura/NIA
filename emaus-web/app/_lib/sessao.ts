// Sessão (FASE 1) — SERVER-ONLY (usa next/headers). O token fica só no cookie httpOnly
// `emaus_token` — nunca em JS do navegador. Server Components/Route Handlers chamam
// GET /auth/me com esse token pra confirmar quem é o usuário (a validação de verdade é
// sempre o backend, aqui só lemos o resultado). `emaus_role` é um 2º cookie httpOnly,
// mais barato, só pro middleware (Edge) gatear rota sem precisar decodificar o JWT.
//
// Tipos/rótulos de papel usáveis em Client Components ficam em `./papel.ts` — não
// reexportar next/headers daqui pra lá.

import { cookies } from "next/headers";
import { API_URL } from "./config";
import type { Papel } from "./papel";

export const COOKIE_TOKEN = "emaus_token";
export const COOKIE_ROLE = "emaus_role";
export const MAX_AGE_SESSAO = 60 * 60 * 24 * 30; // 30 dias — acompanha ACCESS_TOKEN_EXPIRE_MINUTES do backend

export type Sessao = {
  id: number;
  name: string | null;
  email: string;
  role: Papel;
};

export async function getSessao(): Promise<Sessao | null> {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return null;
  try {
    const res = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return null;
    return (await res.json()) as Sessao;
  } catch {
    return null;
  }
}

// Token cru — só pra Server Component que precisa chamar um endpoint autenticado de
// LEITURA direto (ex: listar comentários da revisão). Nunca mandar isto pro cliente.
export async function getToken(): Promise<string | null> {
  const jar = await cookies();
  return jar.get(COOKIE_TOKEN)?.value ?? null;
}
