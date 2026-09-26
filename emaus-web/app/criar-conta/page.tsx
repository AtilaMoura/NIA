import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { TelaAcesso } from "../_ui/TelaAcesso";
import { getSessao } from "../_lib/sessao";
import { destinoSeguro } from "../_lib/destino";
import { CriarContaForm } from "./criar-conta-ui";

export const metadata: Metadata = { title: "Criar conta" };

export default async function CriarContaPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const { next } = await searchParams;
  // Já logado não precisa desta tela
  if (await getSessao()) redirect(destinoSeguro(next));

  return (
    <TelaAcesso titulo="Criar sua conta" subtitulo="Grátis, sem cartão. Leva um minuto.">
      <CriarContaForm />
    </TelaAcesso>
  );
}
