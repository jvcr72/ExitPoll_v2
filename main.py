from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, SessionLocal
import os
import models # Asegúrate de que models.py tenga las clases Usuario y CentroVotacion

app = FastAPI()

# Modelo de la tabla Votos
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

# Esquema para validación de datos
class VotoSchema(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    centro_electoral: str
    mesa: str
    direccion_vivienda: str
    numero_telefonico: str
    candidato: str
    edad: int

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db)):
    try:
        nuevo_voto = VotoDB(**voto.model_dump()) # Usamos model_dump() en lugar de dict() para versiones recientes de Pydantic
        db.add(nuevo_voto)
        db.commit()
        db.refresh(nuevo_voto)
        return {"mensaje": "Voto registrado correctamente", "id": nuevo_voto.id}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

@app.get("/ver-votos")
def listar_votos(db: Session = Depends(get_db)):
    db.rollback()
    votos = db.query(VotoDB).all()
    return votos

@app.get("/debug-tablas")
def debug_tablas():
    inspector = inspect(engine)
    return {"tablas_encontradas": inspector.get_table_names()}

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}