import os
from supabase import create_client, Client

# Obtenemos las variables de entorno configuradas en el panel de Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Inicializamos el cliente de Supabase
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables SUPABASE_URL y SUPABASE_KEY no están configuradas.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)