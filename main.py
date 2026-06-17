from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from models import Usuario, VotoDB
from pydantic import BaseModel

# Forzar eliminación y recreación limpia
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

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
        nuevo_user = Usuario(username="admin", password_hash=get_password_hash("123456"))
        db.add(nuevo_user)
        db.commit()
        return {"mensaje": "Reseteo exitoso con SHA-256 limpio"}
    except Exception as e:
        return {"error_critico": str(e)}

# ... resto de tus endpoints (voto, login) ...
# Asegúrate de usar 'password_hash' al validar en el login