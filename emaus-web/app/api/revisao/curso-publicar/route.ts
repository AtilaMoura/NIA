// Proxy autenticado — publicar (POST) ou despublicar (PUT) um curso. O backend
// decide de novo se quem chama pode (master sempre; outros só se as condições
// de aprovação já bateram; despublicar é só master).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

async function encaminhar(req: NextRequest, caminho: string) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { courseId } = await req.json().catch(() => ({}));
  if (!courseId) return NextResponse.json({ erro: "Curso não informado." }, { status: 400 });

  const res = await fetch(`${API_URL}/cursos/${courseId}/${caminho}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra completar a ação." }, { status: res.status });
  }
  return NextResponse.json(data);
}

export async function POST(req: NextRequest) {
  return encaminhar(req, "publicar");
}

export async function PUT(req: NextRequest) {
  return encaminhar(req, "despublicar");
}
