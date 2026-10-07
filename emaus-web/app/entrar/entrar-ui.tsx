"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { CampoSenha } from "../_ui/CampoSenha";
import { destinoSeguro } from "../_lib/destino";

export function EntrarForm() {
  const router = useRouter();
  const next = useSearchParams().get("next");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [avisoSenha, setAvisoSenha] = useState(false);
  const [perfisDev, setPerfisDev] = useState<{ id: string; rotulo: string }[] | null>(null);

  // Botões de login rápido só existem em dev — em produção nem pergunta (a rota
  // devolveria 404 e sujaria o console).
  useEffect(() => {
    if (process.env.NODE_ENV === "production") return;
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
      router.push(destinoSeguro(next));
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
      router.push(destinoSeguro(next));
      router.refresh();
    } finally {
      setEnviando(false);
    }
  }

  const linkCriarConta = next ? `/criar-conta?next=${encodeURIComponent(next)}` : "/criar-conta";

  return (
    <>
      <form onSubmit={entrar} className="mt-6 grid gap-4">
        <label className="grid gap-1.5 text-[.84rem] font-semibold">
          E-mail
          <input
            type="email"
            name="email"
            autoComplete="email"
            inputMode="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="grid gap-1.5 text-[.84rem] font-semibold">
          <span className="flex items-baseline justify-between">
            Senha
            <button
              type="button"
              onClick={() => setAvisoSenha((v) => !v)}
              className="vidro-destaque text-[.8rem] font-semibold hover:underline"
            >
              Esqueceu a senha?
            </button>
          </span>
          <CampoSenha valor={senha} aoMudar={setSenha} autoComplete="current-password" />
        </label>
        {/* Sem recuperação por e-mail ainda (decisão 2026-09-26): o admin redefine */}
        {avisoSenha && (
          <p className="acesso-aviso m-0">
            Por enquanto, peça pra quem administra o Emaús na sua igreja redefinir sua senha.
          </p>
        )}
        {erro && (
          <p role="alert" className="acesso-erro m-0">
            {erro}
          </p>
        )}
        <button type="submit" disabled={enviando} className="acesso-botao">
          {enviando ? "Entrando…" : "Entrar"}
        </button>
      </form>

      <p className="vidro-suave m-0 mt-5 text-center text-[.9rem]">
        Ainda não tem conta?{" "}
        <Link href={linkCriarConta} className="vidro-destaque font-semibold hover:underline">
          Criar conta grátis
        </Link>
      </p>

      {perfisDev && perfisDev.length > 0 && (
        <div className="mt-5 flex flex-col gap-2 rounded-[var(--tm-radius)] border border-dashed border-white/25 p-3">
          <p className="vidro-suave m-0 text-[.72rem] font-semibold uppercase tracking-wide">
            🔧 Login rápido (dev)
          </p>
          <div className="flex flex-wrap gap-2">
            {perfisDev.map((p) => (
              <button
                key={p.id}
                type="button"
                disabled={enviando}
                onClick={() => entrarRapido(p.id)}
                className="rounded-[var(--tm-radius-pill)] border border-white/30 px-3 py-1 text-[.78rem] hover:border-[#eab676] hover:text-[#eab676] disabled:opacity-50"
              >
                {p.rotulo}
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
