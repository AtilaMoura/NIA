// Proxy autenticado do "Organizar com a IA" do caderno da aula (2026-10-05) —
// mesmo motivo do /api/senha: o token httpOnly nunca sai do servidor. O backend
// junta as anotações da aula + o conteúdo dos slides, chama a IA e salva uma
// versão nova (POST /caderno/aula/{id}/organizar).

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function POST(req: NextRequest, { params }: { params: Promise<{ lessonId: string }> }) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada. Entre de novo." }, { status: 401 });

  const lessonId = Number((await params).lessonId);
  if (!Number.isInteger(lessonId)) return NextResponse.json({ erro: "Aula inválida." }, { status: 400 });

  const { tema } = await req.json().catch(() => ({}));
  const temaSeguro = typeof tema === "string" && /^[a-z0-9-]{1,40}$/.test(tema) ? tema : "";

  const res = await fetch(`${API_URL}/caderno/aula/${lessonId}/organizar?tema=${temaSeguro}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  const corpo = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = typeof corpo.detail === "string" ? corpo.detail : "";
    return NextResponse.json({ erro: msg || "Não deu pra organizar o caderno agora." }, { status: res.status });
  }
  return NextResponse.json(corpo);
}
