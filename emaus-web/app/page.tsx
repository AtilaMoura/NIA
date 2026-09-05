import Link from "next/link";
import type { Metadata } from "next";
import { CabecalhoApp } from "./_ui/CabecalhoApp";
import { LinkBotao } from "./_ui/Botao";
import { CapaCurso } from "./_ui/CapaCurso";
import { Logo, LogoSimbolo } from "./_ui/Logo";
import { CATALOGO, caminhoCapa, type CursoCatalogo } from "./_lib/catalogo";
import { capaExiste } from "./_lib/capas";
import { getSessao } from "./_lib/sessao";
import { listCourses } from "./_lib/api";

export const metadata: Metadata = {
  title: { absolute: "Emaús — cursos de formação bíblica" },
  description:
    "Cursos de Bíblia, doutrina e vida cristã feitos para a pessoa comum entender de verdade. Sem viés de denominação, no seu ritmo.",
};

function CardCurso({ curso, publicado }: { curso: CursoCatalogo; publicado: boolean }) {
  const capaUrl = capaExiste(curso.slug) ? caminhoCapa(curso.slug) : null;
  // "Acessível" = está no catálogo como disponível E foi publicado de verdade no NIA.
  const acessivel = curso.disponivel && curso.courseId != null && publicado;

  const corpo = (
    <>
      <div className="relative">
        <CapaCurso titulo={curso.titulo} tom={curso.tom} capaUrl={capaUrl} />
        {!acessivel && (
          <span className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] bg-black/45 px-2.5 py-1 text-[.7rem] font-semibold text-white backdrop-blur">
            <span aria-hidden>🔒</span> {curso.disponivel ? "Em revisão" : "Em breve"}
          </span>
        )}
      </div>
      <div className="flex flex-1 flex-col gap-1.5 p-4">
        <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.05rem] leading-snug">
          {curso.titulo}
        </h3>
        <p className="m-0 text-[.82rem] font-semibold text-[var(--tm-accent)]">{curso.subtitulo}</p>
        <p className="m-0 mt-1 text-[.83rem] leading-relaxed text-[var(--tm-ink-muted)]">
          {curso.descricao}
        </p>
        <div className="mt-3">
          {acessivel ? (
            <span className="text-[.82rem] font-semibold text-[var(--tm-accent)]">Começar →</span>
          ) : (
            <span className="text-[.82rem] text-[var(--tm-ink-muted)]">
              {curso.disponivel ? "Aguardando publicação" : "Em preparação"}
            </span>
          )}
        </div>
      </div>
    </>
  );

  const base =
    "flex flex-col overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] shadow-[var(--tm-shadow)]";

  if (acessivel) {
    return (
      <Link
        href={`/curso/${curso.courseId}`}
        className={`${base} transition-transform hover:-translate-y-1`}
      >
        {corpo}
      </Link>
    );
  }
  return (
    <div className={`${base} opacity-75`} aria-disabled>
      {corpo}
    </div>
  );
}

const PILARES = [
  {
    titulo: "Para entender de verdade",
    texto:
      "Sem jargão. Cada tópico mostra de onde vem a ideia no texto bíblico antes de dizer o que fazer com ela.",
    icone: (
      <path d="M4 5c4-1.5 8-1.5 8 1 0-2.5 4-2.5 8-1v13c-4-1.5-8-1.5-8 1 0-2.5-4-2.5-8-1V5z" />
    ),
  },
  {
    titulo: "No seu ritmo",
    texto:
      "Leitura, slides e um momento de aplicação em cada tópico. Pare, volte, revise quando quiser — o progresso fica salvo.",
    icone: <path d="M5 19c3-9 8-11 14-13M5 19h4M5 19v-4" />,
  },
  {
    titulo: "Sem viés de denominação",
    texto:
      "O foco é a Escritura e o que a fé cristã sustenta há séculos — não a bandeira de uma igreja específica.",
    icone: (
      <path d="M12 3c2.5 3.2 4 5.6 3.4 8.6C14.9 14 13.6 15.2 12 15.4c-1.7-.2-3-1.4-3.4-3.8C8 8.6 9.5 6.2 12 3z" />
    ),
  },
];

export default async function LandingPage() {
  const [sessao, cursosNia] = await Promise.all([
    getSessao(),
    listCourses().catch(() => []),
  ]);
  const publicadoPorId = new Map(cursosNia.map((c) => [c.id, c.status === "published"]));
  const estaPublicado = (curso: CursoCatalogo) =>
    curso.courseId != null && publicadoPorId.get(curso.courseId) === true;

  const primeiroAcessivel = CATALOGO.find((c) => c.disponivel && estaPublicado(c));

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao?.name ?? null} papel={sessao?.role} hrefMarca="/">
        <span className="text-[var(--tm-accent)]">Cursos</span>
        {sessao ? (
          <Link href="/inicio" className="hover:text-[var(--tm-accent)]">
            Continuar estudando
          </Link>
        ) : (
          <Link href="/entrar" className="hover:text-[var(--tm-accent)]">
            Entrar
          </Link>
        )}
      </CabecalhoApp>

      <main>
        {/* Hero */}
        <section className="grao overflow-hidden border-b border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="relative mx-auto max-w-[var(--tm-maxw)] px-[clamp(1rem,4vw,2rem)] py-16 sm:py-24">
            <LogoSimbolo
              size={340}
              decorativo
              className="pointer-events-none absolute -right-16 -top-10 hidden text-[var(--tm-accent)] opacity-[0.06] sm:block"
            />
            <div className="relative flex max-w-2xl flex-col items-start gap-5">
              <p className="m-0 text-[.78rem] font-semibold uppercase tracking-[.16em] text-[var(--tm-accent)]">
                Formação bíblica
              </p>
              <h1 className="m-0 text-[clamp(2rem,5.5vw,3.2rem)] leading-[1.08]">
                Estudar a Bíblia até o coração arder.
              </h1>
              <p className="m-0 max-w-xl text-[1.02rem] leading-relaxed text-[var(--tm-ink-muted)]">
                Cursos de Bíblia, doutrina e vida cristã para quem quer entender de verdade —
                sem viés de denominação, no seu ritmo.
              </p>
              {primeiroAcessivel?.courseId != null && (
                <div className="mt-1 flex flex-wrap items-center gap-3">
                  <LinkBotao href={`/curso/${primeiroAcessivel.courseId}`}>
                    Começar por “{primeiroAcessivel.titulo}”
                  </LinkBotao>
                  <Link
                    href="#cursos"
                    className="text-[.85rem] font-semibold text-[var(--tm-accent)] hover:underline"
                  >
                    Ver todos os cursos
                  </Link>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Pilares */}
        <section className="mx-auto max-w-[var(--tm-maxw)] px-[clamp(1rem,4vw,2rem)] py-14">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-3">
            {PILARES.map((p) => (
              <div key={p.titulo} className="flex flex-col gap-2">
                <svg
                  width="26"
                  height="26"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="var(--tm-accent)"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden
                >
                  {p.icone}
                </svg>
                <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.05rem]">
                  {p.titulo}
                </h3>
                <p className="m-0 text-[.88rem] leading-relaxed text-[var(--tm-ink-muted)]">
                  {p.texto}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Catálogo */}
        <section
          id="cursos"
          className="mx-auto max-w-[var(--tm-maxw)] scroll-mt-20 px-[clamp(1rem,4vw,2rem)] pb-20"
        >
          <div className="mb-6 flex items-baseline justify-between gap-4">
            <h2 className="m-0 text-[1.4rem]">Todos os cursos</h2>
            <span className="text-[.8rem] text-[var(--tm-ink-muted)]">
              {CATALOGO.filter((c) => c.disponivel && estaPublicado(c)).length} disponível ·{" "}
              {CATALOGO.filter((c) => !(c.disponivel && estaPublicado(c))).length} em preparação
            </span>
          </div>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {CATALOGO.map((curso) => (
              <CardCurso key={curso.slug} curso={curso} publicado={estaPublicado(curso)} />
            ))}
          </div>
        </section>
      </main>

      {/* Rodapé próprio da landing (mais completo que o Rodape padrão) */}
      <footer className="border-t border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
        <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-3 px-[clamp(1rem,4vw,2rem)] py-10">
          <Logo size={22} />
          <p
            className="m-0 max-w-md text-[.9rem] italic leading-relaxed text-[var(--tm-ink-muted)]"
            style={{ fontFamily: "var(--tm-font-display)" }}
          >
            “Não estava ardendo o nosso coração, quando ele nos falava pelo caminho e nos abria
            as Escrituras?” — Lucas 24.32
          </p>
          <p className="m-0 mt-2 text-[.72rem] text-[var(--tm-ink-muted)]">
            Emaús · plataforma de formação bíblica
          </p>
        </div>
      </footer>
    </>
  );
}
