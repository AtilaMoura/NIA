import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Avatar } from "../_ui/Avatar";
import { Chip } from "../_ui/Chip";
import { LinkBotao } from "../_ui/Botao";
import { Rodape } from "../_ui/Rodape";
import { getUser } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { INFO_PAPEL } from "../_lib/papel";
import { progressoDoAluno } from "../_lib/progresso";
import { EditarNome, SairBotao, TrocarSenha } from "./perfil-ui";

export const metadata: Metadata = { title: "Seu perfil" };

const fmtMesAno = new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric" });

// Perfil (redesign 2026-09-27, protótipo 08-perfil.html): conta, resumo do estudo
// (antes era a barra fixa de 1 curso, com título antigo), trocar senha,
// preferências e sair.
export default async function PerfilPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/perfil");
  const token = await getToken();

  const [usuario, { cursos, resumo }] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    progressoDoAluno(sessao.id, token),
  ]);
  const nome = usuario?.name ?? "Aluno";
  const criadoEm = typeof usuario?.created_at === "string" ? new Date(usuario.created_at) : null;

  const cartao = "rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-5";
  const linhaAcao = "flex flex-col gap-3 min-[481px]:flex-row min-[481px]:items-center min-[481px]:justify-between";

  return (
    <>
      <CabecalhoApp nomeUsuario={nome} papel={sessao.role} />

      <main className="mx-auto flex max-w-[640px] flex-col gap-4 px-[clamp(1rem,4vw,2rem)] pb-16 pt-[clamp(1.5rem,4vw,2.5rem)]">
        {/* Conta */}
        <section className={`${cartao} flex flex-col items-center gap-4 text-center min-[481px]:flex-row min-[481px]:text-left`}>
          <Avatar nome={nome} tamanho="lg" />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center justify-center gap-2 min-[481px]:justify-start">
              <EditarNome nomeInicial={usuario?.name ?? ""} />
              <Chip tom={INFO_PAPEL[sessao.role].tom}>{INFO_PAPEL[sessao.role].rotulo}</Chip>
            </div>
            {usuario?.email && <p className="m-0 mt-1 text-[.9rem] text-[var(--tm-ink-muted)]">{usuario.email}</p>}
            {criadoEm && !Number.isNaN(criadoEm.getTime()) && (
              <p className="m-0 text-[.82rem] text-[var(--tm-ink-muted)]">No Emaús desde {fmtMesAno.format(criadoEm)}</p>
            )}
          </div>
        </section>

        {/* Estudo */}
        <section className={cartao}>
          <h2 className="m-0 mb-3 text-[1.05rem]">Seu estudo</h2>
          <div className="grid grid-cols-3 gap-2.5">
            {[
              { valor: cursos.length, rotulo: cursos.length === 1 ? "curso" : "cursos" },
              { valor: resumo.concluidos, rotulo: "tópicos concluídos" },
              { valor: resumo.provasFeitas, rotulo: resumo.provasFeitas === 1 ? "prova feita" : "provas feitas" },
            ].map((n) => (
              <div key={n.rotulo} className="rounded-[var(--tm-radius)] bg-[var(--tm-surface-2)] px-3.5 py-3">
                <b style={{ fontFamily: "var(--tm-font-display)" }} className="block text-[1.35rem] leading-tight">
                  {n.valor}
                </b>
                <span className="text-[.78rem] text-[var(--tm-ink-muted)]">{n.rotulo}</span>
              </div>
            ))}
          </div>
          <Link href="/progresso" className="mt-3.5 inline-block text-[.88rem] font-semibold text-[var(--tm-accent)] hover:underline">
            Ver meu progresso →
          </Link>
        </section>

        {/* Senha */}
        <section className={cartao}>
          <TrocarSenha />
        </section>

        {/* Preferências */}
        <section className={`${cartao} ${linhaAcao}`}>
          <div>
            <h2 className="m-0 text-[1.05rem]">Preferências</h2>
            <p className="m-0 text-[.88rem] text-[var(--tm-ink-muted)]">Tema claro ou escuro e tamanho do texto.</p>
          </div>
          <LinkBotao href="/preferencias" variante="fantasma">
            Ajustar
          </LinkBotao>
        </section>

        {/* Sair */}
        <section className={`${cartao} ${linhaAcao}`}>
          <div>
            <h2 className="m-0 text-[1.05rem]">Sair da conta</h2>
            <p className="m-0 text-[.88rem] text-[var(--tm-ink-muted)]">Neste aparelho.</p>
          </div>
          <SairBotao />
        </section>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
