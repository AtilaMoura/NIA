// Destino depois de entrar/criar conta. Só aceita caminho interno ("/algo"),
// nunca "//dominio" nem URL absoluta — evita redirecionar pra site de fora.
export function destinoSeguro(next: string | null | undefined): string {
  return next && next.startsWith("/") && !next.startsWith("//") ? next : "/inicio";
}
