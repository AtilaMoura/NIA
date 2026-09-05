"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Botao } from "../_ui/Botao";

function proximaRota(): string {
  if (typeof window === "undefined") return "/inicio";
  const next = new URLSearchParams(window.location.search).get("next");
  return next && next.startsWith("/") ? next : "/inicio";
}

export function EntrarForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [perfisDev, setPerfisDev] = useState<{ id: string; rotulo: string }[] | null>(null);

  // Botões de login rápido só existem em dev — a rota devolve 404 em produção.
  useEffect(() => {
    fetch("/api/sessao/dev")
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setPerfisDev(d?.perfis ?? null))
      .catch(() => setPerfisDev(null));
  }, []);

  async function entrar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      const res = await fetch("/api/sessao", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password: senha }),
      });
      const data = await res.json();
      if (!res.ok) {
        setErro(data.erro ?? "Não foi possível entrar.");
        return;
      }
      router.push(proximaRota());
      router.refresh();
    } catch {
      setErro("Falha de conexão. Tente de novo.");
    } finally {
      setEnviando(false);
    }
  }

  async function entrarRapido(perfil: string) {
    setEnviando(true);
    setErro(null);
    try {
      const res = await fetch("/api/sessao/dev", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ perfil }),
      });
      if (!res.ok) {
        setErro("Login rápido falhou — rode o seed de usuários.");
        return;
      }
      router.push(proximaRota());
      router.refresh();
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <form onSubmit={entrar} className="flex flex-col gap-3">
        <label className="flex flex-col gap-1 text-[.82rem] font-semibold">
          E-mail
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.95rem] font-normal"
          />
        </label>
        <label className="flex flex-col gap-1 text-[.82rem] font-semibold">
          Senha
          <input
            type="password"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.95rem] font-normal"
          />
        </label>
        {erro && <p className="m-0 text-[.82rem] text-[var(--tm-danger)]">{erro}</p>}
        <Botao type="submit" disabled={enviando} className="mt-1 justify-center">
          {enviando ? "Entrando…" : "Entrar"}
        </Botao>
      </form>

      {perfisDev && perfisDev.length > 0 && (
        <div className="flex flex-col gap-2 rounded-[var(--tm-radius)] border border-dashed border-[var(--tm-border)] p-3">
          <p className="m-0 text-[.75rem] font-semibold uppercase tracking-wide text-[var(--tm-ink-muted)]">
            🔧 Login rápido (dev)
          </p>
          <div className="flex flex-wrap gap-2">
            {perfisDev.map((p) => (
              <button
                key={p.id}
                type="button"
                disabled={enviando}
                onClick={() => entrarRapido(p.id)}
                className="rounded-[var(--tm-radius-pill)] border border-[var(--tm-border)] px-3 py-1 text-[.78rem] hover:border-[var(--tm-accent)] hover:text-[var(--tm-accent)] disabled:opacity-50"
              >
                {p.rotulo}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
