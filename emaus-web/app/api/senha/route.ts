// Proxy autenticado da troca de senha (perfil, 2026-09-27) — mesmo motivo do
// /api/perfil: o token httpOnly nunca sai do servidor. O backend confere a senha
// atual (POST /auth/trocar-senha).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function POST(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada. Entre de novo." }, { status: 401 });

  const { senhaAtual, senhaNova } = await req.json().catch(() => ({}));
  if (typeof senhaAtual !== "string" || typeof senhaNova !== "string" || !senhaAtual || !senhaNova) {
    return NextResponse.json({ erro: "Preencha a senha atual e a nova." }, { status: 400 });
  }

  const res = await fetch(`${API_URL}/auth/trocar-senha`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ senha_atual: senhaAtual, senha_nova: senhaNova }),
  });
  if (!res.ok) {
    const detalhe = await res.json().catch(() => ({}));
    // 422 do Pydantic vem como lista; pega a mensagem do validador
    const msg =
      typeof detalhe.detail === "string"
        ? detalhe.detail
        : Array.isArray(detalhe.detail)
          ? String(detalhe.detail[0]?.msg ?? "").replace(/^Value error, /, "")
          : "";
    return NextResponse.json({ erro: msg || "Não deu pra trocar a senha." }, { status: res.status });
  }
  return NextResponse.json({ ok: true });
}
