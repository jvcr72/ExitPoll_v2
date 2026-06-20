import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de base de datos desde entorno (Render) o SQLite local como fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Corrección de prefijo "postgres://" en Render para compatibilidad con SQLAlchemy 2.0+
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")

# Configurar motor de base de datos de manera robusta
if is_sqlite:
    # check_same_thread=False es necesario únicamente en SQLite para concurrencia en FastAPI
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Ajustes óptimos de pool de conexiones para PostgreSQL / bases de datos cloud
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la DB en las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()