"use client";

import { useState } from "react";
import Link from "next/link";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { Card } from "../../../components/ui/Card";
import { avaliarResumo } from "../../../lib/api";

type AvaliacaoPanelProps = {
  lessonId: number;
  userId: number;
};

type Estado =
  | { tipo: "idle" }
  | { tipo: "carregando" }
  | { tipo: "erro"; mensagem: string }
  | { tipo: "feito"; veredito: string; diagnostico: string; canAdvance: boolean };

export function AvaliacaoPanel({ lessonId, userId }: AvaliacaoPanelProps) {
  const [resumo, setResumo] = useState("");
  const [estado, setEstado] = useState<Estado>({ tipo: "idle" });

  async function enviar() {
    if (!resumo.trim()) return;
    setEstado({ tipo: "carregando" });
    try {
      const resultado = await avaliarResumo(lessonId, { userId, resumoTexto: resumo });
      setEstado({
        tipo: "feito",
        veredito: resultado.avaliacao.veredito,
        diagnostico: resultado.avaliacao.resumo_diagnostico ?? "",
        canAdvance: resultado.can_advance,
      });
    } catch (e) {
      setEstado({ tipo: "erro", mensagem: e instanceof Error ? e.message : "Erro ao avaliar o resumo." });
    }
  }

  const dominado = estado.tipo === "feito" && estado.veredito === "dominado";

  return (
    <Card className="flex flex-col gap-3 max-w-2xl">
      <h3 className="m-0 text-[.92rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
        Avaliação final
      </h3>
      <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
        Cole abaixo o resumo mostrado no final da lição pra receber o veredito do Tutor.
      </p>
      <textarea
        value={resumo}
        onChange={(e) => setResumo(e.target.value)}
        rows={6}
        placeholder="Cole aqui o texto de === RESUMO ==="
        className="w-full rounded-[var(--nia-radius-md)] border p-3 text-[.85rem]"
        style={{ background: "var(--nia-surface2)", borderColor: "var(--nia-border)", color: "var(--nia-ink)" }}
      />
      <div>
        <Button variant="accent" onClick={enviar} disabled={estado.tipo === "carregando" || !resumo.trim()}>
          {estado.tipo === "carregando" ? "Avaliando..." : "Avaliar"}
        </Button>
      </div>

      {estado.tipo === "erro" && (
        <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-bad)" }}>
          {estado.mensagem}
        </p>
      )}

      {estado.tipo === "feito" && (
        <div className="flex flex-col gap-2">
          <Badge variant={dominado ? "good" : "bad"}>{dominado ? "Dominado" : "Precisa reforçar"}</Badge>
          <p className="m-0 text-[.85rem]" style={{ color: "var(--nia-ink)" }}>
            {estado.diagnostico}
          </p>
          {estado.canAdvance && (
            <Link href="/aluno" className="text-[.83rem] font-bold" style={{ color: "var(--nia-accent)" }}>
              Voltar ao painel para continuar →
            </Link>
          )}
        </div>
      )}
    </Card>
  );
}
