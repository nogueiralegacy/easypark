from sqlalchemy import Column, String, Integer, Date, ForeignKey
from database.base import Base
from sqlalchemy_serializer import SerializerMixin


class UsuarioModel(Base, SerializerMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'easypark'}

    id_usuario = Column('id_usuario', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, nullable=False)
    password = Column('password', String, nullable=False)
    email = Column('email', String, nullable=False)
