from sqlalchemy import Column, Integer, String, ForeignKey, CHAR, JSON, Numeric, TIMESTAMP, CheckConstraint, DateTime, \
    func
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from database.base import Base


class UsuarioModel(Base, SerializerMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'easypark'}

    id_usuario = Column('id_usuario', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, nullable=False)
    password = Column('password', String, nullable=False)
    email = Column('email', String, nullable=False)

    carros = relationship('CarroModel', back_populates='dono', cascade='all, delete-orphan')
    historicos = relationship('HistoricoModel', back_populates='usuario', cascade='all, delete-orphan')


class CarroModel(Base, SerializerMixin):
    __tablename__ = 'carro'
    __table_args__ = {'schema': 'easypark'}

    id_carro = Column('id_carro', Integer, primary_key=True, autoincrement=True)
    placa = Column('placa', String(10), nullable=False)
    id_dono = Column('id_dono', Integer, ForeignKey('easypark.usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    marca = Column('marca', String(50), nullable=False)
    modelo = Column('modelo', String(50), nullable=False)
    cor = Column('cor', String(20), nullable=False)
    cidade = Column('cidade', String(50), nullable=False)
    estado = Column('estado', CHAR(2), nullable=False)

    dono = relationship("UsuarioModel", back_populates="carros")
    historicos = relationship("HistoricoModel", back_populates="carro", cascade="all, delete-orphan")


class EstabelecimentoModel(Base, SerializerMixin):
    __tablename__ = 'estabelecimento'
    __table_args__ = {'schema': 'easypark'}

    id_estabelecimento = Column('id_estabelecimento', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255), nullable=False)
    cnpj = Column('cnpj', String(14), unique=True, nullable=False)
    cep = Column('cep', CHAR(8), nullable=False)
    dados_pagamento = Column('dados_pagamento', JSON, nullable=False)
    preco_por_hora = Column('preco_por_hora', Numeric(10, 2), nullable=False)

    sensores = relationship("SensorModel", back_populates="estabelecimento")
    historicos = relationship("HistoricoModel", back_populates="estabelecimento")


class SensorModel(Base, SerializerMixin):
    __tablename__ = 'sensor'
    __table_args__ = {'schema': 'easypark'}

    id_sensor = Column('id_sensor', Integer, primary_key=True, autoincrement=True)
    hash_sensor = Column('hash_sensor', String(64), unique=True, nullable=False)
    id_estabelecimento = Column('id_estabelecimento', Integer, ForeignKey('easypark.estabelecimento.id_estabelecimento', ondelete='CASCADE'), nullable=False)

    estabelecimento = relationship("EstabelecimentoModel", back_populates="sensores")


class RegistrosEntradaSaidaModel(Base, SerializerMixin):
    __tablename__ = 'registros_entrada_saida'
    __table_args__ = {'schema': 'easypark'}

    id_registro = Column('id_registro', Integer, primary_key=True, autoincrement=True)
    tipo_registro = Column('tipo_registro', String(10), CheckConstraint("tipo_registro IN ('entrada', 'saida')"), nullable=False)
    id_usuario = Column('id_usuario', Integer, ForeignKey('easypark.usuario.id_usuario'))
    id_carro = Column('id_carro', Integer, ForeignKey('easypark.carro.id_carro'))
    id_sensor = Column('id_sensor', Integer, ForeignKey('easypark.sensor.id_sensor'), nullable=False)
    data_hora = Column('data_hora', TIMESTAMP(timezone=True), nullable=False, default=func.now())

    usuario = relationship("UsuarioModel")
    carro = relationship("CarroModel")
    sensor = relationship("SensorModel")

class HistoricoModel(Base):
    __tablename__ = "historico"
    __table_args__ = {"schema": "easypark"}

    id_historico = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("easypark.usuario.id_usuario"), nullable=False)
    id_carro = Column(Integer, ForeignKey("easypark.carro.id_carro"), nullable=False)
    id_estabelecimento = Column(Integer, ForeignKey('easypark.estabelecimento.id_estabelecimento'), nullable=False)
    id_registro_entrada = Column(Integer, ForeignKey("easypark.registros_entrada_saida.id_registro"), nullable=False)
    id_registro_saida = Column(Integer, ForeignKey("easypark.registros_entrada_saida.id_registro"), nullable=False)
    horario_entrada = Column('horario_entrada', TIMESTAMP(timezone=True), nullable=False)
    horario_saida = Column('horario_saida', TIMESTAMP(timezone=True), nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=False)

    usuario = relationship("UsuarioModel", back_populates="historicos")
    carro = relationship("CarroModel", back_populates="historicos")
    estabelecimento = relationship("EstabelecimentoModel", back_populates="historicos")
    registro_entrada = relationship("RegistrosEntradaSaidaModel", foreign_keys=[id_registro_entrada])
    registro_saida = relationship("RegistrosEntradaSaidaModel", foreign_keys=[id_registro_saida])


# VIEWS

class ViewEstacionamentosFinalizadosModel(Base):
    __tablename__ = 'view_estacionamentos_finalizados'
    __table_args__ = {'schema': 'easypark'}

    id_historico = Column(Integer, primary_key=True)
    id_carro = Column(Integer)
    placa = Column(String(10))
    id_usuario = Column(Integer)
    nome_usuario = Column(String(255))
    nome_estabelecimento = Column(String(255))
    horario_entrada = Column(String)
    horario_saida = Column(String)
    preco_por_hora = Column(Integer)
    horas_estacionado = Column(Integer)
    valor_total = Column(Integer)
