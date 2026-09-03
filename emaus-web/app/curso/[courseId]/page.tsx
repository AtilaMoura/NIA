import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CabecalhoApp } from "../../_ui/CabecalhoApp";
import { BarraProgresso } from "../../_ui/BarraProgresso";
import { Rodape } from "../../_ui/Rodape";
import { ALUNO_USER_ID, TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import { getCourse, getUser } from "../../_lib/api";
import { montarArvore } from "../../_lib/arvore";
import { ArvoreCursoUI } from "./arvore-ui";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ courseId: string }>;
}): Promise<Metadata> {
  const { courseId } = await params;
  const curso = await getCourse(Number(courseId)).catch(() => null);
  return { title: curso?.title ?? "Curso" };
}

export default async function CursoPage({
  params,
}: {
  params: Promise<{ courseId: string }>;
}) {
  const { courseId: raw } = await params;
  const courseId = Number(raw);
  if (!Number.isInteger(courseId) || !(TEOLOGIA_COURSE_IDS as readonly number[]).includes(courseId)) {
    notFound();
  }

  const [arvore, usuario] = await Promise.all([
    montarArvore(courseId),
    getUser(ALUNO_USER_ID).catch(() => null),
  ]);
  const { curso, modulos, resumo, proximoTopico } = arvore;

  // Módulo que contém o próximo tópico — fica aberto no accordion.
  const moduloAbertoId =
    modulos.find((m) =>
      m.aulas.some((a) => a.topicos.some((t) => t.estado === "atual")),
    )?.id ?? null;

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"}>
        <Link href="/inicio" className="hover:text-[var(--tm-accent)]">
          Início
        </Link>
        <span className="text-[var(--tm-accent)]">Curso</span>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-6 px-[clamp(1rem,4vw,2rem)] py-8">
        <header className="flex flex-col gap-3">
          <h1 className="text-[1.7rem]">{curso.title}</h1>
          {curso.description && (
            <p className="m-0 max-w-2xl text-[.92rem] text-[var(--tm-ink-muted)]">
              {curso.description}
            </p>
          )}
          <div className="max-w-md">
            <BarraProgresso valor={resumo.percent} rotulo="Progresso do curso" />
            <p className="mt-1 text-[.8rem] text-[var(--tm-ink-muted)]">
              {resumo.concluidos} de {resumo.totalTopicos} tópicos concluídos
            </p>
          </div>
          {proximoTopico && (
            <p className="text-[.85rem]">
              Continuar em{" "}
              <Link
                href={`/topico/${proximoTopico.id}`}
                className="font-semibold text-[var(--tm-accent)] hover:underline"
              >
                {proximoTopico.titulo}
              </Link>
            </p>
          )}
        </header>

        <ArvoreCursoUI modulos={modulos} moduloAbertoId={moduloAbertoId} />
      </main>

      <Rodape />
    </>
  );
}
