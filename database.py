from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Tu variable de entorno debe estar configurada en Render como DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configuramos el motor con parámetros de resiliencia y seguridad SSL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"}, # Obligatorio para conexiones seguras en Render
    pool_pre_ping=True                   # Verifica que la conexión esté viva antes de cada consulta
)

# Creamos la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()