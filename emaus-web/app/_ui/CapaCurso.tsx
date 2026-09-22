import { GRADIENTE_TOM, type TomCurso } from "../_lib/catalogo";

function monograma(titulo: string): string {
  const palavras = titulo
    .replace(/[—–-]/g, " ")
    .split(/\s+/)
    .filter((p) => p.length > 2 && !["dos", "das", "para", "com", "the"].includes(p.toLowerCase()));
  return (palavras[0]?.[0] ?? "E").toUpperCase() + (palavras[1]?.[0] ?? "").toUpperCase();
}

export function CapaCurso({
  titulo,
  tom,
  capaUrl,
  aspecto = "3/2",
  className = "",
}: {
  titulo: string;
  tom: TomCurso;
  capaUrl: string | null;
  /** Proporção da capa (2026-09-21) — parâmetro dedicado em vez de deixar o
   * chamador sobrescrever via className: duas classes 'aspect-[X]' na mesma
   * string não se sobrepõem de forma confiável no Tailwind (não é
   * especificidade CSS normal, é geração de utilitário — a ordem no
   * stylesheet final não segue a ordem da string de classe). */
  aspecto?: "3/2" | "3/4" | "1/1";
  className?: string;
}) {
  // Classes LITERAIS (não construídas por template string) — o Tailwind só
  // gera CSS pra classe que aparece como texto puro no código-fonte; uma
  // classe montada em runtime (`aspect-[${aspecto}]`) não é detectada pelo
  // scanner de conteúdo e sai sem estilo nenhum.
  const classeAspecto =
    aspecto === "3/4" ? "aspect-[3/4]" : aspecto === "1/1" ? "aspect-[1/1]" : "aspect-[3/2]";
  return (
    <div
      className={`relative w-full overflow-hidden ${classeAspecto} ${className}`}
      style={{ background: GRADIENTE_TOM[tom] }}
    >
      {capaUrl && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={capaUrl} alt="" className="absolute inset-0 h-full w-full object-cover" />
      )}
      <div
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at 28% 18%, transparent 45%, rgba(20,12,4,.32) 100%)",
        }}
      />
      {!capaUrl && (
        <span
          aria-hidden
          className="absolute inset-0 flex items-center justify-center text-[2.8rem] font-semibold tracking-wide text-white/25"
          style={{ fontFamily: "var(--tm-font-display)" }}
        >
          {monograma(titulo)}
        </span>
      )}
    </div>
  );
}
