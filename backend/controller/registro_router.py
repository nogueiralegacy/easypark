from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.depends import get_db_session
from schemas.schemas_body import PlacaBody
from services.registro_service import RegistroService

registro_router = APIRouter(prefix='/registro', tags=['Registro'])


@registro_router.post('/registrar', summary='Registrar entrada/saída do veículo')
def registrar_movimentacao(placa_body: PlacaBody, db_session: Session = Depends(get_db_session)):
    registro_service = RegistroService(db_session=db_session)

    resultado = registro_service.registrar_movimentacao(
        placa=placa_body.placa,
        hash_sensor=placa_body.hash_sensor
    )

    return JSONResponse(
        content={
            'msg': 'Registro realizado com sucesso!',
            'dados_registro': resultado
        },
        status_code=status.HTTP_201_CREATED
    )


@registro_router.get('/sessao/{id_usuario}', summary='Verificar se a sessão está ativa')
def sessao_esticionamento(id_usuario: int, db_session: Session = Depends(get_db_session)):
    registro_service = RegistroService(db_session=db_session)
    sessao = registro_service.sessao_estacionamento(id_usuario=id_usuario)
    return sessao
