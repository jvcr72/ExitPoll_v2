from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obtiene la URL desde las variables de entorno de Render
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configuración del motor con parámetros de robustez para servicios en la nube
# pool_pre_ping: Verifica la conexión antes de realizar cualquier consulta
# pool_recycle: Renueva la conexión cada 300 segundos para evitar tiempos de espera
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)

# Sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir tus modelos de tablas
Base = declarative_base()

# Función de dependencia para obtener la sesión en tus rutas (opcional)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()