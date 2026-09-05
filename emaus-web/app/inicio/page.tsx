import type { Metadata } from "next";
import Link from "next/link";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { BarraProgresso } from "../_ui/BarraProgresso";
import { LinkBotao } from "../_ui/Botao";
import { LogoSimbolo } from "../_ui/Logo";
import { Rodape } from "../_ui/Rodape";
import { redirect } from "next/navigation";
import { TEOLOGIA_COURSE_IDS } from "../_lib/config";
import { getUser } from "../_lib/api";
import { montarArvore } from "../_lib/arvore";
import { getSessao } from "../_lib/sessao";
import { papelPodeRevisar } from "../_lib/papel";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export const metadata: Metadata = { title: "Meu estudo" };

export default async function InicioPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/inicio");

  const [arvore, usuario] = await Promise.all([
    montarArvore(CURSO_ID, sessao.id),
    getUser(sessao.id).catch(() => null),
  ]);
  const { curso, resumo, proximoTopico } = arvore;

  // Curso do aluno ainda não publicado: manda pra vitrine (nada pra estudar aqui).
  if (curso.status !== "published" && !papelPodeRevisar(sessao.role)) {
    redirect("/");
  }

  const primeiroNome = (usuario?.name ?? "").split(/\s+/)[0] || null;

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role}>
        <span className="text-[var(--tm-accent)]">Início</span>
        <Link href={`/curso/${CURSO_ID}`} className="hover:text-[var(--tm-accent)]">
          Curso
        </Link>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-10">
        <section className="grao relative overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-6 shadow-[var(--tm-shadow)] sm:p-9">
          <LogoSimbolo
            size={200}
            decorativo
            className="pointer-events-none absolute -bottom-8 -right-8 text-[var(--tm-accent)] opacity-[0.05]"
          />
          <div className="relative">
            {proximoTopico ? (
              <>
                <p className="m-0 text-[.76rem] font-semibold uppercase tracking-[.14em] text-[var(--tm-accent)]">
                  {primeiroNome ? `${primeiroNome}, continue de onde parou` : "Continue de onde parou"}
                </p>
                <h1 className="mb-1 mt-3 text-[clamp(1.5rem,3.5vw,2rem)] leading-tight">
                  {proximoTopico.titulo}
                </h1>
                <p className="m-0 mb-6 text-[.9rem] text-[var(--tm-ink-muted)]">{curso.title}</p>
                <LinkBotao href={`/topico/${proximoTopico.id}`}>Continuar o estudo</LinkBotao>
              </>
            ) : resumo.totalTopicos > 0 ? (
              <>
                <p className="m-0 text-[.76rem] font-semibold uppercase tracking-[.14em] text-[var(--tm-good)]">
                  Em dia
                </p>
                <h1 className="mb-1 mt-3 text-[1.5rem]">Você concluiu tudo que está disponível</h1>
                <p className="m-0 mb-6 text-[.9rem] text-[var(--tm-ink-muted)]">
                  Os próximos tópicos ainda estão em preparação.
                </p>
                <LinkBotao href={`/curso/${CURSO_ID}`} variante="fantasma">
                  Rever o curso
                </LinkBotao>
              </>
            ) : (
              <>
                <h1 className="mb-1 text-[1.5rem]">{curso.title}</h1>
                <p className="m-0 text-[.9rem] text-[var(--tm-ink-muted)]">
                  O conteúdo do curso está sendo preparado.
                </p>
              </>
            )}
          </div>
        </section>

        <section className="flex flex-col gap-3">
          <h2 className="m-0 text-[1.1rem]">Seu progresso</h2>
          <div className="max-w-md">
            <BarraProgresso valor={resumo.percent} rotulo={curso.title} />
            <p className="mt-1.5 text-[.8rem] text-[var(--tm-ink-muted)]">
              {resumo.concluidos} de {resumo.totalTopicos} tópicos concluídos
            </p>
          </div>
          <LinkBotao
            href={`/curso/${CURSO_ID}`}
            variante="fantasma"
            tamanho="sm"
            className="mt-1 self-start"
          >
            Ver todo o curso
          </LinkBotao>
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
