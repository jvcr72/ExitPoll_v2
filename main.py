from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import text
from database import SessionLocal
from auth import verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# PRUEBA DE CONEXIÓN
@app.on_event("startup")
def test_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        logger.info("--- CONEXIÓN EXITOSA ---")
    except Exception as e:
        logger.error(f"--- FALLO DE CONEXIÓN: {e} ---")
    finally:
        db.close()

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/ver-usuarios")
def ver_usuarios(db: Session = Depends(SessionLocal)):
    try:
        usuarios = db.query(Usuario).all()
        return [{"username": u.username} for u in usuarios]
    except Exception as e:
        return {"error": str(e)}

@app.post("/login")
def login(data: dict, db: Session = Depends(SessionLocal)):
    # ... (login logic)
    return {"status": "ok"}