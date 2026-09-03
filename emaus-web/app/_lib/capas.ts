import fs from "node:fs";
import path from "node:path";

// Server-only: checa se a capa gerada já foi colocada em /public/capas/{slug}.jpg.
// Enquanto não existe, o card cai no degradê do tom do curso.
export function capaExiste(slug: string): boolean {
  try {
    return fs.existsSync(path.join(process.cwd(), "public", "capas", `${slug}.jpg`));
  } catch {
    return false;
  }
}
