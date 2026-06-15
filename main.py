from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
from database import SessionLocal
from auth import verify_password, create_access_token, get_current_user, get_password_hash
from models import Usuario, VotoDB

# --- DIAGNÓSTICO DE ESTRUCTURA ---
print("DIRECTORIO ACTUAL:", os.getcwd())
print("ARCHIVOS EN EL DIRECTORIO:", os.listdir())
# ---------------------------------

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/reset-admin")
def reset_admin(db: Session = Depends(get_db)):
    try:
        db.query(Usuario).delete()
        db.commit()
        nuevo_user = Usuario(username="admin", password=get_password_hash("123456"))
        db.add(nuevo_user)
        db.commit()
        return {"mensaje": "Base de datos reseteada. Usuario: admin, Password: 123456"}
    except Exception as e:
        return {"error_detallado": str(e)}

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/ver-usuarios")
def ver_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()
        return [{"username": u.username} for u in usuarios]
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}

class LoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
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