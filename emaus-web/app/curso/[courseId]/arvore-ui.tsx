"use client";

import { useState } from "react";
import Link from "next/link";
import { Chip } from "../../_ui/Chip";
import { contarModulo, type ModuloNo } from "../../_lib/arvore";

// Círculo de status do tópico (redesign 2026-09-21, ver PLANO_REDESIGN_EMAUS.md Fase 4):
// substitui o Selo por texto por um círculo compacto — ✓ cheio (concluído), anel accent
// (atual), anel neutro (disponível, ainda não é o próximo mas dá pra abrir — o curso
// nunca trava aula/tópico, é só apresentação).
function CirculoStatus({ estado }: { estado: ModuloNo["aulas"][number]["topicos"][number]["estado"] }) {
  if (estado === "concluido") {
    return (
      <span className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full bg-[var(--tm-good)] text-[.7rem] font-bold text-white">
        ✓
      </span>
    );
  }
  if (estado === "atual") {
    return <span className="h-[22px] w-[22px] shrink-0 rounded-full border-2 border-[var(--tm-accent)]" aria-hidden />;
  }
  return <span className="h-[22px] w-[22px] shrink-0 rounded-full border-2 border-[var(--tm-border)]" aria-hidden />;
}

function LinhaTopico({
  id,
  titulo,
  referencia,
  estado,
  avaliacaoId,
}: {
  id: number;
  titulo: string;
  referencia: string | null;
  estado: ModuloNo["aulas"][number]["topicos"][number]["estado"];
  avaliacaoId: number | null;
}) {
  if (estado === "em_preparacao") {
    return (
      <div className="flex items-center gap-3 px-4 py-3 opacity-60" title="Conteúdo em preparação">
        <span className="flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full bg-[var(--tm-surface-2)] text-[.7rem] text-[var(--tm-ink-muted)]" aria-hidden>
          …
        </span>
        <span className="text-[var(--tm-ink-muted)]">{titulo}</span>
      </div>
    );
  }

  // Prova travada até concluir o conteúdo (2026-09-19, decisão confirmada —
  // ver PLANO_AVALIACAO_SEPARADA.md, seção "Gating CONFIRMADO"): o backend já
  // recusa (403) se tentarem entrar direto sem concluir. O chip aqui é só a UI.
  //
  // IMPORTANTE: o chip da prova é um <Link> IRMÃO do <Link> do tópico, nunca
  // aninhado dentro dele — <a> dentro de <a> é HTML inválido e o navegador
  // fecha o link de fora antes da hora, quebrando a área clicável.
  const chipProva = avaliacaoId != null && (
    estado === "concluido" ? (
      <Link
        href={`/topico/${id}/prova`}
        className="shrink-0 rounded-[var(--tm-radius-pill)] border border-[var(--tm-accent)] px-2.5 py-1 text-[.72rem] font-semibold text-[var(--tm-accent)] hover:bg-[var(--tm-surface-2)]"
      >
        📝 Prova
      </Link>
    ) : (
      <span
        className="shrink-0 rounded-[var(--tm-radius-pill)] border border-[var(--tm-border)] px-2.5 py-1 text-[.72rem] font-semibold text-[var(--tm-ink-muted)]"
        title="A prova libera depois que você concluir o tópico"
      >
        🔒 Prova
      </span>
    )
  );

  return (
    <div className="flex items-center gap-3 px-4 py-3 transition-colors hover:bg-[var(--tm-surface-2)]">
      <Link href={`/topico/${id}`} className="flex min-w-0 flex-1 items-center gap-3">
        <CirculoStatus estado={estado} />
        <span className="min-w-0 flex-1 truncate">{titulo}</span>
        {referencia && <Chip tom="info" className="shrink-0">{referencia}</Chip>}
      </Link>
      {chipProva}
    </div>
  );
}

function Modulo({ modulo, aberto }: { modulo: ModuloNo; aberto: boolean }) {
  const [open, setOpen] = useState(aberto);
  const { concluidos, total } = contarModulo(modulo);
  const feito = total > 0 && concluidos === total;

  return (
    <div className="overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
      {modulo.cover_image_url && (
        <img
          src={modulo.cover_image_url}
          alt={`Capa do módulo ${modulo.module_index}: ${modulo.titulo}`}
          className="h-28 w-full object-cover sm:h-36"
        />
      )}
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center gap-3 px-4 py-3.5 text-left"
      >
        <span
          aria-hidden
          className={
            "flex h-[34px] w-[34px] shrink-0 items-center justify-center rounded-[10px] text-[.95rem] font-semibold " +
            (feito
              ? "bg-[var(--tm-good)] text-white"
              : total === 0
                ? "bg-[var(--tm-surface-2)] text-[var(--tm-ink-muted)]"
                : "bg-[var(--tm-surface-2)] text-[var(--tm-accent)]")
          }
          style={{ fontFamily: "var(--tm-font-display)" }}
        >
          {feito ? "✓" : modulo.module_index}
        </span>
        <span className="flex-1">
          <span className="block text-[.72rem] uppercase tracking-wide text-[var(--tm-ink-muted)]">
            Módulo {modulo.module_index}
          </span>
          <span style={{ fontFamily: "var(--tm-font-display)" }} className="text-[1.02rem]">
            {modulo.titulo}
          </span>
        </span>
        <span className="shrink-0 text-[.78rem] text-[var(--tm-ink-muted)]">
          {total === 0 ? "em preparação" : `${concluidos}/${total}`}
        </span>
        <span aria-hidden className="shrink-0 text-[var(--tm-ink-muted)] transition-transform" style={{ transform: open ? "rotate(90deg)" : "none" }}>
          ▸
        </span>
      </button>

      {open && (
        <div className="border-t border-[var(--tm-border)]">
          {modulo.aulas.length === 0 && (
            <p className="px-4 py-3 text-[.85rem] text-[var(--tm-ink-muted)]">
              Nenhuma aula cadastrada ainda.
            </p>
          )}
          {modulo.aulas.map((aula) => (
            <div key={aula.id} className="border-b border-[var(--tm-border)] last:border-b-0">
              <div className="bg-[var(--tm-surface-2)]/50 px-4 py-2 text-[.8rem] font-semibold text-[var(--tm-ink-muted)]">
                Aula {aula.lesson_index} · {aula.titulo}
              </div>
              {aula.topicos.length === 0 ? (
                <p className="px-4 py-3 text-[.82rem] text-[var(--tm-ink-muted)]">
                  Tópicos em preparação.
                </p>
              ) : (
                <div className="divide-y divide-[var(--tm-border)]">
                  {aula.topicos.map((t) => (
                    <LinhaTopico
                      key={t.id}
                      id={t.id}
                      titulo={t.titulo}
                      referencia={t.referencia_biblica}
                      estado={t.estado}
                      avaliacaoId={t.avaliacaoId}
                    />
                  ))}
                </div>
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
  return (
    <div className="flex flex-col gap-3">
      {modulos.map((m) => (
        <Modulo key={m.id} modulo={m} aberto={m.id === moduloAbertoId} />
      ))}
    </div>
  );
}
