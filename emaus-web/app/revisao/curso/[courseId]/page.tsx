import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../../_ui/CabecalhoApp";
import { Rodape } from "../../../_ui/Rodape";
import { getSessao, getToken } from "../../../_lib/sessao";
import { papelPodeRevisar } from "../../../_lib/papel";
import { getCourse, getGovernancaCurso } from "../../../_lib/api";
import { GovernancaCursoUI } from "./governanca-ui";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ courseId: string }>;
}): Promise<Metadata> {
  const { courseId } = await params;
  const curso = await getCourse(Number(courseId)).catch(() => null);
  return { title: curso ? `Governança: ${curso.title}` : "Governança do curso" };
}

export default async function GovernancaCursoPage({
  params,
}: {
  params: Promise<{ courseId: string }>;
}) {
  const { courseId: raw } = await params;
  const courseId = Number(raw);
  if (!Number.isInteger(courseId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/revisao/curso/${courseId}`);
  if (!papelPodeRevisar(sessao.role)) redirect("/inicio");

  const curso = await getCourse(courseId).catch(() => null);
  if (!curso) notFound();

  const token = await getToken();
  const governanca = await getGovernancaCurso(courseId, token);
  if (!governanca) notFound();

  const souAdmin = sessao.role === "master" || sessao.role === "admin";

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao.name} papel={sessao.role} hrefMarca="/revisao">
        <Link href="/revisao" className="hover:text-[var(--tm-accent)]">
          Fila de revisão
        </Link>
        <span className="text-[var(--tm-accent)]">Governança do curso</span>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-2xl flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        <h1 className="m-0 text-[1.5rem]">Governança — {curso.title}</h1>

        <GovernancaCursoUI
          courseId={courseId}
          governancaInicial={governanca}
          meuUserId={sessao.id}
          meuPapel={sessao.role}
          souAdmin={souAdmin}
        />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
