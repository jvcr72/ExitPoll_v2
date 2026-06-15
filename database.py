from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Eliminamos cualquier intento de sslmode=require
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Al añadir ?sslmode=disable, le indicamos al driver de postgres que no fuerce el cifrado
# Si tu URL ya tiene parámetros (?), usa &sslmode=disable
conn_url = SQLALCHEMY_DATABASE_URL if "?" in SQLALCHEMY_DATABASE_URL else f"{SQLALCHEMY_DATABASE_URL}?sslmode=disable"

engine = create_engine(conn_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()