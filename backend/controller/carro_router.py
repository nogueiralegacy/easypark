from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.depends import get_db_session
from schemas.schemas_body import CarroBody
from services.carro_service import CarroService

carro_router = APIRouter(prefix='/carro', tags=['Carro'])


@carro_router.post('/cadastrar', summary='Cadastro de carro')
def cadastrar_carro(carro: CarroBody, db_session: Session = Depends(get_db_session)):
    carro_service = CarroService(db_session=db_session)
    id_carro_criado = carro_service.registrar_carro(carro=carro)

    return JSONResponse(
        content={
            'msg': "Carro registrado com sucesso!",
            'id_carro': id_carro_criado
        },
        status_code=status.HTTP_201_CREATED
    )


@carro_router.get('/listar/{id_usuario}', summary='Listar carros de um usuário')
def listar_carros(id_usuario: int, db_session: Session = Depends(get_db_session)):
    carro_service = CarroService(db_session=db_session)
    carros = carro_service.listar_carros_por_usuario(id_usuario=id_usuario)

    if not carros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum carro encontrado para o usuário informado."
        )

    return carros