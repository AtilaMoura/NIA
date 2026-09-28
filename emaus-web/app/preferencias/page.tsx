import type { Metadata } from "next";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Rodape } from "../_ui/Rodape";
import { getUser, type FontSize } from "../_lib/api";
import { getSessao, getToken } from "../_lib/sessao";
import { Preferencias } from "./preferencias-ui";

export const metadata: Metadata = { title: "Preferências" };

export default async function PreferenciasPage() {
  const sessao = await getSessao();
  if (!sessao) redirect("/entrar?next=/preferencias");
  const token = await getToken();

  const [usuario, jar] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    cookies(),
  ]);

  // A fonte da verdade é users/1; o cookie é só o fast-path do SSR. Se o banco
  // não respondeu, cai pro cookie / default.
  const salvo = usuario?.preferred_panel_mode;
  const cookieModo = jar.get("tm_theme")?.value;
  const modo = salvo ?? (cookieModo === "dark" || cookieModo === "auto" ? cookieModo : "light");
  const fsRaw = usuario?.preferred_font_size ?? jar.get("tm_fontsize")?.value ?? "md";
  const fonte: FontSize = fsRaw === "sm" || fsRaw === "lg" ? fsRaw : "md";

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className="mx-auto flex max-w-[640px] flex-col gap-4 px-[clamp(1rem,4vw,2rem)] pb-16 pt-[clamp(1.5rem,4vw,2.5rem)]">
        <h1 className="m-0 text-[1.7rem]">Preferências</h1>
        <Preferencias modoInicial={modo} fonteInicial={fonte} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
