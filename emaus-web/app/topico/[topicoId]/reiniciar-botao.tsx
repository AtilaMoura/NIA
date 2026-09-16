"use client";

// Botão "Recomeçar este tópico" (2026-09-15) — pro aluno que respondeu
// qualquer coisa só pra testar/ver o conteúdo e quer refazer valendo de
// verdade. Não apaga nada (POST /topico-progress/{id}/reiniciar só abre uma
// rodada nova) — recarrega a página inteira pra pegar token/estado frescos.

import { useState } from "react";
import { Botao } from "../../_ui/Botao";
import { reiniciarTopico } from "../../_lib/api";

export function ReiniciarTopicoBotao({ topicoId }: { topicoId: number }) {
  const [carregando, setCarregando] = useState(false);

  async function aoClicar() {
    const confirmado = window.confirm(
      "Recomeçar este tópico? Suas respostas atuais somem da tela (nada é apagado de verdade) e você responde tudo de novo do zero.",
    );
    if (!confirmado) return;
    setCarregando(true);
    try {
      await reiniciarTopico(topicoId);
      window.location.reload();
    } catch (e) {
      console.error("falha ao recomeçar tópico", e);
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
