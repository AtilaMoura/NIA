// Proxy autenticado pra recomeçar um tópico (2026-09-15). O backend identifica
// o aluno pelo token de sessão — não precisa (nem aceita) user_id no corpo.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function POST(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { topicoId } = await req.json().catch(() => ({}));
  if (!topicoId) {
    return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });
  }

  const res = await fetch(`${API_URL}/topico-progress/${topicoId}/reiniciar`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra recomeçar." }, { status: res.status });
  }
  return NextResponse.json(data);
}
