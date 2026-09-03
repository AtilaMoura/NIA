"use client";

import { Avatar } from "../_ui/Avatar";
import { BarraProgresso } from "../_ui/BarraProgresso";
import { Botao, LinkBotao } from "../_ui/Botao";
import { CabecalhoApp } from "../_ui/CabecalhoApp";
import { Card } from "../_ui/Card";
import { Chip } from "../_ui/Chip";
import { Rodape } from "../_ui/Rodape";
import { Selo } from "../_ui/Selo";
import { setTmTheme } from "../_lib/theme";

function Secao({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-3">
      <h2 className="text-[1rem] text-[var(--tm-ink-muted)]">{titulo}</h2>
      <div className="flex flex-wrap items-center gap-3">{children}</div>
    </div>
  );
}

export default function DevKitPage() {
  return (
    <>
      <CabecalhoApp nomeUsuario="Atila Moura">
        <span>Kit visual</span>
      </CabecalhoApp>

      <main className="mx-auto flex max-w-[var(--tm-maxw)] flex-col gap-8 px-[clamp(1rem,4vw,2rem)] py-8">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-[1.6rem]">Kit visual — Emaús</h1>
          <div className="flex gap-2">
            <Botao tamanho="sm" variante="fantasma" onClick={() => setTmTheme("light")}>
              Claro
            </Botao>
            <Botao tamanho="sm" variante="fantasma" onClick={() => setTmTheme("dark")}>
              Escuro
            </Botao>
          </div>
        </div>

        <Secao titulo="Botão">
          <Botao>Primário</Botao>
          <Botao variante="fantasma">Fantasma</Botao>
          <Botao variante="perigo">Perigo</Botao>
          <Botao tamanho="sm">Pequeno</Botao>
          <Botao disabled>Desabilitado</Botao>
          <LinkBotao href="/dev">Link como botão</LinkBotao>
        </Secao>

        <Secao titulo="Chip">
          <Chip>neutro</Chip>
          <Chip tom="info">Ef 4:11-12</Chip>
          <Chip tom="bom">aprovado</Chip>
          <Chip tom="aviso">rascunho</Chip>
        </Secao>

        <Secao titulo="Selo (estado de tópico)">
          <Selo estado="concluido" />
          <Selo estado="atual" />
          <Selo estado="disponivel" />
          <Selo estado="em_preparacao" />
        </Secao>

        <Secao titulo="Avatar">
          <Avatar nome="Atila Moura" />
          <Avatar nome="Atila Moura" tamanho="sm" />
          <Avatar nome="Professor" />
        </Secao>

        <Secao titulo="Barra de progresso">
          <div className="w-full max-w-sm">
            <BarraProgresso valor={40} rotulo="Módulo 1 — Chamado e Fundamento Bíblico" />
          </div>
        </Secao>

        <Secao titulo="Card">
          <Card className="max-w-sm p-5">
            <h3 className="mb-1 text-[1.05rem]">Vocação e Ofícios</h3>
            <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">
              Efésios 4:11-12 — a diferença entre dom e ofício, e como a igreja reconhece.
            </p>
          </Card>
          <Card interativo className="max-w-sm p-5">
            <h3 className="mb-1 text-[1.05rem]">Card interativo</h3>
            <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">Eleva no hover.</p>
          </Card>
        </Secao>
      </main>

      <Rodape />
    </>
  );
}
