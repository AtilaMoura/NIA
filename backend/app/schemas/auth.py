from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

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
