// Proxy autenticado — "esta pessoa tem algum estudo liberado?" (2026-10-06). Usado
// pela navegação (Client Component) pra mostrar ou não o link "Meus estudos". Quem
// decide é o backend (GET /estudo/meus-estudos); aqui só se conta.

import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function GET() {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ tem: false });

  const res = await fetch(`${API_URL}/estudo/meus-estudos`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  const lista = res.ok ? await res.json().catch(() => []) : [];
  return NextResponse.json({ tem: Array.isArray(lista) && lista.length > 0 });
}
