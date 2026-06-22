from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a tu base de datos Supabase
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@db.axszrbfysgdstbipicmc.supabase.co:5432/postgres"

# Creamos el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir tus modelos
Base = declarative_base()

# Dependencia para obtener la sesión en tus rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()