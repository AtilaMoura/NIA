import fs from "node:fs";
import path from "node:path";

export const metadata = { title: "Comparar símbolos" };

const NOMES: Record<string, string> = {
  "simbolo-livro-brasa": "Livro + brasa (aquarela)",
  "simbolo-selo": "Selo circular",
  "simbolo-brasa": "Só brasa",
  "simbolo-livro": "Só livro (traço)",
  "simbolo-traco-unico": "Traço único (linha)",
};

const TAMANHOS = [18, 24, 30, 44, 80, 140];

export default function CompararMarcaPage() {
  let arquivos: string[] = [];
  try {
    arquivos = fs
      .readdirSync(path.join(process.cwd(), "public", "marca", "v2"))
      .filter((f) => f.endsWith(".png"))
      .sort();
  } catch {
    arquivos = [];
  }

  return (
    <main className="mx-auto flex max-w-4xl flex-col gap-10 p-8">
      <h1 className="m-0 text-[1.4rem]">Símbolos gerados — v2</h1>
      {arquivos.length === 0 && (
        <p className="text-[var(--tm-ink-muted)]">
          Nada em <code>public/marca/v2/</code>. Rode{" "}
          <code>python scripts/preparar_imagens_emaus.py simbolos</code>.
        </p>
      )}
      {arquivos.map((f) => {
        const slug = f.replace(".png", "");
        const src = `/marca/v2/${f}`;
        return (
          <section key={f} className="flex flex-col gap-3 border-b border-[var(--tm-border)] pb-8">
            <div className="flex items-baseline gap-3">
              <h2 className="m-0 text-[1.05rem]">{NOMES[slug] ?? slug}</h2>
              <code className="text-[.75rem] text-[var(--tm-ink-muted)]">{slug}</code>
            </div>
            {/* mesma imagem em vários tamanhos, sobre claro e sobre escuro */}
            <div className="grid grid-cols-2 gap-4">
              {(["#faf6ee", "#1b1610"] as const).map((bg) => (
                <div
                  key={bg}
                  className="flex flex-wrap items-end gap-5 rounded-[var(--tm-radius)] border border-[var(--tm-border)] p-5"
                  style={{ background: bg }}
                >
                  {TAMANHOS.map((t) => (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img key={t} src={src} alt={slug} width={t} height={t} style={{ objectFit: "contain" }} />
                  ))}
                </div>
              ))}
            </div>
            {/* como ficaria no cabeçalho, ao lado de "Emaús" */}
            <div className="flex gap-4">
              {(["#faf6ee", "#1b1610"] as const).map((bg) => (
                <span
                  key={bg}
                  className="inline-flex items-center gap-2 rounded-[var(--tm-radius)] border border-[var(--tm-border)] px-4 py-2"
                  style={{ background: bg, color: bg === "#1b1610" ? "#f1e7d6" : "#2b241c" }}
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={src} alt="" width={30} height={30} style={{ objectFit: "contain" }} />
                  <b style={{ fontFamily: "var(--tm-font-display)", fontSize: "1.12rem" }}>Emaús</b>
                </span>
              ))}
            </div>
          </section>
        );
      })}
    </main>
  );
}
