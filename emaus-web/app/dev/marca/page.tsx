import fs from "node:fs";
import path from "node:path";

export const metadata = { title: "Comparar símbolos" };

// Rótulos amigáveis por slug de arquivo (v2 + v3).
const NOMES: Record<string, string> = {
  // v2 (rodada antiga — livro/brasa)
  "simbolo-livro-brasa": "Livro + brasa (aquarela)",
  "simbolo-selo": "Selo circular",
  "simbolo-brasa": "Só brasa",
  "simbolo-livro": "Só livro (traço)",
  "simbolo-traco-unico": "Traço único (linha)",
  // v3 (repensado do zero)
  "01-estrada-horizonte": "01 · Estrada ao horizonte",
  "02-dois-caminhantes": "02 · Dois caminhantes",
  "03-o-terceiro": "03 · O terceiro na estrada",
  "04-amanhecer": "04 · Amanhecer / olhos abertos",
  "05-pao-partido": "05 · Pão partido",
  "06-porta-luz": "06 · Porta e luz",
  "07-monograma-e-estrada": "07 · Monograma E-estrada",
  "08-coracao-que-arde": "08 · Coração que arde",
  "09-escritura-caminho": "09 · Escritura que vira caminho",
  "10-colina-dourada": "10 · Colina dourada",
  "11-logotipo-serif": "11 · Logotipo serif editorial",
  "12-logotipo-sans": "12 · Logotipo sans humanista",
  "13-selo-circular": "13 · Selo circular (nome + Lucas 24)",
  "14-lockup-horizontal": "14 · Lockup horizontal",
  "15-monograma-em": "15 · Monograma EM / ícone de app",
  "16-caligrafia-linha": "16 · Caligrafia em uma linha",
};

const TAMANHOS = [18, 24, 30, 44, 80, 140];

// Descobre as pastas de versão dentro de public/marca (v2, v3, ...).
function listarVersoes(): { versao: string; arquivos: string[] }[] {
  const base = path.join(process.cwd(), "public", "marca");
  let versoes: string[] = [];
  try {
    versoes = fs
      .readdirSync(base, { withFileTypes: true })
      .filter((d) => d.isDirectory() && /^v\d+$/.test(d.name))
      .map((d) => d.name)
      .sort()
      .reverse(); // v3 antes de v2
  } catch {
    versoes = [];
  }
  return versoes.map((versao) => {
    let arquivos: string[] = [];
    try {
      arquivos = fs
        .readdirSync(path.join(base, versao))
        .filter((f) => f.endsWith(".png"))
        .sort();
    } catch {
      arquivos = [];
    }
    return { versao, arquivos };
  });
}

export default function CompararMarcaPage() {
  const versoes = listarVersoes();
  const temAlgo = versoes.some((v) => v.arquivos.length > 0);

  return (
    <main className="mx-auto flex max-w-4xl flex-col gap-14 p-8">
      <header className="flex flex-col gap-2">
        <h1 className="m-0 text-[1.4rem]">Símbolos e logotipos gerados</h1>
        <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">
          Rodada nova (v3): repensada do zero — estrada, caminhantes, amanhecer,
          pão partido, monogramas e logotipos com o nome.
        </p>
      </header>

      {!temAlgo && (
        <p className="text-[var(--tm-ink-muted)]">
          Nada em <code>public/marca/</code>. Gere as imagens com{" "}
          <code>python scripts/gerar_imagem_gemini.py scripts/marca_emaus_v3.json</code> e depois{" "}
          <code>python scripts/preparar_imagens_emaus.py simbolos v3</code>.
        </p>
      )}

      {versoes.map(({ versao, arquivos }) => (
        <section key={versao} className="flex flex-col gap-10">
          <h2 className="m-0 border-b border-[var(--tm-border)] pb-2 text-[1.15rem]">
            {versao === "v3" ? "v3 — repensado do zero" : `${versao} — rodada anterior`}
          </h2>

          {arquivos.length === 0 && (
            <p className="text-[.85rem] text-[var(--tm-ink-muted)]">
              Nada em <code>public/marca/{versao}/</code>.
            </p>
          )}

          {arquivos.map((f) => {
            const slug = f.replace(".png", "");
            const src = `/marca/${versao}/${f}`;
            return (
              <div key={f} className="flex flex-col gap-3 border-b border-[var(--tm-border)] pb-8">
                <div className="flex items-baseline gap-3">
                  <h3 className="m-0 text-[1.05rem]">{NOMES[slug] ?? slug}</h3>
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
                        <img
                          key={t}
                          src={src}
                          alt={slug}
                          width={t}
                          height={t}
                          style={{ objectFit: "contain" }}
                        />
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
              </div>
            );
          })}
        </section>
      ))}
    </main>
  );
}
