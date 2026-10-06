import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../_ui/CabecalhoApp";
import { Rodape } from "../../_ui/Rodape";
import { LinkBotao } from "../../_ui/Botao";
import { getCourse, getUser } from "../../_lib/api";
import { montarArvore } from "../../_lib/arvore";
import { getSessao, getToken } from "../../_lib/sessao";
import { papelPodeRevisar } from "../../_lib/papel";
import { CATALOGO, caminhoCapa, tituloCurto } from "../../_lib/catalogo";
import { capaExiste } from "../../_lib/capas";
import { CapaCurso } from "../../_ui/CapaCurso";
import { ArvoreCursoUI } from "./arvore-ui";

const NIVEL_ROTULO: Record<string, string> = {
  "básico": "Nível básico",
  "intermediário": "Nível intermediário",
  "avançado": "Nível avançado",
  "especialista": "Nível especialista",
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ courseId: string }>;
}): Promise<Metadata> {
  const { courseId } = await params;
  // Quem não pode ver o curso recebe 404 do backend — nem o nome vaza na aba
  const curso = await getCourse(Number(courseId), await getToken()).catch(() => null);
  if (!curso) return { title: "Página não encontrada" };
  // Mesmo título do topo da página (catálogo), não o nome antigo do banco
  const catalogo = CATALOGO.find((c) => c.courseId === Number(courseId));
  return { title: catalogo ? tituloCurto(catalogo) : curso.title };
}

export default async function CursoPage({
  params,
}: {
  params: Promise<{ courseId: string }>;
}) {
  const { courseId: raw } = await params;
  const courseId = Number(raw);
  if (!Number.isInteger(courseId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/curso/${courseId}`);
  const token = await getToken();

  // Quem pode ver este curso é o backend que diz: sem acesso, 404 (2026-10-06)
  const [arvore, usuario] = await Promise.all([
    montarArvore(courseId, sessao.id, token).catch(() => null),
    getUser(sessao.id, token).catch(() => null),
  ]);
  if (!arvore) notFound();
  const { curso, modulos, resumo, linhaDoTempo } = arvore;
  // Título/subtítulo/descrição/capa vêm do catálogo do Emaús (o banco guarda o
  // título antigo em alguns cursos); o banco é o fallback.
  const catalogo = CATALOGO.find((c) => c.courseId === courseId);
  const titulo = catalogo ? tituloCurto(catalogo) : curso.title;
  const descricao = catalogo?.descricao ?? curso.description;
  const capaUrl = catalogo && capaExiste(catalogo.slug) ? caminhoCapa(catalogo.slug) : null;
  const proximo = linhaDoTempo.find((t) => t.estado === "atual") ?? null;

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

      <main className="mx-auto flex max-w-[1000px] flex-col gap-6 px-[clamp(1rem,4vw,2rem)] pb-16 pt-6">
        {!publicado && (
          <p className="m-0 rounded-[var(--tm-radius)] border border-dashed border-[var(--tm-warn)] bg-[var(--tm-verse-bg)] px-3 py-2 text-[.82rem] text-[var(--tm-warn)]">
            Prévia — este curso ainda não foi publicado. O aluno não consegue acessá-lo.{" "}
            <Link href={`/revisao/curso/${courseId}`} className="font-semibold underline">
              Ir para a governança
            </Link>
          </p>
        )}
        <Link
          href={curso.visibilidade === "privado" ? "/estudos" : "/inicio"}
          className="self-start text-[.85rem] font-semibold text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]"
        >
          ← {curso.visibilidade === "privado" ? "Meus estudos" : "Início"}
        </Link>

        {/* Topo compacto (redesign 2026-09-27, protótipo 04-curso.html): capa menor
            ao lado do título em TEXTO — a capa do backend tinha o título antigo
            escrito na imagem e ocupava a primeira tela inteira. */}
        <header className="grid items-center gap-5 md:grid-cols-[320px_1fr] md:gap-8">
          <div className="relative aspect-[21/9] overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] shadow-[var(--tm-shadow)] md:aspect-[4/3]">
            <div className="absolute inset-0 [&>div]:h-full">
              <CapaCurso titulo={titulo} tom={catalogo?.tom ?? "trigo"} capaUrl={capaUrl} />
            </div>
          </div>
          <div>
            <p className="m-0 text-[.72rem] font-bold uppercase tracking-[.14em] text-[var(--tm-accent)]">
              {[catalogo?.categoria, NIVEL_ROTULO[curso.level]].filter(Boolean).join(" · ")}
            </p>
            <h1 className="m-0 mt-1 text-[clamp(1.6rem,4vw,2.2rem)] leading-[1.12]">{titulo}</h1>
            {catalogo?.subtitulo && (
              <p
                className="m-0 mt-1 text-[1.05rem] italic text-[var(--tm-ink-muted)]"
                style={{ fontFamily: "var(--tm-font-display)" }}
              >
                {catalogo.subtitulo}
              </p>
            )}
            {descricao && (
              <p className="m-0 mt-3 max-w-xl text-[.95rem] text-[var(--tm-ink-muted)]">{descricao}</p>
            )}
            <p className="m-0 mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[.82rem] text-[var(--tm-ink-muted)]">
              <span>
                <b className="font-semibold text-[var(--tm-ink)]">{modulos.length}</b> módulo
                {modulos.length !== 1 ? "s" : ""}
              </span>
              <span>
                <b className="font-semibold text-[var(--tm-ink)]">{resumo.totalTopicos}</b> tópico
                {resumo.totalTopicos !== 1 ? "s" : ""}
              </span>
              <span>Com tutor de IA</span>
              <span>No seu ritmo</span>
            </p>
          </div>
        </header>

        {/* Ação principal: próximo tópico + progresso + Continuar */}
        <section className="grid items-center gap-4 rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-5 shadow-[var(--tm-shadow)] md:grid-cols-[1fr_auto] md:px-6">
          <div>
            <p className="m-0 text-[.8rem] text-[var(--tm-ink-muted)]">
              {proximo ? (resumo.concluidos === 0 ? "Comece pelo primeiro tópico" : "Próximo tópico") : "Curso"}
            </p>
            <p className="m-0 mt-0.5 font-semibold">
              {proximo
                ? [proximo.titulo, proximo.referencia_biblica].filter(Boolean).join(" · ")
                : resumo.totalTopicos > 0 && resumo.concluidos === resumo.totalTopicos
                  ? "Você concluiu todos os tópicos 🎉"
                  : "Os próximos tópicos estão em preparação"}
            </p>
            <div className="mt-2.5 flex items-center gap-3 text-[.82rem] text-[var(--tm-ink-muted)]">
              <span className="h-1.5 max-w-[360px] flex-1 overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
                <span
                  className="block h-full rounded-full bg-[var(--tm-good)]"
                  style={{ width: `${resumo.percent}%` }}
                />
              </span>
              {resumo.concluidos} de {resumo.totalTopicos} tópicos · {resumo.percent}%
            </div>
          </div>
          {proximo && (
            <LinkBotao href={`/topico/${proximo.id}`} className="w-full md:w-auto">
              {resumo.concluidos === 0 ? "Começar o curso →" : "Continuar →"}
            </LinkBotao>
          )}
        </section>

        <ArvoreCursoUI modulos={modulos} moduloAbertoId={moduloAbertoId} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
