"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Botao } from "../../../_ui/Botao";
import { Chip } from "../../../_ui/Chip";
import {
  criarComentarioSlide,
  resolverComentario,
  salvarChecklist,
  type Clareza,
  type ChecklistTopico,
  type ImagemSugerida,
  type Profundidade,
  type QualidadeGeral,
  type Reacao,
  type TopicoComment,
} from "../../../_lib/api";

type SlideAtual = { indice: number; total: number; secao: string; temImagem: boolean };

export function PainelRevisao({
  topicoId,
  comentariosIniciais,
  checklistsIniciais,
  meuChecklistInicial,
  aprovado,
  reviewedBy,
}: {
  topicoId: number;
  comentariosIniciais: TopicoComment[];
  checklistsIniciais: ChecklistTopico[];
  meuChecklistInicial: ChecklistTopico | null;
  aprovado: boolean;
  reviewedBy: string | null;
}) {
  const router = useRouter();
  const [slideAtual, setSlideAtual] = useState<SlideAtual | null>(null);
  const [comentarios, setComentarios] = useState(comentariosIniciais);

  useEffect(() => {
    function aoReceber(e: MessageEvent) {
      const d = e.data;
      if (d && d.tipo === "emaus:slide") {
        setSlideAtual({ indice: d.indice, total: d.total, secao: d.secao ?? "", temImagem: !!d.temImagem });
      }
    }
    window.addEventListener("message", aoReceber);
    return () => window.removeEventListener("message", aoReceber);
  }, []);

  async function marcarResolvido(id: number, resolvido: boolean) {
    try {
      const atualizado = await resolverComentario(id, resolvido);
      setComentarios((prev) => prev.map((c) => (c.id === id ? atualizado : c)));
    } catch (e) {
      console.error("falha ao resolver comentário", e);
    }
  }

  const doSlideAtual = slideAtual
    ? comentarios.filter((c) => c.slide_index === slideAtual.indice)
    : [];
  const gerais = comentarios.filter((c) => c.slide_index === null);
  const abertos = comentarios.filter((c) => !c.resolvido).length;

  return (
    <aside className="flex w-full flex-col gap-5 overflow-y-auto border-t border-[var(--tm-border)] bg-[var(--tm-surface)] p-4 lg:w-[380px] lg:border-l lg:border-t-0">
      <div>
        <div className="flex items-center gap-2">
          <Chip tom={aprovado ? "bom" : "aviso"}>{aprovado ? "Aprovado" : "Não aprovado"}</Chip>
          {abertos > 0 && (
            <span className="text-[.78rem] text-[var(--tm-warn)]">
              {abertos} comentário{abertos > 1 ? "s" : ""} aberto{abertos > 1 ? "s" : ""}
            </span>
          )}
        </div>
        {reviewedBy && (
          <p className="m-0 mt-1 text-[.76rem] text-[var(--tm-ink-muted)]">
            Última revisão: {reviewedBy}
          </p>
        )}
      </div>

      <FormularioSlide
        topicoId={topicoId}
        slideAtual={slideAtual}
        onCriado={(novo) => setComentarios((prev) => [...prev, novo])}
      />

      {(doSlideAtual.length > 0 || gerais.length > 0) && (
        <div className="flex flex-col gap-2">
          <h3 className="m-0 text-[.78rem] font-semibold uppercase tracking-wide text-[var(--tm-ink-muted)]">
            Anotações
          </h3>
          {slideAtual && doSlideAtual.length > 0 && (
            <ListaComentarios titulo={`Slide ${slideAtual.indice + 1}`} itens={doSlideAtual} onResolver={marcarResolvido} />
          )}
          {gerais.length > 0 && (
            <ListaComentarios titulo="Gerais" itens={gerais} onResolver={marcarResolvido} />
          )}
        </div>
      )}

      <hr className="border-[var(--tm-border)]" />

      <FormularioChecklist
        topicoId={topicoId}
        checklistInicial={meuChecklistInicial}
        totalRevisores={checklistsIniciais.length}
        onSalvo={() => router.refresh()}
      />
    </aside>
  );
}

function ListaComentarios({
  titulo,
  itens,
  onResolver,
}: {
  titulo: string;
  itens: TopicoComment[];
  onResolver: (id: number, resolvido: boolean) => void;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <p className="m-0 text-[.74rem] font-semibold text-[var(--tm-ink-muted)]">{titulo}</p>
      {itens.map((c) => (
        <div
          key={c.id}
          className={
            "flex flex-col gap-1 rounded-[var(--tm-radius)] border p-2 text-[.82rem] " +
            (c.resolvido
              ? "border-[var(--tm-border)] opacity-60"
              : "border-[var(--tm-warn)] bg-[var(--tm-verse-bg)]")
          }
        >
          <div className="flex items-center gap-1.5">
            {c.reacao === "positivo" && <span aria-hidden>👍</span>}
            {c.reacao === "negativo" && <span aria-hidden>👎</span>}
            {c.imagem_sugerida && <Chip tom="info">imagem {c.imagem_sugerida}</Chip>}
            {c.sobre_imagem && <Chip tom="info">sobre a imagem</Chip>}
          </div>
          {c.texto && <p className="m-0">{c.texto}</p>}
          <button
            type="button"
            onClick={() => onResolver(c.id, !c.resolvido)}
            className="self-start text-[.74rem] font-semibold text-[var(--tm-accent)] hover:underline"
          >
            {c.resolvido ? "Reabrir" : "Marcar resolvido"}
          </button>
        </div>
      ))}
    </div>
  );
}

function FormularioSlide({
  topicoId,
  slideAtual,
  onCriado,
}: {
  topicoId: number;
  slideAtual: SlideAtual | null;
  onCriado: (c: TopicoComment) => void;
}) {
  const [reacao, setReacao] = useState<Reacao | null>(null);
  const [texto, setTexto] = useState("");
  const [imagemSugerida, setImagemSugerida] = useState<ImagemSugerida | null>(null);
  const [sobreImagem, setSobreImagem] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  async function enviar() {
    if (!reacao && !texto.trim() && !imagemSugerida) return;
    setEnviando(true);
    setErro(null);
    try {
      const novo = await criarComentarioSlide({
        topicoId,
        slideIndex: slideAtual?.indice ?? null,
        reacao,
        imagemSugerida,
        sobreImagem,
        texto: texto.trim() || null,
      });
      onCriado(novo);
      setReacao(null);
      setTexto("");
      setImagemSugerida(null);
      setSobreImagem(false);
    } catch (e) {
      console.error("falha ao criar comentário", e);
      setErro("Não deu pra salvar. Tente de novo.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="flex flex-col gap-2.5 rounded-[var(--tm-radius)] border border-[var(--tm-border)] p-3">
      <p className="m-0 text-[.8rem] font-semibold">
        {slideAtual
          ? `Slide ${slideAtual.indice + 1} de ${slideAtual.total}${slideAtual.secao ? ` — ${slideAtual.secao}` : ""}`
          : "Comentário geral do tópico"}
      </p>

      <div className="flex items-center gap-2">
        <button
          type="button"
          aria-pressed={reacao === "positivo"}
          onClick={() => setReacao(reacao === "positivo" ? null : "positivo")}
          className={
            "rounded-[var(--tm-radius-pill)] border px-2.5 py-1 text-[.9rem] " +
            (reacao === "positivo"
              ? "border-[var(--tm-good)] bg-[var(--tm-verse-bg)]"
              : "border-[var(--tm-border)]")
          }
        >
          👍
        </button>
        <button
          type="button"
          aria-pressed={reacao === "negativo"}
          onClick={() => setReacao(reacao === "negativo" ? null : "negativo")}
          className={
            "rounded-[var(--tm-radius-pill)] border px-2.5 py-1 text-[.9rem] " +
            (reacao === "negativo"
              ? "border-[var(--tm-danger)] bg-[var(--tm-verse-bg)]"
              : "border-[var(--tm-border)]")
          }
        >
          👎
        </button>
      </div>

      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        rows={2}
        placeholder="Observação sobre este slide…"
        className="w-full rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-bg)] p-2 text-[.82rem]"
      />

      <div className="flex flex-wrap items-center gap-3 text-[.78rem]">
        <label className="flex items-center gap-1.5">
          <input
            type="radio"
            name={`img-${slideAtual?.indice ?? "geral"}`}
            checked={imagemSugerida === "antes"}
            onChange={() => setImagemSugerida("antes")}
          />
          imagem antes
        </label>
        <label className="flex items-center gap-1.5">
          <input
            type="radio"
            name={`img-${slideAtual?.indice ?? "geral"}`}
            checked={imagemSugerida === "depois"}
            onChange={() => setImagemSugerida("depois")}
          />
          imagem depois
        </label>
        {imagemSugerida && (
          <button
            type="button"
            onClick={() => setImagemSugerida(null)}
            className="text-[var(--tm-ink-muted)] hover:underline"
          >
            limpar
          </button>
        )}
      </div>

      {slideAtual?.temImagem && (
        <label className="flex items-center gap-1.5 text-[.78rem]">
          <input type="checkbox" checked={sobreImagem} onChange={(e) => setSobreImagem(e.target.checked)} />
          Este comentário é sobre a imagem do slide
        </label>
      )}

      <Botao tamanho="sm" onClick={enviar} disabled={enviando} className="self-start">
        {enviando ? "Salvando…" : "Salvar anotação"}
      </Botao>
      {erro && <span className="text-[.78rem] text-[var(--tm-danger)]">{erro}</span>}
    </div>
  );
}

const OPCOES_PROFUNDIDADE: { valor: Profundidade; rotulo: string }[] = [
  { valor: "raso", rotulo: "Raso" },
  { valor: "adequado", rotulo: "Adequado" },
  { valor: "aprofundado", rotulo: "Aprofundado" },
];
const OPCOES_CLAREZA: { valor: Clareza; rotulo: string }[] = [
  { valor: "confuso", rotulo: "Confuso" },
  { valor: "parcialmente_claro", rotulo: "Parcialmente claro" },
  { valor: "claro", rotulo: "Claro" },
];
const OPCOES_QUALIDADE: { valor: QualidadeGeral; rotulo: string }[] = [
  { valor: "fraca", rotulo: "Fraca" },
  { valor: "regular", rotulo: "Regular" },
  { valor: "boa", rotulo: "Boa" },
  { valor: "excelente", rotulo: "Excelente" },
];

function FormularioChecklist({
  topicoId,
  checklistInicial,
  totalRevisores,
  onSalvo,
}: {
  topicoId: number;
  checklistInicial: ChecklistTopico | null;
  totalRevisores: number;
  onSalvo: () => void;
}) {
  const [profundidade, setProfundidade] = useState<Profundidade | "">(checklistInicial?.profundidade ?? "");
  const [clareza, setClareza] = useState<Clareza | "">(checklistInicial?.clareza ?? "");
  const [qualidadeGeral, setQualidadeGeral] = useState<QualidadeGeral | "">(
    checklistInicial?.qualidade_geral ?? "",
  );
  const [observacaoFinal, setObservacaoFinal] = useState(checklistInicial?.observacao_final ?? "");
  const [aprovado, setAprovado] = useState<boolean | null>(checklistInicial?.aprovado ?? null);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [ultimoSalvo, setUltimoSalvo] = useState(checklistInicial);

  async function salvar() {
    if (!profundidade || !clareza || !qualidadeGeral || aprovado === null) {
      setErro("Responda as 3 perguntas e escolha aprovar ou reprovar.");
      return;
    }
    setSalvando(true);
    setErro(null);
    try {
      const salvo = await salvarChecklist({
        topicoId,
        profundidade,
        clareza,
        qualidadeGeral,
        observacaoFinal: observacaoFinal.trim() || null,
        aprovado,
      });
      setUltimoSalvo(salvo);
      onSalvo();
    } catch (e) {
      console.error("falha ao salvar checklist", e);
      setErro("Não deu pra salvar. Tente de novo.");
    } finally {
      setSalvando(false);
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <h3 className="m-0 text-[.9rem] font-semibold">Checklist final</h3>
      <p className="m-0 text-[.76rem] text-[var(--tm-ink-muted)]">
        {totalRevisores > 0
          ? `${totalRevisores} revisor${totalRevisores > 1 ? "es" : ""} já avaliou este tópico.`
          : "Você seria o primeiro a avaliar este tópico."}
      </p>

      <Selecao rotulo="Profundidade do conteúdo" valor={profundidade} onChange={setProfundidade} opcoes={OPCOES_PROFUNDIDADE} />
      <Selecao rotulo="Clareza" valor={clareza} onChange={setClareza} opcoes={OPCOES_CLAREZA} />
      <Selecao rotulo="Qualidade geral" valor={qualidadeGeral} onChange={setQualidadeGeral} opcoes={OPCOES_QUALIDADE} />

      <label className="flex flex-col gap-1 text-[.78rem] font-semibold">
        Observação final (opcional)
        <textarea
          value={observacaoFinal}
          onChange={(e) => setObservacaoFinal(e.target.value)}
          rows={2}
          className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-bg)] p-2 text-[.82rem] font-normal"
        />
      </label>

      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => setAprovado(true)}
          className={
            "flex-1 rounded-[var(--tm-radius)] border px-3 py-1.5 text-[.82rem] font-semibold " +
            (aprovado === true
              ? "border-[var(--tm-good)] bg-[var(--tm-verse-bg)] text-[var(--tm-good)]"
              : "border-[var(--tm-border)]")
          }
        >
          ✓ Aprovar
        </button>
        <button
          type="button"
          onClick={() => setAprovado(false)}
          className={
            "flex-1 rounded-[var(--tm-radius)] border px-3 py-1.5 text-[.82rem] font-semibold " +
            (aprovado === false
              ? "border-[var(--tm-danger)] bg-[var(--tm-verse-bg)] text-[var(--tm-danger)]"
              : "border-[var(--tm-border)]")
          }
        >
          ✕ Reprovar
        </button>
      </div>

      <Botao tamanho="sm" onClick={salvar} disabled={salvando}>
        {salvando ? "Salvando…" : ultimoSalvo ? "Atualizar avaliação" : "Enviar avaliação"}
      </Botao>
      {erro && <span className="text-[.78rem] text-[var(--tm-danger)]">{erro}</span>}
      {ultimoSalvo && !erro && (
        <span className="text-[.78rem] text-[var(--tm-ink-muted)]">
          Sua avaliação: {ultimoSalvo.aprovado ? "aprovado ✓" : "reprovado ✕"} (
          {new Date(ultimoSalvo.updated_at ?? Date.now()).toLocaleString("pt-BR")})
        </span>
      )}
    </div>
  );
}

function Selecao<T extends string>({
  rotulo,
  valor,
  onChange,
  opcoes,
}: {
  rotulo: string;
  valor: T | "";
  onChange: (v: T) => void;
  opcoes: { valor: T; rotulo: string }[];
}) {
  return (
    <label className="flex flex-col gap-1 text-[.78rem] font-semibold">
      {rotulo}
      <select
        value={valor}
        onChange={(e) => onChange(e.target.value as T)}
        className="rounded-[var(--tm-radius)] border border-[var(--tm-border)] bg-[var(--tm-bg)] p-2 text-[.82rem] font-normal"
      >
        <option value="" disabled>
          Escolher…
        </option>
        {opcoes.map((o) => (
          <option key={o.valor} value={o.valor}>
            {o.rotulo}
          </option>
        ))}
      </select>
    </label>
  );
}
