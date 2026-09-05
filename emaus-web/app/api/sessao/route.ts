// Route Handler de sessão — é o único lugar que vê o JWT antes de ele virar cookie
// httpOnly. POST loga (chama /auth/login + /auth/me no NIA), DELETE desloga.

import { NextRequest, NextResponse } from "next/server";
import { API_URL } from "../../_lib/config";
import { COOKIE_ROLE, COOKIE_TOKEN, MAX_AGE_SESSAO, type Sessao } from "../../_lib/sessao";

function gravarCookiesSessao(res: NextResponse, token: string, sessao: Sessao) {
  const opts = {
    httpOnly: true,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: MAX_AGE_SESSAO,
  };
  res.cookies.set(COOKIE_TOKEN, token, opts);
  res.cookies.set(COOKIE_ROLE, sessao.role, opts);
}

export async function POST(req: NextRequest) {
  const { email, password } = await req.json().catch(() => ({}));
  if (!email || !password) {
    return NextResponse.json({ erro: "E-mail e senha são obrigatórios." }, { status: 400 });
  }

  const loginRes = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!loginRes.ok) {
    const detalhe = await loginRes.json().catch(() => ({}));
    return NextResponse.json(
      { erro: detalhe.detail ?? "E-mail ou senha inválidos." },
      { status: 401 },
    );
  }
  const { access_token: token } = await loginRes.json();

  const meRes = await fetch(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (!meRes.ok) {
    return NextResponse.json({ erro: "Não foi possível confirmar a sessão." }, { status: 500 });
  }
  const sessao: Sessao = await meRes.json();

  const res = NextResponse.json({ ok: true, sessao });
  gravarCookiesSessao(res, token, sessao);
  return res;
}

export async function DELETE() {
  const res = NextResponse.json({ ok: true });
  res.cookies.delete(COOKIE_TOKEN);
  res.cookies.delete(COOKIE_ROLE);
  return res;
}
