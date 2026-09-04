import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { LinkBotao } from "../../_ui/Botao";
import { LogoSimbolo } from "../../_ui/Logo";
import { AcoesTopico } from "./topico-ui";
import { ALUNO_USER_ID, THEME_TOPICO, TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import {
  getTopico,
  listLessons,
  listTopicos,
  listTopicoProgress,
  topicoRenderUrl,
  type StatusTopico,
} from "../../_lib/api";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}): Promise<Metadata> {
  const { topicoId } = await params;
  const topico = await getTopico(Number(topicoId)).catch(() => null);
  return { title: topico?.titulo ?? "Tópico" };
}

export default async function TopicoPage({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}) {
  const { topicoId: raw } = await params;
  const topicoId = Number(raw);
  if (!Number.isInteger(topicoId)) notFound();

  const topico = await getTopico(topicoId).catch(() => null);
  if (!topico) notFound();

  const emPreparacao = !topico.content || !topico.is_approved;

  const [lessons, irmaos, progresso] = await Promise.all([
    listLessons(),
    listTopicos(topico.lesson_id),
    listTopicoProgress(ALUNO_USER_ID),
  ]);

  const aula = lessons.find((l) => l.id === topico.lesson_id) ?? null;
  const ordenados = [...irmaos].sort((a, b) => a.topico_index - b.topico_index);
  const posicao = ordenados.findIndex((t) => t.id === topico.id);
  const proximo = ordenados
    .slice(posicao + 1)
    .find((t) => t.content && t.is_approved);
  const progTopico = progresso.find((p) => p.topico_id === topico.id) ?? null;
  const estadoInicial: StatusTopico = progTopico?.status ?? "nao_iniciado";
  const analiseInicial = progTopico?.tutor_analise?.ultima_avaliacao ?? null;

  const barraTopo = (
    <div className="flex items-center gap-3 border-b border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-2.5 text-[.82rem]">
      <Link
        href={`/curso/${CURSO_ID}`}
        className="inline-flex shrink-0 items-center gap-1.5 font-semibold text-[var(--tm-accent)] hover:underline"
      >
        <span aria-hidden>‹</span> Voltar ao curso
      </Link>
      <span className="min-w-0 flex-1 truncate text-[var(--tm-ink-muted)]">
        {aula?.title}
        {posicao >= 0 && ordenados.length > 0 && (
          <span className="ml-2 whitespace-nowrap">
            · Tópico {posicao + 1} de {ordenados.length}
          </span>
        )}
      </span>
      <Link href="/inicio" aria-label="Emaús — início" className="shrink-0">
        <LogoSimbolo size={28} className="opacity-80" />
      </Link>
    </div>
  );

  if (emPreparacao) {
    return (
      <div className="flex min-h-[100dvh] flex-col">
        {barraTopo}
        <main className="mx-auto flex max-w-md flex-1 flex-col items-start justify-center gap-4 px-[clamp(1rem,4vw,2rem)]">
          <h1 className="text-[1.4rem]">Este tópico ainda está em preparação</h1>
          <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
            “{topico.titulo}” ainda não tem conteúdo publicado. Volte em breve.
          </p>
          <LinkBotao href={`/curso/${CURSO_ID}`} variante="fantasma">
            Voltar ao curso
          </LinkBotao>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-[100dvh] flex-col">
      {barraTopo}
      {/* conteúdo do backend, confiável — sem sandbox pra não quebrar o JS de slides.
          allow="fullscreen" é o que faz o botão "Tela cheia" do render funcionar dentro do iframe. */}
      <iframe
        src={topicoRenderUrl(topico.id, { userId: ALUNO_USER_ID, theme: THEME_TOPICO })}
        title={topico.titulo}
        className="w-full flex-1 border-0"
        allow="fullscreen"
        allowFullScreen
      />
      <AcoesTopico
        topicoId={topico.id}
        estadoInicial={estadoInicial}
        proximoTopicoId={proximo?.id ?? null}
        analiseInicial={analiseInicial}
      />
    </div>
  );
}
