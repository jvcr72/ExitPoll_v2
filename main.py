from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal, Base
from auth import hash_password, verify_password, create_access_token, get_current_user
# Aquí importamos ambos desde models
from models import Usuario, VotoDB 

# Inicialización segura
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error al inicializar tablas: {e}")

app = FastAPI()

# ... (resto de tu configuración de CORS y rutas) ...

@app.post("/voto")
def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Esto funcionará porque VotoDB viene de models.py
    nuevo_voto = VotoDB(**voto.model_dump())
    db.add(nuevo_voto)
    db.commit()
    return {"mensaje": "Voto registrado"}