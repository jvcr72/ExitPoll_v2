import requests

URL = "https://exitpoll-v2-produccion.onrender.com/ver-votos" 

try:
    respuesta = requests.get(URL)
    print("Estado de la respuesta:", respuesta.status_code)
    print("Datos recibidos:", respuesta.json())
except Exception as e:
    print("Ocurrió un error:", e)