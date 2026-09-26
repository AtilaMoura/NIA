"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { CampoSenha } from "../_ui/CampoSenha";
import { destinoSeguro } from "../_lib/destino";

export function CriarContaForm() {
  const router = useRouter();
  const next = useSearchParams().get("next");
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
      // Volta pra onde a pessoa queria ir (ex.: um curso), senão /inicio
      router.push(destinoSeguro(next));
      router.refresh();
    } catch {
      setErro("Falha de conexão. Tente de novo.");
    } finally {
      setEnviando(false);
    }
  }

  const linkEntrar = next ? `/entrar?next=${encodeURIComponent(next)}` : "/entrar";

  return (
    <>
      <form onSubmit={criar} className="mt-6 grid gap-4">
        <label className="grid gap-1.5 text-[.84rem] font-semibold">
          Seu nome
          <input name="name" autoComplete="name" required value={nome} onChange={(e) => setNome(e.target.value)} />
        </label>
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
          Crie uma senha
          <CampoSenha valor={senha} aoMudar={setSenha} autoComplete="new-password" minLength={6} />
          <span className="vidro-suave text-[.78rem] font-normal">Pelo menos 6 caracteres.</span>
        </label>
        {erro && (
          <p role="alert" className="acesso-erro m-0">
            {erro}
          </p>
        )}
        <button type="submit" disabled={enviando} className="acesso-botao">
          {enviando ? "Criando…" : "Criar conta"}
        </button>
      </form>

      <p className="vidro-suave m-0 mt-5 text-center text-[.9rem]">
        Já tem conta?{" "}
        <Link href={linkEntrar} className="vidro-destaque font-semibold hover:underline">
          Entrar
        </Link>
      </p>
    </>
  );
}
