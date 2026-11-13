"use client";

import { useCallback, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { API_URL_PUBLICA } from "../../_lib/config";
import {
  aprovarTopicoRevisao,
  enviarAvaliacaoTutor,
  enviarTopicoParaIA,
  marcarProgresso,
  pontuarSlide,
  reiniciarTopico,
  type RevisaoTopico,
  type StatusTopico,
} from "../../_lib/api";

// Ponte de mensagens entre o <iframe> do render (topico.html.j2) e o Next.js —
// sem UI própria (2026-09-11: antes tinha um painel de resultado + lista de
// anotações fixos embaixo do <iframe>; virou tudo parte do próprio slide
// "Resultado" e um botão flutuante dentro do render). Este componente só
// existe porque o <iframe> não tem o token de sessão real (fica só no
// servidor Next.js — ver docstring de topico_respostas.py): quem chama a API
// do tutor e faz a navegação continua sendo aqui, o resultado só volta pro
// <iframe> via postMessage pra aparecer dentro do slide.
const ORIGEM_RENDER = new URL(API_URL_PUBLICA).origin;

export function AcoesTopico({
  topicoId,
  cursoId,
  estadoInicial,
  proximoTopicoId,
  avaliacaoId,
  revisaoInicial = null,
}: {
  topicoId: number;
  cursoId: number;
  estadoInicial: StatusTopico;
  proximoTopicoId: number | null;
  avaliacaoId: number | null;
  // Só vem preenchido para quem pode revisar este curso (NIA-T-026)
  revisaoInicial?: RevisaoTopico | null;
}) {
  const router = useRouter();
  const revisaoRef = useRef<RevisaoTopico | null>(revisaoInicial);

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

  // Modo revisor (NIA-T-026): o render só mostra "📌 Pontuar" e a caixa "Revisão deste tópico"
  // depois de receber isto. Reenviado a cada carga do <iframe> (idempotente no render).
  const enviarModoRevisor = useCallback(() => {
    const r = revisaoRef.current;
    if (!r) return;
    postParaIframe({
      tipo: "emaus:modo-revisor",
      pontos: r.pontos,
      revisao: {
        status: r.status,
        aprovado_por: r.aprovado_por,
        aprovado_em: r.aprovado_em,
        abertos: r.abertos,
      },
    });
  }, [postParaIframe]);

  const aplicarRevisao = useCallback(
    (r: RevisaoTopico) => {
      revisaoRef.current = r;
      postParaIframe({
        tipo: "emaus:revisao-atualizada",
        pontos: r.pontos,
        revisao: {
          status: r.status,
          aprovado_por: r.aprovado_por,
          aprovado_em: r.aprovado_em,
          abertos: r.abertos,
        },
      });
    },
    [postParaIframe],
  );

  const falhaRevisao = useCallback(
    (e: unknown) => {
      const msg = e instanceof Error ? e.message : "Não foi possível concluir. Tente de novo.";
      postParaIframe({ tipo: "emaus:revisao-erro", mensagem: msg });
    },
    [postParaIframe],
  );

  useEffect(() => {
    if (!revisaoInicial) return;
    const iframe = document.querySelector("iframe");
    if (!iframe) return;
    iframe.addEventListener("load", enviarModoRevisor);
    enviarModoRevisor(); // se o render já carregou antes da hidratação
    return () => iframe.removeEventListener("load", enviarModoRevisor);
  }, [revisaoInicial, enviarModoRevisor]);

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
      // Só aceita mensagem do render do backend (2026-09-27) — antes qualquer janela
      // podia mandar "emaus:concluir"/"emaus:navegar" pra esta página.
      if (e.origin !== ORIGEM_RENDER) return;
      const d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.tipo === "emaus:concluir" && typeof d.texto === "string") {
        enviarResumo(d.texto);
      } else if (d.tipo === "emaus:pronto") {
        enviarModoRevisor();
      } else if (d.tipo === "emaus:ponto" && revisaoRef.current) {
        if (typeof d.slideIndex === "number" && typeof d.texto === "string" && d.texto.trim()) {
          pontuarSlide(topicoId, d.slideIndex, d.texto.trim()).then(aplicarRevisao).catch(falhaRevisao);
        }
      } else if (d.tipo === "emaus:revisao-aprovar" && revisaoRef.current) {
        aprovarTopicoRevisao(topicoId).then(aplicarRevisao).catch(falhaRevisao);
      } else if (d.tipo === "emaus:revisao-enviar-ia" && revisaoRef.current) {
        enviarTopicoParaIA(topicoId).then(aplicarRevisao).catch(falhaRevisao);
      } else if (d.tipo === "emaus:refazer-topico") {
        // "↻ Refazer os exercícios" da revisão (2026-09-24): rodada nova (nada
        // apagado) e recarrega o <iframe> do início, sem os parâmetros de
        // "já concluído" — senão ele remontaria o resultado antigo.
        reiniciarTopico(topicoId)
          .then(() => {
            const iframe = document.querySelector("iframe");
            if (!iframe) return;
            const u = new URL(iframe.src);
            ["concluido", "veredito", "resumo", "proximo"].forEach((k) => u.searchParams.delete(k));
            u.searchParams.set("slide", "1");
            iframe.src = u.toString();
          })
          .catch((e) => console.error("falha ao refazer tópico", e));
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
  }, [
    enviarResumo,
    enviarModoRevisor,
    aplicarRevisao,
    falhaRevisao,
    proximoTopicoId,
    avaliacaoId,
    router,
    topicoId,
    cursoId,
  ]);

  return null;
}
