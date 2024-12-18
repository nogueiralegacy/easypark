from pydantic import BaseModel


class UsuarioBody(BaseModel):
    username: str
    password: str
    email: str