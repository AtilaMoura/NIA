import Link from "next/link";
import { Chip } from "./Chip";
import { Selo } from "./Selo";
import type { TopicoNo } from "../_lib/arvore";

const fmtData = new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "short" });

function quando(t: TopicoNo): string | null {
  if (t.concluido_em) return `Concluído em ${fmtData.format(new Date(t.concluido_em))}`;
  if (t.iniciado_em && (t.estado === "atual" || t.estado === "disponivel")) {
    return `Em andamento desde ${fmtData.format(new Date(t.iniciado_em))}`;
  }
  return null;
}

// Linha do tempo de tópicos agrupada por aula — usada em /progresso (o próprio aluno)
// e em /revisao/aluno/[userId] (professor vendo o progresso de alguém, leitura).
export function LinhaDoTempoTopicos({
  linhaDoTempo,
  hrefTopico,
}: {
  linhaDoTempo: TopicoNo[];
  hrefTopico?: (id: number) => string;
}) {
  const montarHref = hrefTopico ?? ((id: number) => `/topico/${id}`);

  const porAula: { aula: string; modulo: string; topicos: TopicoNo[] }[] = [];
  for (const t of linhaDoTempo) {
    const ultima = porAula[porAula.length - 1];
    if (ultima && ultima.aula === t.aulaTitulo) ultima.topicos.push(t);
    else porAula.push({ aula: t.aulaTitulo ?? "Aula", modulo: t.moduloTitulo ?? "", topicos: [t] });
  }

  return (
    <section className="flex flex-col gap-6">
      {porAula.map((grupo, gi) => (
        <div key={gi} className="flex flex-col gap-2">
          <h2 className="m-0 text-[.78rem] font-semibold uppercase tracking-[.1em] text-[var(--tm-ink-muted)]">
            {grupo.aula}
          </h2>
          <ol className="m-0 flex list-none flex-col gap-2 p-0">
            {grupo.topicos.map((t) => {
              const data = quando(t);
              const disponivel = t.estado !== "em_preparacao";
              return (
                <li
                  key={t.id}
                  className="flex flex-col gap-1.5 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3"
                >
                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                    <Selo estado={t.estado} />
                    <span className={t.estado === "em_preparacao" ? "text-[var(--tm-ink-muted)]" : ""}>
                      {t.titulo}
                    </span>
                    {t.referencia_biblica && <Chip tom="info">{t.referencia_biblica}</Chip>}
                    {t.tutor_veredito && (
                      <Chip tom={t.tutor_veredito === "dominado" ? "bom" : "aviso"}>
                        {t.tutor_veredito === "dominado" ? "Tutor: dominado" : "Tutor: reforço"}
                      </Chip>
                    )}
                  </div>
                  {data && <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">{data}</p>}
                  {disponivel && (
                    <Link
                      href={montarHref(t.id)}
                      className="text-[.8rem] font-semibold text-[var(--tm-accent)] hover:underline"
                    >
                      {t.estado === "concluido" ? "Rever" : "Abrir"} tópico
                    </Link>
                  )}
                </li>
              );
            })}
          </ol>
        </div>
      ))}
    </section>
  );
}
