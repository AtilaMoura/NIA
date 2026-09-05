// Proxy autenticado pra /preferencias — mesma razão do /api/perfil. Allowlist estrita
// de campos (nunca repassa o body inteiro pro NIA).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

const CAMPOS_PERMITIDOS = new Set(["preferred_panel_mode", "preferred_font_size"]);

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const payload: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(body)) {
    if (CAMPOS_PERMITIDOS.has(k)) payload[k] = v;
  }
  if (Object.keys(payload).length === 0) {
    return NextResponse.json({ erro: "Nada pra salvar." }, { status: 400 });
  }

  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!meRes.ok) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });
  const { id } = await meRes.json();

  const res = await fetch(`${API_URL}/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detalhe = await res.json().catch(() => ({}));
    return NextResponse.json({ erro: detalhe.detail ?? "Não deu pra salvar." }, { status: res.status });
  }
  return NextResponse.json({ ok: true });
}
