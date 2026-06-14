from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal, Base
from auth import hash_password, verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB 

# Inicialización segura
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error al inicializar tablas: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquemas necesarios
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

# Dependencia necesaria
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    nuevo_voto = VotoDB(**voto.model_dump())
    db.add(nuevo_voto)
    db.commit()
    db.refresh(nuevo_voto)
    return {"mensaje": "Voto registrado", "id": nuevo_voto.id}

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado-v2"}