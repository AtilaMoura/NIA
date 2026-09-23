import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { LinkBotao } from "../../../_ui/Botao";
import { LogoSimbolo } from "../../../_ui/Logo";
import { AcoesProva } from "./prova-ui";
import { ReiniciarAvaliacaoBotao } from "./reiniciar-avaliacao-botao";
import { THEME_TOPICO, TEMA_POR_CURSO, TEOLOGIA_COURSE_IDS } from "../../../_lib/config";
import { getSessao, getToken } from "../../../_lib/sessao";
import { papelPodeRevisar } from "../../../_lib/papel";
import {
  getCourse,
  getTopico,
  getAvaliacaoToken,
  listLessons,
  listModules,
  listTopicos,
  listTopicoProgress,
  listAvaliacaoProgress,
  avaliacaoRenderUrl,
  type StatusTopico,
} from "../../../_lib/api";

const CURSO_ID_FALLBACK = TEOLOGIA_COURSE_IDS[0];

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}): Promise<Metadata> {
  const { topicoId } = await params;
  const topico = await getTopico(Number(topicoId)).catch(() => null);
  return { title: topico ? `${topico.titulo} — Prova` : "Prova" };
}

export default async function ProvaPage({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}) {
  const { topicoId: raw } = await params;
  const topicoId = Number(raw);
  if (!Number.isInteger(topicoId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/topico/${topicoId}/prova`);

  const topico = await getTopico(topicoId).catch(() => null);
  if (!topico) notFound();

  // GATING: tópico não tem prova vinculada
  if (topico.avaliacao_id === null) notFound();

  const tokenSessao = await getToken();

  const [lessons, modules, irmaos, progressoTopicos, progressoAvaliacoes] = await Promise.all([
    listLessons(),
    listModules(),
    listTopicos(topico.lesson_id),
    listTopicoProgress(sessao.id, tokenSessao),
    listAvaliacaoProgress(sessao.id, tokenSessao),
  ]);

  // Token de escopo curto pro <iframe> salvar resposta da prova (2026-09-19)
  let respostasToken: string | null = null;
  if (tokenSessao) {
    respostasToken = await getAvaliacaoToken(tokenSessao, topico.avaliacao_id).catch(() => null);
  }

  const aula = lessons.find((l) => l.id === topico.lesson_id) ?? null;
  const modulo = aula ? modules.find((m) => m.id === aula.module_id) ?? null : null;
  const CURSO_ID = modulo?.course_id ?? CURSO_ID_FALLBACK;
  const tema = TEMA_POR_CURSO[CURSO_ID] ?? THEME_TOPICO;

  // Curso não publicado: só quem revisa passa (o aluno vê tela de gating).
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

  // GATING DE VERDADE: tópico pai precisa estar concluído (salvo revisores)
  const progTopico = progressoTopicos.find((p) => p.topico_id === topico.id) ?? null;
  const statusTopico = progTopico?.status ?? "nao_iniciado";
  if (statusTopico !== "concluido" && !papelPodeRevisar(sessao.role)) {
    return (
      <div className="flex min-h-[100dvh] flex-col">
        <div
          id="barra-topo-topico"
          className="flex items-center gap-3 border-b border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-2.5 text-[.82rem]"
        >
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
        <main className="mx-auto flex max-w-md flex-1 flex-col items-start justify-center gap-4 px-[clamp(1rem,4vw,2rem)]">
          <h1 className="text-[1.4rem]">Termine o tópico primeiro</h1>
          <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
            Você precisa concluir o tópico antes de fazer a prova.&nbsp;“{topico.titulo}”
          </p>
          <LinkBotao href={`/topico/${topico.id}`} variante="fantasma">
            Voltar ao tópico
          </LinkBotao>
        </main>
      </div>
    );
  }

  // Progresso da PROVA (estadoInicial/analiseInicial vêm daqui, não do tópico)
  const progProva = progressoAvaliacoes.find((p) => p.avaliacao_id === topico.avaliacao_id) ?? null;
  const estadoInicial: StatusTopico = progProva?.status ?? "nao_iniciado";
  const analiseInicial = progProva?.tutor_analise?.ultima_avaliacao ?? null;

  const barraTopo = (
    <div
      id="barra-topo-topico"
      className="flex items-center gap-3 border-b border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-2.5 text-[.82rem]"
    >
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
      <ReiniciarAvaliacaoBotao avaliacaoId={topico.avaliacao_id} />
      <Link href="/inicio" aria-label="Emaús — início" className="shrink-0">
        <LogoSimbolo size={28} className="opacity-80" />
      </Link>
    </div>
  );

  return (
    <div className="flex h-[100dvh] flex-col">
      {barraTopo}
      {/* conteúdo do backend, confiável — sem sandbox pra não quebrar o JS de slides.
          allow="fullscreen" é o que faz o botão "Tela cheia" do render funcionar dentro do iframe. */}
      <iframe
        src={avaliacaoRenderUrl(topico.avaliacao_id, {
          userId: sessao.id,
          theme: tema,
          respostasToken: respostasToken ?? undefined,
          // Reabrir uma prova já concluída mostra o resultado direto no slide
          // "Resultado" do render, sem precisar clicar em "Fim" de novo.
          concluido: estadoInicial === "concluido",
          avaliacaoInicial: analiseInicial,
        })}
        title={`${topico.titulo} — Prova`}
        className="w-full flex-1 border-0"
        allow="fullscreen"
        allowFullScreen
      />
      <AcoesProva
        avaliacaoId={topico.avaliacao_id}
        topicoId={topico.id}
        estadoInicial={estadoInicial}
      />
    </div>
  );
}