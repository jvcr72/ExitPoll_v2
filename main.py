from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class VotoSchema(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    centro_electoral: str
    mesa: str
    direccion_vivienda: str
    numero_telefonico: str
    candidato: str
    edad: int
@app.post("/voto")
def registrar_voto(voto: VotoSchema):
    return {"mensaje": "Voto registrado correctamente"}
@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}