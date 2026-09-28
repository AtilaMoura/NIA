from pydantic import BaseModel, field_validator


def _normalizar_email(valor: str) -> str:
    # E-mail não diferencia maiúscula/minúscula: "Fulano@Gmail.com" e
    # "fulano@gmail.com" são a mesma conta. Guardamos e comparamos sempre em minúsculas.
    return valor.strip().lower()


class UserLogin(BaseModel):
    email: str
    password: str

    _email_normalizado = field_validator("email")(_normalizar_email)

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

    _email_normalizado = field_validator("email")(_normalizar_email)

class TrocarSenha(BaseModel):
    """Troca de senha pelo próprio usuário logado (perfil, 2026-09-27)."""
    senha_atual: str
    senha_nova: str

    @field_validator("senha_nova")
    @classmethod
    def _tamanho_minimo(cls, valor: str) -> str:
        # Mesma regra do cadastro no front (mínimo 6)
        if len(valor) < 6:
            raise ValueError("A nova senha precisa ter pelo menos 6 caracteres.")
        return valor


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TopicoTokenRequest(BaseModel):
    topico_id: int


class AvaliacaoTokenRequest(BaseModel):
    avaliacao_id: int


class UserMe(BaseModel):
    id: int
    name: str | None = None
    email: str
    role: str
    preferred_theme: str | None = None

    class Config:
        from_attributes = True
