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


class CarroBody(BaseModel):
    placa: str
    id_dono: int
    marca: str
    modelo: str
    cor: str
    cidade: str
    sigla_estado: str


class PlacaBody(BaseModel):
    placa: str
    hash_sensor: str
