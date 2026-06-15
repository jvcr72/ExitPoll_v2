from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Render añade el parámetro sslmode=require automáticamente a la cadena de conexión interna.
# Si el error persiste, es posible que la URL esté mal copiada en Render.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Usamos una configuración mínima para evitar errores de tipo 'status 1'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()