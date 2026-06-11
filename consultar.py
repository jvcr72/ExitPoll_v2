import requests
# Cambia esta URL por la tuya de Render
URL = "https://exitpoll-v2-produccion.onrender.com/ver-votos"
respuesta = requests.get(URL)
print(respuesta.json())