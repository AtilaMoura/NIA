import Link from "next/link";
import type { TopicoNo } from "../_lib/arvore";
import type { AvaliacaoProgress } from "../_lib/api";

// Lista compacta de tópicos agrupada por módulo (redesign 2026-09-27, protótipo
// 07-progresso.html) — usada em /progresso (o próprio aluno) e em
// /revisao/aluno/[userId] (revisor vendo o progresso de alguém, só leitura).
// A linha inteira é o link; estado, data, veredito do tutor e prova na mesma linha.

const fmtData = new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "short" });

type EstadoLinha = "concluido" | "andamento" | "nao_iniciado" | "preparacao";

// O estado da árvore marca só o 1º não concluído como "atual"; aqui vale o que o
// aluno fez de verdade: começou e não terminou = "Em andamento" (antes aparecia
// "Disponível" com "Em andamento desde…" embaixo).
function estadoDaLinha(t: TopicoNo): EstadoLinha {
  if (t.estado === "em_preparacao") return "preparacao";
  if (t.estado === "concluido") return "concluido";
  if (t.iniciado_em) return "andamento";
  return "nao_iniciado";
}

function subtitulo(t: TopicoNo, estado: EstadoLinha): string {
  const partes: string[] = [];
  if (estado === "concluido" && t.concluido_em) partes.push(`Concluído em ${fmtData.format(new Date(t.concluido_em))}`);
  else if (estado === "andamento" && t.iniciado_em) partes.push(`Em andamento desde ${fmtData.format(new Date(t.iniciado_em))}`);
  else if (estado === "nao_iniciado") partes.push("Não iniciado");
  else if (estado === "preparacao") partes.push("Em preparação");
  if (t.referencia_biblica) partes.push(t.referencia_biblica);
  return partes.join(" · ");
}

const CHIP = "whitespace-nowrap rounded-full border px-2 py-0.5 text-[.72rem] font-semibold";
const CHIP_BOM = `${CHIP} border-[color-mix(in_srgb,var(--tm-good)_55%,transparent)] text-[var(--tm-good)]`;
const CHIP_AVISO = `${CHIP} border-[color-mix(in_srgb,var(--tm-warn)_55%,transparent)] text-[var(--tm-warn)]`;
const CHIP_NEUTRO = `${CHIP} border-[var(--tm-border)] text-[var(--tm-ink-muted)]`;

function Icone({ estado }: { estado: EstadoLinha }) {
  const base = "grid h-[22px] w-[22px] shrink-0 place-items-center rounded-full border-2 text-[.7rem] font-bold";
  if (estado === "concluido") return <span className={`${base} border-[var(--tm-good)] bg-[var(--tm-good)] text-white`}>✓</span>;
  if (estado === "andamento") return <span className={`${base} border-[var(--tm-accent)]`} aria-hidden />;
  if (estado === "preparacao") return <span className={`${base} border-[var(--tm-border)] text-[var(--tm-ink-muted)]`} aria-hidden>…</span>;
  return <span className={`${base} border-[var(--tm-border)]`} aria-hidden />;
}

export function LinhaDoTempoTopicos({
  linhaDoTempo,
  hrefTopico,
  provas,
}: {
  linhaDoTempo: TopicoNo[];
  hrefTopico?: (id: number) => string;
  /** progresso das provas por avaliacao_id — sem ele, o chip da prova não aparece */
  provas?: Map<number, AvaliacaoProgress>;
}) {
  const montarHref = hrefTopico ?? ((id: number) => `/topico/${id}`);

  const porModulo: { modulo: string; topicos: TopicoNo[] }[] = [];
  for (const t of linhaDoTempo) {
    const ultimo = porModulo[porModulo.length - 1];
    if (ultimo && ultimo.modulo === (t.moduloTitulo ?? "")) ultimo.topicos.push(t);
    else porModulo.push({ modulo: t.moduloTitulo ?? "", topicos: [t] });
  }
  // Abre o módulo onde o aluno está (ou o 1º, se ainda não começou)
  const idxAberto = Math.max(0, porModulo.findIndex((g) => g.topicos.some((t) => t.estado === "atual")));

  return (
    <div>
      {porModulo.map((grupo, gi) => {
        const feitos = grupo.topicos.filter((t) => t.estado === "concluido").length;
        const total = grupo.topicos.filter((t) => t.estado !== "em_preparacao").length;
        return (
          <details key={gi} open={gi === idxAberto} className="group border-t border-[var(--tm-border)]">
            <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-3 text-[.76rem] font-bold uppercase tracking-[.1em] text-[var(--tm-ink-muted)] [&::-webkit-details-marker]:hidden">
              <span className="min-w-0">
                Módulo {gi + 1}
                {grupo.modulo && <> · {grupo.modulo}</>}
              </span>
              <span className="flex shrink-0 items-center gap-3 font-semibold normal-case tracking-normal">
                {feitos} de {total}
                <span aria-hidden className="transition-transform group-open:rotate-90">▸</span>
              </span>
            </summary>

            {grupo.topicos.map((t) => {
              const estado = estadoDaLinha(t);
              const prova = t.avaliacaoId != null ? provas?.get(t.avaliacaoId) : undefined;
              const chips: { texto: string; classe: string }[] = [];
              if (t.tutor_veredito) {
                chips.push(
                  t.tutor_veredito === "dominado"
                    ? { texto: "Tutor: dominado", classe: CHIP_BOM }
                    : { texto: "Tutor: reforço", classe: CHIP_AVISO },
                );
              }
              if (provas && t.avaliacaoId != null && estado === "concluido") {
                if (prova?.status === "concluido") {
                  chips.push(
                    prova.tutor_veredito === "reforco"
                      ? { texto: "Prova: revisar", classe: CHIP_AVISO }
                      : { texto: "Prova: pode seguir", classe: CHIP_BOM },
                  );
                } else {
                  chips.push({ texto: "Prova: não feita", classe: CHIP_NEUTRO });
                }
              }

              const miolo = (
                <>
                  <Icone estado={estado} />
                  <span className="min-w-0 flex-1">
                    <span className={"block text-[.95rem] " + (estado === "preparacao" ? "text-[var(--tm-ink-muted)]" : "")}>
                      {t.titulo}
                    </span>
                    <span className="block text-[.76rem] text-[var(--tm-ink-muted)]">{subtitulo(t, estado)}</span>
                  </span>
                  {chips.length > 0 && (
                    <span className="flex w-full flex-wrap gap-1.5 pl-[34px] sm:w-auto sm:justify-end sm:pl-0">
                      {chips.map((c) => (
                        <span key={c.texto} className={c.classe}>
                          {c.texto}
                        </span>
                      ))}
                    </span>
                  )}
                </>
              );
              const linha = "flex flex-wrap items-center gap-3 border-t border-[var(--tm-border)] px-5 py-2.5 sm:flex-nowrap";

              return estado === "preparacao" ? (
                <div key={t.id} className={`${linha} opacity-60`}>
                  {miolo}
                </div>
              ) : (
                <Link key={t.id} href={montarHref(t.id)} className={`${linha} hover:bg-[var(--tm-surface-2)]`}>
                  {miolo}
                </Link>
              );
            })}
          </details>
        );
      })}
    </div>
  );
}
