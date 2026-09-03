import Link from "next/link";
import { Logo } from "./_ui/Logo";
import { LinkBotao } from "./_ui/Botao";

export default function NaoEncontrado() {
  return (
    <main className="mx-auto flex min-h-[80vh] max-w-md flex-col items-start justify-center gap-5 px-[clamp(1rem,4vw,2rem)]">
      <Logo size={24} />
      <h1 className="m-0 text-[1.6rem]">Não encontramos essa página</h1>
      <p className="m-0 text-[.92rem] leading-relaxed text-[var(--tm-ink-muted)]">
        O endereço pode estar errado, ou esse conteúdo ainda está em preparação.
      </p>
      <div className="flex flex-wrap gap-3">
        <LinkBotao href="/">Ir para o início</LinkBotao>
        <Link
          href="/inicio"
          className="inline-flex items-center text-[.85rem] font-semibold text-[var(--tm-accent)] hover:underline"
        >
          Continuar estudando
        </Link>
      </div>
    </main>
  );
}
