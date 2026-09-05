// Proxy autenticado pro checklist de aprovação (área de revisão). O autor nunca vem
// do corpo mandado pelo cliente — é sempre o dono da sessão.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

export async function PUT(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const { topicoId, profundidade, clareza, qualidadeGeral, observacaoFinal, aprovado } = body;
  if (!topicoId || !profundidade || !clareza || !qualidadeGeral || typeof aprovado !== "boolean") {
    return NextResponse.json({ erro: "Preencha as perguntas do checklist." }, { status: 400 });
  }

  const res = await fetch(`${API_URL}/topico-checklists/${topicoId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      profundidade,
      clareza,
      qualidade_geral: qualidadeGeral,
      observacao_final: observacaoFinal ?? null,
      aprovado,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra salvar o checklist." }, { status: res.status });
  }
  return NextResponse.json(data);
}
