import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { LinkBotao } from "../_ui/Botao";
import { Rodape } from "../_ui/Rodape";
import { CapaCurso } from "../_ui/CapaCurso";
import { LinhaDoTempoTopicos } from "../_ui/LinhaDoTempoTopicos";
import { getUser } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { tituloCurto } from "../_lib/catalogo";
import { formatarTempo, progressoDoAluno } from "../_lib/progresso";

export const metadata: Metadata = { title: "Seu progresso" };

// Progresso do aluno (redesign 2026-09-27, protótipo 07-progresso.html): resumo
// geral + um bloco por curso em que ele já estudou (antes era fixo no 1º curso
// do código) + lista compacta de tópicos com tutor e prova.
export default async function ProgressoPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/progresso");
  const token = await getToken();

  const [usuario, { cursos, provas, resumo }] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    progressoDoAluno(sessao.id, sessao.role, token),
  ]);

  const numeros = [
    { valor: String(resumo.concluidos), rotulo: "tópicos concluídos" },
    { valor: String(resumo.dominados), rotulo: "dominados pelo tutor" },
    { valor: String(resumo.provasFeitas), rotulo: "provas feitas" },
    { valor: formatarTempo(resumo.tempoMin), rotulo: "de estudo" },
  ];

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[900px] flex-col gap-7 px-[clamp(1rem,4vw,2rem)] pb-16 pt-[clamp(1.5rem,4vw,2.5rem)]">
        <h1 className="m-0 text-[clamp(1.5rem,4vw,1.9rem)]">Seu progresso</h1>

        {cursos.length === 0 ? (
          <div className="rounded-[var(--tm-radius-lg)] border border-dashed border-[var(--tm-border)] bg-[var(--tm-surface-2)] p-6 text-center">
            <h2 className="m-0 text-[1.2rem]">Você ainda não começou nenhum curso</h2>
            <p className="m-0 mb-4 mt-1.5 text-[var(--tm-ink-muted)]">
              Quando você estudar um tópico, o seu avanço aparece aqui.
            </p>
            <LinkBotao href="/inicio">Escolher um curso</LinkBotao>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              {numeros.map((n) => (
                <div
                  key={n.rotulo}
                  className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-4 py-3.5"
                >
                  <b style={{ fontFamily: "var(--tm-font-display)" }} className="block text-[1.55rem] leading-tight">
                    {n.valor}
                  </b>
                  <span className="text-[.82rem] text-[var(--tm-ink-muted)]">{n.rotulo}</span>
                </div>
              ))}
            </div>

            {cursos.map(({ catalogo, capaUrl, arvore }) => {
              const proximo = arvore.linhaDoTempo.find((t) => t.estado === "atual") ?? null;
              return (
                <section
                  key={catalogo.slug}
                  className="overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] shadow-[var(--tm-shadow)]"
                >
                  <div className="grid items-center gap-4 p-5 sm:grid-cols-[110px_1fr_auto]">
                    <div className="relative hidden aspect-[4/3] overflow-hidden rounded-[var(--tm-radius)] sm:block">
                      <div className="absolute inset-0 [&>div]:h-full">
                        <CapaCurso titulo={catalogo.titulo} tom={catalogo.tom} capaUrl={capaUrl} />
                      </div>
                    </div>
                    <div>
                      <h2 className="m-0 text-[1.15rem]">{tituloCurto(catalogo)}</h2>
                      <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">{catalogo.subtitulo}</p>
                      <div className="mt-2 flex items-center gap-3 text-[.82rem] text-[var(--tm-ink-muted)]">
                        <span className="h-1.5 max-w-[320px] flex-1 overflow-hidden rounded-full bg-[var(--tm-surface-2)]">
                          <span
                            className="block h-full bg-[var(--tm-good)]"
                            style={{ width: `${arvore.resumo.percent}%` }}
                          />
                        </span>
                        {arvore.resumo.concluidos} de {arvore.resumo.totalTopicos} tópicos · {arvore.resumo.percent}%
                      </div>
                    </div>
                    {proximo && (
                      <LinkBotao href={`/topico/${proximo.id}`} className="w-full sm:w-auto">
                        Continuar →
                      </LinkBotao>
                    )}
                  </div>
                  <LinhaDoTempoTopicos linhaDoTempo={arvore.linhaDoTempo} provas={provas} />
                </section>
              );
            })}
          </>
        )}
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
