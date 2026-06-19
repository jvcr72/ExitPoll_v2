from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from models import VotoDB
from database import get_db, engine, Base
import secrets

Base.metadata.create_all(bind=engine)
app = FastAPI()
security = HTTPBasic()

# Función de normalización para asegurar que los centros se unan correctamente
def normalizar_nombre(nombre: str):
    if not nombre: return "Sin Centro"
    return nombre.strip().upper()

# Protección de acceso
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, "admin")
    correct_pass = secrets.compare_digest(credentials.password, "123456")
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acceso denegado")
    return credentials.username

# Endpoint de registro con normalización automática
@app.post("/registrar-voto")
def registrar_voto(cedula: str, candidato: str, db: Session = Depends(get_db)):
    persona = db.query(VotoDB).filter(VotoDB.cedula == cedula).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Cédula no encontrada")
    
    # Normalizamos el centro al registrar (aunque ya debería estar bien)
    persona.centro_electoral = normalizar_nombre(persona.centro_electoral)
    persona.voto_registrado = True
    persona.candidato = candidato
    db.commit()
    return {"message": "Voto registrado correctamente"}

# Endpoint de totalización con data unificada
@app.get("/totalizacion")
def obtener_totalizacion(centro: str = None, db: Session = Depends(get_db)):
    query = db.query(VotoDB)
    
    # Si filtran por centro, también normalizamos el filtro
    if centro:
        centro_norm = normalizar_nombre(centro)
        query = query.filter(VotoDB.centro_electoral == centro_norm)
    
    votos_emitidos = query.filter(VotoDB.voto_registrado == True).all()
    
    conteo = {}
    for v in votos_emitidos:
        c = v.candidato if v.candidato else "Sin Voto"
        conteo[c] = conteo.get(c, 0) + 1
        
    return {
        "centro": centro if centro else "Todos los centros",
        "total_votos": len(votos_emitidos),
        "por_candidato": conteo
    }