import Image from "next/image";
import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { HeroCarousel } from "./HeroCarousel";
import { IMAGEM_DO_HUMOR } from "../_lib/progresso";
import type { CursoComStatus, LayoutProps } from "./types";

function notaChip(score: number | null) {
  if (score === null) return "Revisado pela IA";
  return `Nota do Reviewer ${score.toFixed(1)}`;
}

function PosterCard({ curso, mostrarContinuar, tutorDominado }: { curso: CursoComStatus; mostrarContinuar?: boolean; tutorDominado?: boolean }) {
  const { course, percent, status, linkLicaoId, mood } = curso;
  const conteudoPoster = (
    <div className={`nia-mood-${mood} relative h-[128px] flex items-end p-[.7rem_.8rem] rounded-t-[var(--nia-radius-md)] overflow-hidden`}>
      <Image src={IMAGEM_DO_HUMOR[mood]} alt="" fill sizes="230px" className="object-cover" />
      <div
        className="absolute inset-0"
        style={{ background: "linear-gradient(0deg, color-mix(in srgb, var(--m-a2) 88%, transparent) 0%, color-mix(in srgb, var(--m-a2) 15%, transparent) 55%, transparent 80%)" }}
      />
      <span
        className="absolute top-[.55rem] right-[.6rem] text-[.62rem] px-[.5rem] py-[.15rem] rounded-[var(--nia-radius-pill)]"
        style={{ fontFamily: "var(--nia-font-mono)", color: "var(--m-ink)", background: "color-mix(in srgb, black 22%, transparent)" }}
      >
        {notaChip(course.ai_quality_score)}
      </span>
      {status === "completed" && (
        <span
          className="absolute top-[.55rem] left-[.6rem] text-[.58rem] uppercase tracking-[.05em] font-bold px-[.55rem] py-[.2rem] rounded-[var(--nia-radius-pill)]"
          style={{ fontFamily: "var(--nia-font-display)", color: "var(--m-ink)", background: "color-mix(in srgb, black 22%, transparent)" }}
        >
          Concluído
        </span>
      )}
      <h4
        className="relative text-[.86rem] font-bold leading-[1.25] m-0"
        style={{ fontFamily: "var(--nia-font-display)", color: "var(--m-ink)" }}
      >
        {course.title}
      </h4>
      {status === "in_progress" && (
        <div className="absolute left-0 right-0 bottom-0 h-[4px]" style={{ background: "color-mix(in srgb, black 25%, transparent)" }}>
          <div className="h-full" style={{ width: `${percent}%`, background: "var(--m-ink)" }} />
        </div>
      )}
    </div>
  );

  const rodape = (
    <div className="p-[.7rem_.85rem_.85rem] flex flex-col gap-[.35rem]">
      {status === "in_progress" ? (
        <>
          <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
            {percent}% concluído
          </p>
          <div className="flex items-center gap-[.5rem]">
            <div className="flex-1 h-[5px] rounded-[var(--nia-radius-pill)] overflow-hidden" style={{ background: "var(--nia-surface2)", border: "1px solid var(--nia-border)" }}>
              <div className="h-full" style={{ width: `${percent}%`, background: "var(--nia-accent)" }} />
            </div>
          </div>
          <span className="text-[.74rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
            {mostrarContinuar ? "Continuar →" : "Ver curso →"}
          </span>
          {tutorDominado && (
            <span className="text-[.68rem] flex items-center gap-1" style={{ color: "var(--nia-good)" }}>
              ✓ Tópico anterior dominado
            </span>
          )}
        </>
      ) : status === "completed" ? (
        <>
          <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
            {course.modules_count} módulos
          </p>
          <span className="text-[.74rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
            Rever conteúdo →
          </span>
        </>
      ) : (
        <>
          <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
            {course.modules_count} módulos
          </p>
          <span className="text-[.74rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
            {linkLicaoId ? "Começar →" : "Em preparação"}
          </span>
        </>
      )}
    </div>
  );

  const card = (
    <article
      className="shrink-0 w-[230px] rounded-[var(--nia-radius-md)] overflow-hidden transition-transform hover:-translate-y-[3px]"
      style={{ background: "var(--nia-surface)", border: "1px solid var(--nia-border)" }}
    >
      {conteudoPoster}
      {rodape}
    </article>
  );

  return linkLicaoId ? <Link href={`/aluno/licoes/${linkLicaoId}`}>{card}</Link> : card;
}

function Row({
  titulo,
  hint,
  cursos,
  idAtual,
  tutorDominadoIdAtual,
}: {
  titulo: string;
  hint: string;
  cursos: CursoComStatus[];
  idAtual?: number;
  tutorDominadoIdAtual?: boolean;
}) {
  if (cursos.length === 0) return null;
  return (
    <section>
      <div className="flex items-baseline justify-between gap-4 mb-[.9rem]">
        <h2 className="m-0 text-[1rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}>
          {titulo}
        </h2>
        <span className="text-[.76rem]" style={{ color: "var(--nia-ink-muted)" }}>
          {hint}
        </span>
      </div>
      <div className="flex gap-[.9rem] overflow-x-auto pb-1">
        {cursos.map((c) => (
          <PosterCard
            key={c.course.id}
            curso={c}
            mostrarContinuar={c.course.id === idAtual}
            tutorDominado={c.course.id === idAtual && tutorDominadoIdAtual}
          />
        ))}
      </div>
    </section>
  );
}

// Layout padrão de fábrica — fileiras estilo streaming, definidas em mockup
// (Artifact) antes de portar. Ver PROMPT_UX_ALUNO.md pro contexto da mudança.
export function RetomarLayout({ avatarInitials, avatarTitle, hero, cursos, cursosDestaque, nivel, pontos, streak }: LayoutProps) {
  const emAndamento = cursos.filter((c) => c.status === "in_progress");
  const dominados = cursos.filter((c) => c.status === "completed");

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials={avatarInitials} avatarTitle={avatarTitle}>
        <div
          className="hidden md:flex items-baseline gap-[.65rem] text-[.78rem]"
          style={{ fontFamily: "var(--nia-font-mono)", color: "var(--nia-ink-muted)" }}
        >
          <span>
            Nível <b style={{ color: "var(--nia-ink)" }}>{nivel}</b>
          </span>
          <span className="w-[3px] h-[3px] rounded-full" style={{ background: "var(--nia-border)" }} />
          <span>
            <b style={{ color: "var(--nia-ink)" }}>{pontos}</b> pts
          </span>
          <span className="w-[3px] h-[3px] rounded-full" style={{ background: "var(--nia-border)" }} />
          <span>
            <b style={{ color: "var(--nia-ink)" }}>{streak}</b> {streak === 1 ? "dia seguido" : "dias seguidos"}
          </span>
        </div>
        <Link href="/aluno/explorar" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Explorar
        </Link>
        <Link href="/aluno/progresso" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Progresso
        </Link>
        <Link href="/aluno/perfil" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Perfil
        </Link>
        <Link href="/aluno/preferencias" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Preferências
        </Link>
      </AppTopbar>

      <div className="py-[1.6rem] px-[clamp(1rem,4vw,3rem)] flex flex-col gap-[2rem] max-w-[1800px] mx-auto">
        <HeroCarousel cursos={cursosDestaque} />

        <Row
          titulo="Continuar estudando"
          hint={`${emAndamento.length} em andamento`}
          cursos={emAndamento}
          idAtual={hero?.curso.id}
          tutorDominadoIdAtual={hero?.ultimaAvaliacaoDominada}
        />

        <Row titulo="Já dominado — revisar quando quiser" hint={`${dominados.length} concluído(s)`} cursos={dominados} />

        <Row titulo="Todos os cursos" hint={`${cursos.length} no catálogo`} cursos={cursos} />

        <p className="text-[.68rem] leading-[1.7] pt-4 border-t" style={{ color: "var(--nia-ink-dim, var(--nia-ink-muted))", borderColor: "var(--nia-border)" }}>
          Imagens: Wikimedia Commons —{" "}
          <a className="underline" href="https://commons.wikimedia.org/wiki/File:Human_brain_blue_circuit_white_background_artificial_intelligence_icon_(DALL-_E)_Dec_2024.jpg" target="_blank" rel="noopener noreferrer">AI circuit icon</a> (domínio público),{" "}
          <a className="underline" href="https://commons.wikimedia.org/wiki/File:Internet_Online_Marketing_(27905885880).jpg" target="_blank" rel="noopener noreferrer">Internet Online Marketing</a> (Michael Coghlan, CC BY 2.0),{" "}
          <a className="underline" href="https://commons.wikimedia.org/wiki/File:(Photography_equipment_Tripod_Photo_Camera_Tripod_photograph_in_a_studio).jpg" target="_blank" rel="noopener noreferrer">Photography equipment</a> (CC BY-SA 4.0),{" "}
          <a className="underline" href="https://commons.wikimedia.org/wiki/File:Forest_path_through_a_deciduous_forest_in_spring,_Finland.jpg" target="_blank" rel="noopener noreferrer">Forest path, Finland</a> (CC BY-SA 4.0),{" "}
          <a className="underline" href="https://commons.wikimedia.org/wiki/File:Books_in_a_stack_(a_stack_of_books)_-_Flickr_-_austinevan.jpg" target="_blank" rel="noopener noreferrer">Books in a stack</a> (Evan Bench, CC BY 2.0). Fotos genéricas por humor, não representam o conteúdo real de cada curso.
        </p>
      </div>
    </div>
  );
}
