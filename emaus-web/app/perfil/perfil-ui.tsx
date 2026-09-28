"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Botao } from "../_ui/Botao";
import { salvarPerfil } from "../_lib/api";

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
      await salvarPerfil(limpo);
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

// Trocar senha (perfil, 2026-09-27): senha atual + nova + confirmação. Quem confere a
// senha atual é o backend (POST /auth/trocar-senha, via /api/senha).
export function TrocarSenha() {
  const [aberto, setAberto] = useState(false);
  const [atual, setAtual] = useState("");
  const [nova, setNova] = useState("");
  const [confirma, setConfirma] = useState("");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [ok, setOk] = useState(false);

  function fechar() {
    setAberto(false);
    setAtual("");
    setNova("");
    setConfirma("");
    setErro(null);
  }

  async function salvar(e: React.FormEvent) {
    e.preventDefault();
    if (nova !== confirma) {
      setErro("A confirmação não é igual à nova senha.");
      return;
    }
    setSalvando(true);
    setErro(null);
    try {
      const res = await fetch("/api/senha", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ senhaAtual: atual, senhaNova: nova }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setErro(data.erro ?? "Não deu pra trocar a senha.");
        return;
      }
      fechar();
      setOk(true);
    } catch {
      setErro("Falha de conexão. Tente de novo.");
    } finally {
      setSalvando(false);
    }
  }

  const campo =
    "w-full rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[1rem] font-normal";

  return (
    <div>
      <div className="flex flex-col gap-3 min-[481px]:flex-row min-[481px]:items-center min-[481px]:justify-between">
        <div>
          <h2 className="m-0 text-[1.05rem]">Senha</h2>
          <p className="m-0 text-[.88rem] text-[var(--tm-ink-muted)]">Troque quando quiser. Você continua conectado.</p>
        </div>
        {!aberto && (
          <Botao
            variante="fantasma"
            onClick={() => {
              setOk(false);
              setAberto(true);
            }}
          >
            Trocar senha
          </Botao>
        )}
      </div>

      {aberto && (
        <form onSubmit={salvar} className="mt-4 grid gap-3">
          <label className="grid gap-1 text-[.84rem] font-semibold">
            Senha atual
            <input type="password" autoComplete="current-password" required value={atual} onChange={(e) => setAtual(e.target.value)} className={campo} />
          </label>
          <label className="grid gap-1 text-[.84rem] font-semibold">
            Nova senha
            <input type="password" autoComplete="new-password" required minLength={6} value={nova} onChange={(e) => setNova(e.target.value)} className={campo} />
            <span className="text-[.78rem] font-normal text-[var(--tm-ink-muted)]">Pelo menos 6 caracteres.</span>
          </label>
          <label className="grid gap-1 text-[.84rem] font-semibold">
            Confirme a nova senha
            <input type="password" autoComplete="new-password" required value={confirma} onChange={(e) => setConfirma(e.target.value)} className={campo} />
          </label>
          {erro && (
            <p role="alert" className="m-0 text-[.85rem] text-[var(--tm-danger)]">
              {erro}
            </p>
          )}
          <div className="flex justify-end gap-3">
            <button type="button" onClick={fechar} className="text-[.85rem] text-[var(--tm-ink-muted)] hover:underline">
              Cancelar
            </button>
            <Botao type="submit" disabled={salvando}>
              {salvando ? "Salvando…" : "Salvar nova senha"}
            </Botao>
          </div>
        </form>
      )}

      {ok && (
        <p role="status" className="m-0 mt-3 rounded-[var(--tm-radius)] bg-[color-mix(in_srgb,var(--tm-good)_12%,transparent)] px-3 py-2 text-[.9rem] font-semibold text-[var(--tm-good)]">
          ✓ Senha alterada.
        </p>
      )}
    </div>
  );
}

// "Sair" da página de perfil — mesmo fluxo do menu do avatar.
export function SairBotao() {
  const router = useRouter();
  const [saindo, setSaindo] = useState(false);
  async function sair() {
    setSaindo(true);
    try {
      await fetch("/api/sessao", { method: "DELETE" });
      router.push("/entrar");
      router.refresh();
    } finally {
      setSaindo(false);
    }
  }
  return (
    <Botao variante="perigo" onClick={sair} disabled={saindo}>
      {saindo ? "Saindo…" : "Sair"}
    </Botao>
  );
}
