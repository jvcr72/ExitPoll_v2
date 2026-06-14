from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import engine, SessionLocal, Base
from auth import hash_password, verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB

# --- GESTIÓN DE ARRANQUE PARA LA BASE DE DATOS ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto asegura que la conexión se intente cuando el servidor ya esté listo
    try:
        Base.metadata.create_all(bind=engine)
        print("Base de datos y tablas inicializadas correctamente.")
    except Exception as e:
        print(f"Error crítico al iniciar la base de datos: {e}")
    yield
    # Código de limpieza al apagar (si fuera necesario)

app = FastAPI(lifespan=lifespan)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquemas Pydantic
class LoginSchema(BaseModel):
    username: str
    password: str

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

# RUTA LOGIN
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# RUTA VOTO
@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    nuevo_voto = VotoDB(**voto.model_dump())
    db.add(nuevo_voto)
    db.commit()
    db.refresh(nuevo_voto)
    return {"mensaje": "Voto registrado con éxito"}

# RUTA SALUD
@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado-v2"}