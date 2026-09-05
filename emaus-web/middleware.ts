// Guarda de sessão (FASE 1). Só olha os cookies httpOnly — a validação de verdade do
// token continua sendo o backend (get_current_user) a cada chamada de /auth/me nas
// páginas. Isso aqui é só o gate rápido de rota, roda no Edge.

import { NextRequest, NextResponse } from "next/server";

const PUBLICAS = ["/", "/entrar", "/criar-conta"];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  if (PUBLICAS.includes(pathname)) return NextResponse.next();

  const token = req.cookies.get("emaus_token")?.value;
  if (!token) {
    const url = req.nextUrl.clone();
    url.pathname = "/entrar";
    url.search = `?next=${encodeURIComponent(pathname)}`;
    return NextResponse.redirect(url);
  }

  if (pathname.startsWith("/revisao")) {
    const papel = req.cookies.get("emaus_role")?.value;
    if (papel !== "master" && papel !== "admin" && papel !== "professor") {
      const url = req.nextUrl.clone();
      url.pathname = "/inicio";
      return NextResponse.redirect(url);
    }
  }

  return NextResponse.next();
}

export const config = {
  // Tudo, exceto /api/*, assets internos do Next e arquivos estáticos (extensão no nome).
  matcher: ["/((?!api/|_next/|.*\\..*).*)"],
};
