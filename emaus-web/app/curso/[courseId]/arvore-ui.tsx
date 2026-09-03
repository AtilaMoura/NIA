"use client";

import { useState } from "react";
import Link from "next/link";
import { Chip } from "../../_ui/Chip";
import { Selo } from "../../_ui/Selo";
import { contarModulo, type ModuloNo } from "../../_lib/arvore";

function LinhaTopico({
  id,
  titulo,
  referencia,
  estado,
}: {
  id: number;
  titulo: string;
  referencia: string | null;
  estado: ModuloNo["aulas"][number]["topicos"][number]["estado"];
}) {
  const conteudo = (
    <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
      <Selo estado={estado} />
      <span className={estado === "em_preparacao" ? "text-[var(--tm-ink-muted)]" : ""}>{titulo}</span>
      {referencia && <Chip tom="info">{referencia}</Chip>}
    </div>
  );

  if (estado === "em_preparacao") {
    return (
      <div className="px-4 py-3 opacity-60" title="Conteúdo em preparação">
        {conteudo}
      </div>
    );
  }
  return (
    <Link
      href={`/topico/${id}`}
      className="block px-4 py-3 transition-colors hover:bg-[var(--tm-surface-2)]"
    >
      {conteudo}
    </Link>
  );
}

function Modulo({ modulo, aberto }: { modulo: ModuloNo; aberto: boolean }) {
  const [open, setOpen] = useState(aberto);
  const { concluidos, total } = contarModulo(modulo);

  return (
    <div className="overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center gap-3 px-4 py-3.5 text-left"
      >
        <span aria-hidden className="text-[var(--tm-ink-muted)] transition-transform" style={{ transform: open ? "rotate(90deg)" : "none" }}>
          ▸
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
