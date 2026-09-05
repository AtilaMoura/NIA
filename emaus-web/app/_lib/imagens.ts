import fs from "node:fs";
import path from "node:path";

// Server-only. Checa se um arquivo de imagem já existe em /public/<rel>.
// Enquanto as imagens do Gemini não são geradas, o front cai em placeholder.
export function imagemExiste(rel: string): boolean {
  try {
    return fs.existsSync(path.join(process.cwd(), "public", rel));
  } catch {
    return false;
  }
}

// Slides do carrossel do herói. Usa /heroi/*.jpg quando existir; senão cai nas
// capas de curso que funcionam como ilustração (placeholder até gerar as de herói).
const HEROI = [
  { arquivo: "estrada.jpg", alt: "Dois caminhantes numa estrada ao entardecer" },
  { arquivo: "lamparina.jpg", alt: "Um livro aberto ao lado de uma lamparina" },
  { arquivo: "folhear.jpg", alt: "Mãos folheando um livro antigo" },
  { arquivo: "grupo.jpg", alt: "Um pequeno grupo estudando à luz de vela" },
];

const PLACEHOLDER = [
  { arquivo: "formacao-novo-obreiro.jpg", alt: "Ilustração em aquarela" },
  { arquivo: "como-estudar-a-biblia.jpg", alt: "Ilustração em aquarela" },
  { arquivo: "evangelho-de-joao.jpg", alt: "Ilustração em aquarela" },
  { arquivo: "panorama-da-biblia.jpg", alt: "Ilustração em aquarela" },
];

export function slidesHeroi(): { src: string; alt: string }[] {
  const prontas = HEROI.filter((h) => imagemExiste(`heroi/${h.arquivo}`));
  if (prontas.length > 0) {
    return prontas.map((h) => ({ src: `/heroi/${h.arquivo}`, alt: h.alt }));
  }
  return PLACEHOLDER.filter((p) => imagemExiste(`capas/${p.arquivo}`)).map((p) => ({
    src: `/capas/${p.arquivo}`,
    alt: p.alt,
  }));
}
