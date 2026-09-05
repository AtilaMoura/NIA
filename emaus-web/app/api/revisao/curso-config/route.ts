// Proxy autenticado — configurar tutores e regras de aprovação de um curso.
// O backend confere de novo que quem chama é master/admin.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const { courseId, aprovacaoMasterBasta, aprovacaoExigeTodosTutores, tutorIds } = await req
    .json()
    .catch(() => ({}));
  if (!courseId) return NextResponse.json({ erro: "Curso não informado." }, { status: 400 });

  const res = await fetch(`${API_URL}/cursos/${courseId}/config`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      aprovacao_master_basta: !!aprovacaoMasterBasta,
      aprovacao_exige_todos_tutores: !!aprovacaoExigeTodosTutores,
      tutor_ids: Array.isArray(tutorIds) ? tutorIds : [],
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra salvar a configuração." }, { status: res.status });
  }
  return NextResponse.json(data);
}
