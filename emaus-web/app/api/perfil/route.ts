// Proxy autenticado: só o dono da sessão consegue editar o próprio nome. O token
// httpOnly nunca sai do servidor — é por isso que este endpoint existe (um Client
// Component não tem como anexar Authorization: Bearer sozinho).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { name } = await req.json().catch(() => ({}));
  if (!name || typeof name !== "string") {
    return NextResponse.json({ erro: "Nome inválido." }, { status: 400 });
  }

  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!meRes.ok) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });
  const { id } = await meRes.json();

  const res = await fetch(`${API_URL}/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) {
    const detalhe = await res.json().catch(() => ({}));
    return NextResponse.json({ erro: detalhe.detail ?? "Não deu pra salvar." }, { status: res.status });
  }
  return NextResponse.json({ ok: true });
}
