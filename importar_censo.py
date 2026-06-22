import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import VotoDB, Base

# Carga de base de datos desde entorno (Neon/Postgres) o SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

# Asegurar creación de tablas
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def normalizar_nombre(nombre):
    return str(nombre).strip().upper()

def importar_desde_excel(archivo_excel):
    df = pd.read_excel(archivo_excel)
    
    # Limpiamos filas vacías
    df = df.dropna(subset=['Cedula']) 

    print("Iniciando importación al censo...")
    importados = 0
    omitidos = 0

    for _, row in df.iterrows():
        cedula_str = str(int(row['Cedula'])) if isinstance(row['Cedula'], float) else str(row['Cedula']).strip()
        
        # Evitar duplicados consultando si la cédula ya existe en la base de datos
        existente = db.query(VotoDB).filter(VotoDB.cedula == cedula_str).first()
        if existente:
            omitidos += 1
            continue

        try:
            voto = VotoDB(
                cedula=cedula_str,
                nombre=str(row['Nombre']),
                centro_electoral=normalizar_nombre(row['centro electoral']),
                voto_registrado=False 
            )
            db.add(voto)
            importados += 1
        except Exception as e:
            print(f"Error en fila con cédula {cedula_str}: {e}")
    
    db.commit()
    print(f"¡Censo procesado! Nuevos importados: {importados}, Omitidos (duplicados): {omitidos}")

if __name__ == "__main__":
    importar_desde_excel("censo.xlsx")