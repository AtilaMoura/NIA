"use client";

import { useState } from "react";
import { Botao } from "../../../_ui/Botao";
import { Chip } from "../../../_ui/Chip";
import {
  despublicarCurso,
  publicarCurso,
  salvarAprovacaoCurso,
  salvarConfigCurso,
  type GovernancaCurso,
} from "../../../_lib/api";
import type { Papel } from "../../../_lib/papel";

export function GovernancaCursoUI({
  courseId,
  governancaInicial,
  meuUserId,
  meuPapel,
  souAdmin,
}: {
  courseId: number;
  governancaInicial: GovernancaCurso;
  meuUserId: number;
  meuPapel: Papel;
  souAdmin: boolean;
}) {
  const [gov, setGov] = useState(governancaInicial);
  const minhaAprovacao = gov.aprovacoes.find((a) => a.user_id === meuUserId) ?? null;
  const possoAprovar = souAdmin || gov.sou_tutor;

  return (
    <div className="flex flex-col gap-8">
      <PublicarCard courseId={courseId} gov={gov} onAtualizar={setGov} meuPapel={meuPapel} />

      {souAdmin && (
        <ConfigCard courseId={courseId} gov={gov} onAtualizar={setGov} />
      )}

      {possoAprovar ? (
        <AprovacaoCard
          courseId={courseId}
          minhaAprovacao={minhaAprovacao}
          onAtualizar={(a) =>
            setGov((g) => ({
              ...g,
              aprovacoes: g.aprovacoes.some((x) => x.user_id === a.user_id)
                ? g.aprovacoes.map((x) => (x.user_id === a.user_id ? a : x))
                : [...g.aprovacoes, a],
            }))
          }
        />
      ) : (
        <p className="m-0 text-[.82rem] text-[var(--tm-ink-muted)]">
          Você não é tutor deste curso, então não participa da aprovação de publicação (pode ver o
          andamento abaixo).
        </p>
      )}

      <div className="flex flex-col gap-2">
        <h2 className="m-0 text-[.9rem] font-semibold">Quem já se posicionou</h2>
        {gov.aprovacoes.length === 0 ? (
          <p className="m-0 text-[.82rem] text-[var(--tm-ink-muted)]">Ninguém ainda.</p>
        ) : (
          <ul className="m-0 flex list-none flex-col gap-1.5 p-0">
            {gov.aprovacoes.map((a) => (
              <li
                key={a.user_id}
                className="flex flex-wrap items-center gap-2 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-2 text-[.82rem]"
              >
                <Chip tom={a.aprovado ? "bom" : "aviso"}>{a.aprovado ? "Aprovou" : "Reprovou"}</Chip>
                <span className="font-medium">{a.name ?? "—"}</span>
                <span className="text-[var(--tm-ink-muted)]">({a.papel_no_momento})</span>
                {a.observacao && <span className="text-[var(--tm-ink-muted)]">— {a.observacao}</span>}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

function PublicarCard({
  courseId,
  gov,
  onAtualizar,
  meuPapel,
}: {
  courseId: number;
  gov: GovernancaCurso;
  onAtualizar: (g: GovernancaCurso) => void;
  meuPapel: Papel;
}) {
  const [processando, setProcessando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function publicar() {
    setProcessando(true);
    setErro(null);
    try {
      onAtualizar(await publicarCurso(courseId));
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não deu pra publicar.");
    } finally {
      setProcessando(false);
    }
  }

  async function despublicar() {
    setProcessando(true);
    setErro(null);
    try {
      onAtualizar(await despublicarCurso(courseId));
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não deu pra despublicar.");
    } finally {
      setProcessando(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-4">
      <div className="flex items-center gap-2">
        <Chip tom={gov.publicado ? "bom" : "neutro"}>{gov.publicado ? "Publicado" : "Não publicado"}</Chip>
        {!gov.publicado && (
          <span className="text-[.78rem] text-[var(--tm-ink-muted)]">
            {gov.pode_publicar ? "Condições de aprovação atingidas." : "Ainda faltam aprovações."}
          </span>
        )}
      </div>
      <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">
        Publicar não mexe na aprovação de cada tópico (isso é feito na revisão individual) — é o
        interruptor final do curso inteiro.
      </p>
      <div className="flex gap-2">
        {!gov.publicado && (
          <Botao tamanho="sm" onClick={publicar} disabled={processando || !gov.pode_publicar}>
            {processando ? "Publicando…" : "Publicar curso"}
          </Botao>
        )}
        {gov.publicado && meuPapel === "master" && (
          <Botao tamanho="sm" variante="perigo" onClick={despublicar} disabled={processando}>
            {processando ? "Despublicando…" : "Despublicar"}
          </Botao>
        )}
      </div>
      {erro && <span className="text-[.78rem] text-[var(--tm-danger)]">{erro}</span>}
    </div>
  );
}

function ConfigCard({
  courseId,
  gov,
  onAtualizar,
}: {
  courseId: number;
  gov: GovernancaCurso;
  onAtualizar: (g: GovernancaCurso) => void;
}) {
  const [masterBasta, setMasterBasta] = useState(gov.aprovacao_master_basta);
  const [exigeTodos, setExigeTodos] = useState(gov.aprovacao_exige_todos_tutores);
  const [tutorIds, setTutorIds] = useState(new Set(gov.tutores.map((t) => t.id)));
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  function alternarTutor(id: number) {
    setTutorIds((prev) => {
      const novo = new Set(prev);
      if (novo.has(id)) novo.delete(id);
      else novo.add(id);
      return novo;
    });
  }

  async function salvar() {
    setSalvando(true);
    setErro(null);
    try {
      const atualizado = await salvarConfigCurso({
        courseId,
        aprovacaoMasterBasta: masterBasta,
        aprovacaoExigeTodosTutores: exigeTodos,
        tutorIds: [...tutorIds],
      });
      onAtualizar(atualizado);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não deu pra salvar.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-4">
      <h2 className="m-0 text-[.9rem] font-semibold">Configurar aprovação</h2>

      <label className="flex items-center gap-2 text-[.82rem]">
        <input type="checkbox" checked={masterBasta} onChange={(e) => setMasterBasta(e.target.checked)} />
        Master pode publicar sozinho, sem esperar tutor nenhum
      </label>
      <label className="flex items-center gap-2 text-[.82rem]">
        <input type="checkbox" checked={exigeTodos} onChange={(e) => setExigeTodos(e.target.checked)} />
        Precisa de TODOS os tutores aprovarem (senão, 1 já libera)
      </label>

      <div className="flex flex-col gap-1.5">
        <p className="m-0 text-[.8rem] font-semibold">Tutores deste curso</p>
        {gov.professores_disponiveis.length === 0 ? (
          <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">Nenhum professor cadastrado.</p>
        ) : (
          gov.professores_disponiveis.map((p) => (
            <label key={p.id} className="flex items-center gap-2 text-[.82rem]">
              <input
                type="checkbox"
                checked={tutorIds.has(p.id)}
                onChange={() => alternarTutor(p.id)}
              />
              {p.name ?? p.email}
            </label>
          ))
        )}
      </div>

      <Botao tamanho="sm" onClick={salvar} disabled={salvando} className="self-start">
        {salvando ? "Salvando…" : "Salvar configuração"}
      </Botao>
      {erro && <span className="text-[.78rem] text-[var(--tm-danger)]">{erro}</span>}
    </div>
  );
}

function AprovacaoCard({
  courseId,
  minhaAprovacao,
  onAtualizar,
}: {
  courseId: number;
  minhaAprovacao: GovernancaCurso["aprovacoes"][number] | null;
  onAtualizar: (a: GovernancaCurso["aprovacoes"][number]) => void;
}) {
  const [aprovado, setAprovado] = useState<boolean | null>(minhaAprovacao?.aprovado ?? null);
  const [observacao, setObservacao] = useState(minhaAprovacao?.observacao ?? "");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function salvar() {
    if (aprovado === null) {
      setErro("Escolha aprovar ou reprovar.");
      return;
    }
    setSalvando(true);
    setErro(null);
    try {
      const resultado = await salvarAprovacaoCurso(courseId, aprovado, observacao.trim() || null);
      onAtualizar(resultado);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não deu pra salvar.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div className="flex flex-col gap-3 rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-4">
      <h2 className="m-0 text-[.9rem] font-semibold">Sua avaliação da publicação</h2>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => setAprovado(true)}
          className={
            "flex-1 rounded-[var(--tm-radius)] border px-3 py-1.5 text-[.82rem] font-semibold " +
            (aprovado === true
              ? "border-[var(--tm-good)] bg-[var(--tm-verse-bg)] text-[var(--tm-good)]"
              : "border-[var(--tm-border)]")
          }
        >
          ✓ Aprovar publicação
        </button>
        <button
          type="button"
          onClick={() => setAprovado(false)}
          className={
            "flex-1 rounded-[var(--tm-radius)] border px-3 py-1.5 text-[.82rem] font-semibold " +
            (aprovado === false
              ? "border-[var(--tm-danger)] bg-[var(--tm-verse-bg)] text-[var(--tm-danger)]"
              : "border-[var(--tm-border)]")
          }
        >
          ✕ Reprovar
        </button>
      </div>
      <textarea
        value={observacao}
        onChange={(e) => setObservacao(e.target.value)}
        rows={2}
        placeholder="Observação (opcional)"
        className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-bg)] p-2 text-[.82rem]"
      />
      <Botao tamanho="sm" onClick={salvar} disabled={salvando} className="self-start">
        {salvando ? "Salvando…" : "Salvar avaliação"}
      </Botao>
      {erro && <span className="text-[.78rem] text-[var(--tm-danger)]">{erro}</span>}
    </div>
  );
}
