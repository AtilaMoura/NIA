import type { Metadata } from "next";
import Link from "next/link";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { BarraProgresso } from "../_ui/BarraProgresso";
import { LinkBotao } from "../_ui/Botao";
import { Rodape } from "../_ui/Rodape";
import { LinhaDoTempoTopicos } from "../_ui/LinhaDoTempoTopicos";
import { redirect } from "next/navigation";
import { TEOLOGIA_COURSE_IDS } from "../_lib/config";
import { getUser } from "../_lib/api";
import { montarArvore } from "../_lib/arvore";
import { getSessao, getToken } from "../_lib/sessao";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export const metadata: Metadata = { title: "Seu progresso" };

export default async function ProgressoPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/progresso");
  const token = await getToken();

  const [arvore, usuario] = await Promise.all([
    montarArvore(CURSO_ID, sessao.id, token),
    getUser(sessao.id, token).catch(() => null),
  ]);
  const { curso, resumo, proximoTopico, linhaDoTempo } = arvore;

  const horas = Math.floor(resumo.tempoTotalMin / 60);
  const min = resumo.tempoTotalMin % 60;
  const tempoLabel =
    resumo.tempoTotalMin > 0 ? (horas > 0 ? `${horas}h ${min}min` : `${min}min`) : null;

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

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

        <LinhaDoTempoTopicos linhaDoTempo={linhaDoTempo} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
