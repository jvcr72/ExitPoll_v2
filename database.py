import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Creamos las opciones para el cliente incluyendo el header de autenticación
options = {
    "headers": {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }
}

# Inicializamos el cliente pasando las opciones
supabase: Client = create_client(url, key, options)