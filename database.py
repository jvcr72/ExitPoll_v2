import os
from supabase import create_client, Client

# Obtenemos las variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Validación preventiva: 
# Si faltan las variables, es mejor que el servidor falle al iniciar 
# (con un mensaje claro) que intentar funcionar sin conexión.
if not url or not key:
    raise ValueError("Error crítico: SUPABASE_URL o SUPABASE_KEY no están definidas en el entorno.")

# Inicialización estándar
supabase: Client = create_client(url, key)