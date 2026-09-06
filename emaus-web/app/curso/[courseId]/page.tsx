import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../_ui/CabecalhoApp";
import { BarraProgresso } from "../../_ui/BarraProgresso";
import { Rodape } from "../../_ui/Rodape";
import { LinkBotao } from "../../_ui/Botao";
import { TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import { getCourse, getUser } from "../../_lib/api";
import { montarArvore } from "../../_lib/arvore";
import { getSessao } from "../../_lib/sessao";
import { papelPodeRevisar } from "../../_lib/papel";
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

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/curso/${courseId}`);

  const [arvore, usuario] = await Promise.all([
    montarArvore(courseId, sessao.id),
    getUser(sessao.id).catch(() => null),
  ]);
  const { curso, modulos, resumo, proximoTopico } = arvore;

  const publicado = curso.status === "published";
  const podeRevisar = papelPodeRevisar(sessao.role);

  // Curso não publicado: aluno não entra; quem revisa vê com um aviso de prévia.
  if (!publicado && !podeRevisar) {
    return (
      <>
        <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />
        <main className="mx-auto flex max-w-md flex-col items-start gap-4 px-[clamp(1rem,4vw,2rem)] py-16">
          <h1 className="m-0 text-[1.5rem]">{curso.title}</h1>
          <p className="m-0 text-[.92rem] text-[var(--tm-ink-muted)]">
            Este curso ainda está em preparação e não foi publicado. Volte em breve.
          </p>
          <LinkBotao href="/" variante="fantasma">
            Ver os cursos disponíveis
          </LinkBotao>
        </main>
        <Rodape papel={sessao.role} />
      </>
    );
  }

  // Módulo que contém o próximo tópico — fica aberto no accordion.
  const moduloAbertoId =
    modulos.find((m) => m.aulas.some((a) => a.topicos.some((t) => t.estado === "atual")))?.id ??
    null;

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-6 px-[clamp(1rem,4vw,2rem)] py-8">
        {!publicado && (
          <p className="m-0 rounded-[var(--tm-radius)] border border-dashed border-[var(--tm-warn)] bg-[var(--tm-verse-bg)] px-3 py-2 text-[.82rem] text-[var(--tm-warn)]">
            Prévia — este curso ainda não foi publicado. O aluno não consegue acessá-lo.{" "}
            <Link href={`/revisao/curso/${courseId}`} className="font-semibold underline">
              Ir para a governança
            </Link>
          </p>
        )}
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

      <Rodape papel={sessao.role} />
    </>
  );
}
