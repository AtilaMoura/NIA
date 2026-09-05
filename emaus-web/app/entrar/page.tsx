import type { Metadata } from "next";
import Link from "next/link";
import { LogoSimbolo } from "../_ui/Logo";
import { EntrarForm } from "./entrar-ui";

export const metadata: Metadata = { title: "Entrar" };

export default function EntrarPage() {
  return (
    <main className="mx-auto flex min-h-[100dvh] max-w-sm flex-col justify-center gap-8 px-[clamp(1rem,4vw,2rem)] py-10">
      <div className="flex flex-col items-center gap-3 text-center">
        <LogoSimbolo size={56} className="text-[var(--tm-accent)]" />
        <h1 className="m-0 text-[1.4rem]">Entrar no Emaús</h1>
      </div>

      <EntrarForm />

      <p className="m-0 text-center text-[.85rem] text-[var(--tm-ink-muted)]">
        Ainda não tem conta?{" "}
        <Link href="/criar-conta" className="font-semibold text-[var(--tm-accent)] hover:underline">
          Criar conta
        </Link>
      </p>
    </main>
  );
}
