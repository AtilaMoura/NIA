import type { Course } from "../../lib/api";
import type { Mood } from "../../components/theme/ThemeProvider";

export type CursoComStatus = {
  course: Course;
  percent: number;
  status: "completed" | "in_progress" | "new";
  // Melhor lição pra abrir ao clicar no card: a atual se já estiver pronta,
  // senão a última pronta antes dela (nunca deixa o card sem destino se pelo
  // menos 1 lição do curso já foi aprovada).
  linkLicaoId: number | null;
  // Humor do "pôster" do curso — provisório, ver humorDoCurso() em _lib/progresso.ts.
  mood: Mood;
};

export type HeroInfo = {
  curso: Course;
  percent: number;
  proximaLicaoId: number | null;
  proximaLicaoPronta: boolean;
  proximaLicaoTitulo: string;
  // Preenchido só quando a próxima não está pronta — permite oferecer "rever
  // a última lição" em vez de deixar o aluno sem nenhuma ação possível.
  fallbackLicaoId: number | null;
  moduloIndex: number;
  totalModulos: number;
  // Último veredito do Tutor antes desta lição, se houver — vira o selo
  // "Tópico anterior dominado" no card de continuar.
  ultimaAvaliacaoDominada: boolean;
} | null;

export type TrilhaItem = {
  lessonId: number;
  titulo: string;
  situacao: "done" | "current" | "proximo" | "preparando" | "bloqueado";
};

export type LayoutProps = {
  avatarInitials: string;
  avatarTitle: string;
  hero: HeroInfo;
  cursos: CursoComStatus[];
  trilha: TrilhaItem[];
  // Cursos "em destaque" no carrossel do topo do layout Retomar — não
  // confundir com `hero` (que é o curso em andamento). Vazio quando não há
  // nenhum curso "novo" pra sugerir; a UI adapta (sem setas/dots com 1 só).
  cursosDestaque: CursoComStatus[];
  nivel: number;
  pontos: number;
  streak: number;
};
