import { NextRequest, NextResponse } from "next/server";
import { API_URL } from "../../_lib/config";
import { COOKIE_ROLE, COOKIE_TOKEN, MAX_AGE_SESSAO, type Sessao } from "../../_lib/sessao";

export async function POST(req: NextRequest) {
  const { name, email, password } = await req.json().catch(() => ({}));
  if (!name || !email || !password) {
    return NextResponse.json({ erro: "Preencha nome, e-mail e senha." }, { status: 400 });
  }

  const regRes = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  if (!regRes.ok) {
    const detalhe = await regRes.json().catch(() => ({}));
    return NextResponse.json(
      { erro: detalhe.detail ?? "Não foi possível criar a conta." },
      { status: regRes.status },
    );
  }
  const { access_token: token } = await regRes.json();

  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  const sessao: Sessao = await meRes.json();

  const res = NextResponse.json({ ok: true, sessao });
  const opts = {
    httpOnly: true,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE_SESSAO,
  };
  res.cookies.set(COOKIE_TOKEN, token, opts);
  res.cookies.set(COOKIE_ROLE, sessao.role, opts);
  return res;
}
