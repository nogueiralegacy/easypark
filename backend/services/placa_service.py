from sqlalchemy.orm import Session
from models.models import CarroModel, SensorModel
from sqlalchemy.exc import SQLAlchemyError


class PlacaService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def verificar_hash_sensor(self, hash: str) -> bool:
        try:
            sensor = self.db_session.query(SensorModel).filter_by(hash_sensor=hash).first()
            return sensor is not None
        except SQLAlchemyError as e:
            raise e


    def verificar_placa(self, placa: str) -> bool:
        try:
            carro = self.db_session.query(CarroModel).filter_by(placa=placa).first()
            return carro is not None
        except SQLAlchemyError as e:
            raise e
