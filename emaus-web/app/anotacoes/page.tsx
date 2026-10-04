import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { getUser, minhasAnotacoes } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { cursoPessoal } from "../_lib/catalogo";
import { papelVeEstudosPessoais } from "../_lib/papel";
import { ListaAnotacoes } from "./anotacoes-ui";

export const metadata: Metadata = { title: "Minhas anotações" };

// Minhas anotações (2026-10-04, protótipo 12-anotacoes.html): tudo o que o
// usuário anotou nos slides, por curso → tópico → slide. Antes as anotações só
// apareciam dentro de cada tópico.
export default async function AnotacoesPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/anotacoes");
  const token = await getToken();

  const [usuario, todas] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    minhasAnotacoes(token).catch(() => []),
  ]);
  // Estudos pessoais só aparecem pro Master (mesma regra das outras páginas)
  const anotacoes = papelVeEstudosPessoais(sessao.role) ? todas : todas.filter((a) => !cursoPessoal(a.course_id));

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto w-full max-w-[860px] px-[clamp(1rem,4vw,2rem)] pb-12 pt-[clamp(1.25rem,4vw,2.25rem)]">
        <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">Minhas anotações</h1>
        <p className="m-0 mt-1 text-[var(--tm-ink-muted)]">
          Tudo o que você anotou nos slides, organizado por curso e tópico.
        </p>
        <ListaAnotacoes anotacoes={anotacoes} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
