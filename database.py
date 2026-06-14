from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# Obtenemos la URL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Aseguramos el sslmode
if DATABASE_URL and "?sslmode=require" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Intentamos crear el motor con parámetros de resiliencia
def get_engine():
    # Parámetros para manejar la inactividad de Render
    return create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,  # Verifica la conexión antes de usarla
        pool_recycle=300,    # Recicla conexiones para evitar cierres inesperados
    )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()