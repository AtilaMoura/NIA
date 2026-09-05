// Proxy autenticado pra marcar progresso de tópico. O user_id NUNCA vem do corpo da
// requisição do cliente — é sempre o dono da sessão (o backend também valida isso,
// esta é a 2ª camada: nem chega a mandar user_id errado).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { topicoId, status } = await req.json().catch(() => ({}));
  if (!topicoId || !status) {
    return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });
  }

  const meRes = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
  if (!meRes.ok) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });
  const { id: userId } = await meRes.json();

  const res = await fetch(`${API_URL}/topico-progress/${topicoId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ user_id: userId, status }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra salvar." }, { status: res.status });
  }
  return NextResponse.json(data);
}
