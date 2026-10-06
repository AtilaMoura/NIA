import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../../_ui/CabecalhoApp";
import { Avatar } from "../../../_ui/Avatar";
import { Chip } from "../../../_ui/Chip";
import { Rodape } from "../../../_ui/Rodape";
import { getSessao, getToken } from "../../../_lib/sessao";
import { getPessoa, liberacoesDaPessoa, type TopicoDaPessoa } from "../../../_lib/api";
import { EstudosDaPessoa } from "./estudos-ui";
import { data, dataHora, duracao, quando, ROTULO_PAPEL } from "../../../_lib/pessoas";

export const metadata: Metadata = { title: "Pessoa" };

// Detalhe de uma pessoa (só Master, 2026-09-28): números + o que estudou tópico a
// tópico, agrupado por curso, com datas, slide onde parou, tempo, tutor e prova.
export default async function PessoaPage({ params }: { params: Promise<{ userId: string }> }) {
  const { userId: raw } = await params;
  const userId = Number(raw);
  if (!Number.isInteger(userId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/revisao/pessoas/${userId}`);
  if (sessao.role !== "master") redirect("/revisao/alunos");

  const token = await getToken();
  const [pessoa, liberacoes] = await Promise.all([
    getPessoa(userId, token).catch(() => null),
    liberacoesDaPessoa(userId, token).catch(() => []),
  ]);
  if (!pessoa) notFound();

  // Agrupa por curso, na ordem que o backend já devolve (curso → módulo → aula → tópico)
  const cursos: { id: number; titulo: string; topicos: TopicoDaPessoa[] }[] = [];
  for (const t of pessoa.topicos) {
    let c = cursos.find((x) => x.id === t.course_id);
    if (!c) cursos.push((c = { id: t.course_id, titulo: t.curso, topicos: [] }));
    c.topicos.push(t);
  }

  const numeros = [
    { valor: String(pessoa.topicos_iniciados), rotulo: "tópicos começados" },
    { valor: String(pessoa.topicos_concluidos), rotulo: "concluídos" },
    { valor: String(pessoa.provas_feitas), rotulo: "provas feitas" },
    { valor: duracao(pessoa.tempo_s), rotulo: "de estudo" },
  ];

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} />

      <main className="mx-auto flex w-full max-w-[1100px] flex-col px-[clamp(1rem,4vw,2rem)] pb-12 pt-[clamp(1.25rem,4vw,2.25rem)]">
        <Link href="/revisao/pessoas" className="mb-3.5 text-[.85rem] font-semibold text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]">
          ← Pessoas
        </Link>

        <div className="flex flex-wrap items-center gap-4">
          <Avatar nome={pessoa.name ?? pessoa.email} tamanho="lg" />
          <div className="min-w-0">
            <h1 className="m-0 flex flex-wrap items-center gap-2 text-[1.5rem]">
              {pessoa.name ?? "Sem nome"}
              <Chip tom={pessoa.role === "aluno" ? "neutro" : "info"}>{ROTULO_PAPEL[pessoa.role] ?? pessoa.role}</Chip>
            </h1>
            <p className="m-0 break-all text-[.9rem] text-[var(--tm-ink-muted)]">{pessoa.email}</p>
            <p className="m-0 mt-1.5 flex flex-wrap gap-x-5 gap-y-1 text-[.85rem] text-[var(--tm-ink-muted)]">
              <span>
                Cadastro <b className="font-semibold text-[var(--tm-ink)]">{data(pessoa.cadastro_em)}</b>
              </span>
              <span>
                Último login <b className="font-semibold text-[var(--tm-ink)]">{quando(pessoa.ultimo_login)}</b>
              </span>
              <span>
                Última atividade <b className="font-semibold text-[var(--tm-ink)]">{quando(pessoa.ultima_atividade)}</b>
              </span>
            </p>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-2.5 min-[700px]:grid-cols-4">
          {numeros.map((n) => (
            <div key={n.rotulo} className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-3">
              <b className="block text-[1.45rem] leading-tight" style={{ fontFamily: "var(--tm-font-display)" }}>
                {n.valor}
              </b>
              <span className="text-[.8rem] text-[var(--tm-ink-muted)]">{n.rotulo}</span>
            </div>
          ))}
        </div>

        <EstudosDaPessoa userId={pessoa.id} iniciais={liberacoes} />

        {cursos.length === 0 && (
          <p className="mt-6 text-[.9rem] text-[var(--tm-ink-muted)]">Ainda não abriu nenhum tópico.</p>
        )}

        {cursos.map((c) => {
          const concluidos = c.topicos.filter((t) => t.status === "concluido").length;
          const pct = Math.round((concluidos / c.topicos.length) * 100);
          return (
            <section key={c.id} className="mt-5 overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
              <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3.5">
                <h2 className="m-0 text-[1.05rem]">{c.titulo}</h2>
                <span className="flex items-center gap-2.5 text-[.85rem] text-[var(--tm-ink-muted)]">
                  <span className="h-1.5 w-[140px] overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
                    <i className="block h-full bg-[var(--tm-good)]" style={{ width: `${pct}%` }} />
                  </span>
                  {concluidos} de {c.topicos.length} concluídos
                </span>
              </div>
              <ul className="m-0 list-none divide-y divide-[var(--tm-border)] border-t border-[var(--tm-border)] p-0">
                {c.topicos.map((t) => (
                  <LinhaTopico key={t.topico_id} t={t} />
                ))}
              </ul>
            </section>
          );
        })}
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}

function LinhaTopico({ t }: { t: TopicoDaPessoa }) {
  const ok = t.status === "concluido";
  const detalhes = [
    t.iniciado_em ? `Começou ${dataHora(t.iniciado_em)}` : null,
    ok && t.concluido_em ? `concluiu ${dataHora(t.concluido_em)}` : null,
    !ok && t.ultimo_slide != null ? `parou no slide ${t.ultimo_slide + 1}` : null,
    t.tempo_s > 0 ? duracao(t.tempo_s) : null,
  ].filter(Boolean);

  return (
    <li className="grid grid-cols-[22px_1fr] items-center gap-x-3 gap-y-1.5 px-4 py-2.5 text-[.9rem] min-[560px]:grid-cols-[22px_1fr_auto]">
      <span
        aria-hidden
        className={
          "grid h-[22px] w-[22px] place-items-center rounded-full border-2 text-[.68rem] font-bold " +
          (ok ? "border-[var(--tm-good)] bg-[var(--tm-good)] text-white" : "border-[var(--tm-accent)]")
        }
      >
        {ok ? "✓" : ""}
      </span>
      <span className="min-w-0">
        {t.titulo}
        <small className="block text-[.76rem] text-[var(--tm-ink-muted)]">{detalhes.join(" · ") || "—"}</small>
      </span>
      <span className="col-start-2 flex flex-wrap gap-1.5 min-[560px]:col-start-3 min-[560px]:justify-end">
        <Chip tom={ok ? "bom" : "neutro"}>{ok ? "Concluído" : "Em andamento"}</Chip>
        {t.tutor_veredito && (
          <Chip tom={t.tutor_veredito === "dominado" ? "bom" : "aviso"}>
            Tutor: {t.tutor_veredito === "dominado" ? "dominou" : "reforço"}
          </Chip>
        )}
        {t.prova_status && (
          <Chip tom={t.prova_status === "concluido" ? "bom" : "neutro"}>
            Prova {t.prova_status === "concluido" ? "feita" : "começada"}
          </Chip>
        )}
      </span>
    </li>
  );
}
