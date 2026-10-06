// Proxy autenticado — o Master libera ou pausa um estudo privado pra uma pessoa
// (2026-10-06). Quem decide se pode é o backend (só Master; 403 pros outros).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { userId, courseId, status } = await req.json().catch(() => ({}));
  if (!userId || !courseId || !status) {
    return NextResponse.json({ erro: "Pessoa, estudo e situação são obrigatórios." }, { status: 400 });
  }

  const res = await fetch(`${API_URL}/matriculas/pessoa/${userId}/curso/${courseId}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra mudar o acesso." }, { status: res.status });
  }
  return NextResponse.json(data);
}
