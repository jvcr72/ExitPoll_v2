from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class CentroDeVotacion(Base):
    __tablename__ = "centros_de_votacion"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    direccion = Column(String)
    codigo_centro = Column(String, unique=True)

class Skippin(Base): # He corregido el nombre de la clase según lo solicitado
    __tablename__ = "skippines"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    identificador = Column(String)
    centro_id = Column(Integer, ForeignKey("centros_de_votacion.id"))

class VotoDB(Base):
    __tablename__ = "votos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    cedula = Column(String)
    centro_electoral = Column(String)
    mesa = Column(String)
    direccion_vivienda = Column(String)
    numero_telefonico = Column(String)
    candidato = Column(String)
    edad = Column(Integer)