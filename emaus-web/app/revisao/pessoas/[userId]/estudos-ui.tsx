"use client";

import { useState } from "react";
import { Botao } from "../../../_ui/Botao";
import { Chip } from "../../../_ui/Chip";
import { mudarLiberacaoEstudo, type LiberacaoEstudo } from "../../../_lib/api";
import { quando } from "../../../_lib/pessoas";

// Estudos privados desta pessoa (2026-10-06): o Master libera ou pausa cada um.
// O backend é quem decide e guarda (PUT /matriculas/...); aqui só se mostra o que
// ele devolveu e se manda o pedido. Pausar não apaga nada — o progresso fica.
export function EstudosDaPessoa({ userId, iniciais }: { userId: number; iniciais: LiberacaoEstudo[] }) {
  const [lista, setLista] = useState(iniciais);
  const [mexendo, setMexendo] = useState<number | null>(null);
  const [erro, setErro] = useState<string | null>(null);

  async function mudar(e: LiberacaoEstudo, status: "ativa" | "pausada") {
    setMexendo(e.course_id);
    setErro(null);
    try {
      const novo = await mudarLiberacaoEstudo(userId, e.course_id, status);
      setLista((l) => l.map((x) => (x.course_id === novo.course_id ? novo : x)));
    } catch (err) {
      setErro(err instanceof Error ? err.message : "Não deu pra mudar o acesso.");
    } finally {
      setMexendo(null);
    }
  }

  return (
    <section className="mt-5 overflow-hidden rounded-[var(--tm-radius-lg)] border border-[var(--tm-border)] bg-[var(--tm-surface)]">
      <div className="px-4 py-3.5">
        <h2 className="m-0 text-[1.05rem]">Estudos liberados</h2>
        <p className="m-0 mt-0.5 text-[.82rem] text-[var(--tm-ink-muted)]">
          Estudos privados só aparecem pra quem você liberar. Pausar esconde o estudo, mas guarda o progresso.
        </p>
      </div>
      {lista.length === 0 ? (
        <p className="m-0 border-t border-[var(--tm-border)] px-4 py-3 text-[.88rem] text-[var(--tm-ink-muted)]">
          Nenhum estudo privado cadastrado ainda.
        </p>
      ) : (
        <ul className="m-0 list-none divide-y divide-[var(--tm-border)] border-t border-[var(--tm-border)] p-0">
          {lista.map((e) => {
            const ativo = e.status === "ativa";
            return (
              <li key={e.course_id} className="flex flex-wrap items-center gap-x-3 gap-y-2 px-4 py-2.5 text-[.9rem]">
                <span className="min-w-0 flex-1">
                  {e.titulo}
                  {e.atualizada_em && (
                    <small className="block text-[.76rem] text-[var(--tm-ink-muted)]">
                      {ativo ? "Liberado" : "Pausado"} {quando(e.atualizada_em)}
                    </small>
                  )}
                </span>
                <Chip tom={ativo ? "bom" : "neutro"}>{ativo ? "Liberado" : e.status === null ? "Sem acesso" : "Pausado"}</Chip>
                <Botao
                  tamanho="sm"
                  variante={ativo ? "fantasma" : "primario"}
                  disabled={mexendo !== null}
                  onClick={() => mudar(e, ativo ? "pausada" : "ativa")}
                >
                  {mexendo === e.course_id ? "Salvando…" : ativo ? "Pausar" : "Liberar"}
                </Botao>
              </li>
            );
          })}
        </ul>
      )}
      {erro && (
        <p role="alert" className="m-0 border-t border-[var(--tm-border)] px-4 py-2.5 text-[.85rem] text-[var(--tm-danger)]">
          {erro}
        </p>
      )}
    </section>
  );
}
