import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../../_ui/CabecalhoApp";
import { Rodape } from "../../_ui/Rodape";
import { getSessao, getToken } from "../../_lib/sessao";
import { listPessoas } from "../../_lib/api";
import { sinalDe } from "../../_lib/pessoas";
import { ListaPessoas } from "./pessoas-ui";

export const metadata: Metadata = { title: "Pessoas" };

// Pessoas (só Master, 2026-09-28, protótipo 10-pessoas.html): todo mundo — alunos,
// admins e professores — com último login, última atividade, tópicos, provas e
// tempo de estudo. Admin/professor continuam com /revisao/alunos.
export default async function PessoasPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/revisao/pessoas");
  if (sessao.role !== "master") redirect("/revisao/alunos");

  const token = await getToken();
  const pessoas = await listPessoas(token);

  const resumo = [
    { valor: pessoas.length, rotulo: "pessoas cadastradas" },
    {
      valor: pessoas.filter((p) => ["hoje", "semana"].includes(sinalDe(p.ultima_atividade))).length,
      rotulo: "estudaram nos últimos 7 dias",
    },
    { valor: pessoas.reduce((t, p) => t + p.topicos_concluidos, 0), rotulo: "tópicos concluídos (todos)" },
    {
      valor: pessoas.filter((p) => (p.role === "admin" || p.role === "professor") && p.topicos_concluidos === 0).length,
      rotulo: "admins/professores sem concluir nada",
      alerta: true,
    },
  ];

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} />

      <main className="mx-auto flex w-full max-w-[1100px] flex-col px-[clamp(1rem,4vw,2rem)] pb-12 pt-[clamp(1.25rem,4vw,2.25rem)]">
        <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">Pessoas</h1>
        <p className="m-0 mt-1 text-[var(--tm-ink-muted)]">Quem está estudando, desde quando e quanto.</p>
        <p className="m-0 mt-3.5 rounded-[var(--tm-radius)] bg-[var(--tm-surface-2)] px-3.5 py-2.5 text-[.85rem] text-[var(--tm-ink-muted)]">
          ⓘ Último login e tempo de estudo são registrados a partir de 28/09/2026. Antes disso só existe a atividade nos tópicos.
        </p>

        <div className="mt-4 grid grid-cols-2 gap-2.5 min-[700px]:grid-cols-4">
          {resumo.map((n) => (
            <div key={n.rotulo} className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-3">
              <b
                className={"block text-[1.45rem] leading-tight " + (n.alerta && n.valor > 0 ? "text-[var(--tm-warn)]" : "")}
                style={{ fontFamily: "var(--tm-font-display)" }}
              >
                {n.valor}
              </b>
              <span className="text-[.8rem] text-[var(--tm-ink-muted)]">{n.rotulo}</span>
            </div>
          ))}
        </div>

        <ListaPessoas pessoas={pessoas} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
