import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print(f"DEBUG: URL cargada: {url}")
# Imprimimos solo los primeros 5 caracteres de la key para no exponerla toda
print(f"DEBUG: Key cargada: {key[:5]}...") 

supabase: Client = create_client(url, key)