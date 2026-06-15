from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Se desactiva el SSL en los parámetros de conexión para evitar el cierre inesperado
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"sslmode": "disable"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()