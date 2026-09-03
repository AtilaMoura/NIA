import { LogoSimbolo } from "./_ui/Logo";

export default function Carregando() {
  return (
    <div className="flex min-h-[70vh] items-center justify-center" role="status" aria-label="Carregando">
      <LogoSimbolo
        size={44}
        decorativo
        className="animate-pulse text-[var(--tm-accent)] opacity-70"
      />
    </div>
  );
}
