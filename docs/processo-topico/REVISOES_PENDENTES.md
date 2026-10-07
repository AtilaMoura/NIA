# Revisões pendentes — tópicos antigos no padrão novo

Tópicos publicados ANTES do processo novo (`BASE.md`, 2026-09-30) precisam passar pelas
3 fases da revisão. Atualizar esta lista a cada tópico concluído.

**Como revisar (o que funcionou no Redes, 2026-10-01):**
1. **Fase A — diagnóstico:** `python backend/_diagnostico_topicos.py <ids>` (lê a produção;
   `DIAG_BASE=http://localhost:8100` pra conferir o local antes de publicar)
2. **Fase B — auditoria de fato:** dossiê `fontes/<curso>/topico<ids>-<slug>.md` + um relatório
   `fontes/<curso>/topico<id>-<slug>-auditoria.md` por tópico (afirmação → fonte → status)
3. **Fase C — corrigir e republicar:** script idempotente que lê o conteúdo do PRÓPRIO destino
   (modelo: `backend/_revisar_redes_t28_30.py local|prod`), valida, faz PUT
4. **Áudio por último**, do texto final: `backend/_gerar_audio_topico.py` (narração → REVISAR →
   voz → mp3 → aplicar local → scp → aplicar prod)

## Situação

| Curso | Tópicos | Status | Observação |
|---|---|---|---|
| Redes e Câmeras | T28, T29, T30 | ✅ concluído 2026-10-01 | 1 erro de conceito por tópico em média; IP de exemplo real trocado |
| Redes e Câmeras | T31 | ✅ já nasceu no padrão | — |
| **Obreiro I** | **T1–T5** | ⏳ pendente | Prioridade: **reconferir TODAS as citações bíblicas** contra o `biblia_service` (já houve citação de memória errada no T2) — e conferir também a própria fonte: no T66 a bible-api veio com "pela que há" (faltando "fé", 2Tm 3:15) e "mas quais" (2Pe 3:16). **Rótulo "(ARC)"** das citações do T1–T5: o texto da bible-api não bate com a ARC — trocar pra "(Almeida)" ou confirmar a edição. T5 está sem `imagem_capa`. T1 e parte do T2 já têm áudio antigo (voz 2.5) — reaproveitar se o texto não mudar |
| **IA / Agentes LLM** | **T13–T20** | ⏳ pendente | Conferir contra a apostila (`Estudo IA/aula 0N.md`) e papers. T20 (Embeddings) saiu do Groq com correção manual. Imagens no estilo antigo — trocar pro estilo escolhido (isométrico claro). Tema mudou pra vinho-ouro |
| **Inglês** | **T9 → T10 → T11 → T27** | ✅ Aula 1 revisada — T9 ✅ T10 ✅ T11 ✅ (2026-10-06) · T27 ✅ (2026-10-07). T6/T7/T8 GUARDADOS no curso 14 (2026-10-07) — revisar quando voltarem pra grade, ver `ingles.md` → Guardados | Roteiro aprovado em `ingles.md` → "Revisar tópico antigo no padrão novo". Decidido: narração em PT por bloco (2026-10-06). Um por vez, com revisão do Atila entre eles |

**Prova junto com a revisão (decisão do Atila, 2026-10-07):** todo tópico revisado aqui ganha a
prova no padrão novo (banco de perguntas + sorteio, regra do curso) com `/criar-provas-topicos`,
inclusive os 18 que já têm prova antiga. Regras: [PROVA.md](PROVA.md).

## Achados do Redes que valem pros outros cursos
- O **resumo** costuma repetir a afirmação errada do corpo — revisar os dois.
- Exemplo com dado real (IP, telefone, nome) → trocar por dado de documentação/fictício explícito.
- Continuidade ("no próximo módulo…") quebra quando a grade muda — conferir com a grade atual.
- Narração por IA erra número por extenso e corta frase — revisar SEMPRE antes da voz.
