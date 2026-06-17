from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS GET ---

@app.get("/")
def read_root():
    """Ruta raíz para que Render no muestre error 404"""
    return {"mensaje": "API de ExitPoll operativa"}

@app.get("/api/v1/salud")
def salud():
    """Endpoint para monitoreo de Render"""
    return {"status": "ok"}

@app.get("/reset-admin")
def reset_admin(db: Session = Depends(get_db)):
    """Resetea el usuario administrador"""
    db.query(Usuario).delete()
    nuevo_user = Usuario(username="admin", password_hash=get_password_hash("123456"))
    db.add(nuevo_user)
    db.commit()
    return {"mensaje": "Reseteo exitoso"}

@app.get("/ver-votos")
def listar_votos(db: Session = Depends(get_db)):
    """Consulta todos los votos registrados"""
    return db.query(VotoDB).all()

# --- ENDPOINTS POST ---

class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

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

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    nuevo_voto = VotoDB(**voto.model_dump())
    db.add(nuevo_voto)
    db.commit()
    return {"mensaje": "Voto registrado con éxito"}