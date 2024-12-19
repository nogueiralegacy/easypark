from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decouple import config
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi import status
from jose import jwt, JWTError
from email_validator import EmailNotValidError, validate_email
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from models.models import UsuarioModel
from schemas.schemas_body import UsuarioBody

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

        usuario_model = UsuarioModel(
            username=usuario.username,
            password=crypt_context.hash(usuario.password),
            email=usuario.email
        )

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


    def login_usuario(self, usuario: UsuarioBody, expires_in: int = 60):
        usuario_cadastrado = self.db_session.query(UsuarioModel).filter_by(username=usuario.username).first()

        if usuario_cadastrado is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Usuário ou senha incorretos'
            )

        if not crypt_context.verify(usuario.password, usuario_cadastrado.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Usuário ou senha incorretos.'
            )

        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': usuario_cadastrado.username,
            'exp': exp,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat(),
            'id_usuario': usuario_cadastrado.id_usuario,
        }


    def logout_usuario(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            payload = None

        if payload:
            payload['exp'] = datetime.utcnow()
            return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        else:
            return JSONResponse(
                content={"message": "Token inválido ou expirado"},
                status_code=status.HTTP_400_BAD_REQUEST
            )


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
