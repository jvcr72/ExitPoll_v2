from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import VotoDB # Cambiado de Censo a VotoDB
from database import get_db, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/buscar-persona/{cedula}")
def buscar_persona(cedula: str, db: Session = Depends(get_db)):
    persona = db.query(VotoDB).filter(VotoDB.cedula == cedula).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Cédula no encontrada")
    if persona.voto_registrado:
        raise HTTPException(status_code=400, detail="Esta persona ya ejerció su derecho")
    return {"nombre": f"{persona.nombre} {persona.apellido}", "centro_electoral": persona.centro_electoral}

@app.post("/registrar-voto")
def registrar_voto(cedula: str, candidato: str, db: Session = Depends(get_db)):
    persona = db.query(VotoDB).filter(VotoDB.cedula == cedula).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Cédula no encontrada")
    if persona.voto_registrado:
        raise HTTPException(status_code=400, detail="Voto duplicado")
    
    persona.voto_registrado = True
    persona.candidato = candidato
    db.commit()
    return {"message": "Voto registrado exitosamente"}

@app.get("/totalizacion")
def obtener_totalizacion(db: Session = Depends(get_db)):
    total_votantes = db.query(VotoDB).count()
    votos_emitidos = db.query(VotoDB).filter(VotoDB.voto_registrado == True).all()
    
    conteo = {}
    for v in votos_emitidos:
        c = v.candidato
        conteo[c] = conteo.get(c, 0) + 1
        
    return {
        "total_censo": total_votantes,
        "total_votos": len(votos_emitidos),
        "por_candidato": conteo
    }