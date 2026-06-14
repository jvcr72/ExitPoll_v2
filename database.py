from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obtenemos la URL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Si la URL no termina en ?sslmode=require, se lo añadimos
if DATABASE_URL and "?sslmode=require" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Configuración del motor con reintentos
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_recycle=300,    # Recicla conexiones viejas
    pool_size=5,         # Tamaño del pool para instancias pequeñas
    max_overflow=2
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()