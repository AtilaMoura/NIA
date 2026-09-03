"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Button } from "../../components/ui/Button";
import { IMAGEM_DO_HUMOR } from "../_lib/progresso";
import type { CursoComStatus } from "./types";

function notaChip(score: number | null) {
  if (score === null) return "Revisado pela IA";
  return `Nota do Reviewer ${score.toFixed(1)}`;
}

// Carrossel de cursos em destaque — foto vem do pool fixo por humor
// (IMAGEM_DO_HUMOR, provisório — ver comentário lá). Se adapta ao número
// real de "novos" cursos: sem setas/dots quando só tem 1, sem seção nenhuma
// quando não tem nenhum.
export function HeroCarousel({ cursos }: { cursos: CursoComStatus[] }) {
  const [index, setIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const temCarrossel = cursos.length > 1;

  useEffect(() => {
    if (!temCarrossel || paused) return;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;
    const timer = setInterval(() => setIndex((i) => (i + 1) % cursos.length), 6000);
    return () => clearInterval(timer);
  }, [temCarrossel, paused, cursos.length, index]);

  if (cursos.length === 0) return null;
  const atual = cursos[index] ?? cursos[0];

  return (
    <section
      className={`nia-mood-${atual.mood} relative overflow-hidden rounded-[var(--nia-radius-lg)] min-h-[clamp(280px,38vw,480px)] flex items-end`}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <Image
        src={IMAGEM_DO_HUMOR[atual.mood]}
        alt=""
        fill
        priority
        sizes="1180px"
        className="object-cover object-[center_30%]"
      />
      <div
        className="absolute inset-0"
        style={{
          background:
            "linear-gradient(0deg, var(--m-a2) 8%, color-mix(in srgb, var(--m-a2) 65%, transparent) 45%, color-mix(in srgb, var(--m-a2) 15%, transparent) 75%, transparent 100%)",
        }}
      />
      <div
        className="absolute inset-0"
        style={{ background: "linear-gradient(100deg, color-mix(in srgb, var(--m-a2) 55%, transparent) 0%, transparent 55%)" }}
      />

      <div className="relative p-[1.2rem] sm:p-[2.2rem] lg:p-[2.8rem] max-w-[720px]">
        <p
          className="text-[.68rem] sm:text-[.7rem] uppercase tracking-[.16em] m-0 mb-3"
          style={{ fontFamily: "var(--nia-font-display)", color: "color-mix(in srgb, var(--m-ink) 80%, transparent)" }}
        >
          Destaque da semana
        </p>
        <span
          className="inline-flex items-center text-[.72rem] px-[.7rem] py-[.28rem] rounded-[var(--nia-radius-pill)] mb-3"
          style={{
            fontFamily: "var(--nia-font-mono)",
            color: "var(--m-ink)",
            background: "color-mix(in srgb, black 20%, transparent)",
            border: "1px solid color-mix(in srgb, var(--m-ink) 30%, transparent)",
          }}
        >
          {notaChip(atual.course.ai_quality_score)}
        </span>
        <h1
          className="text-[1.5rem] sm:text-[2rem] lg:text-[2.4rem] font-bold leading-[1.15] m-0 mb-3"
          style={{ fontFamily: "var(--nia-font-display)", color: "var(--m-ink)" }}
        >
          {atual.course.title}
        </h1>
        {atual.course.description && (
          <p
            className="text-[.92rem] lg:text-[1rem] leading-[1.6] m-0 mb-5 max-w-[60ch]"
            style={{ color: "color-mix(in srgb, var(--m-ink) 82%, transparent)" }}
          >
            {atual.course.description}
          </p>
        )}
        <div
          className="flex gap-[1.1rem] mb-5 text-[.74rem] uppercase"
          style={{ fontFamily: "var(--nia-font-mono)", color: "color-mix(in srgb, var(--m-ink) 75%, transparent)" }}
        >
          <span>Nível {atual.course.level}</span>
          <span>{atual.course.modules_count} módulos</span>
        </div>
        {atual.linkLicaoId ? (
          <Link href={`/aluno/licoes/${atual.linkLicaoId}`}>
            <Button style={{ background: "var(--m-ink)", color: "var(--m-a)" }}>Começar curso</Button>
          </Link>
        ) : (
          <span
            className="inline-flex items-center text-[.82rem] px-[1.1rem] py-[.6rem] rounded-[var(--nia-radius-pill)]"
            style={{ fontFamily: "var(--nia-font-display)", fontWeight: 700, color: "var(--m-ink)", border: "1px solid color-mix(in srgb, var(--m-ink) 35%, transparent)" }}
          >
            Em preparação
          </span>
        )}
      </div>

      {temCarrossel && (
        <>
          <button
            type="button"
            aria-label="Destaque anterior"
            onClick={() => setIndex((i) => (i - 1 + cursos.length) % cursos.length)}
            className="absolute top-1/2 left-4 -translate-y-1/2 w-[38px] h-[38px] rounded-full flex items-center justify-center text-white text-xl cursor-pointer"
            style={{ background: "rgba(0,0,0,.35)", border: "1px solid rgba(255,255,255,.35)" }}
          >
            ‹
          </button>
          <button
            type="button"
            aria-label="Próximo destaque"
            onClick={() => setIndex((i) => (i + 1) % cursos.length)}
            className="absolute top-1/2 right-4 -translate-y-1/2 w-[38px] h-[38px] rounded-full flex items-center justify-center text-white text-xl cursor-pointer"
            style={{ background: "rgba(0,0,0,.35)", border: "1px solid rgba(255,255,255,.35)" }}
          >
            ›
          </button>
          <div className="absolute bottom-[1.1rem] right-[1.6rem] flex gap-[.4rem]">
            {cursos.map((c, i) => (
              <button
                key={c.course.id}
                type="button"
                aria-label={`Ir pro destaque ${i + 1}`}
                onClick={() => setIndex(i)}
                className="h-[6px] rounded-[var(--nia-radius-pill)] cursor-pointer p-0"
                style={{ width: i === index ? 20 : 6, background: i === index ? "#fff" : "rgba(255,255,255,.45)" }}
              />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
