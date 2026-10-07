"use client";

import { useState } from "react";
import Link from "next/link";
import { contarModulo, type ModuloNo } from "../../_lib/arvore";

// Lista de módulos do curso (redesign 2026-09-27, protótipo aprovado em
// prototipos-front/04-curso.html): sem as faixas de capa de cada módulo (cortavam
// o texto desenhado na imagem e pesavam ~1-2 MB cada), mini barra de progresso,
// "Próximo" no tópico atual e módulos em preparação compactos.

type Estado = ModuloNo["aulas"][number]["topicos"][number]["estado"];
type Prova = ModuloNo["aulas"][number]["topicos"][number]["prova"];

// Chip da prova liberada: aprovado (verde), precisa refazer (laranja) ou ainda não feita.
const CHIP_PROVA: Record<NonNullable<Prova> | "nao_feita", { texto: string; classe: string }> = {
  feita: {
    texto: "✓ Prova feita",
    classe: "border-[color-mix(in_srgb,var(--tm-good)_55%,transparent)] text-[var(--tm-good)]",
  },
  refazer: {
    texto: "↺ Refazer prova",
    classe: "border-[color-mix(in_srgb,var(--tm-warn)_55%,transparent)] text-[var(--tm-warn)]",
  },
  nao_feita: { texto: "📝 Prova", classe: "border-[var(--tm-accent)] text-[var(--tm-accent)]" },
};

// Círculo de status: ✓ cheio (concluído), anel accent com halo (atual), anel neutro
// (disponível — o curso nunca trava tópico, é só apresentação).
function CirculoStatus({ estado }: { estado: Estado }) {
  if (estado === "concluido") {
    return (
      <span className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full bg-[var(--tm-good)] text-[.7rem] font-bold text-white">
        ✓
      </span>
    );
  }
  if (estado === "atual") {
    return (
      <span
        className="h-[22px] w-[22px] shrink-0 rounded-full border-2 border-[var(--tm-accent)] shadow-[0_0_0_3px_color-mix(in_srgb,var(--tm-accent)_20%,transparent)]"
        aria-hidden
      />
    );
  }
  return <span className="h-[22px] w-[22px] shrink-0 rounded-full border-2 border-[var(--tm-border)]" aria-hidden />;
}

const CHIP = "shrink-0 whitespace-nowrap rounded-[var(--tm-radius-pill)] border px-2.5 py-0.5 text-[.72rem] font-semibold";

function LinhaTopico({
  id,
  titulo,
  referencia,
  estado,
  avaliacaoId,
  prova,
}: {
  id: number;
  titulo: string;
  referencia: string | null;
  estado: Estado;
  avaliacaoId: number | null;
  prova: Prova;
}) {
  if (estado === "em_preparacao") {
    return (
      <div className="flex items-center gap-3 border-t border-[var(--tm-border)] px-4 py-3 opacity-55" title="Conteúdo em preparação">
        <span className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full border-2 border-[var(--tm-border)] text-[.7rem] text-[var(--tm-ink-muted)]" aria-hidden>
          …
        </span>
        <span className="min-w-0 flex-1 text-[var(--tm-ink-muted)]">
          {titulo} <span className="text-[.78rem]">· em preparação</span>
        </span>
      </div>
    );
  }

  // Prova travada até concluir o conteúdo (2026-09-19, ver PLANO_AVALIACAO_SEPARADA.md):
  // o backend já recusa (403) se tentarem entrar direto. O chip é só a UI.
  // IMPORTANTE: o chip da prova é um <Link> IRMÃO do <Link> do tópico, nunca aninhado
  // — <a> dentro de <a> é HTML inválido e quebra a área clicável.
  const chipProva =
    avaliacaoId != null &&
    (estado === "concluido" ? (
      <Link
        href={`/topico/${id}/prova`}
        className={`${CHIP} ${CHIP_PROVA[prova ?? "nao_feita"].classe} hover:bg-[var(--tm-surface-2)]`}
      >
        {CHIP_PROVA[prova ?? "nao_feita"].texto}
      </Link>
    ) : (
      <span
        className={`${CHIP} border-[var(--tm-border)] text-[var(--tm-ink-muted)]`}
        title="A prova libera depois que você concluir o tópico"
      >
        🔒 Prova
      </span>
    ));

  const atual = estado === "atual";

  return (
    <div className="flex items-center gap-3 border-t border-[var(--tm-border)] px-4 py-3 transition-colors hover:bg-[var(--tm-surface-2)]">
      <Link href={`/topico/${id}`} className="flex min-w-0 flex-1 items-center gap-3">
        <CirculoStatus estado={estado} />
        <span className={"min-w-0 flex-1 " + (atual ? "font-semibold" : "")}>
          {titulo}
          {/* No celular a referência vai pra baixo do título (o chip some) */}
          {referencia && (
            <span className="block text-[.75rem] font-normal text-[var(--tm-ink-muted)] sm:hidden">{referencia}</span>
          )}
        </span>
        {atual && (
          <span className="shrink-0 text-[.68rem] font-bold uppercase tracking-[.08em] text-[var(--tm-accent)]">
            Próximo
          </span>
        )}
        {referencia && (
          <span className={`${CHIP} hidden border-[var(--tm-border)] text-[var(--tm-ink-muted)] sm:inline`}>
            {referencia}
          </span>
        )}
      </Link>
      {chipProva}
    </div>
  );
}

function Modulo({ modulo, aberto, aoAlternar }: { modulo: ModuloNo; aberto: boolean; aoAlternar: () => void }) {
  const { concluidos, total } = contarModulo(modulo);
  const feito = total > 0 && concluidos === total;
  const emPreparacao = total === 0;
  const pct = total === 0 ? 0 : Math.round((concluidos / total) * 100);

  // Módulo sem nenhum tópico: linha compacta, tracejada, sem abrir
  if (emPreparacao) {
    return (
      <div className="flex items-center gap-3 rounded-[var(--tm-radius-lg)] border border-dashed border-[var(--tm-border)] px-4 py-2.5">
        <span
          aria-hidden
          className="flex h-[34px] w-[34px] shrink-0 items-center justify-center rounded-[10px] border border-dashed border-[var(--tm-border)] text-[.95rem] text-[var(--tm-ink-muted)]"
          style={{ fontFamily: "var(--tm-font-display)" }}
        >
          {modulo.module_index}
        </span>
        <span className="min-w-0 flex-1">
          <span className="block text-[.7rem] uppercase tracking-[.1em] text-[var(--tm-ink-muted)]">
            Módulo {modulo.module_index}
          </span>
          <span style={{ fontFamily: "var(--tm-font-display)" }} className="text-[.95rem] text-[var(--tm-ink-muted)]">
            {modulo.titulo}
          </span>
        </span>
        <span className="shrink-0 text-[.78rem] text-[var(--tm-ink-muted)]">em preparação</span>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
      <button
        type="button"
        onClick={aoAlternar}
        aria-expanded={aberto}
        className="flex w-full items-center gap-3 px-4 py-3.5 text-left"
      >
        <span
          aria-hidden
          className={
            "flex h-[36px] w-[36px] shrink-0 items-center justify-center rounded-[10px] text-[.95rem] font-semibold " +
            (feito ? "bg-[var(--tm-good)] text-white" : "bg-[var(--tm-surface-2)] text-[var(--tm-accent)]")
          }
          style={{ fontFamily: "var(--tm-font-display)" }}
        >
          {feito ? "✓" : modulo.module_index}
        </span>
        <span className="min-w-0 flex-1">
          <span className="block text-[.7rem] uppercase tracking-[.1em] text-[var(--tm-ink-muted)]">
            Módulo {modulo.module_index}
          </span>
          <span style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.02rem]">
            {modulo.titulo}
          </span>
        </span>
        <span className="shrink-0 text-right text-[.8rem] text-[var(--tm-ink-muted)]">
          {concluidos} de {total}
          <span className="ml-auto mt-1 hidden h-1 w-16 overflow-hidden rounded-full bg-[var(--tm-surface-2)] sm:block">
            <span className="block h-full bg-[var(--tm-good)]" style={{ width: `${pct}%` }} />
          </span>
        </span>
        <span
          aria-hidden
          className="shrink-0 text-[var(--tm-ink-muted)] transition-transform"
          style={{ transform: aberto ? "rotate(90deg)" : "none" }}
        >
          ▸
        </span>
      </button>

      {aberto && (
        <div className="border-t border-[var(--tm-border)]">
          {modulo.aulas.map((aula) => (
            <div key={aula.id}>
              <div className="bg-[color-mix(in_srgb,var(--tm-surface-2)_60%,transparent)] px-4 py-2 text-[.78rem] font-semibold text-[var(--tm-ink-muted)]">
                Aula {aula.lesson_index} · {aula.titulo}
              </div>
              {aula.topicos.length === 0 ? (
                <p className="m-0 border-t border-[var(--tm-border)] px-4 py-3 text-[.82rem] text-[var(--tm-ink-muted)]">
                  Tópicos em preparação.
                </p>
              ) : (
                aula.topicos.map((t) => (
                  <LinhaTopico
                    key={t.id}
                    id={t.id}
                    titulo={t.titulo}
                    referencia={t.referencia_biblica}
                    estado={t.estado}
                    avaliacaoId={t.avaliacaoId}
                    prova={t.prova}
                  />
                ))
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export function ArvoreCursoUI({
  modulos,
  moduloAbertoId,
}: {
  modulos: ModuloNo[];
  moduloAbertoId: number | null;
}) {
  const [abertos, setAbertos] = useState<Set<number>>(
    () => new Set(moduloAbertoId != null ? [moduloAbertoId] : []),
  );
  const comConteudo = modulos.filter((m) => contarModulo(m).total > 0);
  const todosAbertos = comConteudo.length > 0 && comConteudo.every((m) => abertos.has(m.id));

  function alternar(id: number) {
    setAbertos((atual) => {
      const novo = new Set(atual);
      if (novo.has(id)) novo.delete(id);
      else novo.add(id);
      return novo;
    });
  }

  return (
    <section className="mt-3">
      <div className="mb-3.5 flex items-baseline justify-between gap-4">
        <h2 className="m-0 text-[1.2rem]">Conteúdo do curso</h2>
        {comConteudo.length > 1 && (
          <button
            type="button"
            onClick={() => setAbertos(todosAbertos ? new Set() : new Set(comConteudo.map((m) => m.id)))}
            className="text-[.82rem] font-semibold text-[var(--tm-accent)] hover:underline"
          >
            {todosAbertos ? "Fechar todos" : "Abrir todos"}
          </button>
        )}
      </div>
      <div className="flex flex-col gap-2.5">
        {modulos.map((m) => (
          <Modulo key={m.id} modulo={m} aberto={abertos.has(m.id)} aoAlternar={() => alternar(m.id)} />
        ))}
      </div>
    </section>
  );
}
