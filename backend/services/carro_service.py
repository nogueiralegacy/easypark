from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import CarroModel
from schemas.schemas_body import CarroBody


class CarroService:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def registrar_carro(self, carro: CarroBody):
        carro_model = CarroModel(
            placa=carro.placa,
            id_dono=carro.id_dono,
            marca=carro.marca,
            modelo=carro.modelo,
            cor=carro.cor,
            cidade=carro.cidade,
            estado=carro.sigla_estado
        )

        try:
            self.db_session.add(carro_model)
            self.db_session.commit()
            return carro_model.id_carro  # Retornar novo id do carro
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao registrar novo carro."
            )


    def listar_carros_por_usuario(self, id_usuario: int):
        carros = self.db_session.query(CarroModel).filter_by(id_dono=id_usuario).all()
        return [
            {
                "id_carro": carro.id_carro,
                "placa": carro.placa,
                "marca": carro.marca,
                "modelo": carro.modelo,
                "cor": carro.cor,
                "cidade": carro.cidade,
                "estado": carro.estado
            }
            for carro in carros
        ]
