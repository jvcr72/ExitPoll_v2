import requests

# URL de tu API
url = "https://exitpoll-v2.onrender.com/voto"

# Datos de prueba
datos_voto = {
    "nombre": "Juan",
    "apellido": "Perez",
    "cedula": "12345678",
    "centro_electoral": "Escuela Bolivar",
    "mesa": "1",
    "direccion_vivienda": "Av. Principal",
    "numero_telefonico": "04140000000",
    "candidato": "Candidato X",
    "edad": 30
}

print("Enviando voto de prueba...")
response = requests.post(url, json=datos_voto)

if response.status_code == 200:
    print("¡Éxito! Respuesta del servidor:", response.json())
else:
    print("Hubo un error:", response.status_code, response.text)