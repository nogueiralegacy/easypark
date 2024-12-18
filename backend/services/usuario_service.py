from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decouple import config
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from jose import jwt, JWTError
from email_validator import EmailNotValidError, validate_email

from models.usuario_model import UsuarioModel
from schemas.usuario_body import UsuarioBody

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=['sha256_crypt'])


class UsuarioService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def registrar_usuario(self, usuario: UsuarioBody):
        if not self.validar_email(usuario.email):
            raise HTTPException(
                detail='Endereço de email invalido',
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )

        usuario_model = UsuarioModel(username=usuario.username, password=usuario.password, email=usuario.email)

        username_ja_cadastrado = self.db_session.query(UsuarioModel).filter_by(username=usuario.username).first()
        email_ja_cadastrado = self.db_session.query(UsuarioModel).filter_by(email=usuario.email).first()
        if username_ja_cadastrado is not None or email_ja_cadastrado is not None:
            raise HTTPException(
                detail="Username ou email já cadastrados para outro usuário!",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            self.db_session.add(usuario_model)
            self.db_session.commit()
            return usuario_model.id_usuario  # Retornar novo id usuario
        except IntegrityError:
            raise HTTPException(
                detail="Erro ao registrar novo usuario",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def validar_email(self, email: str):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False


    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token de acesso inválido'
            )

        usuario_cadastrado = self.db_session.query(UsuarioModel).filter_by(username=data['sub']).first()
        if usuario_cadastrado is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token de acesso invalido.'
            )
