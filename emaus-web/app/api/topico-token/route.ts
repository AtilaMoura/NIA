// Renova o token de escopo curto (2h) do render do tópico sem recarregar o <iframe> (NIA-T-030).
// Quem pede é sempre o dono da sessão (cookie); o backend emite o token para ele.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function POST(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const topicoId = Number(body.topicoId);
  if (!Number.isInteger(topicoId)) return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });

  const res = await fetch(`${API_URL}/auth/topico-token`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ topico_id: topicoId, somente_leitura: false }),
    cache: "no-store",
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || typeof data.access_token !== "string") {
    return NextResponse.json({ erro: "Não deu pra renovar a sessão." }, { status: res.ok ? 502 : res.status });
  }
  return NextResponse.json({ token: data.access_token });
}
