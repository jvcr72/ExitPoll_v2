from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from models import VotoDB
from database import get_db, engine, Base
import secrets

# Inicializamos la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

# Lógica de autenticación
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, "admin")
    correct_pass = secrets.compare_digest(credentials.password, "123456")
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Acceso denegado"
        )
    return credentials.username

# --- Aquí irían tus endpoints ---
# Ejemplo de cómo usar get_db en tus rutas:
# @app.post("/voto")
# def registrar_voto(voto: VotoSchema, db: Session = Depends(get_db)):
#     ...