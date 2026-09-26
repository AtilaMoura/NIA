import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { TelaAcesso } from "../_ui/TelaAcesso";
import { getSessao } from "../_lib/sessao";
import { destinoSeguro } from "../_lib/destino";
import { EntrarForm } from "./entrar-ui";

export const metadata: Metadata = { title: "Entrar" };

export default async function EntrarPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const { next } = await searchParams;
  // Já logado não precisa desta tela
  if (await getSessao()) redirect(destinoSeguro(next));

  return (
    <TelaAcesso titulo="Bem-vindo de volta" subtitulo="Entre pra continuar de onde parou.">
      <EntrarForm />
    </TelaAcesso>
  );
}
