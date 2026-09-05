import type { Metadata } from "next";
import Link from "next/link";
import { LogoSimbolo } from "../_ui/Logo";
import { CriarContaForm } from "./criar-conta-ui";

export const metadata: Metadata = { title: "Criar conta" };

export default function CriarContaPage() {
  return (
    <main className="mx-auto flex min-h-[100dvh] max-w-sm flex-col justify-center gap-8 px-[clamp(1rem,4vw,2rem)] py-10">
      <div className="flex flex-col items-center gap-3 text-center">
        <LogoSimbolo size={56} className="text-[var(--tm-accent)]" />
        <h1 className="m-0 text-[1.4rem]">Criar conta no Emaús</h1>
      </div>

      <CriarContaForm />

      <p className="m-0 text-center text-[.85rem] text-[var(--tm-ink-muted)]">
        Já tem conta?{" "}
        <Link href="/entrar" className="font-semibold text-[var(--tm-accent)] hover:underline">
          Entrar
        </Link>
      </p>
    </main>
  );
}
