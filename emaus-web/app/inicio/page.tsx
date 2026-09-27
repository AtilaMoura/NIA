import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { CartaoContinuar, CartaoCurso, MiniaturaEmBreve } from "../_ui/CartoesAluno";
import { FileiraRolavel } from "../_ui/FileiraRolavel";
import { getUser } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { meusCursos, emAndamento } from "../_lib/meus-cursos";
import { primeiroNome } from "../_lib/nome";
import { tituloCurto } from "../_lib/catalogo";

export const metadata: Metadata = { title: "Meu estudo" };

// Home de quem está logado (redesign 2026-09-27, protótipo aprovado em
// prototipos-front/03-inicio.html): "Continuar estudando" em destaque, grade só
// com os cursos abertos e os "em breve" numa fileira compacta à parte.
// Só Formação bíblica — estudos pessoais do Master ficam em /estudos.
export default async function InicioPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/inicio");
  const token = await getToken();

  const [usuario, cursos] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    meusCursos("Formação bíblica", sessao, token),
  ]);

  const abertos = cursos.filter((c) => c.aberto);
  const emBreve = cursos.filter((c) => !c.aberto);
  const continuando = emAndamento(cursos);
  const nome = primeiroNome(usuario?.name);
  const novo = continuando.length === 0 && abertos.every((c) => c.percent === 0);
  const primeiroAberto = abertos.find((c) => !c.soRevisores) ?? abertos[0];

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-[clamp(1.75rem,5vw,2.5rem)] px-[clamp(1rem,4vw,2rem)] pb-16 pt-[clamp(1.5rem,4vw,2.5rem)]">
        <div>
          <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">
            {novo ? "Que bom ter você aqui" : "Bom te ver de volta"}
            {nome ? `, ${nome}` : ""}
          </h1>
          <p className="m-0 mt-1 text-[.95rem] text-[var(--tm-ink-muted)]">
            {novo ? "Escolha um curso pra começar." : "Continue de onde parou."}
          </p>
        </div>

        {continuando.length > 0 && (
          <section className="flex flex-col gap-3.5">
            <h2 className="m-0 text-[1.15rem]">Continuar estudando</h2>
            {continuando.map((c) => (
              <CartaoContinuar key={c.catalogo.slug} curso={c} />
            ))}
          </section>
        )}

        {/* Aluno sem nenhum progresso: aponta o primeiro curso aberto */}
        {novo && primeiroAberto?.catalogo.courseId != null && (
          <div className="flex flex-wrap items-center justify-between gap-4 rounded-[var(--tm-radius-lg)] border border-dashed border-[var(--tm-border)] bg-[var(--tm-surface-2)] px-6 py-5">
            <p className="m-0 text-[.95rem]">
              <strong>Por onde começar?</strong>{" "}
              <span className="text-[var(--tm-ink-muted)]">
                O curso {tituloCurto(primeiroAberto.catalogo)} já está aberto.
              </span>
            </p>
            <Link
              href={`/curso/${primeiroAberto.catalogo.courseId}`}
              className="inline-flex items-center rounded-[var(--tm-radius-pill)] bg-[var(--tm-accent)] px-5 py-2.5 text-[.92rem] font-semibold text-[var(--tm-bg)] hover:bg-[var(--tm-accent-2)]"
            >
              Começar o curso →
            </Link>
          </div>
        )}

        <section>
          <div className="mb-3.5 flex items-baseline justify-between gap-4">
            <h2 className="m-0 text-[1.15rem]">Seus cursos</h2>
            <small className="text-[.82rem] text-[var(--tm-ink-muted)]">
              {abertos.length} aberto{abertos.length !== 1 ? "s" : ""}
            </small>
          </div>
          {abertos.length > 0 ? (
            <div className="grid gap-4 min-[560px]:grid-cols-2 lg:grid-cols-3">
              {abertos.map((c) => (
                <CartaoCurso key={c.catalogo.slug} curso={c} />
              ))}
            </div>
          ) : (
            <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
              Nenhum curso aberto ainda — volte em breve.
            </p>
          )}
        </section>

        {emBreve.length > 0 && (
          <FileiraRolavel titulo="Em breve">
            {emBreve.map((c) => (
              <MiniaturaEmBreve key={c.catalogo.slug} curso={c} />
            ))}
          </FileiraRolavel>
        )}
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
