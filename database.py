from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Render usa la variable DATABASE_URL que configuramos
# Si no la encuentra (como cuando corres local), usa SQLite por defecto
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./votos.db")

# Si la URL empieza por 'postgres://', SQLAlchemy necesita 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()