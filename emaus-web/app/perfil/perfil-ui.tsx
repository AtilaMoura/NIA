"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Botao } from "../_ui/Botao";
import { ALUNO_USER_ID } from "../_lib/config";
import { updateUser } from "../_lib/api";

export function EditarNome({ nomeInicial }: { nomeInicial: string }) {
  const router = useRouter();
  const [editando, setEditando] = useState(false);
  const [valor, setValor] = useState(nomeInicial);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(false);

  async function salvar() {
    const limpo = valor.trim();
    if (!limpo || limpo === nomeInicial) {
      setEditando(false);
      return;
    }
    setSalvando(true);
    setErro(false);
    try {
      await updateUser(ALUNO_USER_ID, { name: limpo });
      setEditando(false);
      router.refresh();
    } catch (e) {
      console.error("falha ao salvar nome", e);
      setErro(true);
    } finally {
      setSalvando(false);
    }
  }

  if (!editando) {
    return (
      <div className="flex items-center gap-2">
        <h1 className="m-0 text-[1.3rem]">{nomeInicial || "Aluno"}</h1>
        <button
          type="button"
          onClick={() => {
            setValor(nomeInicial);
            setEditando(true);
          }}
          className="text-[.78rem] font-semibold text-[var(--tm-accent)] hover:underline"
        >
          Editar
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex flex-wrap items-center gap-2">
        <input
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          autoFocus
          onKeyDown={(e) => {
            if (e.key === "Enter") salvar();
            if (e.key === "Escape") setEditando(false);
          }}
          className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-2.5 py-1.5 text-[1rem]"
        />
        <Botao tamanho="sm" onClick={salvar} disabled={salvando}>
          {salvando ? "Salvando…" : "Salvar"}
        </Botao>
        <button
          type="button"
          onClick={() => setEditando(false)}
          className="text-[.8rem] text-[var(--tm-ink-muted)] hover:underline"
        >
          Cancelar
        </button>
      </div>
      {erro && (
        <span className="text-[.78rem] text-[var(--tm-danger)]">
          Não deu pra salvar. Tente de novo.
        </span>
      )}
    </div>
  );
}
