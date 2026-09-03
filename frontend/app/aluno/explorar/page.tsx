import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { melhorLicaoParaAbrir, percentDoCurso, progressoMaisAvancado } from "../_lib/progresso";
import { getUser, listCourses, listLessons, listModules, listProgress } from "../../lib/api";
import { MOCK_USER_ID } from "../../lib/constants";

// Explorar — catálogo com TODOS os cursos do NIA, sem controle de acesso (não
// existe conceito de matrícula hoje; a venda acontece fora da plataforma).
// Sem navegação por humor/categoria ainda: Course.category não é populado por
// nenhum código do pipeline — fingir essa navegação mostraria dado falso.
export default async function ExplorarPage() {
  const [user, courses, modules, lessons, progressos] = await Promise.all([
    getUser(MOCK_USER_ID),
    listCourses(),
    listModules(),
    listLessons(),
    listProgress(),
  ]);

  const progressosDoAluno = progressos.filter((p) => p.user_id === MOCK_USER_ID);

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials="TF" avatarTitle={user.name ?? "Aluno"}>
        <Link href="/aluno/progresso" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Progresso
        </Link>
        <Link href="/aluno/perfil" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Perfil
        </Link>
      </AppTopbar>

      <div className="p-[1.15rem] flex flex-col gap-4">
        <div>
          <h1 className="m-0 text-xl font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
            Explorar
          </h1>
          <p className="m-0 text-[.82rem]" style={{ color: "var(--nia-ink-muted)" }}>
            Todos os cursos disponíveis no NIA.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-[.85rem]">
          {courses.map((course) => {
            const progresso = progressoMaisAvancado(course, modules, progressosDoAluno);
            const percent = percentDoCurso(course, modules, progresso);
            const linkLicaoId = melhorLicaoParaAbrir(course, modules, lessons, progresso);
            const concluido = progresso?.status === "completed";
            const status = concluido ? "completed" : progresso ? "in_progress" : "new";
            const label = concluido ? "Concluído" : progresso ? "Em andamento" : "Novo";

            return (
              <Card key={course.id} className="flex flex-col gap-2">
                <Badge variant={status === "completed" ? "good" : status === "in_progress" ? "neutral" : "new"}>{label}</Badge>
                <h4 className="m-0 text-[.92rem] leading-[1.25]" style={{ fontFamily: "var(--nia-font-display)" }}>
                  {course.title}
                </h4>
                <p className="m-0 text-[.75rem]" style={{ color: "var(--nia-ink-muted)" }}>
                  Nível {course.level} · {course.modules_count} módulos
                </p>
                {progresso && <ProgressBar value={percent} size="sm" />}
                {linkLicaoId ? (
                  <Link href={`/aluno/licoes/${linkLicaoId}`}>
                    <Button variant={progresso ? "ghost" : "accent"} size="sm" className="mt-1">
                      {progresso ? "Continuar" : "Começar"}
                    </Button>
                  </Link>
                ) : (
                  <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
                    Nenhuma lição gerada ainda
                  </p>
                )}
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
