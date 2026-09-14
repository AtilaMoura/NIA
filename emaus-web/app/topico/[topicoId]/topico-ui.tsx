"use client";

import { useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import { enviarAvaliacaoTutor, marcarProgresso, type StatusTopico } from "../../_lib/api";

// Ponte de mensagens entre o <iframe> do render (topico.html.j2) e o Next.js —
// sem UI própria (2026-09-11: antes tinha um painel de resultado + lista de
// anotações fixos embaixo do <iframe>; virou tudo parte do próprio slide
// "Resultado" e um botão flutuante dentro do render). Este componente só
// existe porque o <iframe> não tem o token de sessão real (fica só no
// servidor Next.js — ver docstring de topico_respostas.py): quem chama a API
// do tutor e faz a navegação continua sendo aqui, o resultado só volta pro
// <iframe> via postMessage pra aparecer dentro do slide.
export function AcoesTopico({
  topicoId,
  cursoId,
  estadoInicial,
  proximoTopicoId,
}: {
  topicoId: number;
  cursoId: number;
  estadoInicial: StatusTopico;
  proximoTopicoId: number | null;
}) {
  const router = useRouter();

  useEffect(() => {
    if (estadoInicial === "nao_iniciado") {
      marcarProgresso(topicoId, "em_andamento").catch((e) =>
        console.error("falha ao marcar em_andamento", e),
      );
    }
  }, [topicoId, estadoInicial]);

  const postParaIframe = useCallback((msg: unknown) => {
    const iframe = document.querySelector("iframe");
    (iframe as HTMLIFrameElement | null)?.contentWindow?.postMessage(msg, "*");
  }, []);

  const enviarResumo = useCallback(
    async (texto: string) => {
      try {
        const prog = await enviarAvaliacaoTutor(topicoId, texto);
        const avaliacao = prog.tutor_analise?.ultima_avaliacao;
        postParaIframe({
          tipo: "emaus:avaliacao-resultado",
          veredito: avaliacao?.veredito ?? null,
          resumo_diagnostico: avaliacao?.resumo_diagnostico ?? "",
          temProximo: proximoTopicoId != null,
        });
        router.refresh();
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        postParaIframe({
          tipo: "emaus:avaliacao-erro",
          mensagem: msg.includes("503")
            ? "O tutor está sobrecarregado agora."
            : "Não deu pra falar com o tutor agora.",
        });
        console.error("falha ao avaliar tópico", e);
      }
    },
    [topicoId, proximoTopicoId, postParaIframe, router],
  );

  useEffect(() => {
    function aoReceber(e: MessageEvent) {
      const d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.tipo === "emaus:concluir" && typeof d.texto === "string") {
        enviarResumo(d.texto);
      } else if (d.tipo === "emaus:concluir-fallback") {
        // Plano B — só usado se a avaliação falhar de verdade (tutor
        // sobrecarregado / sem cota), botão que aparece dentro do slide.
        marcarProgresso(topicoId, "concluido")
          .then(() => router.refresh())
          .catch((e) => console.error("falha ao concluir tópico (fallback)", e));
      } else if (d.tipo === "emaus:navegar") {
        if (d.destino === "proximo" && proximoTopicoId != null) {
          router.push(`/topico/${proximoTopicoId}`);
        } else {
          router.push(`/curso/${cursoId}`);
        }
      }
    }
    window.addEventListener("message", aoReceber);
    return () => window.removeEventListener("message", aoReceber);
  }, [enviarResumo, proximoTopicoId, router, topicoId, cursoId]);

  return null;
}
