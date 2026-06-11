from database import engine
import models

print("Creando tablas en la base de datos...")
models.Base.metadata.create_all(bind=engine)
print("Tablas creadas exitosamente.")