import { TEMA_POR_CURSO, THEME_TOPICO } from "./config";
import { getCourse } from "./api";

// Tema do render de slides de um curso (2026-10-06). Vem do próprio curso no banco
// (`identidade_visual.tema_slides`, gravado pela API) — assim curso novo não precisa de
// deploy nem do id de produção no código. O mapa fixo do config fica como reserva pros
// cursos antigos; sem nenhum dos dois, o tema padrão.
export async function temaDoCurso(courseId: number, token?: string | null): Promise<string> {
  const curso = await getCourse(courseId, token).catch(() => null);
  const doBanco = curso?.identidade_visual?.tema_slides;
  return (typeof doBanco === "string" && doBanco) || TEMA_POR_CURSO[courseId] || THEME_TOPICO;
}
