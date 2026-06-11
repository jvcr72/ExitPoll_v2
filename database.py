from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Si la URL no tiene ?sslmode=require al final, añádelo en las variables de entorno de Render
# Engine más robusto
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    },
    pool_pre_ping=True,      # Verifica conexión antes de usarla
    pool_recycle=300,        # Recicla conexiones cada 5 min para evitar que se cierren
    pool_timeout=30          # Aumenta el tiempo de espera de conexión
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()