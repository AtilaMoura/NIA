import type { Metadata } from "next";
import Link from "next/link";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { BarraProgresso } from "../_ui/BarraProgresso";
import { LinkBotao } from "../_ui/Botao";
import { Chip } from "../_ui/Chip";
import { Selo } from "../_ui/Selo";
import { Rodape } from "../_ui/Rodape";
import { ALUNO_USER_ID, TEOLOGIA_COURSE_IDS } from "../_lib/config";
import { getUser } from "../_lib/api";
import { montarArvore, type TopicoNo } from "../_lib/arvore";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export const metadata: Metadata = { title: "Seu progresso" };

const fmtData = new Intl.DateTimeFormat("pt-BR", { day: "numeric", month: "short" });

function quando(t: TopicoNo): string | null {
  if (t.concluido_em) return `Concluído em ${fmtData.format(new Date(t.concluido_em))}`;
  if (t.iniciado_em && (t.estado === "atual" || t.estado === "disponivel")) {
    return `Em andamento desde ${fmtData.format(new Date(t.iniciado_em))}`;
  }
  return null;
}

export default async function ProgressoPage() {
  const [arvore, usuario] = await Promise.all([
    montarArvore(CURSO_ID),
    getUser(ALUNO_USER_ID).catch(() => null),
  ]);
  const { curso, resumo, proximoTopico, linhaDoTempo } = arvore;

  // Agrupa a linha do tempo por aula, preservando a ordem do curso.
  const porAula: { aula: string; modulo: string; topicos: TopicoNo[] }[] = [];
  for (const t of linhaDoTempo) {
    const ultima = porAula[porAula.length - 1];
    if (ultima && ultima.aula === t.aulaTitulo) ultima.topicos.push(t);
    else porAula.push({ aula: t.aulaTitulo ?? "Aula", modulo: t.moduloTitulo ?? "", topicos: [t] });
  }

  const horas = Math.floor(resumo.tempoTotalMin / 60);
  const min = resumo.tempoTotalMin % 60;
  const tempoLabel =
    resumo.tempoTotalMin > 0 ? (horas > 0 ? `${horas}h ${min}min` : `${min}min`) : null;

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"}>
        <Link href="/inicio" className="hover:text-[var(--tm-accent)]">
          Início
        </Link>
        <Link href={`/curso/${CURSO_ID}`} className="hover:text-[var(--tm-accent)]">
          Curso
        </Link>
        <span className="text-[var(--tm-accent)]">Progresso</span>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        <header className="flex flex-col gap-3">
          <h1 className="m-0 text-[1.6rem]">Seu progresso</h1>
          <div className="max-w-md">
            <BarraProgresso valor={resumo.percent} rotulo={curso.title} />
            <p className="mt-1.5 text-[.8rem] text-[var(--tm-ink-muted)]">
              {resumo.concluidos} de {resumo.totalTopicos} tópicos concluídos
              {tempoLabel && <> · {tempoLabel} de estudo</>}
            </p>
          </div>
        </header>

        {resumo.concluidos === 0 && !proximoTopico ? (
          <p className="text-[.9rem] text-[var(--tm-ink-muted)]">
            O conteúdo do curso ainda está sendo preparado.
          </p>
        ) : resumo.concluidos === 0 ? (
          <div className="flex flex-col items-start gap-3 rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-6">
            <p className="m-0 text-[.92rem]">
              Você ainda não concluiu nenhum tópico. Comece pelo primeiro.
            </p>
            {proximoTopico && (
              <LinkBotao href={`/topico/${proximoTopico.id}`}>
                Começar: {proximoTopico.titulo}
              </LinkBotao>
            )}
          </div>
        ) : null}

        <section className="flex flex-col gap-6">
          {porAula.map((grupo, gi) => (
            <div key={gi} className="flex flex-col gap-2">
              <h2 className="m-0 text-[.78rem] font-semibold uppercase tracking-[.1em] text-[var(--tm-ink-muted)]">
                {grupo.aula}
              </h2>
              <ol className="m-0 flex list-none flex-col gap-2 p-0">
                {grupo.topicos.map((t) => {
                  const data = quando(t);
                  const disponivel = t.estado !== "em_preparacao";
                  return (
                    <li
                      key={t.id}
                      className="flex flex-col gap-1.5 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3"
                    >
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                        <Selo estado={t.estado} />
                        <span
                          className={
                            t.estado === "em_preparacao" ? "text-[var(--tm-ink-muted)]" : ""
                          }
                        >
                          {t.titulo}
                        </span>
                        {t.referencia_biblica && <Chip tom="info">{t.referencia_biblica}</Chip>}
                        {t.tutor_veredito && (
                          <Chip tom={t.tutor_veredito === "dominado" ? "bom" : "aviso"}>
                            {t.tutor_veredito === "dominado" ? "Tutor: dominado" : "Tutor: reforço"}
                          </Chip>
                        )}
                      </div>
                      {data && (
                        <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">{data}</p>
                      )}
                      {disponivel && (
                        <Link
                          href={`/topico/${t.id}`}
                          className="text-[.8rem] font-semibold text-[var(--tm-accent)] hover:underline"
                        >
                          {t.estado === "concluido" ? "Rever" : "Abrir"} tópico
                        </Link>
                      )}
                    </li>
                  );
                })}
              </ol>
            </div>
          ))}
        </section>
      </main>

      <Rodape />
    </>
  );
}
