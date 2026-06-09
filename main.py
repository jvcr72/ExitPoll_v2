from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "La API está funcionando en la raíz"}

@app.get("/api/v1/salud")
def check_salud():
    return {"status": "conectado"}