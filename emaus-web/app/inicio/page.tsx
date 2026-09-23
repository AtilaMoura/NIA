import type { Metadata } from "next";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { Prateleira } from "../_ui/Prateleira";
import { PosterCurso } from "../_ui/PosterCurso";
import { CartaoContinuar } from "../_ui/CartaoContinuar";
import { redirect } from "next/navigation";
import { CATALOGO, caminhoCapa, type CategoriaCurso } from "../_lib/catalogo";
import { capaExiste } from "../_lib/capas";
import { getUser, listCourses } from "../_lib/api";
import { montarArvore, type ArvoreCurso } from "../_lib/arvore";
import { getSessao, getToken } from "../_lib/sessao";
import { papelPodeRevisar } from "../_lib/papel";

export const metadata: Metadata = { title: "Meu estudo" };

// Home multi-curso estilo streaming (redesign 2026-09-21, ver PLANO_REDESIGN_EMAUS.md
// Fase 3) — antes era hardcoded pra 1 curso só (TEOLOGIA_COURSE_IDS[0]), mesmo já
// existindo 4 cursos disponíveis. "Continuar estudando" vira prateleira (não hero de
// tela cheia); as demais prateleiras são fixas por categoria do catálogo.
export default async function InicioPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/inicio");
  const token = await getToken();

  const [usuario] = await Promise.all([getUser(sessao.id, token).catch(() => null)]);

  const disponiveisParaAluno = CATALOGO.filter((c) => c.disponivel && c.courseId != null);

  const arvores = await Promise.all(
    disponiveisParaAluno.map((c) =>
      montarArvore(c.courseId!, sessao.id, token).catch((): ArvoreCurso | null => null),
    ),
  );

  type Item = {
    slug: string;
    percent: number;
    proximoTopico: { id: number; titulo: string } | null;
  };

  // Só entra na lista quem está publicado (revisor vê tudo, aluno só o que já
  // saiu — mesma regra que já existia na página de tópico/curso).
  const itens: Item[] = [];
  disponiveisParaAluno.forEach((c, i) => {
    const a = arvores[i];
    if (!a) return;
    const publicado = a.curso.status === "published" || papelPodeRevisar(sessao.role);
    if (!publicado) return;
    itens.push({ slug: c.slug, percent: a.resumo.percent, proximoTopico: a.proximoTopico });
  });
  const itemPorSlug = new Map(itens.map((it) => [it.slug, it]));

  const continuando = itens.filter((it) => it.percent > 0 && it.percent < 100 && it.proximoTopico);

  const primeiroNome = (usuario?.name ?? "").split(/\s+/)[0] || null;
  const categorias: CategoriaCurso[] = ["Formação bíblica", "Estudos pessoais"];

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        <h1 className="m-0 text-[1.4rem]" style={{ fontFamily: "var(--tm-font-display)" }}>
          {primeiroNome ? `Bom te ver de volta, ${primeiroNome}` : "Bom te ver de volta"}
        </h1>

        {continuando.length > 0 && (
          <Prateleira titulo="Continuar estudando">
            {continuando.map((it) => {
              const c = CATALOGO.find((x) => x.slug === it.slug)!;
              return (
                <CartaoContinuar
                  key={it.slug}
                  nomeCurso={c.titulo}
                  tituloTopico={it.proximoTopico!.titulo}
                  percent={it.percent}
                  tom={c.tom}
                  capaUrl={capaExiste(c.slug) ? caminhoCapa(c.slug) : null}
                  href={`/topico/${it.proximoTopico!.id}`}
                />
              );
            })}
          </Prateleira>
        )}

        {itens.length === 0 && (
          <p className="text-[.9rem] text-[var(--tm-ink-muted)]">
            Nenhum curso disponível ainda pra você — volte em breve.
          </p>
        )}

        {categorias.map((categoria) => {
          const cursosCategoria = CATALOGO.filter((c) => c.categoria === categoria);
          if (cursosCategoria.length === 0) return null;
          return (
            <Prateleira key={categoria} titulo={categoria}>
              {cursosCategoria.map((c) => {
                const item = itemPorSlug.get(c.slug);
                return (
                  <PosterCurso
                    key={c.slug}
                    titulo={c.titulo}
                    subtitulo={c.subtitulo}
                    tom={c.tom}
                    capaUrl={capaExiste(c.slug) ? caminhoCapa(c.slug) : null}
                    href={item && c.courseId != null ? `/curso/${c.courseId}` : undefined}
                    bloqueado={!item}
                    percentConcluido={item?.percent}
                  />
                );
              })}
            </Prateleira>
          );
        })}
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
