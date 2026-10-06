import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { AcoesProva } from "./prova-ui";
import { temaDoCurso } from "../../../_lib/tema";
import { getSessao, getToken } from "../../../_lib/sessao";
import { papelPodeRevisar } from "../../../_lib/papel";
import { CATALOGO, tituloCurto } from "../../../_lib/catalogo";
import { TelaAviso } from "../../../_ui/TelaAviso";
import { preferenciasDosSlides } from "../../../_lib/preferencias-slides";
import {
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

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}): Promise<Metadata> {
  const { topicoId } = await params;
  // Sem acesso, o backend responde 404/403 — nem o título vaza na aba
  const topico = await getTopico(Number(topicoId), await getToken()).catch(() => null);
  if (!topico) return { title: "Página não encontrada" };
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
  const tokenSessao = await getToken();

  // Quem pode abrir é o backend que decide (2026-10-06): 404 = sem acesso (ou não
  // existe), 403 = curso ainda não publicado.
  const topico = await getTopico(topicoId, tokenSessao).catch((e: Error) =>
    e.message.startsWith("NIA 403") ? ("nao_publicado" as const) : null,
  );
  if (!topico) notFound();
  if (topico === "nao_publicado") {
    return (
      <TelaAviso
        voltarHref="/inicio"
        voltarRotulo="Voltar ao início"
        icone="🌱"
        titulo="Este curso ainda está em preparação"
        texto="Ele ainda não foi publicado. Volte em breve — enquanto isso, veja os cursos que já estão abertos."
        acao={{ href: "/inicio", rotulo: "Ver os cursos abertos" }}
      />
    );
  }

  // GATING: tópico não tem prova vinculada
  if (topico.avaliacao_id === null) notFound();

  const [lessons, modules, irmaos, progressoTopicos, progressoAvaliacoes] = await Promise.all([
    listLessons(tokenSessao),
    listModules(tokenSessao),
    listTopicos(topico.lesson_id, tokenSessao),
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
  if (!modulo) notFound();
  const CURSO_ID = modulo.course_id;
  const tema = await temaDoCurso(CURSO_ID, tokenSessao);

  const ordenados = [...irmaos].sort((a, b) => a.topico_index - b.topico_index);
  const posicao = ordenados.findIndex((t) => t.id === topico.id);

  const catalogo = CATALOGO.find((c) => c.courseId === CURSO_ID);
  const ondeTopico = [
    catalogo ? tituloCurto(catalogo) : null,
    aula ? `Aula ${aula.lesson_index}` : null,
    posicao >= 0 && ordenados.length > 0 ? `Tópico ${posicao + 1} de ${ordenados.length}` : null,
  ]
    .filter(Boolean)
    .join(" · ");

  // GATING DE VERDADE: tópico pai precisa estar concluído (salvo revisores)
  const progTopico = progressoTopicos.find((p) => p.topico_id === topico.id) ?? null;
  const statusTopico = progTopico?.status ?? "nao_iniciado";
  if (statusTopico !== "concluido" && !papelPodeRevisar(sessao.role)) {
    return (
      <TelaAviso
        voltarHref={`/topico/${topico.id}`}
        voltarRotulo="Voltar ao tópico"
        onde={ondeTopico}
        tituloBarra={topico.titulo}
        icone="🔒"
        titulo="A prova abre quando você concluir o tópico"
        texto={`Falta terminar “${topico.titulo}”.`}
        passos={[
          "Leia os slides até o fim e responda os checkpoints.",
          "No último slide, envie pro tutor corrigir.",
          "Pronto: a prova libera aqui.",
        ]}
        acao={{ href: `/topico/${topico.id}`, rotulo: "Continuar o tópico →" }}
      />
    );
  }

  // Progresso da PROVA (estadoInicial/analiseInicial vêm daqui, não do tópico)
  const progProva = progressoAvaliacoes.find((p) => p.avaliacao_id === topico.avaliacao_id) ?? null;
  const estadoInicial: StatusTopico = progProva?.status ?? "nao_iniciado";
  const analiseInicial = progProva?.tutor_analise?.ultima_avaliacao ?? null;


  // Mesma barra única do render do tópico (2026-09-27): voltar (ao tópico),
  // título e menu ⋯ com "Recomeçar esta prova".
  const onde = [catalogo ? tituloCurto(catalogo) : null, aula ? `Aula ${aula.lesson_index}` : null, "Prova do tópico"]
    .filter(Boolean)
    .join(" · ");

  return (
    <div className="flex h-[100dvh] flex-col">
      {/* conteúdo do backend, confiável — sem sandbox pra não quebrar o JS de slides.
          allow="fullscreen" é o que faz o botão "Tela cheia" do render funcionar dentro do iframe. */}
      <iframe
        src={avaliacaoRenderUrl(topico.avaliacao_id, {
          ...(await preferenciasDosSlides()),
          userId: sessao.id,
          theme: tema,
          respostasToken: respostasToken ?? undefined,
          // Reabrir uma prova já concluída mostra o resultado direto no slide
          // "Resultado" do render, sem precisar clicar em "Fim" de novo.
          concluido: estadoInicial === "concluido",
          avaliacaoInicial: analiseInicial,
          onde,
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