from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from auth import hash_password, verify_password, create_access_token, get_current_user
import models 
from models import Usuario

app = FastAPI()

# --- Configuración de CORS (Prioridad Alta) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Base de Datos ---
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

# --- Esquemas Pydantic ---
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

class UserSchema(BaseModel):
    username: str
    password: str

# --- Dependencia de DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---
@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed = hash_password(user.password)
    nuevo_usuario = Usuario(username=user.username, password=hashed)
    db.add(nuevo_usuario)
    db.commit()
    return {"mensaje": "Usuario registrado exitosamente"}

@app.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/voto")
def registrar_voto(
    voto: VotoSchema, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        nuevo_voto = VotoDB(**voto.model_dump())
        db.add(nuevo_voto)
        db.commit()
        db.refresh(nuevo_voto)
        return {"mensaje": f"Voto registrado por {current_user}", "id": nuevo_voto.id}
    except Exception as e:
        db.rollback()
        # Esto te permitirá ver el error real en los logs de Render
        print(f"Error al registrar voto: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ver-votos")
def listar_votos(db: Session = Depends(get_db)):
    return db.query(VotoDB).all()

@app.get("/api/v1/salud")
def check_salud():
return {"status": "conectado-v2"}