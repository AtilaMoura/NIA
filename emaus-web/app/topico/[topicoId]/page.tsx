import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { AcoesTopico } from "./topico-ui";
import { temaDoCurso } from "../../_lib/tema";
import { getSessao, getToken } from "../../_lib/sessao";
import { papelPodeRevisar } from "../../_lib/papel";
import { CATALOGO, tituloCurto } from "../../_lib/catalogo";
import { TelaAviso } from "../../_ui/TelaAviso";
import { preferenciasDosSlides } from "../../_lib/preferencias-slides";
import {
  getTopico,
  getTopicoToken,
  listLessons,
  listModules,
  listTopicos,
  listTopicoProgress,
  topicoRenderUrl,
  type StatusTopico,
} from "../../_lib/api";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ topicoId: string }>;
}): Promise<Metadata> {
  const { topicoId } = await params;
  // Sem acesso, o backend responde 404/403 — nem o título vaza na aba
  const topico = await getTopico(Number(topicoId), await getToken()).catch(() => null);
  if (!topico) return { title: "Página não encontrada" };
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

  const emPreparacao = !topico.content || !topico.is_approved;
  const [lessons, modules, irmaos, progresso] = await Promise.all([
    listLessons(tokenSessao),
    listModules(tokenSessao),
    listTopicos(topico.lesson_id, tokenSessao),
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
  if (!modulo) notFound();
  const CURSO_ID = modulo.course_id;
  const tema = await temaDoCurso(CURSO_ID, tokenSessao);

  const ordenados = [...irmaos].sort((a, b) => a.topico_index - b.topico_index);
  const posicao = ordenados.findIndex((t) => t.id === topico.id);
  const proximo = ordenados
    .slice(posicao + 1)
    .find((t) => t.content && t.is_approved);
  const progTopico = progresso.find((p) => p.topico_id === topico.id) ?? null;
  const estadoInicial: StatusTopico = progTopico?.status ?? "nao_iniciado";
  const analiseInicial = progTopico?.tutor_analise?.ultima_avaliacao ?? null;


  // Texto "onde estou" da barra de cima do render (2026-09-27): a barra do Emaús
  // saiu — o render tem uma barra só, com voltar, título e menu ⋯ (Recomeçar lá dentro).
  const catalogo = CATALOGO.find((c) => c.courseId === CURSO_ID);
  const onde = [
    catalogo ? tituloCurto(catalogo) : null,
    aula ? `Aula ${aula.lesson_index}` : null,
    posicao >= 0 && ordenados.length > 0 ? `Tópico ${posicao + 1} de ${ordenados.length}` : null,
  ]
    .filter(Boolean)
    .join(" · ");

  if (emPreparacao) {
    return (
      <TelaAviso
        voltarHref={`/curso/${CURSO_ID}`}
        voltarRotulo="Voltar ao curso"
        onde={onde}
        tituloBarra={topico.titulo}
        icone="✍️"
        titulo="Este tópico ainda está em preparação"
        texto={`“${topico.titulo}” ainda não tem conteúdo publicado. Volte em breve.`}
        acao={{ href: `/curso/${CURSO_ID}`, rotulo: "Voltar ao curso" }}
      />
    );
  }


  return (
    <div className="flex h-[100dvh] flex-col">
      {/* conteúdo do backend, confiável — sem sandbox pra não quebrar o JS de slides.
          allow="fullscreen" é o que faz o botão "Tela cheia" do render funcionar dentro do iframe. */}
      <iframe
        src={topicoRenderUrl(topico.id, {
          ...(await preferenciasDosSlides()),
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
          onde,
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
