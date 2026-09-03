import { BibliotecaLayout } from "./_layouts/BibliotecaLayout";
import { RetomarLayout } from "./_layouts/RetomarLayout";
import { TrilhaLayout } from "./_layouts/TrilhaLayout";
import type { CursoComStatus, HeroInfo, TrilhaItem } from "./_layouts/types";
import { humorDoCurso, melhorLicaoParaAbrir, modulosDoCurso, percentDoCurso, progressoMaisAvancado, trilhaDoCurso } from "./_lib/progresso";
import { getUser, listCourses, listLessons, listModules, listProgress } from "../lib/api";
import { MOCK_USER_ID } from "../lib/constants";

// Painel do aluno — escolhe o layout (Retomar/Biblioteca/Trilha) com base em
// User.preferred_panel_layout (Fase 4), decidido no server pra não ter flash de
// layout errado. MOCK_USER_ID no lugar de sessão real até a Fase 0 existir.
export default async function PainelAlunoPage() {
  const [user, courses, modules, lessons, progressos] = await Promise.all([
    getUser(MOCK_USER_ID),
    listCourses(),
    listModules(),
    listLessons(),
    listProgress(),
  ]);

  const progressosDoAluno = progressos.filter((p) => p.user_id === MOCK_USER_ID);

  const cursos: CursoComStatus[] = courses.map((course) => {
    const progresso = progressoMaisAvancado(course, modules, progressosDoAluno);
    const percent = percentDoCurso(course, modules, progresso);
    const status: CursoComStatus["status"] = progresso
      ? progresso.status === "completed"
        ? "completed"
        : "in_progress"
      : "new";
    const linkLicaoId = melhorLicaoParaAbrir(course, modules, lessons, progresso);
    return { course, percent, status, linkLicaoId, mood: humorDoCurso(course.id) };
  });

  const cursoEmAndamento = cursos.find((c) => c.status === "in_progress");
  const cursoAtual = cursoEmAndamento?.course;
  const progressoAtual = cursoAtual ? progressoMaisAvancado(cursoAtual, modules, progressosDoAluno) : undefined;

  let hero: HeroInfo = null;
  let trilha: TrilhaItem[] = [];
  if (cursoAtual && progressoAtual) {
    const modulosOrdenados = modulosDoCurso(cursoAtual, modules);
    const moduloAtual = modulosOrdenados.find((m) => m.id === progressoAtual.module_id);
    const licao = lessons.find(
      (l) => l.module_id === progressoAtual.module_id && l.lesson_index === progressoAtual.current_lesson_index
    );
    const proximaLicaoPronta = !!(licao?.is_approved && licao?.content);
    const historico = progressoAtual.tutor_analysis?.historico ?? [];
    hero = {
      curso: cursoAtual,
      percent: percentDoCurso(cursoAtual, modules, progressoAtual),
      proximaLicaoId: licao?.id ?? null,
      proximaLicaoPronta,
      proximaLicaoTitulo: licao?.title ?? "",
      fallbackLicaoId: proximaLicaoPronta ? null : melhorLicaoParaAbrir(cursoAtual, modules, lessons, progressoAtual),
      moduloIndex: moduloAtual?.module_index ?? 1,
      totalModulos: modulosOrdenados.length,
      ultimaAvaliacaoDominada: historico.length > 0 && historico[historico.length - 1].veredito === "dominado",
    };
    trilha = trilhaDoCurso(cursoAtual, modules, lessons, progressoAtual);
  }

  // Cursos em destaque pro carrossel: os "novos" (sem progresso), ordenados
  // pela nota do Reviewer (sem nota fica por último, ordem por id como
  // desempate determinístico). Capado em 5 pra não virar um carrossel infinito.
  const cursosDestaque = cursos
    .filter((c) => c.status === "new")
    .sort((a, b) => (b.course.ai_quality_score ?? -1) - (a.course.ai_quality_score ?? -1) || a.course.id - b.course.id)
    .slice(0, 5);

  const layoutProps = {
    avatarInitials: "TF",
    avatarTitle: user.name ?? "Aluno",
    hero,
    cursos,
    trilha,
    cursosDestaque,
    nivel: user.level ?? 1,
    pontos: user.total_points ?? 0,
    streak: user.streak_days ?? 0,
  };

  if (user.preferred_panel_layout === "biblioteca") return <BibliotecaLayout {...layoutProps} />;
  if (user.preferred_panel_layout === "trilha") return <TrilhaLayout {...layoutProps} />;
  return <RetomarLayout {...layoutProps} />;
}
