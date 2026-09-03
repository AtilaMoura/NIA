"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Botao, LinkBotao } from "../../_ui/Botao";
import { Chip } from "../../_ui/Chip";
import { ALUNO_USER_ID, TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import { setTopicoProgress, type StatusTopico } from "../../_lib/api";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export function AcoesTopico({
  topicoId,
  estadoInicial,
  proximoTopicoId,
}: {
  topicoId: number;
  estadoInicial: StatusTopico;
  proximoTopicoId: number | null;
}) {
  const router = useRouter();
  const [concluido, setConcluido] = useState(estadoInicial === "concluido");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(false);

  // Ao abrir: marca em_andamento (só se ainda não começou). Fire-and-forget.
  useEffect(() => {
    if (estadoInicial === "nao_iniciado") {
      setTopicoProgress(topicoId, ALUNO_USER_ID, "em_andamento").catch((e) =>
        console.error("falha ao marcar em_andamento", e),
      );
    }
  }, [topicoId, estadoInicial]);

  async function marcarConcluido() {
    setSalvando(true);
    setErro(false);
    setConcluido(true); // otimista
    try {
      await setTopicoProgress(topicoId, ALUNO_USER_ID, "concluido");
      router.refresh();
    } catch (e) {
      console.error("falha ao concluir tópico", e);
      setConcluido(false);
      setErro(true);
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div className="flex flex-wrap items-center gap-3 border-t border-[var(--tm-border)] bg-[var(--tm-bg)] px-[clamp(1rem,4vw,2rem)] py-3">
      {concluido ? (
        <>
          <Chip tom="bom">✓ Concluído</Chip>
          {proximoTopicoId != null ? (
            <LinkBotao href={`/topico/${proximoTopicoId}`} tamanho="sm">
              Próximo tópico
            </LinkBotao>
          ) : (
            <LinkBotao href={`/curso/${CURSO_ID}`} variante="fantasma" tamanho="sm">
              Voltar ao curso
            </LinkBotao>
          )}
        </>
      ) : (
        <>
          <Botao tamanho="sm" onClick={marcarConcluido} disabled={salvando}>
            {salvando ? "Salvando…" : "Marcar como concluído"}
          </Botao>
          {erro && (
            <span className="text-[.8rem] text-[var(--tm-danger)]">
              Não deu pra salvar. Tente de novo.
            </span>
          )}
        </>
      )}
    </div>
  );
}
