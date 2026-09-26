import Link from "next/link";
import { redirect } from "next/navigation";
import type { Metadata } from "next";
import { CabecalhoApp } from "./_ui/CabecalhoApp";
import { LinkBotao } from "./_ui/Botao";
import { CapaCurso } from "./_ui/CapaCurso";
import { Rodape } from "./_ui/Rodape";
import { CATALOGO, caminhoCapa, type CursoCatalogo } from "./_lib/catalogo";
import { capaExiste } from "./_lib/capas";
import { slidesHeroi } from "./_lib/imagens";
import { getSessao } from "./_lib/sessao";
import { listCourses } from "./_lib/api";

// Página de visitante (redesign 2026-09-26, protótipo aprovado em
// prototipos-front/01-visitante.html). Curta e direta: apresenta a plataforma,
// mostra só 3 cursos em destaque e chama pra criar conta. Nada de grade completa
// nem de estudos pessoais — esses ficam numa página só do Master.
// Logado não vê esta página: vai direto pra /inicio.

export const metadata: Metadata = {
  title: { absolute: "Emaús — cursos de formação bíblica" },
  description:
    "Cursos de Bíblia e vida cristã para entender de verdade: no seu ritmo, sem viés de denominação e com um tutor que acompanha.",
};

// Cursos em destaque, na ordem de exibição (slugs do CATALOGO).
const DESTAQUES = ["formacao-novo-obreiro", "panorama-da-biblia", "como-estudar-a-biblia"];

// Título curto só pra caber no card (o título completo continua no catálogo).
const TITULO_CURTO: Record<string, string> = {
  "formacao-novo-obreiro": "Formação do Obreiro I",
};

const PASSOS = [
  { titulo: "Escolha um curso", texto: "Comece pelo que faz sentido pra você agora." },
  { titulo: "Estude tópico a tópico", texto: "Leitura, slides e aplicação. Pare e volte quando puder." },
  { titulo: "O tutor acompanha", texto: "Seu progresso fica salvo e o tutor aponta o que revisar." },
];

function CardDestaque({ curso, aberto }: { curso: CursoCatalogo; aberto: boolean }) {
  const capaUrl = capaExiste(curso.slug) ? caminhoCapa(curso.slug) : null;
  const titulo = TITULO_CURTO[curso.slug] ?? curso.titulo;

  // "Em breve" fica compacto (capa pequena ao lado do texto) até o desktop;
  // o curso aberto fica horizontal e largo no tablet.
  const layout = aberto
    ? "flex-col sm:col-span-2 sm:flex-row lg:col-span-1 lg:flex-col"
    : "flex-row lg:flex-col";
  const capaLayout = aberto
    ? "sm:w-[48%] sm:flex-none lg:w-full"
    : "w-[34%] flex-none lg:w-full";

  const corpo = (
    <>
      <div className={`relative overflow-hidden ${capaLayout}`}>
        <CapaCurso titulo={curso.titulo} tom={curso.tom} capaUrl={capaUrl} className="h-full" />
        <span
          className={
            "absolute left-2.5 top-2.5 rounded-[var(--tm-radius-pill)] px-2.5 py-1 text-[.7rem] font-semibold " +
            (aberto ? "bg-[var(--tm-accent)] text-[var(--tm-bg)]" : "bg-black/60 text-white")
          }
        >
          {aberto ? "Aberto" : "Em breve"}
        </span>
      </div>
      <div className={`flex flex-1 flex-col gap-1 ${aberto ? "p-4 sm:justify-center sm:p-6 lg:justify-start lg:p-4" : "p-3.5 lg:p-4"}`}>
        <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 text-[1.05rem] leading-snug">
          {titulo}
        </h3>
        <p className="m-0 text-[.82rem] font-semibold text-[var(--tm-accent)]">{curso.subtitulo}</p>
        <p
          className={
            "m-0 mt-1 line-clamp-3 text-[.85rem] leading-relaxed text-[var(--tm-ink-muted)] " +
            (aberto ? "" : "hidden lg:block")
          }
        >
          {curso.descricao}
        </p>
        {aberto && (
          <span className="mt-auto pt-2 text-[.85rem] font-semibold text-[var(--tm-accent)]">Começar →</span>
        )}
      </div>
    </>
  );

  const base = `flex overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] shadow-[var(--tm-shadow)] ${layout}`;

  if (aberto && curso.courseId != null) {
    return (
      <Link href={`/curso/${curso.courseId}`} className={`${base} transition-transform hover:-translate-y-1`}>
        {corpo}
      </Link>
    );
  }
  return (
    <div className={base} aria-disabled>
      {corpo}
    </div>
  );
}

export default async function PaginaVisitante() {
  const sessao = await getSessao();
  if (sessao) redirect("/inicio");

  const cursosNia = await listCourses().catch(() => []);
  const publicado = (c: CursoCatalogo) =>
    c.disponivel && c.courseId != null && cursosNia.some((n) => n.id === c.courseId && n.status === "published");

  const destaques = DESTAQUES.map((slug) => CATALOGO.find((c) => c.slug === slug)).filter(
    (c): c is CursoCatalogo => !!c,
  );
  // "E mais N": só formação bíblica, fora os destaques (estudos pessoais nunca entram aqui).
  const outros = CATALOGO.filter(
    (c) => c.categoria === "Formação bíblica" && !DESTAQUES.includes(c.slug),
  );
  const exemplosOutros = outros
    .filter((c) => !c.disponivel)
    .slice(0, 5)
    .map((c) => c.titulo.replace(/^O /, ""));

  const heroi = slidesHeroi()[0];

  return (
    <>
      <CabecalhoApp nomeUsuario={null} />

      <main>
        {/* ---------- Abertura ---------- */}
        <section className="grao border-b border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="mx-auto grid max-w-[var(--tm-maxw)] items-center gap-5 px-[clamp(1rem,4vw,2rem)] py-[clamp(1.25rem,4vw,2.75rem)] md:grid-cols-[1.3fr_.7fr] md:gap-8 lg:grid-cols-[1.25fr_.75fr] lg:gap-12">
            <div className="flex flex-col items-start">
              <p className="m-0 mb-2 text-[.72rem] font-semibold uppercase tracking-[.18em] text-[var(--tm-accent)]">
                Formação bíblica
              </p>
              <h1 className="m-0 text-[clamp(1.8rem,4.4vw,2.6rem)] leading-[1.1]">
                Estudar a Bíblia até o coração arder.
              </h1>
              <p className="m-0 mt-3 max-w-lg text-[1rem] leading-relaxed text-[var(--tm-ink-muted)]">
                Cursos de Bíblia e vida cristã para entender de verdade: no seu ritmo, sem viés de
                denominação e com um tutor que acompanha.
              </p>
              <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-3">
                <LinkBotao href="/criar-conta">Criar conta grátis</LinkBotao>
                <Link href="/entrar" className="text-[.9rem] font-semibold text-[var(--tm-accent)] hover:underline">
                  Já tenho conta →
                </Link>
              </div>
              <p className="m-0 mt-3 text-[.8rem] text-[var(--tm-ink-muted)]">
                Grátis · sem cartão · leva um minuto
              </p>
            </div>

            {heroi && (
              <div className="order-first aspect-[21/9] overflow-hidden rounded-[var(--tm-radius)] border border-[var(--tm-border)] shadow-[var(--tm-shadow)] md:order-none md:aspect-[4/3] md:max-h-[300px] md:rounded-[var(--tm-radius-lg)]">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={heroi.src} alt={heroi.alt} className="h-full w-full object-cover" />
              </div>
            )}
          </div>
        </section>

        {/* ---------- Como funciona ---------- */}
        <section
          id="como-funciona"
          className="mx-auto max-w-[var(--tm-maxw)] scroll-mt-20 px-[clamp(1rem,4vw,2rem)] py-[clamp(2.5rem,7vw,4.5rem)]"
        >
          <h2 className="m-0 text-[clamp(1.4rem,3.5vw,1.8rem)]">Como funciona</h2>
          <p className="m-0 mt-1.5 text-[.95rem] text-[var(--tm-ink-muted)]">
            Do cadastro ao primeiro estudo em poucos minutos.
          </p>
          <ol className="m-0 mt-7 grid list-none gap-5 p-0 sm:grid-cols-3 sm:gap-8">
            {PASSOS.map((p, i) => (
              <li key={p.titulo} className="flex items-start gap-3.5">
                <span
                  style={{ fontFamily: "var(--tm-font-display)" }}
                  className="grid h-9 w-9 flex-none place-items-center rounded-full border border-[var(--tm-verse-border)] bg-[var(--tm-verse-bg)] font-semibold text-[var(--tm-accent)]"
                >
                  {i + 1}
                </span>
                <div>
                  <h3 style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 text-[1.02rem]">
                    {p.titulo}
                  </h3>
                  <p className="m-0 mt-0.5 text-[.9rem] leading-relaxed text-[var(--tm-ink-muted)]">{p.texto}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>

        {/* ---------- Cursos em destaque ---------- */}
        <section
          id="cursos"
          className="mx-auto max-w-[var(--tm-maxw)] scroll-mt-20 px-[clamp(1rem,4vw,2rem)] pb-[clamp(2.5rem,7vw,4.5rem)]"
        >
          <h2 className="m-0 text-[clamp(1.4rem,3.5vw,1.8rem)]">Cursos em destaque</h2>
          <p className="m-0 mt-1.5 text-[.95rem] text-[var(--tm-ink-muted)]">
            Um já está aberto. Os próximos chegam em breve.
          </p>

          <div className="mt-7 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {destaques.map((c) => (
              <CardDestaque key={c.slug} curso={c} aberto={publicado(c)} />
            ))}
          </div>

          {outros.length > 0 && (
            <p className="m-0 mt-5 rounded-[var(--tm-radius)] border border-dashed border-[var(--tm-border)] px-4 py-3.5 text-[.9rem] text-[var(--tm-ink-muted)]">
              <strong className="text-[var(--tm-ink)]">
                E mais {outros.length} curso{outros.length !== 1 ? "s" : ""} em preparação
              </strong>
              {exemplosOutros.length > 0 && <>: {exemplosOutros.join(", ")} e outros.</>}
            </p>
          )}
        </section>

        {/* ---------- Fechamento ---------- */}
        <section className="grao border-t border-[var(--tm-border)] bg-[var(--tm-surface-2)]">
          <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-col items-center gap-4 px-[clamp(1rem,4vw,2rem)] py-[clamp(2.5rem,7vw,4.5rem)] text-center">
            <p
              style={{ fontFamily: "var(--tm-font-display)" }}
              className="m-0 max-w-md text-[1rem] italic leading-relaxed text-[var(--tm-ink-muted)]"
            >
              “Não estava ardendo o nosso coração, quando ele nos falava pelo caminho e nos abria as
              Escrituras?” — Lucas 24.32
            </p>
            <h2 className="m-0 text-[clamp(1.5rem,4vw,2rem)]">Comece hoje. É de graça.</h2>
            <LinkBotao href="/criar-conta">Criar conta grátis</LinkBotao>
          </div>
        </section>
      </main>

      <Rodape logado={false} />
    </>
  );
}
