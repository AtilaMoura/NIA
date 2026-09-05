// Proxy autenticado — aprovar/reprovar a publicação de um curso. Autor sempre vem
// da sessão (o backend confere de novo, e ainda checa se professor é tutor do curso).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { courseId, aprovado, observacao } = await req.json().catch(() => ({}));
  if (!courseId || typeof aprovado !== "boolean") {
    return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });
  }

  const res = await fetch(`${API_URL}/cursos/${courseId}/aprovacao`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ aprovado, observacao: observacao ?? null }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra salvar a aprovação." }, { status: res.status });
  }
  return NextResponse.json(data);
}
