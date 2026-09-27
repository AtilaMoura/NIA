// Nome pra exibir (saudação, avatar). Tolera nomes com rótulo entre parênteses,
// como "Master (Atila)": o que está nos parênteses é a pessoa, o resto é rótulo.

/** Primeiro nome da pessoa: "Master (Atila)" → "Atila"; "Maria Souza" → "Maria". */
export function primeiroNome(nome: string | null | undefined): string | null {
  if (!nome) return null;
  const entreParenteses = nome.match(/\(([^)]+)\)/)?.[1];
  const base = (entreParenteses ?? nome).trim();
  return base.split(/\s+/)[0] || null;
}

/** Iniciais só com letras: "Maria Souza" → "MS"; "Master (Atila)" → "AT". */
export function iniciais(nome: string | null | undefined): string {
  const pessoa = nome?.match(/\(([^)]+)\)/)?.[1] ?? nome ?? "";
  const palavras = pessoa
    .replace(/[^\p{L}\s]/gu, " ")
    .split(/\s+/)
    .filter(Boolean);
  if (palavras.length === 0) return "?";
  if (palavras.length === 1) return palavras[0].slice(0, 2).toUpperCase();
  return (palavras[0][0] + palavras[palavras.length - 1][0]).toUpperCase();
}
