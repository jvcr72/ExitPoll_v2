from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

# Definir el modelo de la tabla para que se cree en PostgreSQL
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

# Esto crea la tabla "votos" en tu base de datos automáticamente
Base.metadata.create_all(bind=engine)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db)):
    # Crear un objeto de base de datos con los datos recibidos
    nuevo_voto = VotoDB(**voto.dict())
    db.add(nuevo_voto)
    db.commit()
    db.refresh(nuevo_voto)
    return {"mensaje": "Voto registrado correctamente en la base de datos"}

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}
@app.get("/ver-votos")
def listar_votos(db: Session = Depends(get_db)):
    votos = db.query(VotoDB).all()
    return votos