# -*- coding: utf-8 -*-
"""
Script de migração: extrai avaliação embutida no Topico.content (slides
avaliacao_intro / avaliacao_pergunta / resultado) para a nova tabela Avaliacao,
e replica TopicoResposta (gate_id 'ef*') e TopicoProgress para
AvaliacaoResposta / AvaliacaoProgress.

Idempotente: se Avaliacao já existe para o topico_id, pula o tópico.
Nunca apaga nada — só copia/cria registros novos.

Uso:
    docker exec nia_backend python _migrar_avaliacao_separada.py --dry-run   # simula (default)
    docker exec nia_backend python _migrar_avaliacao_separada.py --apply    # aplica de verdade
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models.models import (
    Topico,
    Avaliacao,
    AvaliacaoProgress,
    AvaliacaoResposta,
    TopicoProgress,
    TopicoResposta,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migra avaliação embutida no Topico.content para tabela Avaliacao separada"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Simula a migração sem gravar no banco (padrão)",
    )
    group.add_argument(
        "--apply",
        action="store_true",
        help="Aplica a migração de verdade (commit no final)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dry_run = not args.apply

    db = SessionLocal()
    try:
        topicos = db.query(Topico).filter(Topico.content.isnot(None)).all()

        total_migrados = 0
        total_pulados_ja_migrado = 0
        total_pulados_sem_avaliacao = 0
        total_erros = 0

        for topico in topicos:
            try:
                # PASSO 1: processar slides do tópico
                content_dict = json.loads(topico.content)
                slides = content_dict.get("slides", [])

                slides_avaliacao_intro = [s for s in slides if s.get("tipo") == "avaliacao_intro"]
                slides_avaliacao_pergunta = [s for s in slides if s.get("tipo") == "avaliacao_pergunta"]
                slides_resto = [
                    s for s in slides if s.get("tipo") not in ("avaliacao_intro", "avaliacao_pergunta")
                ]

                if not slides_avaliacao_intro and not slides_avaliacao_pergunta:
                    print(
                        f"  [PULADO] Topico {topico.id} '{topico.titulo}': sem avaliação embutida, nada a migrar"
                    )
                    total_pulados_sem_avaliacao += 1
                    continue

                # Verificar idempotência: já existe Avaliacao para este topico?
                avaliacao_existente = db.query(Avaliacao).filter(Avaliacao.topico_id == topico.id).first()
                if avaliacao_existente:
                    print(
                        f"  [PULADO] Topico {topico.id} '{topico.titulo}': já migrado (Avaliacao.id={avaliacao_existente.id}), pulando"
                    )
                    total_pulados_ja_migrado += 1
                    continue

                # Montar conteúdo da nova Avaliacao
                intro_slide = slides_avaliacao_intro[0] if slides_avaliacao_intro else {}
                avaliacao_conteudo = {
                    "intro": {k: v for k, v in intro_slide.items() if k not in ("tipo", "secao")},
                    "perguntas": [s.get("pergunta") for s in slides_avaliacao_pergunta],
                    "resultado": {"titulo": "Resultado da prova", "proximo_topico_label": "Voltar ao tópico"},
                }

                slides_antes = len(slides)
                slides_depois = len(slides_resto)

                if dry_run:
                    print(
                        f"  [DRY-RUN] Topico {topico.id} '{topico.titulo}': "
                        f"{len(slides_avaliacao_intro)} intro + {len(slides_avaliacao_pergunta)} perguntas -> "
                        f"slides: {slides_antes} -> {slides_depois} (criaria Avaliacao NOVO)"
                    )
                    avaliacao_id_placeholder = "NOVO"
                else:
                    nova_avaliacao = Avaliacao(
                        topico_id=topico.id,
                        conteudo=avaliacao_conteudo,
                        is_approved=True,
                    )
                    db.add(nova_avaliacao)
                    db.flush()  # garante nova_avaliacao.id
                    avaliacao_id_placeholder = nova_avaliacao.id
                    print(
                        f"  [APPLY] Topico {topico.id} '{topico.titulo}': "
                        f"criou Avaliacao.id={avaliacao_id_placeholder} "
                        f"({len(slides_avaliacao_intro)} intro + {len(slides_avaliacao_pergunta)} perguntas, "
                        f"slides: {slides_antes} -> {slides_depois})"
                    )

                    # Atualizar Topico.content removendo slides de avaliação
                    novo_content_dict = {**content_dict, "slides": slides_resto}
                    topico.content = json.dumps(novo_content_dict, ensure_ascii=False)

                # PASSO 2: migrar TopicoResposta com gate_id 'ef*'
                respostas_ef = (
                    db.query(TopicoResposta)
                    .filter(TopicoResposta.topico_id == topico.id, TopicoResposta.gate_id.like("ef%"))
                    .all()
                )

                if dry_run:
                    print(f"    -> {len(respostas_ef)} TopicoResposta 'ef*' seriam copiadas para AvaliacaoResposta")
                else:
                    for r in respostas_ef:
                        ar = AvaliacaoResposta(
                            user_id=r.user_id,
                            avaliacao_id=nova_avaliacao.id,
                            gate_id=r.gate_id,
                            question_id=r.question_id,
                            tipo=r.tipo,
                            resposta_dada=r.resposta_dada,
                            correta=r.correta,
                            tentativas=r.tentativas,
                            rodada=1,
                            respondido_em=r.respondido_em,
                            updated_at=r.updated_at,
                        )
                        db.add(ar)
                    print(f"    -> {len(respostas_ef)} AvaliacaoResposta criadas")

                # PASSO 3: migrar TopicoProgress -> AvaliacaoProgress
                progressos = db.query(TopicoProgress).filter(TopicoProgress.topico_id == topico.id).all()
                usuarios_com_ef = {r.user_id for r in respostas_ef}
                criados_progress = 0

                for tp in progressos:
                    if tp.user_id not in usuarios_com_ef:
                        continue

                    status_novo = "concluido" if tp.status == "concluido" else "em_andamento"

                    if dry_run:
                        print(f"    -> AvaliacaoProgress para user_id={tp.user_id} com status='{status_novo}'")
                    else:
                        ap = AvaliacaoProgress(
                            user_id=tp.user_id,
                            avaliacao_id=nova_avaliacao.id,
                            status=status_novo,
                            rodada_atual=1,
                        )
                        if status_novo == "concluido":
                            ap.tutor_veredito = tp.tutor_veredito
                            ap.tutor_analise = tp.tutor_analise
                            ap.avaliado_em = tp.avaliado_em
                            ap.iniciado_em = tp.iniciado_em
                            ap.concluido_em = tp.concluido_em
                        db.add(ap)
                        criados_progress += 1

                if not dry_run:
                    print(f"    -> {criados_progress} AvaliacaoProgress criados")

                total_migrados += 1

            except Exception as e:
                total_erros += 1
                print(f"  [ERRO] Topico {topico.id} '{topico.titulo}': {e}")
                if not dry_run:
                    raise

        # PASSO 4: commit ou rollback
        if not dry_run:
            try:
                db.commit()
                print("\n[COMMIT] Migração aplicada com sucesso.")
            except Exception as e:
                db.rollback()
                print(f"\n[ROLLBACK] Erro durante commit: {e}")
                raise

        # PASSO 5: validação final (só se --apply e sem exceção)
        if not dry_run and total_erros == 0:
            print("\n[VALIDAÇÃO] Conferindo contagens TopicoResposta 'ef*' vs AvaliacaoResposta...")
            for topico in topicos:
                avaliacao = db.query(Avaliacao).filter(Avaliacao.topico_id == topico.id).first()
                if not avaliacao:
                    continue

                count_tr = (
                    db.query(TopicoResposta)
                    .filter(TopicoResposta.topico_id == topico.id, TopicoResposta.gate_id.like("ef%"))
                    .count()
                )
                count_ar = (
                    db.query(AvaliacaoResposta)
                    .filter(AvaliacaoResposta.avaliacao_id == avaliacao.id)
                    .count()
                )

                if count_tr != count_ar:
                    print(
                        f"  [AVISO] Topico {topico.id} '{topico.titulo}': "
                        f"TopicoResposta ef*={count_tr} != AvaliacaoResposta={count_ar}"
                    )

        # Resumo final
        print("\n=== RESUMO ===")
        print(f"Tópicos migrados:      {total_migrados}")
        print(f"Pulados (já migrado):  {total_pulados_ja_migrado}")
        print(f"Pulados (sem avaliação): {total_pulados_sem_avaliacao}")
        print(f"Erros:                 {total_erros}")
        if dry_run:
            print("\nModo DRY-RUN — nenhuma alteração foi gravada. Rode com --apply para aplicar.")

    finally:
        db.close()


if __name__ == "__main__":
    main()