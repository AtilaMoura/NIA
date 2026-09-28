// Formatação da página Pessoas do Master (2026-09-28). Sem nada de server — usado
// também no componente cliente (filtro/busca).

const FUSO = "America/Sao_Paulo";

function diaNoFuso(d: Date): string {
  return d.toLocaleDateString("en-CA", { timeZone: FUSO }); // AAAA-MM-DD
}

function diasEntre(d: Date, agora: Date): number {
  const a = new Date(diaNoFuso(d) + "T00:00:00Z").getTime();
  const b = new Date(diaNoFuso(agora) + "T00:00:00Z").getTime();
  return Math.round((b - a) / 86400000);
}

// "hoje, 16:10" · "ontem, 00:20" · "há 3 dias" · "12/09" · "—"
export function quando(iso: string | null | undefined, agora = new Date()): string {
  if (!iso) return "—";
  const d = new Date(iso);
  const dias = diasEntre(d, agora);
  const hora = d.toLocaleTimeString("pt-BR", { timeZone: FUSO, hour: "2-digit", minute: "2-digit" });
  if (dias <= 0) return `hoje, ${hora}`;
  if (dias === 1) return `ontem, ${hora}`;
  if (dias < 30) return `há ${dias} dias`;
  return data(iso);
}

// "12/09" (ano só se não for o atual)
export function data(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  const mesmoAno = d.getFullYear() === new Date().getFullYear();
  return d.toLocaleDateString("pt-BR", { timeZone: FUSO, day: "2-digit", month: "2-digit", ...(mesmoAno ? {} : { year: "numeric" }) });
}

export function dataHora(iso: string | null | undefined): string {
  if (!iso) return "—";
  return `${data(iso)} ${new Date(iso).toLocaleTimeString("pt-BR", { timeZone: FUSO, hour: "2-digit", minute: "2-digit" })}`;
}

// Bolinha de cor: até 2 dias (verde), até 7 (laranja), mais que isso (vermelho)
export type Sinal = "hoje" | "semana" | "parado" | "nunca";
export function sinalDe(iso: string | null | undefined, agora = new Date()): Sinal {
  if (!iso) return "nunca";
  const dias = diasEntre(new Date(iso), agora);
  if (dias <= 2) return "hoje";
  if (dias <= 7) return "semana";
  return "parado";
}

export function duracao(segundos: number): string {
  const min = Math.round(segundos / 60);
  if (min <= 0) return "—";
  const h = Math.floor(min / 60);
  const m = min % 60;
  return h > 0 ? `${h}h ${m}min` : `${m} min`;
}

// A última vez que a pessoa apareceu (login ou atividade de estudo)
export function ultimoAcesso(p: { ultimo_login: string | null; ultima_atividade: string | null }): string | null {
  const a = p.ultimo_login ? new Date(p.ultimo_login).getTime() : 0;
  const b = p.ultima_atividade ? new Date(p.ultima_atividade).getTime() : 0;
  if (!a && !b) return null;
  return a >= b ? p.ultimo_login : p.ultima_atividade;
}

export const ROTULO_PAPEL: Record<string, string> = {
  master: "Master",
  admin: "Admin",
  professor: "Professor",
  aluno: "Aluno",
};
