// Login rápido de DEV — nunca em produção. As credenciais de teste ficam só aqui no
// servidor (nunca vão pro bundle do cliente); o botão em /entrar só manda qual perfil
// quer, este handler é quem sabe a senha. Mesmo login de verdade por baixo (POST
// /auth/login no NIA) — não é bypass de segurança, só evita digitar a cada teste.

import { NextRequest, NextResponse } from "next/server";
import { API_URL } from "../../../_lib/config";
import { COOKIE_ROLE, COOKIE_TOKEN, MAX_AGE_SESSAO, type Sessao } from "../../../_lib/sessao";

const SENHA_TESTE = "emaus2026";

const PERFIS_DEV = [
  { id: "master", email: "master@emaus.local", rotulo: "Master (Atila)" },
  { id: "admin1", email: "admin1@emaus.local", rotulo: "Admin 1" },
  { id: "professor1", email: "professor1@emaus.local", rotulo: "Professor 1" },
  { id: "aluno", email: "teste-fase7@nia.local", rotulo: "Aluno" },
] as const;

export function GET() {
  if (process.env.NODE_ENV === "production") {
    return NextResponse.json({ erro: "Indisponível em produção." }, { status: 404 });
  }
  return NextResponse.json({ perfis: PERFIS_DEV.map(({ id, rotulo }) => ({ id, rotulo })) });
}

export async function POST(req: NextRequest) {
  if (process.env.NODE_ENV === "production") {
    return NextResponse.json({ erro: "Indisponível em produção." }, { status: 404 });
  }
  const { perfil } = await req.json().catch(() => ({}));
  const alvo = PERFIS_DEV.find((p) => p.id === perfil);
  if (!alvo) {
    return NextResponse.json({ erro: "Perfil de teste desconhecido." }, { status: 400 });
  }

  const loginRes = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: alvo.email, password: SENHA_TESTE }),
  });
  if (!loginRes.ok) {
    return NextResponse.json({ erro: "Usuário de teste não encontrado — rode o seed." }, { status: 500 });
  }
  const { access_token: token } = await loginRes.json();
  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  const sessao: Sessao = await meRes.json();

  const res = NextResponse.json({ ok: true, sessao });
  const opts = { httpOnly: true, sameSite: "lax" as const, secure: false, path: "/", maxAge: MAX_AGE_SESSAO };
  res.cookies.set(COOKIE_TOKEN, token, opts);
  res.cookies.set(COOKIE_ROLE, sessao.role, opts);
  return res;
}
