import Link from "next/link";
import { LinkBotao } from "./Botao";

// Tela de aviso do tópico/prova (redesign 2026-09-27, protótipo 06-prova.html #bloqueio):
// "a prova abre quando concluir o tópico", "tópico em preparação", "curso em preparação".
// Mesma barra de cima do render dos slides (voltar · onde · título), pra quem sai
// de um slide e cai aqui não sentir que mudou de site.
export function TelaAviso({
  voltarHref,
  voltarRotulo,
  onde,
  tituloBarra,
  icone,
  titulo,
  texto,
  passos,
  acao,
}: {
  voltarHref: string;
  voltarRotulo: string;
  onde?: string;
  tituloBarra?: string;
  icone: string;
  titulo: string;
  texto: string;
  passos?: string[];
  acao: { href: string; rotulo: string };
}) {
  return (
    <div className="flex min-h-[100dvh] flex-col">
      <header className="flex min-h-14 items-center gap-2.5 border-b border-[var(--tm-border)] px-[clamp(.75rem,3vw,1.5rem)] py-2">
        <Link
          href={voltarHref}
          aria-label={voltarRotulo}
          title={voltarRotulo}
          className="grid h-[38px] w-[38px] shrink-0 place-items-center rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] hover:border-[var(--tm-accent)] hover:text-[var(--tm-accent)]"
        >
          ‹
        </Link>
        <div className="min-w-0 flex-1 leading-tight">
          {onde && <p className="m-0 truncate text-[.72rem] text-[var(--tm-ink-muted)]">{onde}</p>}
          {tituloBarra && (
            <p style={{ fontFamily: "var(--tm-font-display)" }} className="m-0 truncate text-[1rem] font-semibold">
              {tituloBarra}
            </p>
          )}
        </div>
      </header>

      <main className="mx-auto w-full max-w-[460px] px-5 pb-12 pt-[clamp(2rem,10vh,5rem)] text-center">
        <div
          aria-hidden
          className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-full bg-[var(--tm-surface-2)] text-[1.6rem]"
        >
          {icone}
        </div>
        <h1 className="m-0 text-[1.55rem] leading-tight">{titulo}</h1>
        <p className="m-0 mt-2.5 text-[var(--tm-ink-muted)]">{texto}</p>
        {passos && passos.length > 0 && (
          <ol className="my-5 list-decimal rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] py-4 pl-9 pr-4 text-left text-[.92rem] [&>li+li]:mt-1.5">
            {passos.map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ol>
        )}
        <LinkBotao href={acao.href} className={"w-full " + (passos?.length ? "" : "mt-6")}>
          {acao.rotulo}
        </LinkBotao>
      </main>
    </div>
  );
}
