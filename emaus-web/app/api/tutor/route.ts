// Proxy autenticado pra avaliação do Tutor. Mesma trava: user_id sempre vem da sessão,
// nunca do corpo mandado pelo cliente.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function POST(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { topicoId, resumoTexto } = await req.json().catch(() => ({}));
  if (!topicoId || !resumoTexto) {
    return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });
  }

  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!meRes.ok) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });
  const { id: userId } = await meRes.json();

  const res = await fetch(`${API_URL}/pipeline/topicos/${topicoId}/avaliar`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ user_id: userId, resumo_texto: resumoTexto }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra falar com o tutor." }, { status: res.status });
  }
  return NextResponse.json(data);
}
