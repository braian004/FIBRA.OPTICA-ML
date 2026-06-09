import requests
import json

# 1. Cargar datos desde un archivo JSON
with open(r'data/processed/features_localidades.csv') as file:
    datos = json.load(file)

# 2. Recorrer los puntos y llamar a la API
for punto in datos:
    lat = punto['lat']
    lon = punto['lon']
    poblacion_real = punto['poblacion']
    
    # Llamada a la API (ajusta la URL a tu endpoint)
    response = requests.post(
        "http://127.0.0.1:8000/api/analizar",
        json={"lat": lat, "lon": lon}
    )
    
    if response.status_code == 200:
        resultado = response.json()
        poblacion_predicha = resultado['poblacion_automatica']
        
        if poblacion_real == poblacion_predicha:
            print(f"Lat: {lat}, Lon: {lon} -> Coincide población: {poblacion_real}")
        else:
            print(f"Lat: {lat}, Lon: {lon} -> Discrepancia: Real={poblacion_real}, Predicha={poblacion_predicha}")
    else:
        print(f"Error en la API para Lat: {lat}, Lon: {lon} (Código: {response.status_code})")