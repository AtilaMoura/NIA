import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../../_ui/CabecalhoApp";
import { Avatar } from "../../_ui/Avatar";
import { Rodape } from "../../_ui/Rodape";
import { TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import { getSessao, getToken } from "../../_lib/sessao";
import { papelPodeRevisar } from "../../_lib/papel";
import { listUsers } from "../../_lib/api";
import { montarArvore } from "../../_lib/arvore";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export const metadata: Metadata = { title: "Progresso dos alunos" };

export default async function RevisaoAlunosPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/revisao/alunos");
  if (!papelPodeRevisar(sessao.role)) redirect("/inicio");

  const token = await getToken();
  const usuarios = await listUsers(token);
  const alunos = usuarios.filter((u) => u.role === "aluno" || !u.role);

  const comProgresso = await Promise.all(
    alunos.map(async (a) => {
      const arvore = await montarArvore(CURSO_ID, a.id, token).catch(() => null);
      return { ...a, resumo: arvore?.resumo ?? null };
    }),
  );

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} />

      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-[clamp(1rem,4vw,2rem)] py-8">
        <h1 className="m-0 text-[1.5rem]">Progresso dos alunos</h1>

        {comProgresso.length === 0 && (
          <p className="text-[.9rem] text-[var(--tm-ink-muted)]">Nenhum aluno cadastrado ainda.</p>
        )}

        <ul className="m-0 flex list-none flex-col gap-2 p-0">
          {comProgresso.map((a) => (
            <li key={a.id}>
              <Link
                href={`/revisao/aluno/${a.id}`}
                className="flex items-center gap-3 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3 hover:border-[var(--tm-accent)]"
              >
                <Avatar nome={a.name ?? "Aluno"} />
                <div className="min-w-0 flex-1">
                  <p className="m-0 truncate font-medium">{a.name ?? "Sem nome"}</p>
                  <p className="m-0 truncate text-[.78rem] text-[var(--tm-ink-muted)]">{a.email}</p>
                </div>
                {a.resumo && (
                  <span className="shrink-0 text-[.8rem] text-[var(--tm-accent)]">
                    {a.resumo.concluidos}/{a.resumo.totalTopicos} tópicos
                  </span>
                )}
              </Link>
            </li>
          ))}
        </ul>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
