import type { Metadata } from "next";
import Link from "next/link";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { BarraProgresso } from "../_ui/BarraProgresso";
import { Avatar } from "../_ui/Avatar";
import { Chip } from "../_ui/Chip";
import { Rodape } from "../_ui/Rodape";
import { redirect } from "next/navigation";
import { TEOLOGIA_COURSE_IDS } from "../_lib/config";
import { getUser } from "../_lib/api";
import { montarArvore } from "../_lib/arvore";
import { getSessao, getToken } from "../_lib/sessao";
import { INFO_PAPEL } from "../_lib/papel";
import { EditarNome } from "./perfil-ui";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export const metadata: Metadata = { title: "Seu perfil" };

export default async function PerfilPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/perfil");
  const token = await getToken();

  const [arvore, usuario] = await Promise.all([
    montarArvore(CURSO_ID, sessao.id, token),
    getUser(sessao.id, token).catch(() => null),
  ]);
  const { curso, resumo, proximoTopico } = arvore;
  const nome = usuario?.name ?? "Aluno";

  return (
    <>
      <CabecalhoApp nomeUsuario={nome} papel={sessao.role} />

      <main className="mx-auto flex max-w-2xl flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-10">
        <section className="flex items-center gap-4">
          <Avatar nome={nome} tamanho="lg" />
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <EditarNome nomeInicial={usuario?.name ?? ""} />
              <Chip tom={INFO_PAPEL[sessao.role].tom}>{INFO_PAPEL[sessao.role].rotulo}</Chip>
            </div>
            {usuario?.email && (
              <p className="m-0 text-[.86rem] text-[var(--tm-ink-muted)]">{usuario.email}</p>
            )}
          </div>
        </section>

        <section className="flex flex-col gap-3">
          <h2 className="m-0 text-[1.05rem]">Estudo</h2>
          <div className="max-w-md">
            <BarraProgresso valor={resumo.percent} rotulo={curso.title} />
            <p className="mt-1.5 text-[.8rem] text-[var(--tm-ink-muted)]">
              {resumo.concluidos} de {resumo.totalTopicos} tópicos concluídos
            </p>
          </div>
          {proximoTopico && (
            <p className="m-0 text-[.85rem]">
              Em andamento:{" "}
              <Link
                href={`/topico/${proximoTopico.id}`}
                className="font-semibold text-[var(--tm-accent)] hover:underline"
              >
                {proximoTopico.titulo}
              </Link>
            </p>
          )}
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
