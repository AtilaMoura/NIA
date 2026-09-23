"use client";

import { useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import { enviarAvaliacaoTutorProva, marcarProgressoAvaliacao, type StatusTopico } from "../../../_lib/api";

// Ponte de mensagens entre o <iframe> do render (avaliacao.html.j2) e o Next.js —
// sem UI própria. Este componente só existe porque o <iframe> não tem o token de
// sessão real (fica só no servidor Next.js): quem chama a API do tutor e faz a
// navegação continua sendo aqui, o resultado só volta pro <iframe> via postMessage.
export function AcoesProva({
  avaliacaoId,
  topicoId,
  estadoInicial,
}: {
  avaliacaoId: number;
  topicoId: number;
  estadoInicial: StatusTopico;
}) {
  const router = useRouter();

  useEffect(() => {
    if (estadoInicial === "nao_iniciado") {
      marcarProgressoAvaliacao(avaliacaoId, "em_andamento").catch((e) =>
        console.error("falha ao marcar em_andamento", e),
      );
    }
  }, [avaliacaoId, estadoInicial]);

  const postParaIframe = useCallback((msg: unknown) => {
    const iframe = document.querySelector("iframe");
    (iframe as HTMLIFrameElement | null)?.contentWindow?.postMessage(msg, "*");
  }, []);

  const enviarResumo = useCallback(
    async (texto: string) => {
      try {
        const prog = await enviarAvaliacaoTutorProva(avaliacaoId, texto);
        const avaliacao = prog.tutor_analise?.ultima_avaliacao;
        postParaIframe({
          tipo: "emaus:avaliacao-resultado",
          veredito: avaliacao?.veredito ?? null,
          resumo_diagnostico: avaliacao?.resumo_diagnostico ?? "",
          temProximo: false,
        });
        // SEM router.refresh() aqui (achado 2026-09-23): o refresh gera um token
        // de resposta novo na página → muda o src do <iframe> → ele recarrega e
        // o resultado some (com veredito "reforco" voltava pro "Clique em Fim").
        // A prova não mostra nada que dependa do status fora do <iframe>; ao
        // voltar pro tópico (router.push) os dados já vêm frescos do servidor.
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        postParaIframe({
          tipo: "emaus:avaliacao-erro",
          mensagem: msg.includes("503")
            ? "O tutor está sobrecarregado agora."
            : "Não deu pra falar com o tutor agora.",
        });
        console.error("falha ao avaliar prova", e);
      }
    },
    [avaliacaoId, postParaIframe],
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
        // Mesmo motivo do enviarResumo: sem refresh, senão o <iframe> recarrega.
        marcarProgressoAvaliacao(avaliacaoId, "concluido")
          .catch((e) => console.error("falha ao concluir prova (fallback)", e));
      } else if (d.tipo === "emaus:navegar") {
        // Prova não tem "próximo" — SEMPRE volta pro tópico de origem.
        router.push(`/topico/${topicoId}`);
      } else if (d.tipo === "emaus:fullscreen-toggle" && typeof d.ligado === "boolean") {
        // Fallback pra navegadores sem Fullscreen API pra elemento genérico
        // (iOS Safari) — o render pediu via postMessage porque requestFullscreen()
        // não existe/falhou lá dentro. Faz na marra: iframe cobre a viewport
        // toda e a barra "Voltar ao curso" some, sem depender de permissão do
        // navegador.
        const iframe = document.querySelector("iframe");
        const barra = document.getElementById("barra-topo-topico");
        if (d.ligado) {
          if (iframe) {
            iframe.style.position = "fixed";
            iframe.style.inset = "0";
            iframe.style.width = "100vw";
            iframe.style.height = "100dvh";
            iframe.style.zIndex = "9999";
          }
          if (barra) barra.style.display = "none";
        } else {
          if (iframe) {
            iframe.style.position = "";
            iframe.style.inset = "";
            iframe.style.width = "";
            iframe.style.height = "";
            iframe.style.zIndex = "";
          }
          if (barra) barra.style.display = "";
        }
      }
    }
    window.addEventListener("message", aoReceber);
    return () => window.removeEventListener("message", aoReceber);
  }, [enviarResumo, avaliacaoId, topicoId, router]);

  return null;
}