from datetime import datetime

import pytz
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.models import CarroModel, SensorModel, RegistrosEntradaSaidaModel, EstabelecimentoModel, HistoricoModel


class RegistroService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def registrar_movimentacao(self, placa: str, hash_sensor: str):
        # 1. Obter o carro com a placa já validada
        carro = self.db_session.query(CarroModel).filter_by(placa=placa).first()

        # 2. Obter o sensor com a hash já validada
        sensor = self.db_session.query(SensorModel).filter_by(hash_sensor=hash_sensor).first()

        # 3. Determinar o tipo de registro (entrada/saída)
        num_registros = (
            self.db_session.query(func.count(RegistrosEntradaSaidaModel.id_registro))
            .filter(
                RegistrosEntradaSaidaModel.id_usuario == carro.id_dono,
                RegistrosEntradaSaidaModel.id_carro == carro.id_carro
            )
            .scalar()
        )
        tipo_registro = 'entrada' if num_registros % 2 == 0 else 'saida'

        # 4. Criar o registro na tabela registros_entrada_saida
        novo_registro = RegistrosEntradaSaidaModel(
            tipo_registro=tipo_registro,
            id_usuario=carro.id_dono,
            id_carro=carro.id_carro,
            id_sensor=sensor.id_sensor
        )

        try:
            self.db_session.add(novo_registro)
            self.db_session.commit()

            if tipo_registro == 'saida':
                self.registrar_historico(carro=carro, registro_saida=novo_registro, sensor=sensor)

            return {
                'id_registro': novo_registro.id_registro,
                'tipo_registro': novo_registro.tipo_registro,
                'data_hora': novo_registro.data_hora.isoformat()
            }
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                detail=f"Erro ao registrar movimentação: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )


    def registrar_historico(self, carro: CarroModel, registro_saida: RegistrosEntradaSaidaModel, sensor: SensorModel):
        # 1. Localizar o último registro de entrada
        registro_entrada = (
            self.db_session.query(RegistrosEntradaSaidaModel)
            .filter(
                RegistrosEntradaSaidaModel.id_usuario == carro.id_dono,
                RegistrosEntradaSaidaModel.id_carro == carro.id_carro,
                RegistrosEntradaSaidaModel.tipo_registro == 'entrada'
            )
            .order_by(RegistrosEntradaSaidaModel.data_hora.desc())
            .first()
        )

        if not registro_entrada:
            raise HTTPException(
                detail="Não foi possível localizar o registro de entrada correspondente.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # 2. Buscar o preço por hora do estabelecimento
        preco_por_hora = (
            self.db_session.query(EstabelecimentoModel.preco_por_hora)
            .filter_by(id_estabelecimento=sensor.id_estabelecimento)
            .scalar()
        )

        if preco_por_hora is None:
            raise HTTPException(
                detail="Preço por hora não configurado para o estabelecimento.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # 3. Calcular o tempo e o valor
        tempo_permanencia = registro_saida.data_hora - registro_entrada.data_hora
        horas = tempo_permanencia.total_seconds() / 3600
        valor_pago = round(horas * float(preco_por_hora), 2)

        # 4. Inserir na tabela historico
        novo_historico = HistoricoModel(
            id_usuario=carro.id_dono,
            id_carro=carro.id_carro,
            id_estabelecimento=sensor.id_estabelecimento,
            id_registro_entrada=registro_entrada.id_registro,
            id_registro_saida=registro_saida.id_registro,
            horario_entrada=registro_entrada.data_hora,
            horario_saida=registro_saida.data_hora,
            valor_pago=valor_pago
        )

        try:
            self.db_session.add(novo_historico)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise HTTPException(
                detail=f"Erro ao registrar histórico: {str(e)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )


    def sessao_estacionamento(self, id_usuario: int):
        if self.sessao_ativa_estacionamento(id_usuario=id_usuario):
            carro = self.db_session.query(CarroModel).filter_by(id_dono=id_usuario).first()
            registro_entrado = (
                self.db_session.query(RegistrosEntradaSaidaModel)
                .filter(
                    RegistrosEntradaSaidaModel.id_usuario == id_usuario,
                    RegistrosEntradaSaidaModel.id_carro == carro.id_carro,
                    RegistrosEntradaSaidaModel.tipo_registro == 'entrada'
                )
                .order_by(RegistrosEntradaSaidaModel.data_hora.desc())
                .first()
            )

            tempo_permanencia = datetime.utcnow().replace(tzinfo=pytz.UTC) - registro_entrado.data_hora.astimezone(pytz.UTC)
            return {
                'is_sessao_ativa': True,
                'msg': 'Sessao ativa no estacionamento',
                'dados_sessao': {
                    'horario_entrada': registro_entrado.data_hora,
                    'tempo_sessao_ativa_em_minutos': tempo_permanencia.total_seconds() // 60,
                    'carro': carro
                }
            }
        else:
            return {
                'is_sessao_ativa': False,
                'msg': 'Nenhuma sessao ativa no estacionamento'
            }

    def sessao_ativa_estacionamento(self, id_usuario: int):
        carro = self.db_session.query(CarroModel).filter_by(id_dono=id_usuario).first()

        num_registros = (
            self.db_session.query(func.count(RegistrosEntradaSaidaModel.id_registro))
            .filter(
                RegistrosEntradaSaidaModel.id_usuario == carro.id_dono,
                RegistrosEntradaSaidaModel.id_carro == carro.id_carro
            )
            .scalar()
        )
        tipo_registro = 'entrada' if num_registros % 2 == 0 else 'saida'

        return tipo_registro != 'entrada'
