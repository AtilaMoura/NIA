// Proxy autenticado pra anotação de slide (área de revisão). O autor nunca vem do
// corpo mandado pelo cliente — é sempre o dono da sessão; o backend confere de novo.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../../_lib/config";
import { COOKIE_TOKEN } from "../../../_lib/sessao";

async function encaminhar(
  req: NextRequest,
  montarChamada: (token: string, body: Record<string, unknown>) => Promise<Response>,
) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });
  const body = await req.json().catch(() => ({}));
  const res = await montarChamada(token, body);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    return NextResponse.json({ erro: data.detail ?? "Não deu pra salvar." }, { status: res.status });
  }
  return NextResponse.json(data);
}

export async function POST(req: NextRequest) {
  return encaminhar(req, (token, body) =>
    fetch(`${API_URL}/topico-comments/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        topico_id: body.topicoId,
        slide_index: body.slideIndex ?? null,
        reacao: body.reacao ?? null,
        imagem_sugerida: body.imagemSugerida ?? null,
        sobre_imagem: !!body.sobreImagem,
        texto: body.texto ?? null,
      }),
    }),
  );
}

export async function PUT(req: NextRequest) {
  return encaminhar(req, (token, body) =>
    fetch(`${API_URL}/topico-comments/${body.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ texto: body.texto, resolvido: body.resolvido }),
    }),
  );
}
