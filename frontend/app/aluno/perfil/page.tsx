import Link from "next/link";
import { AppTopbar } from "../../components/shell/AppTopbar";
import { Avatar } from "../../components/ui/Avatar";
import { Badge } from "../../components/ui/Badge";
import { Card } from "../../components/ui/Card";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { getUser } from "../../lib/api";
import { MOCK_USER_ID } from "../../lib/constants";

const NOMES_BADGE: Record<string, string> = {
  "primeira-licao-dominada": "Primeira lição dominada",
  "streak-3-dias": "3 dias seguidos",
  "streak-7-dias": "7 dias seguidos",
  "primeiro-curso-concluido": "Primeiro curso concluído",
};

// Perfil — identidade do aluno (nível/pontos/streak já existiam no schema do
// User, mas nenhum código escrevia neles até a gamificação ser implementada).
export default async function PerfilPage() {
  const user = await getUser(MOCK_USER_ID);

  const points = user.total_points ?? 0;
  const level = user.level ?? 1;
  const pontosNoNivel = points % 100;
  const streak = user.streak_days ?? 0;
  const badges = user.badges ?? [];
  const topicos = user.preferred_topics ?? [];

  return (
    <div className="min-h-screen" style={{ background: "var(--nia-bg)", color: "var(--nia-ink)", fontFamily: "var(--nia-font-body)" }}>
      <AppTopbar avatarInitials="TF" avatarTitle={user.name ?? "Aluno"}>
        <Link href="/aluno/explorar" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Explorar
        </Link>
        <Link href="/aluno/progresso" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Progresso
        </Link>
        <Link href="/aluno/preferencias" className="text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
          Preferências
        </Link>
      </AppTopbar>

      <div className="p-[1.15rem] flex flex-col gap-5 max-w-2xl">
        <div className="flex items-center gap-4">
          <Avatar initials="TF" title={user.name ?? "Aluno"} />
          <div>
            <h1 className="m-0 text-xl font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
              {user.name ?? "Aluno"}
            </h1>
            <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
              Nível {level}
            </p>
          </div>
        </div>

        <Card className="flex flex-col gap-3">
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <span className="text-[.85rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
              Nível {level}
            </span>
            <span className="text-[.78rem]" style={{ color: "var(--nia-ink-muted)" }}>
              {pontosNoNivel}/100 pontos pro próximo nível
            </span>
          </div>
          <ProgressBar value={pontosNoNivel} />
          <div className="flex gap-6 mt-1">
            <div>
              <p className="m-0 text-[1.2rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
                {points}
              </p>
              <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
                pontos totais
              </p>
            </div>
            <div>
              <p className="m-0 text-[1.2rem] font-bold" style={{ fontFamily: "var(--nia-font-display)", color: "var(--nia-accent)" }}>
                🔥 {streak}
              </p>
              <p className="m-0 text-[.72rem]" style={{ color: "var(--nia-ink-muted)" }}>
                dias seguidos
              </p>
            </div>
          </div>
        </Card>

        <Card className="flex flex-col gap-2">
          <h2 className="m-0 text-[.85rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
            Conquistas
          </h2>
          {badges.length === 0 ? (
            <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
              Nenhuma conquista ainda — continue estudando pra desbloquear a primeira.
            </p>
          ) : (
            <div className="flex gap-2 flex-wrap">
              {badges.map((b) => (
                <Badge key={b} variant="good">
                  {NOMES_BADGE[b] ?? b}
                </Badge>
              ))}
            </div>
          )}
        </Card>

        <Card className="flex flex-col gap-2">
          <h2 className="m-0 text-[.85rem] font-bold" style={{ fontFamily: "var(--nia-font-display)" }}>
            Interesses
          </h2>
          {topicos.length === 0 ? (
            <p className="m-0 text-[.8rem]" style={{ color: "var(--nia-ink-muted)" }}>
              Nenhum tópico de interesse configurado ainda.
            </p>
          ) : (
            <div className="flex gap-2 flex-wrap">
              {topicos.map((t) => (
                <span
                  key={t}
                  className="text-[.78rem] px-[.7rem] py-[.35rem] rounded-[var(--nia-radius-pill)]"
                  style={{ background: "var(--nia-surface2)", border: "1px solid var(--nia-border)", color: "var(--nia-ink-muted)" }}
                >
                  {t}
                </span>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
