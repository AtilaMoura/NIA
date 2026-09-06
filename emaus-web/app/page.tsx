import Link from "next/link";
import type { Metadata } from "next";
import { CabecalhoApp } from "./_ui/CabecalhoApp";
import { LinkBotao } from "./_ui/Botao";
import { CapaCurso } from "./_ui/CapaCurso";
import { Rodape } from "./_ui/Rodape";
import { Carrossel } from "./_ui/Carrossel";
import { CATALOGO, caminhoCapa, type CursoCatalogo } from "./_lib/catalogo";
import { capaExiste } from "./_lib/capas";
import { imagemExiste, slidesHeroi } from "./_lib/imagens";
import { getSessao } from "./_lib/sessao";
import { listCourses, type Course } from "./_lib/api";

export const metadata: Metadata = {
  title: { absolute: "Emaús — cursos de formação bíblica" },
  description:
    "Cursos de Bíblia, doutrina e vida cristã feitos para a pessoa comum entender de verdade. Sem viés de denominação, no seu ritmo.",
};

const NIVEL_ROTULO: Record<string, string> = {
  "básico": "Nível básico",
  "intermediário": "Nível intermediário",
  "avançado": "Nível avançado",
  "especialista": "Nível especialista",
};

function CardCurso({
  curso,
  publicado,
  meta,
}: {
  curso: CursoCatalogo;
  publicado: boolean;
  meta?: Course;
}) {
  const capaUrl = capaExiste(curso.slug) ? caminhoCapa(curso.slug) : null;
  const acessivel = curso.disponivel && curso.courseId != null && publicado;

  const corpo = (
    <>
      <div className="relative">
        <CapaCurso titulo={curso.titulo} tom={curso.tom} capaUrl={capaUrl} />
        {!acessivel && (
          <span className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-[var(--tm-radius-pill)] bg-black/50 px-2.5 py-1 text-[.72rem] font-semibold text-white backdrop-blur">
            <span aria-hidden>🔒</span> {curso.disponivel ? "Em revisão" : "Em breve"}
          </span>
        )}
      </div>
      <div className="flex flex-1 flex-col gap-1.5 p-4">
        <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.05rem] leading-snug">
          {curso.titulo}
        </h3>
        <p className="m-0 text-[.82rem] font-semibold text-[var(--tm-accent)]">{curso.subtitulo}</p>
        <p className="m-0 mt-1 line-clamp-3 text-[.83rem] leading-relaxed text-[var(--tm-ink-muted)]">
          {curso.descricao}
        </p>
        {acessivel && (
          <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-[.72rem] text-[var(--tm-ink-muted)]">
            {meta?.level && <span>{NIVEL_ROTULO[meta.level] ?? meta.level}</span>}
            <span>Com tutor de IA</span>
            <span>No seu ritmo</span>
          </div>
        )}
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

const PASSOS = [
  {
    n: 1,
    slug: "passo-1-conta",
    titulo: "Crie sua conta",
    texto: "É de graça e leva um minuto. Nenhum cartão, nenhum compromisso.",
  },
  {
    n: 2,
    slug: "passo-2-escolher",
    titulo: "Escolha um curso",
    texto: "Comece pelo que faz sentido pra você agora — dá pra trocar quando quiser.",
  },
  {
    n: 3,
    slug: "passo-3-ritmo",
    titulo: "Estude tópico a tópico",
    texto: "Leitura, slides e um momento de aplicação. Pare e volte quando puder.",
  },
  {
    n: 4,
    slug: "passo-4-progresso",
    titulo: "Progresso e tutor acompanham",
    texto: "Seu avanço fica salvo, e um tutor aponta o que ficou raso antes de seguir.",
  },
];

const DIFERENCIAIS = [
  {
    titulo: "Para entender de verdade",
    texto:
      "Sem jargão. Cada tópico mostra de onde vem a ideia no texto bíblico antes de dizer o que fazer com ela.",
    icone: <path d="M4 5c4-1.5 8-1.5 8 1 0-2.5 4-2.5 8-1v13c-4-1.5-8-1.5-8 1 0-2.5-4-2.5-8-1V5z" />,
  },
  {
    titulo: "No seu ritmo",
    texto:
      "Leitura, slides e aplicação em cada tópico. Pare, volte, revise quando quiser — o progresso fica salvo.",
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
  const [sessao, cursosNia] = await Promise.all([getSessao(), listCourses().catch(() => [])]);
  const cursoPorId = new Map(cursosNia.map((c) => [c.id, c]));
  const estaPublicado = (curso: CursoCatalogo) =>
    curso.courseId != null && cursoPorId.get(curso.courseId)?.status === "published";

  const primeiroAcessivel = CATALOGO.find((c) => c.disponivel && estaPublicado(c));
  const heroi = slidesHeroi();
  const disponiveis = CATALOGO.filter((c) => c.disponivel && estaPublicado(c));
  const emBreve = CATALOGO.filter((c) => !(c.disponivel && estaPublicado(c)));

  const ctaPrimario = primeiroAcessivel?.courseId
    ? { href: `/curso/${primeiroAcessivel.courseId}`, texto: `Começar por "${primeiroAcessivel.titulo}"` }
    : { href: sessao ? "/inicio" : "/entrar", texto: "Começar agora" };

  return (
    <>
      <CabecalhoApp nomeUsuario={sessao?.name ?? null} papel={sessao?.role} />

      <main>
        {/* ---------- Herói ---------- */}
        <section className="grao overflow-hidden border-b border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="mx-auto grid max-w-[var(--tm-maxw)] items-center gap-10 px-[clamp(1rem,4vw,2rem)] py-14 sm:py-20 lg:grid-cols-[1.05fr_0.95fr] lg:gap-14">
            <div className="flex max-w-xl flex-col items-start gap-5">
              <p className="m-0 text-[.76rem] font-semibold uppercase tracking-[.18em] text-[var(--tm-accent)]">
                Formação bíblica
              </p>
              <h1 className="m-0 text-[clamp(2.1rem,5.5vw,3.4rem)] leading-[1.06]">
                Estudar a Bíblia até o coração arder.
              </h1>
              <p className="m-0 text-[1.05rem] leading-relaxed text-[var(--tm-ink-muted)]">
                Cursos de Bíblia, doutrina e vida cristã para a pessoa comum entender de
                verdade — sem viés de denominação, no seu ritmo, com um tutor que acompanha.
              </p>
              <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-3">
                <LinkBotao href={ctaPrimario.href}>{ctaPrimario.texto}</LinkBotao>
                <Link
                  href={sessao && primeiroAcessivel?.courseId ? `/curso/${primeiroAcessivel.courseId}` : "/entrar"}
                  className="text-[.88rem] font-semibold text-[var(--tm-accent)] hover:underline"
                >
                  Espiar um tópico →
                </Link>
              </div>
              <p className="m-0 text-[.8rem] text-[var(--tm-ink-muted)]">
                Grátis para começar · conteúdo revisado tópico a tópico
              </p>
            </div>

            <div className="w-full max-w-[22rem] justify-self-center sm:max-w-[26rem] lg:justify-self-end">
              {heroi.length > 0 ? (
                <Carrossel slides={heroi} className="w-full shadow-[var(--tm-shadow)]" />
              ) : (
                <div className="aspect-square w-full rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]" />
              )}
            </div>
          </div>
        </section>

        {/* ---------- Como funciona ---------- */}
        <section
          id="como-funciona"
          className="mx-auto max-w-[var(--tm-maxw)] scroll-mt-20 px-[clamp(1rem,4vw,2rem)] py-16"
        >
          <h2 className="m-0 mb-2 text-[1.5rem]">Como funciona</h2>
          <p className="m-0 mb-10 max-w-lg text-[.92rem] text-[var(--tm-ink-muted)]">
            Do cadastro ao primeiro tópico estudado, sem burocracia.
          </p>
          <ol className="m-0 grid list-none grid-cols-1 gap-x-8 gap-y-10 p-0 sm:grid-cols-2 lg:grid-cols-4">
            {PASSOS.map((p) => {
              const img = imagemExiste(`como-funciona/${p.slug}.png`)
                ? `/como-funciona/${p.slug}.png`
                : null;
              return (
                <li key={p.n} className="flex flex-col gap-3">
                  <div className="flex h-16 w-16 items-center justify-center rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
                    {img ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={img} alt="" className="h-11 w-11 object-contain" aria-hidden />
                    ) : (
                      <span
                        style={{ fontFamily: "var(--tm-font-display)" }}
                        className="text-[1.4rem] font-semibold text-[var(--tm-accent)]"
                      >
                        {p.n}
                      </span>
                    )}
                  </div>
                  <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 text-[1.02rem]">
                    {p.titulo}
                  </h3>
                  <p className="m-0 text-[.86rem] leading-relaxed text-[var(--tm-ink-muted)]">
                    {p.texto}
                  </p>
                </li>
              );
            })}
          </ol>
        </section>

        {/* ---------- Diferenciais ---------- */}
        <section className="border-y border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="mx-auto grid max-w-[var(--tm-maxw)] grid-cols-1 gap-10 px-[clamp(1rem,4vw,2rem)] py-16 sm:grid-cols-3">
            {DIFERENCIAIS.map((d) => (
              <div key={d.titulo} className="flex flex-col gap-3">
                <span className="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[var(--tm-verse-border)] bg-[var(--tm-verse-bg)]">
                  <svg
                    width="22"
                    height="22"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="var(--tm-accent)"
                    strokeWidth="1.6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden
                  >
                    {d.icone}
                  </svg>
                </span>
                <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 text-[1.1rem]">
                  {d.titulo}
                </h3>
                <p className="m-0 text-[.9rem] leading-relaxed text-[var(--tm-ink-muted)]">
                  {d.texto}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* ---------- Catálogo ---------- */}
        <section
          id="cursos"
          className="mx-auto max-w-[var(--tm-maxw)] scroll-mt-20 px-[clamp(1rem,4vw,2rem)] py-16"
        >
          <div className="mb-8 flex items-end justify-between gap-4">
            <div>
              <h2 className="m-0 text-[1.5rem]">Os cursos</h2>
              <p className="m-0 mt-1 text-[.9rem] text-[var(--tm-ink-muted)]">
                {disponiveis.length} disponível{disponiveis.length !== 1 ? "eis" : ""} ·{" "}
                {emBreve.length} em preparação
              </p>
            </div>
          </div>

          {disponiveis.length > 0 && (
            <div className="mb-10 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {disponiveis.map((curso) => (
                <CardCurso
                  key={curso.slug}
                  curso={curso}
                  publicado
                  meta={curso.courseId != null ? cursoPorId.get(curso.courseId) : undefined}
                />
              ))}
            </div>
          )}

          {emBreve.length > 0 && (
            <>
              <h3 className="m-0 mb-4 text-[.82rem] font-semibold uppercase tracking-[.12em] text-[var(--tm-ink-muted)]">
                Em preparação
              </h3>
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {emBreve.map((curso) => (
                  <CardCurso key={curso.slug} curso={curso} publicado={false} />
                ))}
              </div>
            </>
          )}
        </section>

        {/* ---------- CTA final ---------- */}
        <section className="grao border-t border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-col items-start gap-4 px-[clamp(1rem,4vw,2rem)] py-16 sm:items-center sm:text-center">
            <h2 className="m-0 max-w-xl text-[clamp(1.5rem,3.5vw,2rem)] leading-tight">
              Comece hoje. É de graça.
            </h2>
            <p className="m-0 max-w-md text-[.95rem] text-[var(--tm-ink-muted)]">
              Crie a conta e abra o primeiro tópico agora mesmo.
            </p>
            <LinkBotao href={ctaPrimario.href} className="mt-1">
              {ctaPrimario.texto}
            </LinkBotao>
          </div>
        </section>
      </main>

      <Rodape logado={!!sessao} papel={sessao?.role} versiculo />
    </>
  );
}
