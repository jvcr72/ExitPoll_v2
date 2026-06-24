from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client
import os

# Configuración (Usa variables de entorno por seguridad)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="API ExitPoll v2")

# Definición de modelo para validación de datos
class Voto(BaseModel):
    nombre: str
    opcion: str

@app.post("/voto", status_code=201)
def registrar_voto(voto: Voto):
    try:
        # Usamos la vista de bypass creada anteriormente
        response = supabase.table("votos_api").insert(voto.dict()).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        # Log técnico para depuración
        print(f"Error en inserción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar el voto en la base de datos")

@app.get("/health")
def health_check():
    return {"status": "online"}