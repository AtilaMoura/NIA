"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Botao, LinkBotao } from "../../_ui/Botao";
import { Chip } from "../../_ui/Chip";
import { TEOLOGIA_COURSE_IDS } from "../../_lib/config";
import {
  enviarAvaliacaoTutor,
  marcarProgresso,
  type AvaliacaoTutor,
  type StatusTopico,
} from "../../_lib/api";

const CURSO_ID = TEOLOGIA_COURSE_IDS[0];

export function AcoesTopico({
  topicoId,
  estadoInicial,
  proximoTopicoId,
  analiseInicial,
}: {
  topicoId: number;
  estadoInicial: StatusTopico;
  proximoTopicoId: number | null;
  analiseInicial: AvaliacaoTutor | null;
}) {
  const router = useRouter();
  const [concluido, setConcluido] = useState(estadoInicial === "concluido");
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState(false);

  // --- fluxo do Tutor ---
  const [resumo, setResumo] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [avaliacao, setAvaliacao] = useState<AvaliacaoTutor | null>(analiseInicial);
  const [erroTutor, setErroTutor] = useState<string | null>(null);
  const [mostrarManual, setMostrarManual] = useState(false);
  const textoManual = useRef("");

  // Ao abrir: marca em_andamento (só se ainda não começou). Fire-and-forget.
  useEffect(() => {
    if (estadoInicial === "nao_iniciado") {
      marcarProgresso(topicoId, "em_andamento").catch((e) =>
        console.error("falha ao marcar em_andamento", e),
      );
    }
  }, [topicoId, estadoInicial]);

  // O render (iframe) manda o "=== RESUMO ===" pronto quando o aluno chega no
  // último slide. Aceita só o formato esperado — o texto em si é inócuo.
  useEffect(() => {
    function aoReceber(e: MessageEvent) {
      const d = e.data;
      if (d && d.tipo === "emaus:resumo" && typeof d.texto === "string") {
        setResumo(d.texto);
        setMostrarManual(false);
      }
    }
    window.addEventListener("message", aoReceber);
    return () => window.removeEventListener("message", aoReceber);
  }, []);

  // Se o resumo não chegou (render em cache antigo, aluno não terminou os
  // slides), depois de um tempo oferece colar manualmente. O timer reinicia
  // quando `resumo` chega — o cleanup limpa antes de disparar.
  useEffect(() => {
    if (concluido || resumo != null) return;
    const t = setTimeout(() => setMostrarManual(true), 4000);
    return () => clearTimeout(t);
  }, [concluido, resumo]);

  const enviarResumo = useCallback(
    async (texto: string) => {
      const limpo = texto.trim();
      if (!limpo) return;
      setEnviando(true);
      setErroTutor(null);
      try {
        const prog = await enviarAvaliacaoTutor(topicoId, limpo);
        const nova = prog.tutor_analise?.ultima_avaliacao ?? null;
        setAvaliacao(nova);
        if (prog.status === "concluido") {
          setConcluido(true);
          router.refresh();
        }
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        setErroTutor(
          msg.includes("503")
            ? "O tutor está indisponível agora. Você pode marcar como concluído e pedir a avaliação depois."
            : "Não deu pra falar com o tutor. Tente de novo em instantes.",
        );
        console.error("falha ao avaliar tópico", e);
      } finally {
        setEnviando(false);
      }
    },
    [topicoId, router],
  );

  async function marcarConcluido() {
    setSalvando(true);
    setErro(false);
    setConcluido(true); // otimista
    try {
      await marcarProgresso(topicoId, "concluido");
      router.refresh();
    } catch (e) {
      console.error("falha ao concluir tópico", e);
      setConcluido(false);
      setErro(true);
    } finally {
      setSalvando(false);
    }
  }

  const temPainelTutor = resumo != null || mostrarManual || avaliacao != null || enviando;

  return (
    <div className="border-t border-[var(--tm-border)] bg-[var(--tm-bg)]">
      {temPainelTutor && (
        <div className="mx-auto max-w-[var(--tm-maxw)] px-[clamp(1rem,4vw,2rem)] py-3">
          <PainelTutor
            avaliacao={avaliacao}
            enviando={enviando}
            erro={erroTutor}
            temResumo={resumo != null}
            reavaliar={avaliacao != null && avaliacao.veredito === "reforco"}
            onEnviar={() => {
              if (resumo != null) enviarResumo(resumo);
              else if (textoManual.current) enviarResumo(textoManual.current);
            }}
          />
          {resumo == null && mostrarManual && avaliacao == null && (
            <details className="mt-2 text-[.82rem] text-[var(--tm-ink-muted)]">
              <summary className="cursor-pointer">Colar o resumo manualmente</summary>
              <p className="mt-2">
                Vá até o último slide do estudo e copie o “Resumo para colar no chat”. Cole aqui:
              </p>
              <textarea
                onChange={(ev) => (textoManual.current = ev.target.value)}
                rows={4}
                className="mt-1 w-full rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-2 text-[.82rem]"
                placeholder="=== RESUMO — Tópico ..."
              />
            </details>
          )}
        </div>
      )}

      <div className="mx-auto flex max-w-[var(--tm-maxw)] flex-wrap items-center gap-3 px-[clamp(1rem,4vw,2rem)] py-3">
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
    </div>
  );
}

function PainelTutor({
  avaliacao,
  enviando,
  erro,
  temResumo,
  reavaliar,
  onEnviar,
}: {
  avaliacao: AvaliacaoTutor | null;
  enviando: boolean;
  erro: string | null;
  temResumo: boolean;
  reavaliar: boolean;
  onEnviar: () => void;
}) {
  if (avaliacao) {
    const dominado = avaliacao.veredito === "dominado";
    return (
      <div className="flex flex-col gap-2 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3">
        <div className="flex items-center gap-2">
          <Chip tom={dominado ? "bom" : "aviso"}>
            {dominado ? "Tópico dominado" : "Precisa de reforço"}
          </Chip>
          <span className="text-[.78rem] font-semibold text-[var(--tm-ink-muted)]">
            Avaliação do tutor
          </span>
        </div>
        <p className="m-0 text-[.88rem]">{avaliacao.resumo_diagnostico}</p>

        {!dominado && avaliacao.reforco_sugerido?.foco && (
          <p className="m-0 text-[.84rem] text-[var(--tm-ink-muted)]">
            <strong className="text-[var(--tm-ink)]">Foco do reforço:</strong>{" "}
            {avaliacao.reforco_sugerido.foco}
          </p>
        )}

        {!dominado && avaliacao.lacunas?.length > 0 && (
          <ul className="m-0 flex list-none flex-col gap-1 p-0 text-[.82rem] text-[var(--tm-ink-muted)]">
            {avaliacao.lacunas.map((l, i) => (
              <li key={i}>
                <strong className="text-[var(--tm-ink)]">{l.tema}:</strong> {l.evidencia}
              </li>
            ))}
          </ul>
        )}

        {avaliacao.pontos_fortes?.length > 0 && (
          <p className="m-0 text-[.82rem] text-[var(--tm-good)]">
            {avaliacao.pontos_fortes.join(" · ")}
          </p>
        )}

        {reavaliar && (
          <div>
            <Botao tamanho="sm" variante="fantasma" onClick={onEnviar} disabled={enviando}>
              {enviando ? "Avaliando…" : "Reestudei — avaliar de novo"}
            </Botao>
          </div>
        )}
        {erro && <span className="text-[.8rem] text-[var(--tm-danger)]">{erro}</span>}
      </div>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-surface)] p-3">
      <div className="min-w-0 flex-1">
        <p className="m-0 text-[.86rem] font-semibold">Avaliação do tutor</p>
        <p className="m-0 text-[.8rem] text-[var(--tm-ink-muted)]">
          {temResumo
            ? "Seu resumo do estudo está pronto. Envie para o tutor avaliar se você já domina o tópico."
            : "Termine os slides do estudo para gerar o resumo, ou cole o resumo manualmente abaixo."}
        </p>
      </div>
      <Botao tamanho="sm" onClick={onEnviar} disabled={enviando}>
        {enviando ? "Avaliando…" : "Enviar meu resumo"}
      </Botao>
      {erro && (
        <span className="w-full text-[.8rem] text-[var(--tm-danger)]">{erro}</span>
      )}
    </div>
  );
}
