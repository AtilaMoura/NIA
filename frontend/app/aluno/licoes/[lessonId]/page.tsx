import Link from "next/link";
import { Badge } from "../../../components/ui/Badge";
import { getCourse, getLesson, getModule, lessonRenderUrl } from "../../../lib/api";
import { MOCK_USER_ID } from "../../../lib/constants";
import { AvaliacaoPanel } from "./AvaliacaoPanel";

type PageProps = { params: Promise<{ lessonId: string }> };

// Página da lição — o render (GET /lessons/{id}/render) é um HTML completo e
// independente com seu próprio topbar/navbar/botão de tela cheia (temas Vidro
// Fumê etc., sistema separado — ver memória nia-visual-padroes), por isso ocupa
// a tela inteira em vez de ficar dentro de uma moldura — duplicar um topbar
// nosso por cima do topbar do renderer só rouba espaço e conflita visualmente.
// allowFullScreen é o que destrava o botão "⛶" que o renderer já tem.
export default async function LicaoPage({ params }: PageProps) {
  const { lessonId } = await params;
  const lesson = await getLesson(Number(lessonId));
  const module = await getModule(lesson.module_id);
  const course = await getCourse(module.course_id);

  const pronta = lesson.is_approved && !!lesson.content;

  if (!pronta) {
    return (
      <div
        className="min-h-screen flex items-center justify-center p-4"
        style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}
      >
        <div
          className="rounded-[var(--nia-radius-lg)] border p-6 flex flex-col gap-2 max-w-md"
          style={{ borderColor: "var(--nia-border)", background: "var(--nia-surface)" }}
        >
          <Badge variant="info">Em preparação</Badge>
          <p className="m-0 text-[.85rem]" style={{ color: "var(--nia-ink-muted)" }}>
            Essa lição ainda está sendo gerada e revisada pelo admin. Volte mais tarde.
          </p>
          <Link href="/aluno" className="text-[.83rem] font-bold" style={{ color: "var(--nia-accent)" }}>
            ← Voltar ao painel
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)" }}>
      <Link
        href="/aluno"
        aria-label={`Voltar ao painel — ${course.title}`}
        title="Voltar ao painel"
        className="fixed top-3 left-3 z-50 w-8 h-8 rounded-full border flex items-center justify-center shadow-md"
        style={{ borderColor: "var(--nia-border)", background: "var(--nia-surface)", color: "var(--nia-ink)" }}
      >
        ←
      </Link>

      <iframe
        src={lessonRenderUrl(lesson.id, { userId: MOCK_USER_ID })}
        title={lesson.title}
        allowFullScreen
        allow="fullscreen"
        className="w-full block"
        style={{ height: "100dvh", border: "none" }}
      />

      <div className="p-4">
        <AvaliacaoPanel lessonId={lesson.id} userId={MOCK_USER_ID} />
      </div>
    </div>
  );
}
