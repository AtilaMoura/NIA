"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Botao } from "../_ui/Botao";

export function CriarContaForm() {
  const router = useRouter();
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function criar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      const res = await fetch("/api/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: nome, email, password: senha }),
      });
      const data = await res.json();
      if (!res.ok) {
        setErro(data.erro ?? "Não foi possível criar a conta.");
        return;
      }
      router.push("/inicio");
      router.refresh();
    } catch {
      setErro("Falha de conexão. Tente de novo.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={criar} className="flex flex-col gap-3">
      <label className="flex flex-col gap-1 text-[.82rem] font-semibold">
        Nome
        <input
          required
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.95rem] font-normal"
        />
      </label>
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
          minLength={6}
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.95rem] font-normal"
        />
      </label>
      {erro && <p className="m-0 text-[.82rem] text-[var(--tm-danger)]">{erro}</p>}
      <Botao type="submit" disabled={enviando} className="mt-1 justify-center">
        {enviando ? "Criando…" : "Criar conta"}
      </Botao>
    </form>
  );
}
