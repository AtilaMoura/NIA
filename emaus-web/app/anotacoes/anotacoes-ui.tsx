"use client";

import Link from "next/link";
import { Fragment, useMemo, useState } from "react";
import type { AnotacaoMinha } from "../_lib/api";
import { data } from "../_lib/pessoas";

// Busca + filtro por curso + agrupamento curso → tópico (tudo no navegador: são
// poucas anotações por pessoa). Nota salva do tira-dúvida do tutor começa com
// "❓" (ver salvarDuvidaComoAnotacao no render) e ganha o selo "Dúvida".

type GrupoTopico = { topicoId: number; titulo: string; modulo: string; notas: AnotacaoMinha[] };
type GrupoAula = { lessonId: number; titulo: string; modulo: string; topicos: GrupoTopico[] };
type GrupoCurso = { courseId: number; curso: string; aulas: GrupoAula[] };

// Curso → aula → tópico (a aula é a unidade do "Caderno da aula", 2026-10-05)
function agrupar(lista: AnotacaoMinha[]): GrupoCurso[] {
  const cursos: GrupoCurso[] = [];
  for (const a of lista) {
    let c = cursos.find((x) => x.courseId === a.course_id);
    if (!c) cursos.push((c = { courseId: a.course_id, curso: a.curso, aulas: [] }));
    let au = c.aulas.find((x) => x.lessonId === a.lesson_id);
    if (!au) c.aulas.push((au = { lessonId: a.lesson_id, titulo: a.aula_titulo, modulo: a.modulo_titulo, topicos: [] }));
    let t = au.topicos.find((x) => x.topicoId === a.topico_id);
    if (!t) au.topicos.push((t = { topicoId: a.topico_id, titulo: a.topico_titulo, modulo: a.modulo_titulo, notas: [] }));
    t.notas.push(a);
  }
  return cursos;
}

function normalizar(s: string) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

// Realça o termo buscado (ignorando acento e maiúscula) sem mexer no texto
function Realce({ texto, termo }: { texto: string; termo: string }) {
  if (!termo) return <>{texto}</>;
  const alvo = normalizar(texto);
  const t = normalizar(termo);
  const partes: { s: string; marca: boolean }[] = [];
  let i = 0;
  for (let achou = alvo.indexOf(t); achou !== -1; achou = alvo.indexOf(t, i)) {
    if (achou > i) partes.push({ s: texto.slice(i, achou), marca: false });
    partes.push({ s: texto.slice(achou, achou + t.length), marca: true });
    i = achou + t.length;
  }
  if (i < texto.length) partes.push({ s: texto.slice(i), marca: false });
  return (
    <>
      {partes.map((p, k) =>
        p.marca ? (
          <mark key={k} className="rounded-[3px] bg-[color-mix(in_srgb,var(--tm-verse-border)_45%,transparent)] px-0.5 text-inherit">
            {p.s}
          </mark>
        ) : (
          <Fragment key={k}>{p.s}</Fragment>
        ),
      )}
    </>
  );
}

function CopiarTopico({ notas }: { notas: AnotacaoMinha[] }) {
  const [copiado, setCopiado] = useState(false);
  async function copiar() {
    const texto = [
      notas[0].topico_titulo,
      "",
      ...notas.map((n) => `Slide ${n.slide_index + 1}${n.slide_titulo ? ` — ${n.slide_titulo}` : ""}\n${n.texto}`),
    ].join("\n\n");
    try {
      await navigator.clipboard.writeText(texto);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 2500);
    } catch {
      setCopiado(false);
    }
  }
  return (
    <button
      type="button"
      onClick={copiar}
      className="rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-1.5 text-[.82rem] font-semibold"
    >
      {copiado ? "✓ Copiado" : `Copiar ${notas.length === 1 ? "a anotação" : `as ${notas.length} anotações`}`}
    </button>
  );
}

function Nota({ n, termo, comTopico }: { n: AnotacaoMinha; termo: string; comTopico: boolean }) {
  const duvida = n.texto.includes("❓");
  return (
    <div className="grid gap-1.5 px-4 py-3.5">
      <p className="m-0 flex flex-wrap items-center gap-x-2.5 gap-y-1 text-[.78rem] text-[var(--tm-ink-muted)]">
        <b className="font-bold text-[var(--tm-accent)]">
          {comTopico ? `${n.topico_titulo} · ` : ""}Slide {n.slide_index + 1}
        </b>
        {n.slide_titulo && <span>{n.slide_titulo}</span>}
        {duvida && (
          <span className="rounded-full border border-[var(--tm-verse-border)] bg-[var(--tm-verse-bg)] px-2 text-[.68rem] font-bold text-[var(--tm-accent)]">
            Dúvida
          </span>
        )}
      </p>
      <p className="m-0 whitespace-pre-wrap text-[.95rem]">
        <Realce texto={n.texto} termo={termo} />
      </p>
      <p className="m-0 flex gap-4 text-[.82rem] font-semibold">
        <Link href={`/topico/${n.topico_id}?slide=${n.slide_index + 1}`} className="text-[var(--tm-accent)] hover:underline">
          Abrir no slide ▶
        </Link>
      </p>
    </div>
  );
}

export function ListaAnotacoes({ anotacoes }: { anotacoes: AnotacaoMinha[] }) {
  const [busca, setBusca] = useState("");
  const [curso, setCurso] = useState<number | "todos">("todos");

  const cursosDisponiveis = useMemo(() => agrupar(anotacoes).map((c) => ({ id: c.courseId, nome: c.curso })), [anotacoes]);
  const termo = busca.trim();

  const filtradas = useMemo(() => {
    const t = normalizar(termo);
    return anotacoes.filter(
      (a) =>
        (curso === "todos" || a.course_id === curso) &&
        (!t || normalizar(`${a.texto} ${a.slide_titulo ?? ""} ${a.topico_titulo}`).includes(t)),
    );
  }, [anotacoes, curso, termo]);

  if (anotacoes.length === 0) {
    return (
      <section className="mt-6 rounded-[var(--tm-radius-lg)] border border-dashed border-[var(--tm-border)] px-4 py-10 text-center">
        <h2 className="m-0 text-[1.2rem]">Você ainda não fez anotações</h2>
        <p className="m-0 mt-1.5 text-[var(--tm-ink-muted)]">
          Durante o tópico, use o botão ✍️ em qualquer slide. Tudo o que você anotar aparece aqui.
        </p>
      </section>
    );
  }

  const grupos = agrupar(filtradas);
  const nTopicos = grupos.reduce((s, c) => s + c.aulas.reduce((x, a) => x + a.topicos.length, 0), 0);

  return (
    <>
      <div className="mt-4 flex flex-wrap gap-2.5">
        <input
          type="search"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          placeholder="Buscar nas anotações"
          aria-label="Buscar nas anotações"
          className="min-w-[200px] flex-1 rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3.5 py-2"
        />
        {cursosDisponiveis.length > 1 && (
          <select
            value={curso}
            onChange={(e) => setCurso(e.target.value === "todos" ? "todos" : Number(e.target.value))}
            aria-label="Curso"
            className="max-w-full rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)] px-3 py-2 text-[.88rem]"
          >
            <option value="todos">Todos os cursos</option>
            {cursosDisponiveis.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nome}
              </option>
            ))}
          </select>
        )}
      </div>
      <p className="m-0 mt-2.5 text-[.82rem] text-[var(--tm-ink-muted)]">
        {termo
          ? `${filtradas.length} ${filtradas.length === 1 ? "anotação encontrada" : "anotações encontradas"}`
          : `${filtradas.length} ${filtradas.length === 1 ? "anotação" : "anotações"} em ${nTopicos} ${nTopicos === 1 ? "tópico" : "tópicos"}`}
      </p>

      {grupos.length === 0 && (
        <p className="mt-6 text-center text-[.9rem] text-[var(--tm-ink-muted)]">Nada encontrado com “{termo}”.</p>
      )}

      {grupos.map((c) => (
        <section key={c.courseId} className="mt-6">
          <h2 className="m-0 text-[1.15rem]">{c.curso}</h2>

          {termo ? (
            // Buscando: lista direta das notas que bateram, com o tópico no rótulo
            <div className="mt-3 divide-y divide-[var(--tm-border)] overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
              {c.aulas.flatMap((a) => a.topicos).flatMap((t) => t.notas).map((n) => (
                <Nota key={`${n.topico_id}-${n.slide_index}`} n={n} termo={termo} comTopico />
              ))}
            </div>
          ) : (
            c.aulas.map((au, ai) => (
              <div key={au.lessonId} className="mt-4">
                <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1.5">
                  <p className="m-0 text-[.8rem] font-bold uppercase tracking-[.08em] text-[var(--tm-ink-muted)]">
                    {au.modulo} · {au.titulo}
                  </p>
                  <Link
                    href={`/anotacoes/aula/${au.lessonId}`}
                    className="rounded-full border border-[var(--tm-accent)] px-3 py-1 text-[.8rem] font-semibold text-[var(--tm-accent)] hover:bg-[var(--tm-accent)] hover:text-[var(--tm-bg)]"
                  >
                    📓 Caderno da aula
                  </Link>
                </div>
                {au.topicos.map((t, i) => {
                  const ultima = t.notas.map((n) => n.atualizado_em ?? "").sort().at(-1);
                  return (
                    <details
                      key={t.topicoId}
                      open={i === 0 && ai === 0 && c === grupos[0]}
                      className="group mt-3 overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]"
                    >
                      <summary className="flex cursor-pointer list-none items-center gap-3 px-4 py-3.5 [&::-webkit-details-marker]:hidden">
                        <span className="min-w-0 flex-1">
                          <b className="block font-semibold">{t.titulo}</b>
                          <small className="text-[.78rem] text-[var(--tm-ink-muted)]">
                            {t.notas.length} {t.notas.length === 1 ? "anotação" : "anotações"}
                            {ultima ? ` · última em ${data(ultima)}` : ""}
                          </small>
                        </span>
                        <span aria-hidden className="text-[var(--tm-ink-muted)] transition-transform group-open:rotate-90">
                          ›
                        </span>
                      </summary>
                      <div className="divide-y divide-[var(--tm-border)] border-t border-[var(--tm-border)]">
                        {t.notas.map((n) => (
                          <Nota key={n.slide_index} n={n} termo="" comTopico={false} />
                        ))}
                      </div>
                      <div className="flex justify-end border-t border-[var(--tm-border)] bg-[var(--tm-surface-2)] px-4 py-2.5">
                        <CopiarTopico notas={t.notas} />
                      </div>
                    </details>
                  );
                })}
              </div>
            ))
          )}
        </section>
      ))}
    </>
  );
}
