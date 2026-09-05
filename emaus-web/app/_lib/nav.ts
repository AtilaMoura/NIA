// Itens do menu do usuário — compartilhados entre o dropdown do desktop
// (MenuUsuario) e o drawer do mobile (MenuMobile).

import { papelPodeRevisar, type Papel } from "./papel";

export type ItemNav = { href: string; rotulo: string };

const BASE: ItemNav[] = [
  { href: "/inicio", rotulo: "Meu estudo" },
  { href: "/perfil", rotulo: "Perfil" },
  { href: "/progresso", rotulo: "Progresso" },
  { href: "/preferencias", rotulo: "Preferências" },
];

export function itensUsuario(papel: Papel | null | undefined): ItemNav[] {
  if (papel && papelPodeRevisar(papel)) {
    return [...BASE, { href: "/revisao", rotulo: "Área de revisão" }];
  }
  return BASE;
}
