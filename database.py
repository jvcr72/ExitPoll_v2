import os
from supabase import create_client, Client

# Obtenemos las variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Validación estricta
if not url:
    raise Exception("ERROR: La variable SUPABASE_URL no está definida en Render")
if not key:
    raise Exception("ERROR: La variable SUPABASE_KEY no está definida en Render")

supabase: Client = create_client(url, key)