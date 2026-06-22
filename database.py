import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Se obtiene la variable desde la configuración que acabas de guardar en Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configuración del motor con parámetros de reconexión automática
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"connect_timeout": 10}
)

# Sesión para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()