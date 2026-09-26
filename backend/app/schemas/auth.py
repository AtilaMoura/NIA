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
