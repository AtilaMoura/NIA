// Navegação do Emaús — uma fonte de verdade, usada no cabeçalho (desktop + mobile)
// e no rodapé. A barra principal é IGUAL em toda tela e só cresce se o usuário for
// revisor. A sub-nav da revisão só aparece dentro de /revisao/*.

import { papelPodeRevisar, type Papel } from "./papel";

export type ItemNav = { href: string; rotulo: string };

// Onde o logo leva: sempre o mesmo destino (não muda por página).
export function hrefMarca(logado: boolean): string {
  return logado ? "/inicio" : "/";
}

// Barra principal — mesma ordem sempre.
export function navPrincipal(papel: Papel | null | undefined): ItemNav[] {
  const base: ItemNav[] = [
    { href: "/inicio", rotulo: "Início" },
    { href: "/#cursos", rotulo: "Cursos" },
    { href: "/progresso", rotulo: "Meu progresso" },
  ];
  if (papel && papelPodeRevisar(papel)) {
    base.push({ href: "/revisao", rotulo: "Revisão" });
  }
  return base;
}

// Nav pra quem está deslogado (na landing).
export const NAV_DESLOGADO: ItemNav[] = [
  { href: "/#cursos", rotulo: "Cursos" },
  { href: "/#como-funciona", rotulo: "Como funciona" },
];

// Sub-nav da área de revisão (2ª linha, só dentro de /revisao/*).
export const NAV_REVISAO: ItemNav[] = [
  { href: "/revisao", rotulo: "Fila de revisão" },
  { href: "/revisao/alunos", rotulo: "Alunos" },
];

// Itens do menu do avatar (Sair é tratado à parte).
export const ITENS_AVATAR: ItemNav[] = [
  { href: "/perfil", rotulo: "Perfil" },
  { href: "/preferencias", rotulo: "Preferências" },
];

// Qual item da barra está "ativo" pra uma dada rota.
export function itemAtivo(pathname: string, href: string): boolean {
  const alvo = href.split("#")[0].replace(/\/$/, "") || "/";
  if (alvo === "/inicio") return pathname === "/inicio";
  if (alvo === "/") return pathname === "/" || pathname.startsWith("/curso");
  if (alvo === "/progresso") return pathname === "/progresso";
  if (alvo === "/revisao") return pathname.startsWith("/revisao");
  return pathname === alvo || pathname.startsWith(alvo + "/");
}
