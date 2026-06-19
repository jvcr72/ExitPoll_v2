from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Censo
from database import get_db

app = FastAPI()

# 1. Búsqueda y Validación (Paso 1 y 2 del usuario)
@app.get("/buscar-persona/{cedula}")
def buscar_persona(cedula: str, db: Session = Depends(get_db)):
    persona = db.query(Censo).filter(Censo.cedula == cedula).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Cédula no encontrada")
    if persona.voto_registrado:
        raise HTTPException(status_code=400, detail="Esta persona ya ejerció su derecho")
    
    return {
        "nombre": persona.nombre, 
        "centro_electoral": persona.centro_electoral
    }

# 2. Listado de Centros (Para el desplegable inicial)
@app.get("/obtener-centros")
def obtener_centros(db: Session = Depends(get_db)):
    centros = db.query(Censo.centro_electoral).distinct().all()
    # Retorna solo los nombres de los centros
    return [c[0] for c in centros]

# 3. Datos para el Centro de Totalización
@app.get("/totalizacion")
def obtener_totalizacion(db: Session = Depends(get_db)):
    total_censo = db.query(Censo).count()
    votos_emitidos = db.query(Censo).filter(Censo.voto_registrado == True).all()
    
    conteo = {}
    for v in votos_emitidos:
        c = v.candidato_votado
        conteo[c] = conteo.get(c, 0) + 1
        
    return {
        "total_censo": total_censo,
        "total_votos": len(votos_emitidos),
        "faltan_por_votar": total_censo - len(votos_emitidos),
        "por_candidato": conteo
    }

# 4. Registro de Voto (Endpoint adicional necesario para completar el flujo)
@app.post("/registrar-voto")
def registrar_voto(cedula: str, candidato: str, db: Session = Depends(get_db)):
    persona = db.query(Censo).filter(Censo.cedula == cedula).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Cédula no encontrada")
    if persona.voto_registrado:
        raise HTTPException(status_code=400, detail="Voto duplicado")
    
    persona.voto_registrado = True
    persona.candidato_votado = candidato
    db.commit()
    return {"message": "Voto registrado exitosamente"}