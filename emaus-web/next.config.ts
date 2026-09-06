import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Front puro cliente da API do NIA — sem rewrites/proxy, chama o backend direto
  // via NEXT_PUBLIC_API_URL (browser) / API_URL_INTERNAL (server).

  // Build "standalone": gera .next/standalone/server.js com só as deps usadas —
  // imagem Docker de produção pequena (ver Dockerfile.prod).
  output: "standalone",
};

export default nextConfig;
