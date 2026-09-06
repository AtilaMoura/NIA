import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { LogoSimbolo } from "../../../_ui/Logo";
import { THEME_TOPICO, TEMA_POR_CURSO, ALUNO_USER_ID } from "../../../_lib/config";
import { getSessao, getToken } from "../../../_lib/sessao";
import { papelPodeRevisar } from "../../../_lib/papel";
import {
  getTopico,
  listLessons,
  listModules,
  listTopicoComments,
  listChecklistsTopico,
  topicoRenderUrl,
} from "../../../_lib/api";
import { PainelRevisao } from "./revisao-ui";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}): Promise<Metadata> {
  const { topicoId } = await params;
  const topico = await getTopico(Number(topicoId)).catch(() => null);
  return { title: topico ? `Revisar: ${topico.titulo}` : "Revisar tópico" };
}

export default async function RevisaoTopicoPage({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}) {
  const { topicoId: raw } = await params;
  const topicoId = Number(raw);
  if (!Number.isInteger(topicoId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/revisao/topico/${topicoId}`);
  if (!papelPodeRevisar(sessao.role)) redirect("/inicio");

  const topico = await getTopico(topicoId).catch(() => null);
  if (!topico) notFound();
  if (!topico.content) {
    return (
      <div className="mx-auto flex min-h-[100dvh] max-w-md flex-col items-start justify-center gap-4 px-[clamp(1rem,4vw,2rem)]">
        <h1 className="text-[1.3rem]">Este tópico ainda não tem conteúdo</h1>
        <Link href="/revisao" className="font-semibold text-[var(--tm-accent)] hover:underline">
          ‹ Voltar pra fila
        </Link>
      </div>
    );
  }

  const token = await getToken();
  const [lessons, modules, comentarios, checklists] = await Promise.all([
    listLessons(),
    listModules(),
    listTopicoComments(topicoId, token),
    listChecklistsTopico(topicoId, token),
  ]);
  const aula = lessons.find((l) => l.id === topico.lesson_id) ?? null;
  const modulo = aula ? modules.find((m) => m.id === aula.module_id) ?? null : null;
  const tema = (modulo && TEMA_POR_CURSO[modulo.course_id]) || THEME_TOPICO;
  const meuChecklist = checklists.find((c) => c.user_id === sessao.id) ?? null;

  return (
    <div className="flex h-[100dvh] flex-col">
      <div className="flex items-center gap-3 border-b border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-2.5 text-[.82rem]">
        <Link
          href="/revisao"
          className="inline-flex shrink-0 items-center gap-1.5 font-semibold text-[var(--tm-accent)] hover:underline"
        >
          <span aria-hidden>‹</span> Fila de revisão
        </Link>
        <span className="min-w-0 flex-1 truncate text-[var(--tm-ink-muted)]">
          {aula?.title} · {topico.titulo}
        </span>
        <Link href="/inicio" aria-label="Emaús — início" className="shrink-0">
          <LogoSimbolo size={28} className="opacity-80" />
        </Link>
      </div>

      <div className="flex min-h-0 flex-1 flex-col lg:flex-row">
        <iframe
          src={topicoRenderUrl(topico.id, { userId: ALUNO_USER_ID, theme: tema, contexto: "revisao" })}
          title={topico.titulo}
          className="min-h-[45dvh] w-full flex-1 border-0"
          allow="fullscreen"
          allowFullScreen
        />
        <PainelRevisao
          topicoId={topico.id}
          comentariosIniciais={comentarios}
          checklistsIniciais={checklists}
          meuChecklistInicial={meuChecklist}
          aprovado={topico.is_approved}
          reviewedBy={topico.reviewed_by}
        />
      </div>
    </div>
  );
}
