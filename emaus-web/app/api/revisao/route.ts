// Proxy autenticado da revisão feita na própria tela do tópico (NIA-T-026). Quem age é sempre
// o dono da sessão (o cookie), nunca um id vindo do corpo; o backend confere a permissão de
// novo (master/admin ou professor tutor do curso). Devolve a revisão já atualizada.

import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { API_URL } from "../../_lib/config";
import { COOKIE_TOKEN } from "../../_lib/sessao";

async function chamar(token: string, caminho: string, corpo?: unknown) {
  const res = await fetch(`${API_URL}${caminho}`, {
    method: corpo === undefined ? "GET" : "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: corpo === undefined ? undefined : JSON.stringify(corpo),
    cache: "no-store",
  });
  const data = await res.json().catch(() => ({}));
  return { res, data };
}

export async function POST(req: NextRequest) {
  const jar = await cookies();
  const token = jar.get(COOKIE_TOKEN)?.value;
  if (!token) return NextResponse.json({ erro: "Sessão expirada." }, { status: 401 });

  const body = await req.json().catch(() => ({}));
  const topicoId = Number(body.topicoId);
  if (!Number.isInteger(topicoId)) return NextResponse.json({ erro: "Dados incompletos." }, { status: 400 });

  let etapa;
  if (body.acao === "ponto") {
    const texto = typeof body.texto === "string" ? body.texto.trim() : "";
    if (!texto || !Number.isInteger(body.slideIndex)) {
      return NextResponse.json({ erro: "Escreva o ponto antes de enviar." }, { status: 400 });
    }
    etapa = await chamar(token, "/topico-comments/", {
      topico_id: topicoId,
      slide_index: body.slideIndex,
      texto,
    });
  } else if (body.acao === "aprovar") {
    etapa = await chamar(token, `/topicos/${topicoId}/revisao/aprovar`, {
      observacao: typeof body.observacao === "string" ? body.observacao : null,
    });
  } else if (body.acao === "enviar-ia") {
    etapa = await chamar(token, `/topicos/${topicoId}/revisao/enviar-ia`, {});
  } else {
    return NextResponse.json({ erro: "Ação desconhecida." }, { status: 400 });
  }

  if (!etapa.res.ok) {
    return NextResponse.json(
      { erro: typeof etapa.data.detail === "string" ? etapa.data.detail : "Não deu pra concluir." },
      { status: etapa.res.status },
    );
  }

  // Sempre devolve o estado completo da revisão (o render redesenha pontos e caixa com isto)
  const atual = await chamar(token, `/topicos/${topicoId}/revisao`);
  if (!atual.res.ok) {
    return NextResponse.json({ erro: "Salvo, mas não consegui recarregar a revisão." }, { status: atual.res.status });
  }
  return NextResponse.json(atual.data);
}
