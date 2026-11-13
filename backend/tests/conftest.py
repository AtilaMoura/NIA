"""Fixtures dos testes — rodam contra o Postgres LOCAL (docker nia_db, localhost:5432).

Isolamento: cada teste roda dentro de uma transação externa com SAVEPOINT; os commits do
código viram "release savepoint" e no fim tudo é desfeito (rollback). Nada é gravado de
verdade e nenhum dado pré-existente é apagado. A senha vem do backend/.env em memória.
Recusa rodar se o banco não for localhost (nunca contra produção).
"""
import os
import sys
import uuid
from pathlib import Path

import pytest
from dotenv import dotenv_values

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

# DATABASE_URL precisa estar definida ANTES de importar app.database.
_url = os.environ.get("TEST_DATABASE_URL") or (dotenv_values(AQUI.parent / ".env").get("DATABASE_URL") or "")
_url = _url.replace("@db:", "@localhost:")
if not _url:
    raise RuntimeError("Defina TEST_DATABASE_URL ou DATABASE_URL no backend/.env (banco LOCAL).")
_host = _url.split("@")[-1].split("/")[0].split(":")[0]
if _host not in ("localhost", "127.0.0.1"):
    raise RuntimeError(f"Os testes só rodam em banco local (host atual: {_host}).")
os.environ["DATABASE_URL"] = _url

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core.auth import get_current_user  # noqa: E402
from app.database import engine, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.models import (  # noqa: E402
    Course, CourseTutor, Lesson, Module, Topico, TopicoAnotacao, User,
)


@pytest.fixture()
def db():
    conexao = engine.connect()
    transacao = conexao.begin()
    sessao = Session(bind=conexao, join_transaction_mode="create_savepoint")
    try:
        yield sessao
    finally:
        sessao.close()
        transacao.rollback()
        conexao.close()


@pytest.fixture()
def cenario(db):
    """Curso > módulo > aula > tópico publicado, e usuários de cada perfil."""
    sufixo = uuid.uuid4().hex[:8]

    contador = iter(range(1, 100))

    def novo_user(papel):
        u = User(email=f"teste-{papel}-{next(contador)}-{sufixo}@exemplo.test", name=f"Teste {papel}", role=papel)
        db.add(u)
        db.flush()
        return u

    def novo_topico(lesson, indice):
        t = Topico(lesson_id=lesson.id, topico_index=indice, titulo=f"Tópico teste {indice}",
                   content='{"slides": []}', is_approved=True)
        db.add(t)
        db.flush()
        return t

    curso = Course(title=f"Curso teste {sufixo}", level="básico", duration_hours=1, structure={}, status="published")
    db.add(curso)
    db.flush()
    modulo = Module(course_id=curso.id, module_index=1, title="Módulo teste", duration_hours=1)
    db.add(modulo)
    db.flush()
    aula = Lesson(module_id=modulo.id, lesson_index=1, title="Aula teste")
    db.add(aula)
    db.flush()
    topico = novo_topico(aula, 1)

    outro_curso = Course(title=f"Outro curso {sufixo}", level="básico", duration_hours=1, structure={}, status="published")
    db.add(outro_curso)
    db.flush()

    aluno, master, admin = novo_user("aluno"), novo_user("master"), novo_user("admin")
    prof_tutor, prof_fora = novo_user("professor"), novo_user("professor")
    db.add(CourseTutor(course_id=curso.id, user_id=prof_tutor.id))
    # prof_fora é tutor só de OUTRO curso
    db.add(CourseTutor(course_id=outro_curso.id, user_id=prof_fora.id))
    db.flush()

    class C:  # noqa: N801
        pass

    c = C()
    c.db, c.curso, c.topico, c.aula = db, curso, topico, aula
    c.aluno, c.master, c.admin, c.prof_tutor, c.prof_fora = aluno, master, admin, prof_tutor, prof_fora
    c.novo_topico = lambda indice=2: novo_topico(aula, indice)
    c.nova_anotacao = lambda user, topico, slide=0, texto="ajustar isto": _anotacao(db, user, topico, slide, texto)
    return c


def _anotacao(db, user, topico, slide, texto):
    a = TopicoAnotacao(user_id=user.id, topico_id=topico.id, slide_index=slide, texto=texto)
    db.add(a)
    db.flush()
    return a


@pytest.fixture()
def api(db):
    """TestClient com o banco da transação do teste e o usuário escolhido por header X-Teste-User."""
    def _get_db():
        yield db

    def _usuario(request: __import__("fastapi").Request):
        uid = request.headers.get("x-teste-user")
        if not uid:
            from fastapi import HTTPException
            raise HTTPException(401, "sem usuário no teste")
        return db.query(User).filter(User.id == int(uid)).first()

    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[get_current_user] = _usuario
    cliente = TestClient(app)
    yield cliente
    app.dependency_overrides.clear()


def como(user):
    """Cabeçalho que diz ao TestClient quem está logado."""
    return {"X-Teste-User": str(user.id)}
