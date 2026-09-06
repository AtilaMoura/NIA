import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Build "standalone" pra imagem Docker de produção enxuta (ver Dockerfile.prod).
  output: "standalone",
};

export default nextConfig;
