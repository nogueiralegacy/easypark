from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.depends import get_db_session, token_verifier
from schemas.usuario_body import UsuarioBody, LoginBody, Logout
from services.usuario_service import UsuarioService

db_session: Session = Depends(get_db_session)
usuario_router = APIRouter(prefix='/usuario', tags=['Usuario'])


@usuario_router.post('/cadastro', summary='Cadastro de usuario')
def cadastrar_usuario(usuario: UsuarioBody, db_session: Session = Depends(get_db_session)):
    usuario_service = UsuarioService(db_session=db_session)
    id_usuario_criado = usuario_service.registrar_usuario(usuario=usuario)

    return JSONResponse(
        content={
            'msg': "Usuário registrado com sucesso!",
            'id_login': id_usuario_criado
        },
        status_code=status.HTTP_201_CREATED
    )


@usuario_router.post('/login', summary='Login')
def realizar_login(login: LoginBody, db_session: Session = Depends(get_db_session)):
    usuario_service = UsuarioService(db_session=db_session)
    usuario_body = UsuarioBody(username=login.username, password=login.password)
    auth_data = usuario_service.login_usuario(usuario=usuario_body)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )


@usuario_router.post('/logout', summary='Rota para o usuario realizar logout')
def logout_usuario(token: Logout, db_session: Session = Depends(get_db_session)):
    usuario_service = UsuarioService(db_session=db_session)
    new_token = usuario_service.logout_usuario(token.token)
    return JSONResponse(
        content={"message": "Logout realizado com sucesso", "new_token": new_token},
        status_code=status.HTTP_200_OK
    )
