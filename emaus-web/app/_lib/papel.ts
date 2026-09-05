// Tipos/constantes de papel — sem nada de server (`next/headers`), pra poder ser
// importado tanto de Server Components quanto de Client Components (ex: MenuUsuario
// precisa do rótulo do papel pra mostrar o selo no cabeçalho).

export type Papel = "aluno" | "admin" | "master" | "professor";

export function papelPodeRevisar(papel: Papel): boolean {
  return papel === "master" || papel === "admin" || papel === "professor";
}

// Rótulo + cor de apresentação de cada papel — o valor de verdade é sempre
// users.role no banco, isto aqui é só pra mostrar na tela (cabeçalho, /perfil).
export const INFO_PAPEL: Record<Papel, { rotulo: string; tom: "info" | "aviso" | "bom" | "neutro" }> = {
  master: { rotulo: "Master", tom: "aviso" },
  admin: { rotulo: "Admin", tom: "info" },
  professor: { rotulo: "Professor", tom: "bom" },
  aluno: { rotulo: "Aluno", tom: "neutro" },
};
