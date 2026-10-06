import type { Metadata } from "next";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { CabecalhoApp } from "../../../_ui/CabecalhoApp";
import { Rodape } from "../../../_ui/Rodape";
import { getCaderno, getUser, listLessons, listModules } from "../../../_lib/api";
import { getSessao, getToken } from "../../../_lib/sessao";
import { TEMA_POR_CURSO, THEME_TOPICO } from "../../../_lib/config";
import { Caderno } from "./caderno-ui";
import { Caveat, IBM_Plex_Mono } from "next/font/google";

// Letra "à mão" e a mono das etiquetas do caderno (mesmas do Resumo_Aula1_Atila.html)
const mao = Caveat({ subsets: ["latin"], weight: ["500", "700"], variable: "--cad-fonte-mao", display: "swap" });
const mono = IBM_Plex_Mono({ subsets: ["latin"], weight: ["400", "500"], variable: "--cad-fonte-mono", display: "swap" });

export const metadata: Metadata = { title: "Caderno da aula" };

// Caderno da aula (2026-10-05, protótipo 13-caderno.html): as anotações de uma
// aula em duas versões — "Minhas notas" (original, intocada) e "Caderno
// organizado" (IA organiza por assunto e corrige contra os slides). Cores do
// tema do curso.
export default async function CadernoPage({ params }: { params: Promise<{ lessonId: string }> }) {
  const lessonId = Number((await params).lessonId);
  if (!Number.isInteger(lessonId)) notFound();

  const sessao = await getSessao();
  if (!sessao) redirect(`/entrar?next=/anotacoes/aula/${lessonId}`);
  const token = await getToken();

  // Curso da aula (pro tema). Aula de curso sem acesso nem vem do backend → 404
  const [aulas, modulos] = await Promise.all([listLessons(token), listModules(token)]);
  const aula = aulas.find((l) => l.id === lessonId);
  const modulo = aula ? modulos.find((m) => m.id === aula.module_id) : undefined;
  if (!modulo) notFound();

  const tema = TEMA_POR_CURSO[modulo.course_id] ?? THEME_TOPICO;
  const [usuario, estado] = await Promise.all([
    getUser(sessao.id, token).catch(() => null),
    getCaderno(lessonId, tema, token).catch(() => null),
  ]);
  if (!estado) notFound();

  return (
    <>
      <CabecalhoApp nomeUsuario={usuario?.name ?? "Aluno"} papel={sessao.role} />

      <main className={`${mao.variable} ${mono.variable} mx-auto w-full max-w-[820px] px-[clamp(1rem,4vw,2rem)] pb-12 pt-[clamp(1.1rem,3vw,1.75rem)]`}>
        <Link href="/anotacoes" className="cad-sem-impressao text-[.85rem] font-semibold text-[var(--tm-ink-muted)] hover:text-[var(--tm-accent)]">
          ← Minhas anotações
        </Link>
        <Caderno estadoInicial={estado} tema={tema} />
      </main>

      <Rodape papel={sessao.role} />
    </>
  );
}
