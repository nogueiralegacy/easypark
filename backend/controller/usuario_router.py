from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.depends import get_db_session, token_verifier
from schemas.usuario_body import UsuarioBody
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