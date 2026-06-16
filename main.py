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

@app.get("/reset-admin")
def reset_admin(db: Session = Depends(get_db)):
    try:
        db.query(Usuario).delete()
        db.commit()
        nuevo_user = Usuario(username="admin", password=get_password_hash("123456"))
        db.add(nuevo_user)
        db.commit()
        return {"mensaje": "Base de datos inicializada con SHA-256"}
    except Exception as e:
        return {"error": str(e)}

# Login actualizado para usar la nueva verificación
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