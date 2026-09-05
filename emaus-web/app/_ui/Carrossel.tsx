"use client";

import { useEffect, useRef, useState } from "react";

export type SlideCarrossel = { src: string; alt: string };

// Carrossel de ilustrações. Rotação automática a cada `intervalo` ms, pausa no
// hover/foco. Respeita prefers-reduced-motion (sem auto, só as bolinhas).
export function Carrossel({
  slides,
  intervalo = 5000,
  className = "",
}: {
  slides: SlideCarrossel[];
  intervalo?: number;
  className?: string;
}) {
  const [i, setI] = useState(0);
  const [pausado, setPausado] = useState(false);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const semMovimento =
      typeof window !== "undefined" &&
      window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (semMovimento || pausado || slides.length < 2) return;
    timer.current = setInterval(() => setI((v) => (v + 1) % slides.length), intervalo);
    return () => {
      if (timer.current) clearInterval(timer.current);
    };
  }, [pausado, slides.length, intervalo]);

  if (slides.length === 0) return null;

  return (
    <div
      className={
        "relative aspect-square overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] " +
        className
      }
      onMouseEnter={() => setPausado(true)}
      onMouseLeave={() => setPausado(false)}
      onFocus={() => setPausado(true)}
      onBlur={() => setPausado(false)}
    >
      {slides.map((s, idx) => (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          key={s.src}
          src={s.src}
          alt={idx === i ? s.alt : ""}
          aria-hidden={idx !== i}
          className={
            "absolute inset-0 h-full w-full object-cover transition-opacity duration-700 " +
            (idx === i ? "opacity-100" : "opacity-0")
          }
        />
      ))}
      {/* véu quente pra casar com o tema e dar profundidade */}
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-tr from-[var(--tm-bg)]/45 via-transparent to-transparent" />

      {slides.length > 1 && (
        <div className="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5">
          {slides.map((s, idx) => (
            <button
              key={s.src}
              type="button"
              aria-label={`Ver ilustração ${idx + 1}`}
              aria-current={idx === i}
              onClick={() => setI(idx)}
              className={
                "h-1.5 rounded-full transition-all " +
                (idx === i ? "w-5 bg-[var(--tm-gold)]" : "w-1.5 bg-white/50 hover:bg-white/80")
              }
            />
          ))}
        </div>
      )}
    </div>
  );
}
