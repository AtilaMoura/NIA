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
  avaliacaoId,
}: {
  topicoId: number;
  cursoId: number;
  estadoInicial: StatusTopico;
  proximoTopicoId: number | null;
  avaliacaoId: number | null;
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
          temAvaliacao: avaliacaoId != null,
        });
        // SEM router.refresh() (achado real 2026-09-23, Tópico 19 em produção):
        // o refresh gera token de resposta novo → muda o src do <iframe> → ele
        // recarrega e o resultado some (com "reforco" voltava pro "Clique em
        // Fim"). Mesmo bug/correção da prova (prova-ui.tsx). Próximo tópico,
        // prova e árvore do curso já carregam frescos no router.push.
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
    [topicoId, proximoTopicoId, avaliacaoId, postParaIframe],
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
        marcarProgresso(topicoId, "concluido")
          .catch((e) => console.error("falha ao concluir tópico (fallback)", e));
      } else if (d.tipo === "emaus:navegar") {
        if (d.destino === "prova" && avaliacaoId != null) {
          router.push(`/topico/${topicoId}/prova`);
        } else if (d.destino === "proximo" && proximoTopicoId != null) {
          router.push(`/topico/${proximoTopicoId}`);
        } else {
          router.push(`/curso/${cursoId}`);
        }
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
  }, [enviarResumo, proximoTopicoId, avaliacaoId, router, topicoId, cursoId]);

  return null;
}
