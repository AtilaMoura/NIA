import Link from "next/link";
import type { ReactNode } from "react";

// Moldura das telas de acesso (/entrar e /criar-conta) — redesign 2026-09-26,
// protótipo aprovado em prototipos-front/02-entrar-criar-conta.html.
// Fundo = ilustração da lamparina na tela inteira; formulário num cartão de vidro.
// Estilos em globals.css (.acesso-*). Sobre a imagem o logo é sempre o creme.
export function TelaAcesso({
  titulo,
  subtitulo,
  children,
}: {
  titulo: string;
  subtitulo: string;
  children: ReactNode;
}) {
  return (
    <>
      <div className="acesso-fundo" aria-hidden />

      <div className="acesso-tela">
        <header className="flex items-center justify-between gap-4 px-[clamp(1rem,4vw,2.5rem)] py-4">
          <Link href="/" aria-label="Emaús — início" className="inline-flex items-center gap-2">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/marca/final/logo1-simbolo-escuro.png" alt="" width={35} height={30} className="h-[30px] w-auto" />
            <span style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.15rem] font-semibold">
              Emaús
            </span>
          </Link>
          <Link href="/" className="text-[.85rem] font-semibold opacity-85 hover:underline hover:opacity-100">
            ← Voltar ao início
          </Link>
        </header>

        <main className="acesso-conteudo">
          {/* Versículo + o que a pessoa ganha (desktop: à esquerda do cartão) */}
          <div className="acesso-apresentacao flex max-w-[30rem] flex-col gap-4">
            <p className="acesso-versiculo m-0">
              “Não estava ardendo o nosso coração, quando ele nos falava pelo caminho e nos abria as
              Escrituras?”
              <small className="mt-1.5 block text-[.8rem] not-italic opacity-75">Lucas 24.32</small>
            </p>
            <ul className="acesso-ganhos m-0 grid list-none gap-2 p-0 text-[.92rem]">
              <li className="flex items-start gap-2.5">Cursos de Bíblia e vida cristã, no seu ritmo</li>
              <li className="flex items-start gap-2.5">Seu progresso fica salvo em qualquer aparelho</li>
              <li className="flex items-start gap-2.5">Um tutor que corrige e aponta o que revisar</li>
            </ul>
          </div>

          <div className="acesso-cartao">
            <h1 className="m-0 text-[clamp(1.5rem,4vw,1.85rem)]">{titulo}</h1>
            <p className="vidro-suave m-0 mt-1.5 text-[.95rem]">{subtitulo}</p>
            {children}
          </div>
        </main>
      </div>
    </>
  );
}
