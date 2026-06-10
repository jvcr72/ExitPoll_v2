import requests
import time

url = "https://exitpoll-v2.onrender.com/api/v1/salud"

print("Iniciando prueba de conexión...")
for i in range(5):
    start = time.time()
    try:
        response = requests.get(url)
        end = time.time()
        print(f"Petición {i+1}: Status {response.status_code} - Tiempo: {end-start:.4f}s")
    except Exception as e:
        print(f"Error en petición {i+1}: {e}")
    time.sleep(1)
print("Prueba finalizada.")