import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { Button } from "../../components/ui/Button";
import type { LayoutProps, TrilhaItem } from "./types";

const DOT_LABEL: Record<TrilhaItem["situacao"], string> = {
  done: "✔",
  current: "",
  proximo: "",
  preparando: "",
  bloqueado: "🔒",
};

function corDoDot(situacao: TrilhaItem["situacao"]) {
  if (situacao === "done") return { background: "color-mix(in srgb, var(--nia-good) 20%, var(--nia-surface))", borderColor: "var(--nia-good)", color: "var(--nia-good)" };
  if (situacao === "current") return { background: "var(--nia-accent)", borderColor: "var(--nia-accent)", color: "var(--nia-accent-ink)" };
  return { background: "var(--nia-surface)", borderColor: "var(--nia-border)", color: "var(--nia-ink-muted)" };
}

function legendaSituacao(item: TrilhaItem, index: number) {
  if (item.situacao === "done") return "Concluído";
  if (item.situacao === "current") return "Em andamento";
  if (item.situacao === "preparando") return "Em preparação pelo admin";
  if (item.situacao === "proximo") return "A seguir";
  return "Bloqueado";
}

// Layout alternativo (escolhido em /aluno/preferencias): caminho vertical do curso atual.
export function TrilhaLayout({ avatarInitials, avatarTitle, hero, cursos, trilha }: LayoutProps) {
  const outrosCursos = cursos.filter((c) => c.course.id !== hero?.curso.id);

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials={avatarInitials} avatarTitle={avatarTitle}>
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

      {!hero ? (
        <p className="p-[1.15rem] text-[.85rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Nenhum curso em andamento ainda.
        </p>
      ) : (
        <section className="max-w-md mx-auto px-[1.2rem] pt-[1.6rem] pb-8">
          <p
            className="text-center text-[.7rem] uppercase tracking-[.13em] m-0 mb-1"
            style={{ color: "var(--nia-accent)", fontFamily: "var(--nia-font-display)" }}
          >
            Seu módulo atual
          </p>
          <h2
            className="text-center m-0 text-[1.2rem]"
            style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}
          >
            {hero.curso.title}
          </h2>

          <ol className="list-none m-0 mt-5 p-0 flex flex-col gap-1 relative">
            {trilha.map((item, i) => (
              <li key={item.lessonId} className="relative flex gap-[.9rem] py-[.65rem]">
                <span
                  className="w-9 h-9 rounded-full border-2 flex items-center justify-center shrink-0 text-[.8rem] font-bold"
                  style={corDoDot(item.situacao)}
                >
                  {DOT_LABEL[item.situacao] || i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <h5 className="m-0 text-[.92rem]" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}>
                    {i + 1}. {item.titulo}
                  </h5>
                  <p className="m-0 text-[.77rem]" style={{ color: "var(--nia-ink-muted)" }}>
                    {legendaSituacao(item, i)}
                  </p>
                  {item.situacao === "current" && (
                    <Link href={`/aluno/licoes/${item.lessonId}`}>
                      <Button variant="accent" size="sm" className="mt-2">
                        Continuar
                      </Button>
                    </Link>
                  )}
                  {item.situacao === "done" && (
                    <Link href={`/aluno/licoes/${item.lessonId}`} className="text-[.75rem] font-bold" style={{ color: "var(--nia-accent)" }}>
                      Rever →
                    </Link>
                  )}
                </div>
              </li>
            ))}
          </ol>

          {outrosCursos.length > 0 && (
            <div className="mt-7">
              <p className="text-[.7rem] uppercase tracking-[.13em] m-0 mb-2" style={{ color: "var(--nia-accent)", fontFamily: "var(--nia-font-display)" }}>
                Outros cursos
              </p>
              <div className="flex gap-2 overflow-x-auto pb-1">
                {outrosCursos.map((c) => (
                  <span
                    key={c.course.id}
                    className="shrink-0 text-[.77rem] px-[.8rem] py-[.45rem] rounded-[var(--nia-radius-pill)] whitespace-nowrap"
                    style={{ background: "var(--nia-surface)", border: "1px solid var(--nia-border)", color: "var(--nia-ink-muted)" }}
                  >
                    {c.course.title}
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
