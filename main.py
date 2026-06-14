from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from auth import verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB

app = FastAPI()

# Esquemas
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

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET para el Frontend
@app.get("/")
def read_root():
    return FileResponse("index.html")

# 2. GET para el diagnóstico de usuarios
@app.get("/ver-usuarios")
def ver_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()
        return [{"username": u.username} for u in usuarios]
    except Exception as e:
        return {"error": str(e)}

# 3. GET para salud del sistema
@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}

# Rutas POST (necesarias para el flujo completo)
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    nuevo_voto = VotoDB(**voto.model_dump())
    db.add(nuevo_voto)
    db.commit()
    return {"mensaje": "Voto registrado con éxito"}