import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { LinkBotao } from "../../_ui/Botao";
import { LogoSimbolo } from "../../_ui/Logo";
import { AcoesTopico } from "./topico-ui";
import { ReiniciarTopicoBotao } from "./reiniciar-botao";
import { THEME_TOPICO, TEMA_POR_CURSO, TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import { getSessao, getToken } from "../../_lib/sessao";
import { papelPodeRevisar } from "../../_lib/papel";
import {
  getCourse,
  getTopico,
  getTopicoToken,
  listLessons,
  listModules,
  listTopicos,
  listTopicoProgress,
  topicoRenderUrl,
  type StatusTopico,
} from "../../_lib/api";

const CURSO_ID_FALLBACK = TEOLOGIA_COURSE_IDS[0];

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
  searchParams,
}: {
  params: Promise<{ topicoId: string }>;
  searchParams: Promise<{ slide?: string }>;
}) {
  const { topicoId: raw } = await params;
  // ?slide=N (1-based) — vem do "📖 Rever no slide N" da revisão da prova
  // (2026-09-23): abre o tópico direto no slide pra reler.
  const slidePedido = Number((await searchParams).slide);
  const topicoId = Number(raw);
  if (!Number.isInteger(topicoId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/topico/${topicoId}`);

  const topico = await getTopico(topicoId).catch(() => null);
  if (!topico) notFound();

  const emPreparacao = !topico.content || !topico.is_approved;
  const tokenSessao = await getToken();

  const [lessons, modules, irmaos, progresso] = await Promise.all([
    listLessons(),
    listModules(),
    listTopicos(topico.lesson_id),
    listTopicoProgress(sessao.id, tokenSessao),
  ]);

  // Token de escopo curto pro <iframe> salvar resposta de exercício (2026-09-09)
  // e anotação por slide. Só busca se o tópico é mesmo exibível — sem isso o
  // render funciona igual, só sem salvar (mesmo comportamento de antes desta
  // função existir).
  let respostasToken: string | null = null;
  if (!emPreparacao && tokenSessao) {
    respostasToken = await getTopicoToken(tokenSessao, topico.id).catch(() => null);
  }

  const aula = lessons.find((l) => l.id === topico.lesson_id) ?? null;
  const modulo = aula ? modules.find((m) => m.id === aula.module_id) ?? null : null;
  const CURSO_ID = modulo?.course_id ?? CURSO_ID_FALLBACK;
  const tema = TEMA_POR_CURSO[CURSO_ID] ?? THEME_TOPICO;

  // Curso não publicado: só quem revisa passa (o aluno vê "em preparação").
  const curso = await getCourse(CURSO_ID).catch(() => null);
  if (curso && curso.status !== "published" && !papelPodeRevisar(sessao.role)) {
    return (
      <main className="mx-auto flex min-h-[100dvh] max-w-md flex-col items-start justify-center gap-4 px-[clamp(1rem,4vw,2rem)]">
        <h1 className="text-[1.4rem]">Curso em preparação</h1>
        <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
          Este curso ainda não foi publicado.
        </p>
        <LinkBotao href="/" variante="fantasma">
          Ver os cursos disponíveis
        </LinkBotao>
      </main>
    );
  }
  const ordenados = [...irmaos].sort((a, b) => a.topico_index - b.topico_index);
  const posicao = ordenados.findIndex((t) => t.id === topico.id);
  const proximo = ordenados
    .slice(posicao + 1)
    .find((t) => t.content && t.is_approved);
  const progTopico = progresso.find((p) => p.topico_id === topico.id) ?? null;
  const estadoInicial: StatusTopico = progTopico?.status ?? "nao_iniciado";
  const analiseInicial = progTopico?.tutor_analise?.ultima_avaliacao ?? null;

  const barraTopo = (
    <div
      id="barra-topo-topico"
      className="flex items-center gap-3 border-b border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-2.5 text-[.82rem]">
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
      {!emPreparacao && <ReiniciarTopicoBotao topicoId={topico.id} />}
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
        src={topicoRenderUrl(topico.id, {
          userId: sessao.id,
          theme: tema,
          // botão "📄 PDF" no render só pra quem revisa (professor/admin/master)
          pdf: papelPodeRevisar(sessao.role),
          respostasToken: respostasToken ?? undefined,
          // Reabrir um tópico já concluído mostra o resultado direto no slide
          // "Resultado" do render, sem precisar clicar em "Fim" de novo.
          concluido: estadoInicial === "concluido",
          avaliacaoInicial: analiseInicial,
          temProximo: proximo?.id != null,
          avaliacaoId: topico.avaliacao_id,
          slide: Number.isInteger(slidePedido) && slidePedido > 0 ? slidePedido : undefined,
        })}
        title={topico.titulo}
        className="w-full flex-1 border-0"
        allow="fullscreen"
        allowFullScreen
      />
      <AcoesTopico
        topicoId={topico.id}
        cursoId={CURSO_ID}
        estadoInicial={estadoInicial}
        proximoTopicoId={proximo?.id ?? null}
        avaliacaoId={topico.avaliacao_id}
      />
    </div>
  );
}
