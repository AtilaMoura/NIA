import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../../_ui/CabecalhoApp";
import { BarraProgresso } from "../../../_ui/BarraProgresso";
import { Rodape } from "../../../_ui/Rodape";
import { LinhaDoTempoTopicos } from "../../../_ui/LinhaDoTempoTopicos";
import { TEOLOGIA_COURSE_IDS } from "../../../_lib/config";
import { getSessao, getToken } from "../../../_lib/sessao";
import { papelPodeRevisar } from "../../../_lib/papel";
import { getUser } from "../../../_lib/api";
import { montarArvore } from "../../../_lib/arvore";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export async function generateMetadata({
  params,
}: {
  params: Promise<{ userId: string }>;
}): Promise<Metadata> {
  const { userId } = await params;
  const token = await getToken();
  const aluno = await getUser(Number(userId), token).catch(() => null);
  return { title: aluno ? `Progresso: ${aluno.name}` : "Progresso do aluno" };
}

export default async function RevisaoAlunoPage({
  params,
}: {
  params: Promise<{ userId: string }>;
}) {
  const { userId: raw } = await params;
  const userId = Number(raw);
  if (!Number.isInteger(userId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/revisao/aluno/${userId}`);
  if (!papelPodeRevisar(sessao.role)) redirect("/inicio");
  const token = await getToken();

  const aluno = await getUser(userId, token).catch(() => null);
  if (!aluno) notFound();

  const arvore = await montarArvore(CURSO_ID, userId, token);
  const { curso, resumo, linhaDoTempo } = arvore;

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} />

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        <header className="flex flex-col gap-3">
          <h1 className="m-0 text-[1.6rem]">Progresso de {aluno.name}</h1>
          <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">{aluno.email}</p>
          <div className="max-w-md">
            <BarraProgresso valor={resumo.percent} rotulo={curso.title} />
            <p className="mt-1.5 text-[.8rem] text-[var(--tm-ink-muted)]">
              {resumo.concluidos} de {resumo.totalTopicos} tópicos concluídos
            </p>
          </div>
        </header>

        {linhaDoTempo.length === 0 ? (
          <p className="text-[.9rem] text-[var(--tm-ink-muted)]">Ainda sem tópicos disponíveis.</p>
        ) : (
          <LinhaDoTempoTopicos
            linhaDoTempo={linhaDoTempo}
            hrefTopico={(id) => `/revisao/topico/${id}`}
          />
        )}
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
