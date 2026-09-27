import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { CartaoContinuar, CartaoCurso } from "../_ui/CartoesAluno";
import { getUser } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { papelVeEstudosPessoais } from "../_lib/papel";
import { meusCursos, emAndamento } from "../_lib/meus-cursos";

// Título dinâmico: pra quem não é Master, nem o nome da página aparece na aba
export async function generateMetadata(): Promise<Metadata> {
  const sessao = await getSessao();
  return { title: papelVeEstudosPessoais(sessao?.role) ? "Estudos pessoais" : "Página não encontrada" };
}

// Estudos pessoais do Master (2026-09-27) — saíram da vitrine e da /inicio.
// Versão funcional com os mesmos cartões da /inicio; o desenho próprio desta
// página ainda vai passar pelo fluxo de protótipo (REVISAO_FRONT_PAGINAS.md).
export default async function EstudosPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/estudos");
  // Pra quem não é Master, a página não existe
  if (!papelVeEstudosPessoais(sessao.role)) notFound();
  const token = await getToken();

  const [usuario, cursos] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    meusCursos("Estudos pessoais", sessao, token),
  ]);
  const abertos = cursos.filter((c) => c.aberto);
  const continuando = emAndamento(cursos);

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Master"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-[clamp(1.75rem,5vw,2.5rem)] px-[clamp(1rem,4vw,2rem)] pb-16 pt-[clamp(1.5rem,4vw,2.5rem)]">
        <div>
          <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">Estudos pessoais</h1>
          <p className="m-0 mt-1 text-[.95rem] text-[var(--tm-ink-muted)]">
            Só você vê esta página. Alunos não têm acesso a estes cursos.
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

        <section>
          <h2 className="m-0 mb-3.5 text-[1.15rem]">Seus estudos</h2>
          <div className="grid gap-4 min-[560px]:grid-cols-2 lg:grid-cols-3">
            {abertos.map((c) => (
              <CartaoCurso key={c.catalogo.slug} curso={c} />
            ))}
          </div>
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
