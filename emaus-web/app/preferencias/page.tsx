import type { Metadata } from "next";
import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { getUser, type FontSize } from "../_lib/api";
import { getSessao } from "../_lib/sessao";
import { Preferencias } from "./preferencias-ui";

export const metadata: Metadata = { title: "Preferências" };

export default async function PreferenciasPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/preferencias");

  const [usuario, jar] = await Promise.all([
    getUser(sessao.id).catch(() => null),
    cookies(),
  ]);

  // A fonte da verdade é users/1; o cookie é só o fast-path do SSR. Se o banco
  // não respondeu, cai pro cookie / default.
  const modo =
    usuario?.preferred_panel_mode ??
    (jar.get("tm_theme")?.value === "dark" ? "dark" : "light");
  const fsRaw = usuario?.preferred_font_size ?? jar.get("tm_fontsize")?.value ?? "md";
  const fonte: FontSize = fsRaw === "sm" || fsRaw === "lg" ? fsRaw : "md";

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role}>
        <Link href="/inicio" className="hover:text-[var(--tm-accent)]">
          Início
        </Link>
        <span className="text-[var(--tm-accent)]">Preferências</span>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-xl flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-10">
        <h1 className="m-0 text-[1.5rem]">Preferências</h1>
        <Preferencias modoInicial={modo} fonteInicial={fonte} />
        <p className="m-0 text-[.8rem] text-[var(--tm-ink-muted)]">
          As preferências são aplicadas na hora e ficam salvas na sua conta.
        </p>
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
