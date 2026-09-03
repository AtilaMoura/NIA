import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { Badge } from "../../components/ui/Badge";
import { Card } from "../../components/ui/Card";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { modulosDoCurso, percentDoCurso, progressoMaisAvancado } from "../_lib/progresso";
import { getUser, listCourses, listLessons, listModules, listProgress, type Course, type Lesson, type Module, type Progress } from "../../lib/api";
import { MOCK_USER_ID } from "../../lib/constants";

type ItemHistorico = {
  lessonId: number;
  titulo: string;
  veredito: string;
  diagnostico: string;
  ordem: number;
};

function historicoDoCurso(course: Course, modules: Module[], lessons: Lesson[], progressosDoAluno: Progress[]): ItemHistorico[] {
  const modulosIds = new Set(modulosDoCurso(course, modules).map((m) => m.id));
  const progressosDoCurso = progressosDoAluno.filter((p) => modulosIds.has(p.module_id));

  const itens: ItemHistorico[] = [];
  for (const progresso of progressosDoCurso) {
    for (const entrada of progresso.tutor_analysis?.historico ?? []) {
      const licao = lessons.find((l) => l.id === entrada.lesson_id);
      if (!licao) continue;
      const modulo = modules.find((m) => m.id === licao.module_id);
      itens.push({
        lessonId: licao.id,
        titulo: licao.title,
        veredito: entrada.veredito,
        diagnostico: entrada.resumo_diagnostico,
        ordem: (modulo?.module_index ?? 0) * 1000 + licao.lesson_index,
      });
    }
  }
  return itens.sort((a, b) => a.ordem - b.ordem);
}

type UltimoVeredito = { lessonId: number; titulo: string; cursoTitulo: string; veredito: string; diagnostico: string };

// Último veredito de cada lição (não a contagem de tentativas) — processa os
// históricos na ordem cronológica original (sem reordenar por posição), então
// a última ocorrência de cada lesson_id é sempre a tentativa mais recente.
function ultimosVereditos(progressosDoAluno: Progress[], lessons: Lesson[], modules: Module[], courses: Course[]): Map<number, UltimoVeredito> {
  const mapa = new Map<number, UltimoVeredito>();
  for (const progresso of progressosDoAluno) {
    for (const entrada of progresso.tutor_analysis?.historico ?? []) {
      const licao = lessons.find((l) => l.id === entrada.lesson_id);
      if (!licao) continue;
      const modulo = modules.find((m) => m.id === licao.module_id);
      const curso = modulo ? courses.find((c) => c.id === modulo.course_id) : undefined;
      mapa.set(entrada.lesson_id, {
        lessonId: entrada.lesson_id,
        titulo: licao.title,
        cursoTitulo: curso?.title ?? "",
        veredito: entrada.veredito,
        diagnostico: entrada.resumo_diagnostico,
      });
    }
  }
  return mapa;
}

// Fase 5 — dashboard de progresso: histórico de avaliações do Tutor por lição,
// direto de Progress.tutor_analysis (um curso pode ter mais de um Progress, um
// por módulo — junta o histórico de todos).
export default async function ProgressoPage() {
  const [user, courses, modules, lessons, progressos] = await Promise.all([
    getUser(MOCK_USER_ID),
    listCourses(),
    listModules(),
    listLessons(),
    listProgress(),
  ]);

  const progressosDoAluno = progressos.filter((p) => p.user_id === MOCK_USER_ID);
  const cursosDoAluno = courses.filter((c) => progressoMaisAvancado(c, modules, progressosDoAluno));
  const cursosEmAndamento = cursosDoAluno.filter((c) => progressoMaisAvancado(c, modules, progressosDoAluno)?.status !== "completed");

  const mapaVereditos = ultimosVereditos(progressosDoAluno, lessons, modules, courses);
  const topicosDominados = [...mapaVereditos.values()].filter((v) => v.veredito === "dominado").length;
  const pontosDeAtencao = [...mapaVereditos.values()].filter((v) => v.veredito !== "dominado");

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials="TF" avatarTitle={user.name ?? "Aluno"}>
        <Link href="/aluno" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Painel
        </Link>
        <Link href="/aluno/explorar" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Explorar
        </Link>
        <Link href="/aluno/perfil" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Perfil
        </Link>
        <Link href="/aluno/preferencias" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Preferências
        </Link>
      </AppTopbar>

      <div className="p-[1.15rem] flex flex-col gap-5 max-w-2xl">
        <h1 className="text-xl font-bold m-0" style={{ fontFamily: "var(--nia-font-display)" }}>
          Progresso
        </h1>

        {cursosDoAluno.length === 0 && (
          <p className="text-[.85rem]" style={{ color: "var(--nia-ink-muted)" }}>
            Nenhum curso iniciado ainda.
          </p>
        )}

        {cursosDoAluno.length > 0 && (
          <div className="flex gap-6 p-4 rounded-[var(--nia-radius-lg)] border" style={{ borderColor: "var(--nia-border)", background: "var(--nia-surface)" }}>
            <div>
              <p className="m-0 text-[1.3rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
                {cursosEmAndamento.length}
              </p>
              <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
                curso(s) em andamento
              </p>
            </div>
            <div>
              <p className="m-0 text-[1.3rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
                {topicosDominados}
              </p>
              <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
                tópicos dominados
              </p>
            </div>
          </div>
        )}

        {pontosDeAtencao.length > 0 && (
          <Card className="flex flex-col gap-3">
            <h2 className="m-0 text-[.9rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
              Pontos de atenção
            </h2>
            <ul className="list-none m-0 p-0 flex flex-col gap-3">
              {pontosDeAtencao.map((item) => (
                <li key={item.lessonId} className="border-t pt-3" style={{ borderColor: "var(--nia-border)" }}>
                  <div className="flex items-center justify-between gap-2 flex-wrap mb-1">
                    <div>
                      <Link
                        href={`/aluno/licoes/${item.lessonId}`}
                        className="text-[.85rem] font-bold"
                        style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}
                      >
                        {item.titulo}
                      </Link>
                      <p className="m-0 text-[.7rem]" style={{ color: "var(--nia-ink-muted)" }}>
                        {item.cursoTitulo}
                      </p>
                    </div>
                    <Badge variant="bad">Precisa reforçar</Badge>
                  </div>
                  <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
                    {item.diagnostico}
                  </p>
                </li>
              ))}
            </ul>
          </Card>
        )}

        {cursosDoAluno.map((course) => {
          const progresso = progressoMaisAvancado(course, modules, progressosDoAluno);
          const percent = percentDoCurso(course, modules, progresso);
          const concluido = progresso?.status === "completed";
          const historico = historicoDoCurso(course, modules, lessons, progressosDoAluno);

          return (
            <Card key={course.id} className="flex flex-col gap-3">
              <div className="flex items-center justify-between gap-3 flex-wrap">
                <h2 className="m-0 text-[.98rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
                  {course.title}
                </h2>
                <Badge variant={concluido ? "good" : "neutral"}>{concluido ? "Concluído" : "Em andamento"}</Badge>
              </div>
              <ProgressBar value={percent} label={`${percent}%`} />

              {historico.length === 0 ? (
                <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
                  Ainda sem avaliações registradas.
                </p>
              ) : (
                <ul className="list-none m-0 p-0 flex flex-col gap-3">
                  {historico.map((item, index) => {
                    const dominado = item.veredito === "dominado";
                    return (
                      <li key={`${item.lessonId}-${index}`} className="border-t pt-3" style={{ borderColor: "var(--nia-border)" }}>
                        <div className="flex items-center justify-between gap-2 flex-wrap mb-1">
                          <Link
                            href={`/aluno/licoes/${item.lessonId}`}
                            className="text-[.85rem] font-bold"
                            style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-ink)" }}
                          >
                            {item.titulo}
                          </Link>
                          <Badge variant={dominado ? "good" : "bad"}>{dominado ? "Dominado" : "Precisa reforçar"}</Badge>
                        </div>
                        <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
                          {item.diagnostico}
                        </p>
                      </li>
                    );
                  })}
                </ul>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
}
