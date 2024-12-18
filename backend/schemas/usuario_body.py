from pydantic import BaseModel, Field


class UsuarioBody(BaseModel):
    username: str
    password: str
    email: str = Field(None)


class LoginBody(BaseModel):
    username: str
    password: str


class Logout(BaseModel):
    token: str