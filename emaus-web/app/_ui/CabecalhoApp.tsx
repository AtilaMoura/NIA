import Link from "next/link";
import { AlternarTema } from "./AlternarTema";
import { MenuUsuario } from "./MenuUsuario";
import { MenuMobile } from "./MenuMobile";
import { NavPrincipal } from "./NavPrincipal";
import { Logo } from "./Logo";
import { LinkBotao } from "./Botao";
import type { Papel } from "../_lib/papel";
import { hrefMarca } from "../_lib/nav";

// Cabeçalho fixo — IGUAL em toda tela. A navegação vem do papel do usuário
// (_lib/nav.ts), não é mais montada por página. O logo sempre leva pro mesmo
// lugar: /inicio se logado, / se não.
export function CabecalhoApp({
  nomeUsuario,
  papel,
}: {
  nomeUsuario?: string | null;
  papel?: Papel | null;
}) {
  const logado = !!nomeUsuario;

  return (
    <header className="sticky top-0 z-30 border-b border-[var(--tm-border)] bg-[var(--tm-bg)]/90 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-[var(--tm-maxw)] items-center gap-5 px-[clamp(1rem,4vw,2rem)]">
        <Link href={hrefMarca(logado)} aria-label="Emaús — início" className="shrink-0">
          <Logo size={30} />
        </Link>

        <NavPrincipal papel={papel} logado={logado} />

        <div className="ml-auto flex items-center gap-2">
          {/* Visitante no celular: sem botão de tema, senão Entrar + Criar conta não cabem em 360px */}
          <span className={logado ? "contents" : "hidden sm:contents"}>
            <AlternarTema />
          </span>
          {logado ? (
            <span className="hidden sm:block">
              <MenuUsuario nome={nomeUsuario!} papel={papel ?? null} />
            </span>
          ) : (
            // Visitante: Entrar + Criar conta visíveis em qualquer largura (sem
            // menu hambúrguer — a página de visitante é curta, não precisa).
            <>
              <LinkBotao href="/entrar" variante="fantasma" tamanho="sm">
                Entrar
              </LinkBotao>
              <LinkBotao href="/criar-conta" tamanho="sm">
                Criar conta
              </LinkBotao>
            </>
          )}
          {logado && <MenuMobile nome={nomeUsuario} papel={papel ?? null} />}
        </div>
      </div>
    </header>
  );
}
