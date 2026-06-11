from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class CentroVotacion(Base):
    __tablename__ = "centros_votacion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    centro_id = Column(Integer, ForeignKey("centros_votacion.id"))