from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import supabase
import secrets

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

# Endpoint de ejemplo para registrar votos
@app.post("/voto")
def registrar_voto(nombre: str, opcion: str):
    try:
        response = supabase.table("votos").insert({
            "nombre": nombre, 
            "opcion": opcion
        }).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint básico para verificar que la app está viva
@app.get("/")
def read_root():
    return {"message": "API de ExitPoll activa y conectada a Supabase REST"}