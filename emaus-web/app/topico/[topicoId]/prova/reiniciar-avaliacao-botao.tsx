"use client";

// Botão "Recomeçar esta prova" (2026-09-19) — pro aluno que respondeu
// qualquer coisa só pra testar/ver o conteúdo e quer refazer valendo de
// verdade. Não apaga nada (POST /avaliacao-progress/{id}/reiniciar só abre uma
// rodada nova) — recarrega a página inteira pra pegar token/estado frescos.

import { useState } from "react";
import { Botao } from "../../../_ui/Botao";
import { reiniciarAvaliacao } from "../../../_lib/api";

export function ReiniciarAvaliacaoBotao({ avaliacaoId }: { avaliacaoId: number }) {
  const [carregando, setCarregando] = useState(false);

  async function aoClicar() {
    const confirmado = window.confirm(
      "Recomeçar esta prova? Suas respostas atuais somem da tela (nada é apagado de verdade) e você responde tudo de novo do zero.",
    );
    if (!confirmado) return;
    setCarregando(true);
    try {
      await reiniciarAvaliacao(avaliacaoId);
      window.location.reload();
    } catch (e) {
      console.error("falha ao recomeçar prova", e);
      setCarregando(false);
    }
  }

  return (
    <Botao
      variante="fantasma"
      tamanho="sm"
      onClick={aoClicar}
      disabled={carregando}
      className="shrink-0"
    >
      {carregando ? "Recomeçando…" : "↺ Recomeçar"}
    </Botao>
  );
}