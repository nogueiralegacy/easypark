from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.placa_service import PlacaService
from schemas.schemas_body import PlacaBody
from database.depends import get_db_session
from fastapi.responses import JSONResponse

placa_router = APIRouter(prefix='/placa', tags=['Placa'])


@placa_router.post('/verificar', summary='Verificar se placa está cadastrada')
def verificar_placa(placa_body: PlacaBody, db_session: Session = Depends(get_db_session)):
    placa_service = PlacaService(db_session=db_session)

    sensor_cadastrado = placa_service.verificar_hash_sensor(hash=placa_body.hash_sensor)
    if not sensor_cadastrado:
        return JSONResponse(
            content={
                'msg': "Sensor não cadastrado"
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    placa_cadastrada = placa_service.verificar_placa(placa=placa_body.placa)
    if placa_cadastrada:
        return JSONResponse(
            content={
                'msg': "Placa cadastrada",
                "status": True
            },
            status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={
                'msg': "Placa não cadastrada",
                "status": False
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
