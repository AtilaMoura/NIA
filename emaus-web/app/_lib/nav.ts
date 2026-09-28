// Navegação do Emaús — uma fonte de verdade, usada no cabeçalho (desktop + mobile)
// e no rodapé. A barra principal é IGUAL em toda tela e só cresce se o usuário for
// revisor. A sub-nav da revisão só aparece dentro de /revisao/*.

import { papelPodeRevisar, papelVeEstudosPessoais, type Papel } from "./papel";

// "icone" é opcional (emoji) — só o menu mobile usa hoje (redesign 2026-09-21, ver
// PLANO_REDESIGN_EMAUS.md Fase 5); a barra desktop ignora o campo.
export type ItemNav = { href: string; rotulo: string; icone?: string };

// Onde o logo leva: sempre o mesmo destino (não muda por página).
export function hrefMarca(logado: boolean): string {
  return logado ? "/inicio" : "/";
}

// Barra principal — mesma ordem sempre. Sem "Cursos" (2026-09-26): logado, "/"
// redireciona pra /inicio, que já é a vitrine de cursos do aluno.
export function navPrincipal(papel: Papel | null | undefined): ItemNav[] {
  const base: ItemNav[] = [
    { href: "/inicio", rotulo: "Início", icone: "🏠" },
    { href: "/progresso", rotulo: "Meu progresso", icone: "📈" },
  ];
  if (papel && papelPodeRevisar(papel)) {
    base.push({ href: "/revisao", rotulo: "Revisão", icone: "🗂️" });
  }
  // Estudos pessoais do Master saíram da /inicio (2026-09-27) e têm página própria
  if (papelVeEstudosPessoais(papel)) {
    base.push({ href: "/estudos", rotulo: "Estudos pessoais", icone: "📓" });
  }
  return base;
}

// Nav pra quem está deslogado (na landing).
export const NAV_DESLOGADO: ItemNav[] = [
  { href: "/#cursos", rotulo: "Cursos", icone: "📚" },
  { href: "/#como-funciona", rotulo: "Como funciona", icone: "💡" },
];

// Sub-nav da área de revisão (2ª linha, só dentro de /revisao/*). O Master vê
// "Pessoas" (todo mundo, com acesso e tempo — 2026-09-28) no lugar de "Alunos".
export function navRevisao(papel: Papel | null | undefined): ItemNav[] {
  return [
    { href: "/revisao", rotulo: "Fila de revisão", icone: "🗂️" },
    papel === "master"
      ? { href: "/revisao/pessoas", rotulo: "Pessoas", icone: "👥" }
      : { href: "/revisao/alunos", rotulo: "Alunos", icone: "🧑‍🎓" },
  ];
}

// Itens do menu do avatar (Sair é tratado à parte).
export const ITENS_AVATAR: ItemNav[] = [
  { href: "/perfil", rotulo: "Perfil", icone: "👤" },
  { href: "/preferencias", rotulo: "Preferências", icone: "⚙️" },
];

// Qual item da barra está "ativo" pra uma dada rota.
export function itemAtivo(pathname: string, href: string): boolean {
  // Âncoras da página de visitante (/#cursos, /#como-funciona) nunca ficam
  // "ativas" — senão as duas acendem juntas em "/".
  if (href.includes("#")) return false;
  const alvo = href.split("#")[0].replace(/\/$/, "") || "/";
  if (alvo === "/inicio") return pathname === "/inicio";
  if (alvo === "/") return pathname === "/" || pathname.startsWith("/curso");
  if (alvo === "/progresso") return pathname === "/progresso";
  if (alvo === "/revisao") return pathname.startsWith("/revisao");
  return pathname === alvo || pathname.startsWith(alvo + "/");
}
