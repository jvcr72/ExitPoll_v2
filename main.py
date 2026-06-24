from fastapi import FastAPI, HTTPException
from database import supabase

app = FastAPI()

@app.post("/voto")
def registrar_voto(nombre: str, opcion: str):
    try:
        # Usamos el nombre de tabla exacto: "Votos"
        data = {
            "nombre": nombre,
            "opcion": opcion
        }
        
        # Ejecutamos la inserción
        response = supabase.table("Votos").insert(data).execute()
        
        return {"message": "Voto registrado con éxito", "data": response.data}
    
    except Exception as e:
        # Si algo falla, el error nos dirá exactamente por qué
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "API de Votación Activa"}