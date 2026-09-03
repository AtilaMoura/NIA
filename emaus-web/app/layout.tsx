import type { Metadata } from "next";
import { cookies } from "next/headers";
import { Fraunces, Source_Sans_3 } from "next/font/google";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  variable: "--tm-font-display-loaded",
  display: "swap",
});

const sourceSans = Source_Sans_3({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--tm-font-body-loaded",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:4200"),
  applicationName: "Emaús",
  title: {
    default: "Emaús — formação bíblica",
    template: "%s · Emaús",
  },
  description:
    "Cursos de estudo da Bíblia e preparação para o serviço, feitos para você entender de verdade.",
  openGraph: {
    siteName: "Emaús",
    locale: "pt_BR",
    type: "website",
    title: "Emaús — formação bíblica",
    description:
      "Cursos de Bíblia, doutrina e vida cristã para a pessoa comum entender de verdade.",
  },
};

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const jar = await cookies();
  const theme = jar.get("tm_theme")?.value === "dark" ? "dark" : "light";
  const fsRaw = jar.get("tm_fontsize")?.value ?? "md";
  const fontsize = fsRaw === "sm" || fsRaw === "lg" ? fsRaw : "md";

  return (
    <html
      lang="pt-BR"
      data-tm-theme={theme}
      data-tm-fontsize={fontsize}
      className={`${fraunces.variable} ${sourceSans.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
