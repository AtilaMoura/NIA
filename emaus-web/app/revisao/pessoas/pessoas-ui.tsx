"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Avatar } from "../../_ui/Avatar";
import type { PessoaResumo } from "../../_lib/api";
import { duracao, quando, ROTULO_PAPEL, sinalDe, ultimoAcesso, type Sinal } from "../../_lib/pessoas";

// Filtro por papel + busca + ordenação da página Pessoas (tudo no navegador — a
// lista é pequena). Tabela no desktop, cartões no celular.

const FILTROS = [
  { valor: "todos", rotulo: "Todos" },
  { valor: "aluno", rotulo: "Alunos" },
  { valor: "admin", rotulo: "Admins" },
  { valor: "professor", rotulo: "Professores" },
] as const;

type Ordem = "atividade" | "nome" | "cadastro" | "parado";

const COR_SINAL: Record<Sinal, string> = {
  hoje: "bg-[var(--tm-good)]",
  semana: "bg-[var(--tm-warn)]",
  parado: "bg-[var(--tm-bad,#a5352b)]",
  nunca: "bg-[var(--tm-border)]",
};

function tempoDe(iso: string | null): number {
  return iso ? new Date(iso).getTime() : 0;
}

export function ListaPessoas({ pessoas }: { pessoas: PessoaResumo[] }) {
  const [filtro, setFiltro] = useState<(typeof FILTROS)[number]["valor"]>("todos");
  const [busca, setBusca] = useState("");
  const [ordem, setOrdem] = useState<Ordem>("atividade");

  const visiveis = useMemo(() => {
    const termo = busca.trim().toLowerCase();
    const lista = pessoas.filter((p) => {
      // Master entra em "Todos" e em "Admins" (é da equipe)
      if (filtro === "admin" && p.role !== "admin" && p.role !== "master") return false;
      if (filtro !== "todos" && filtro !== "admin" && p.role !== filtro) return false;
      if (termo && !`${p.name ?? ""} ${p.email}`.toLowerCase().includes(termo)) return false;
      return true;
    });
    const recente = (p: PessoaResumo) => tempoDe(ultimoAcesso(p));
    return [...lista].sort((a, b) => {
      if (ordem === "nome") return (a.name ?? a.email).localeCompare(b.name ?? b.email, "pt-BR");
      if (ordem === "cadastro") return tempoDe(b.cadastro_em) - tempoDe(a.cadastro_em);
      if (ordem === "parado") return recente(a) - recente(b);
      return recente(b) - recente(a);
    });
  }, [pessoas, filtro, busca, ordem]);

  const grade =
    "grid grid-cols-2 gap-x-3 gap-y-2 min-[760px]:grid-cols-[2.2fr_1.1fr_1.2fr_.8fr_.6fr_.8fr_14px] min-[760px]:items-center";
  const rot = "block text-[.7rem] uppercase tracking-[.06em] text-[var(--tm-ink-muted)] min-[760px]:hidden";

  return (
    <>
      <div className="mt-5 flex flex-wrap items-center gap-2.5">
        <div role="group" aria-label="Filtrar por papel" className="inline-flex overflow-hidden rounded-full border border-[var(--tm-border)]">
          {FILTROS.map((f) => (
            <button
              key={f.valor}
              type="button"
              aria-pressed={filtro === f.valor}
              onClick={() => setFiltro(f.valor)}
              className={
                "px-3.5 py-1.5 text-[.85rem] " +
                (filtro === f.valor ? "bg-[var(--tm-accent)] font-semibold text-[var(--tm-bg)]" : "text-[var(--tm-ink-muted)]")
              }
            >
              {f.rotulo}
            </button>
          ))}
        </div>
        <input
          type="search"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          placeholder="Buscar por nome ou e-mail"
          aria-label="Buscar"
          className="min-w-[180px] flex-1 rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-2 text-[.9rem]"
        />
        <select
          value={ordem}
          onChange={(e) => setOrdem(e.target.value as Ordem)}
          aria-label="Ordenar"
          className="rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.85rem]"
        >
          <option value="atividade">Mais recente</option>
          <option value="parado">Mais parado</option>
          <option value="nome">Nome</option>
          <option value="cadastro">Cadastro</option>
        </select>
      </div>

      <div className="mt-4 overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
        <div
          className={
            grade +
            " hidden border-b border-[var(--tm-border)] bg-[var(--tm-surface-2)] px-4 py-2.5 text-[.72rem] font-bold uppercase tracking-[.08em] text-[var(--tm-ink-muted)] min-[760px]:grid"
          }
        >
          <span>Pessoa</span>
          <span>Último login</span>
          <span>Última atividade</span>
          <span>Tópicos</span>
          <span>Provas</span>
          <span>Tempo</span>
          <span />
        </div>

        <div className="divide-y divide-[var(--tm-border)]">
        {visiveis.length === 0 && (
          <p className="m-0 px-4 py-6 text-center text-[.9rem] text-[var(--tm-ink-muted)]">Ninguém encontrado.</p>
        )}

        {visiveis.map((p) => {
          const sinal = sinalDe(p.ultima_atividade);
          const elevado = p.role !== "aluno";
          return (
            <Link
              key={p.id}
              href={`/revisao/pessoas/${p.id}`}
              className={grade + " px-4 py-3 text-[.88rem] hover:bg-[var(--tm-surface-2)]"}
            >
              <span className="col-span-2 flex min-w-0 items-center gap-2.5 min-[760px]:col-span-1">
                <Avatar nome={p.name ?? p.email} />
                <span className="min-w-0">
                  <b className="block truncate font-semibold">{p.name ?? "Sem nome"}</b>
                  <span
                    className={
                      "rounded-full border px-1.5 text-[.7rem] font-bold " +
                      (elevado ? "border-[var(--tm-accent)] text-[var(--tm-accent)]" : "border-[var(--tm-border)] text-[var(--tm-ink-muted)]")
                    }
                  >
                    {ROTULO_PAPEL[p.role] ?? p.role}
                  </span>
                </span>
              </span>
              <span>
                <span className={rot}>Último login</span>
                {quando(p.ultimo_login)}
              </span>
              <span>
                <span className={rot}>Última atividade</span>
                <span className="inline-flex items-center gap-1.5 whitespace-nowrap">
                  <span aria-hidden className={"h-2 w-2 shrink-0 rounded-full " + COR_SINAL[sinal]} />
                  {quando(p.ultima_atividade)}
                </span>
              </span>
              <span>
                <span className={rot}>Tópicos</span>
                {p.topicos_concluidos} de {p.topicos_iniciados}
              </span>
              <span>
                <span className={rot}>Provas</span>
                {p.provas_feitas}
              </span>
              <span>
                <span className={rot}>Tempo</span>
                {duracao(p.tempo_s)}
              </span>
              <span aria-hidden className="hidden text-[var(--tm-ink-muted)] min-[760px]:block">
                ›
              </span>
            </Link>
          );
        })}
        </div>
      </div>
      <p className="m-0 mt-2 text-[.78rem] text-[var(--tm-ink-muted)]">
        Tópicos: concluídos de começados. Bolinha: verde até 2 dias, laranja até 7, vermelha mais que isso.
      </p>
    </>
  );
}
