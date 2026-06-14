from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal, Base
from auth import hash_password, verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB

# IMPORTANTE: Crear tablas fuera de la ejecución de rutas, pero protegidas
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error al crear tablas: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado-v2"}

# ... resto de tus rutas ...