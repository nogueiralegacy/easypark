from sqlalchemy.orm import Session
from models.models import ViewEstacionamentosFinalizadosModel


class ViewService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def listar_estacionamentos_finalizados(self, id_usuario: int):
        estacionamentos_finalizados = self.db_session.query(ViewEstacionamentosFinalizadosModel).filter_by(id_usuario=id_usuario).all()
        return estacionamentos_finalizados
    