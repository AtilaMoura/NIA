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
  className = "",
}: {
  titulo: string;
  tom: TomCurso;
  capaUrl: string | null;
  className?: string;
}) {
  return (
    <div
      className={`relative aspect-[3/2] w-full overflow-hidden ${className}`}
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
