from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Si la URL no tiene ?sslmode=require al final, añádelo en las variables de entorno de Render
# Engine más robusto
# Modifica tu engine en database.py así:
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    },
    pool_pre_ping=True,      # Fundamental: verifica que la conexión siga viva
    pool_recycle=300,        # Recicla la conexión cada 5 minutos
    pool_timeout=30          # Espera hasta 30 segundos antes de fallar
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()