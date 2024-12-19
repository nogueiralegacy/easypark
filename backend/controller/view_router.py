from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.depends import get_db_session
from services.view_service import ViewService

view_router = APIRouter(prefix='/view', tags=['View'])


@view_router.get('/historico/{id_usuario}', summary='View historico de estacionamento finalizados por usuário')
def historico(id_usuario: int, db_session: Session = Depends(get_db_session)):
    view_service = ViewService(db_session)
    estacionamentos = view_service.listar_estacionamentos_finalizados(id_usuario=id_usuario)

    if not estacionamentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum histórico encontrado para o usuário informado."
        )

    return {
        'estacionamentos_finalizados': estacionamentos
    }
