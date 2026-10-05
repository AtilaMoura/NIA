"use client";

import Link from "next/link";
import { Fragment, useState, type ButtonHTMLAttributes, type ReactNode } from "react";
import type { BlocoCaderno, CadernoEstado } from "../../../_lib/api";
import { data } from "../../../_lib/pessoas";
import "./caderno.css";

// Caderno da aula (2026-10-05, protótipo 13-caderno.html). Desenha os blocos que
// a IA devolveu (nunca HTML dela) e alterna com a versão original das notas.

const FUSO = "America/Sao_Paulo";

function hora(iso: string) {
  return new Date(iso).toLocaleTimeString("pt-BR", { timeZone: FUSO, hour: "2-digit", minute: "2-digit" });
}

// **negrito** → <strong>; o resto vira texto puro (React escapa)
function Rico({ texto }: { texto?: string | null }) {
  if (!texto) return null;
  const partes = texto.split(/\*\*(.+?)\*\*/g);
  return (
    <>
      {partes.map((p, i) => (i % 2 === 1 ? <strong key={i}>{p}</strong> : <Fragment key={i}>{p}</Fragment>))}
    </>
  );
}

// Cores do tema do curso → variáveis --c-* (claro, escuro e "automático").
// Só passa valor com cara de cor CSS (o arquivo de temas é nosso, mas não custa).
function estiloCores(cores: CadernoEstado["cores"]): string {
  if (!cores) return "";
  const corOk = (v: string) => /^[#a-zA-Z0-9(),.%\s-]{1,40}$/.test(v);
  const nomes: Record<string, string> = {
    bg: "--c-bg", surface: "--c-surface", surface2: "--c-surface2", border: "--c-border",
    borderSoft: "--c-border-soft", ink: "--c-ink", dim: "--c-dim", faint: "--c-faint",
    accent: "--c-accent", accentSoft: "--c-accent-soft", accent2: "--c-accent2", fix: "--c-fix", fixSoft: "--c-fix-soft",
  };
  const decl = (m: Record<string, string>) =>
    Object.entries(nomes)
      .filter(([k]) => m[k] && corOk(m[k]))
      .map(([k, v]) => `${v}:${m[k]};`)
      .join("");
  return (
    `.cad-tema{${decl(cores.claro)}}` +
    `[data-tm-theme="dark"] .cad-tema{${decl(cores.escuro)}}` +
    `@media (prefers-color-scheme: dark){[data-tm-theme="auto"] .cad-tema{${decl(cores.escuro)}}}`
  );
}

function Bloco({ b, alt }: { b: BlocoCaderno; alt: boolean }) {
  switch (b.tipo) {
    case "nota":
    case "nota_alt":
      return (
        <div className={"cad-nota" + (b.tipo === "nota_alt" || alt ? " alt" : "")}>
          {b.rotulo && <div className="cad-rotulo">{b.rotulo}</div>}
          <Rico texto={b.texto} />
          {b.referencia && <div className="cad-ref">{b.referencia}</div>}
        </div>
      );
    case "correcao":
      return (
        <div className="cad-fix">
          <span className="cad-fix-tag">correção</span>
          {b.era && <div className="cad-fix-era">“{b.era}”</div>}
          <div className="cad-fix-agora">
            <Rico texto={b.agora} />
          </div>
          {b.topico_id && b.slide && (
            <Link className="cad-fix-fonte cad-sem-impressao" href={`/topico/${b.topico_id}?slide=${b.slide}`}>
              ver no slide {b.slide} ▶
            </Link>
          )}
        </div>
      );
    case "passos":
      return (
        <div className="cad-passos">
          {(b.itens ?? []).map((it, i) => (
            <div key={i} className="cad-passo">
              <span className="cad-passo-n">{i + 1}</span>
              <div>
                <b>
                  <Rico texto={it.titulo} />
                </b>
                {it.detalhe && (
                  <span>
                    <Rico texto={it.detalhe} />
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      );
    case "tabela":
      return (
        <div className="cad-tbl">
          <table>
            {(b.colunas ?? []).length > 0 && (
              <thead>
                <tr>
                  {b.colunas!.map((c, i) => (
                    <th key={i}>{c}</th>
                  ))}
                </tr>
              </thead>
            )}
            <tbody>
              {(b.linhas ?? []).map((l, i) => (
                <tr key={i}>
                  {l.map((c, j) => (
                    <td key={j}>
                      <Rico texto={c} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    case "lembrete":
      return <div className="cad-margem">→ {b.texto}</div>;
    default:
      return (
        <p className="cad-p">
          <Rico texto={b.texto} />
        </p>
      );
  }
}

function Botao({ children, forte, ...props }: { children: ReactNode; forte?: boolean } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      {...props}
      className={
        "rounded-full border px-3.5 py-1.5 text-[.82rem] font-semibold disabled:cursor-not-allowed disabled:opacity-60 " +
        (forte
          ? "border-[var(--tm-accent)] bg-[var(--tm-accent)] text-[var(--tm-bg)]"
          : "border-[var(--tm-border)] bg-[var(--tm-surface)] hover:border-[var(--tm-accent)]")
      }
    >
      {children}
    </button>
  );
}

export function Caderno({ estadoInicial, tema }: { estadoInicial: CadernoEstado; tema: string }) {
  const [estado, setEstado] = useState(estadoInicial);
  const [versao, setVersao] = useState<"caderno" | "original">(estadoInicial.caderno ? "caderno" : "original");
  const [gerando, setGerando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const c = estado.caderno;
  const nNotas = estado.anotacoes.length;
  const semCota = estado.geracoes_restantes_hoje <= 0;

  async function organizar() {
    setGerando(true);
    setErro(null);
    setVersao("caderno");
    try {
      const res = await fetch(`/api/caderno/${estado.lesson_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tema }),
      });
      const corpo = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(corpo.erro || "Não deu pra organizar agora.");
      setEstado(corpo as CadernoEstado);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Não deu pra organizar agora.");
      if (!estado.caderno) setVersao("original");
    } finally {
      setGerando(false);
    }
  }

  // Notas originais agrupadas por tópico
  const porTopico: { id: number; titulo: string; notas: CadernoEstado["anotacoes"] }[] = [];
  for (const n of estado.anotacoes) {
    let g = porTopico.find((x) => x.id === n.topico_id);
    if (!g) porTopico.push((g = { id: n.topico_id, titulo: n.topico_titulo, notas: [] }));
    g.notas.push(n);
  }

  return (
    <div className="cad-tema">
      <style>{estiloCores(estado.cores)}</style>

      <div className="mt-3 flex flex-wrap items-end justify-between gap-3.5">
        <div className="min-w-0">
          <p className="m-0 text-[.78rem] font-bold uppercase tracking-[.1em] text-[var(--tm-accent)]">
            {estado.curso} · Módulo {estado.modulo_index} · Aula {estado.aula_index}
          </p>
          <h1 className="m-0 mt-0.5 text-[clamp(1.4rem,4vw,1.75rem)]">{estado.aula}</h1>
        </div>
        {nNotas > 0 && (
          <div role="group" aria-label="Versão" className="cad-sem-impressao inline-flex overflow-hidden rounded-full border border-[var(--tm-border)] bg-[var(--tm-surface)]">
            {(["original", "caderno"] as const).map((v) => (
              <button
                key={v}
                type="button"
                aria-pressed={versao === v}
                onClick={() => setVersao(v)}
                className={
                  "whitespace-nowrap px-3.5 py-1.5 text-[.86rem] " +
                  (versao === v ? "bg-[var(--tm-accent)] font-semibold text-[var(--tm-bg)]" : "text-[var(--tm-ink-muted)]")
                }
              >
                {v === "original" ? "Minhas notas" : "Caderno organizado"}
              </button>
            ))}
          </div>
        )}
      </div>

      {nNotas === 0 ? (
        <section className="mt-4 rounded-[var(--tm-radius-lg)] border border-dashed border-[var(--tm-border)] px-4 py-10 text-center">
          <h2 className="m-0 text-[1.2rem]">Nada anotado nesta aula ainda</h2>
          <p className="m-0 mt-1.5 text-[var(--tm-ink-muted)]">
            Anote nos slides (botão ✍️) e depois volte aqui pra organizar tudo num caderno.
          </p>
        </section>
      ) : (
        <>
          {versao === "caderno" && (
            <div className="cad-sem-impressao mt-3.5 flex flex-wrap items-center gap-x-3.5 gap-y-2 text-[.82rem] text-[var(--tm-ink-muted)]">
              <span>
                {gerando
                  ? "✦ Organizando…"
                  : c?.criado_em
                    ? `✦ Organizado pela IA em ${data(c.criado_em)} às ${hora(c.criado_em)} · a partir de ${c.anotacoes_usadas} ${c.anotacoes_usadas === 1 ? "anotação" : "anotações"} · versão ${c.versao}`
                    : "Ainda não organizado"}
              </span>
              <span className="flex-1" />
              {c && (
                <Botao onClick={organizar} disabled={gerando || semCota}>
                  ↻ Atualizar caderno
                </Botao>
              )}
              {c && <Botao onClick={() => window.print()}>Imprimir / PDF</Botao>}
            </div>
          )}

          {versao === "caderno" && c && estado.novas_desde_caderno > 0 && !gerando && (
            <div className="cad-sem-impressao mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 rounded-[var(--tm-radius)] border border-[color-mix(in_srgb,var(--tm-warn)_45%,transparent)] bg-[color-mix(in_srgb,var(--tm-warn)_8%,transparent)] px-4 py-2.5 text-[.88rem]">
              <span>
                <b className="text-[var(--tm-warn)]">
                  Você anotou {estado.novas_desde_caderno} {estado.novas_desde_caderno === 1 ? "coisa nova" : "coisas novas"}
                </b>{" "}
                depois que este caderno foi organizado.
              </span>
              <Botao forte onClick={organizar} disabled={semCota}>
                ↻ Atualizar caderno
              </Botao>
            </div>
          )}

          {erro && (
            <p role="alert" className="cad-sem-impressao m-0 mt-3 rounded-[var(--tm-radius)] border border-[var(--tm-danger,#a5352b)] px-4 py-2.5 text-[.88rem] text-[var(--tm-danger,#a5352b)]">
              {erro}
            </p>
          )}
          {semCota && versao === "caderno" && (
            <p className="cad-sem-impressao m-0 mt-2 text-[.8rem] text-[var(--tm-ink-muted)]">
              Você já organizou o máximo de cadernos de hoje. Amanhã libera de novo.
            </p>
          )}

          {versao === "caderno" && gerando && (
            <article className="cad-caderno">
              <div className="cad-gerando">
                <div className="cad-pena">organizando o seu caderno…</div>
                <p className="cad-p" style={{ color: "var(--c-dim)" }}>
                  Lendo {nNotas} {nNotas === 1 ? "anotação" : "anotações"} e o conteúdo dos slides. Leva uns 20 segundos.
                </p>
                <div className="cad-linhas">
                  <i />
                  <i />
                  <i />
                </div>
              </div>
            </article>
          )}

          {versao === "caderno" && !gerando && !c && (
            <section className="cad-caderno">
              <div className="cad-gerando">
                <div className="cad-pena">organize suas anotações</div>
                <p className="cad-p" style={{ color: "var(--c-dim)" }}>
                  A IA junta as {nNotas} {nNotas === 1 ? "anotação" : "anotações"} desta aula por assunto, confere com os slides e
                  marca o que precisa de correção. As suas notas originais continuam iguais.
                </p>
                <div className="mt-3">
                  <Botao forte onClick={organizar} disabled={semCota}>
                    ✦ Organizar com a IA
                  </Botao>
                </div>
              </div>
            </section>
          )}

          {versao === "caderno" && !gerando && c && (
            <article className="cad-caderno">
              <div className="cad-folha">
                <div className="cad-data">
                  {c.criado_em ? data(c.criado_em) : ""} — caderno da Aula {estado.aula_index}
                </div>
                <h2 className="cad-titulo">Minhas anotações</h2>
                <p className="cad-sub">{c.conteudo.subtitulo}</p>
                <div className="cad-chips">
                  {estado.topicos.map((t, i) => (
                    <span key={t.id} className={"cad-chip" + (t.concluido ? " ok" : "")} title={t.titulo}>
                      <i />
                      <span>
                        {i + 1} · {t.titulo}
                      </span>
                    </span>
                  ))}
                </div>

                {c.conteudo.secoes.map((s, i) => {
                  let nNota = 0;
                  return (
                    <Fragment key={i}>
                      {i > 0 && <hr className="cad-divisor" />}
                      <section className="cad-secao">
                        <div className="cad-eyebrow">Assunto {i + 1}</div>
                        <h3 className="cad-h2">{s.titulo}</h3>
                        {s.blocos.map((b, j) => {
                          // Alterna as cores dos post-its quando a IA não alternou
                          const alt = b.tipo === "nota" ? nNota++ % 2 === 1 : false;
                          return <Bloco key={j} b={b} alt={alt} />;
                        })}
                      </section>
                    </Fragment>
                  );
                })}

                {c.conteudo.pratica.length > 0 && (
                  <>
                    <hr className="cad-divisor" />
                    <section className="cad-secao">
                      <div className="cad-eyebrow">Pra levar</div>
                      <h3 className="cad-h2">O que eu vou praticar</h3>
                      <ul className="cad-check">
                        {c.conteudo.pratica.map((p, i) => (
                          <li key={i}>
                            <Rico texto={p} />
                          </li>
                        ))}
                      </ul>
                    </section>
                  </>
                )}

                <hr className="cad-divisor" />
                <section className="cad-secao">
                  <div className="cad-eyebrow">Revisão</div>
                  <h3 className="cad-h2">Veredito da aula</h3>
                  <div className="cad-veredito">
                    <span className="cad-carimbo">
                      {c.conteudo.veredito.pontos.length === 0
                        ? "nada pra corrigir"
                        : `${c.conteudo.veredito.pontos.length} ${c.conteudo.veredito.pontos.length === 1 ? "ponto" : "pontos"} pra reforçar`}
                    </span>
                    <p className="cad-p">
                      <Rico texto={c.conteudo.veredito.resumo} />
                    </p>
                    {c.conteudo.veredito.pontos.map((p, i) => (
                      <Fragment key={i}>
                        <h3>{p.titulo}</h3>
                        <ul>
                          <li>
                            <Rico texto={p.detalhe} />
                          </li>
                        </ul>
                      </Fragment>
                    ))}
                  </div>
                </section>
              </div>
              <div className="cad-rodape">
                Organizado pela IA a partir das suas anotações e do conteúdo dos slides. Confira as correções na fonte.
              </div>
            </article>
          )}

          {versao === "original" && (
            <section className="mt-4">
              <p className="m-0 text-[.85rem] text-[var(--tm-ink-muted)]">
                Exatamente como você escreveu — a IA nunca altera esta versão.
              </p>
              {porTopico.map((g) => (
                <div key={g.id} className="mt-3.5 overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
                  <h3 className="m-0 border-b border-[var(--tm-border)] bg-[var(--tm-surface-2)] px-4 py-3 text-[1rem]">{g.titulo}</h3>
                  <div className="divide-y divide-[var(--tm-border)]">
                    {g.notas.map((n) => (
                      <div key={n.slide_index} className="px-4 py-3">
                        <p className="m-0 text-[.78rem] text-[var(--tm-ink-muted)]">
                          <b className="text-[var(--tm-accent)]">Slide {n.slide_index + 1}</b>
                          {n.slide_titulo ? ` · ${n.slide_titulo}` : ""}
                        </p>
                        <p className="m-0 mt-1 whitespace-pre-wrap">{n.texto}</p>
                        <Link
                          href={`/topico/${n.topico_id}?slide=${n.slide_index + 1}`}
                          className="cad-sem-impressao mt-1.5 inline-block text-[.82rem] font-semibold text-[var(--tm-accent)] hover:underline"
                        >
                          Abrir no slide ▶
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </section>
          )}
        </>
      )}
    </div>
  );
}
