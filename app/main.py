from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
import math
import os

# =====================================================================
# 1. CÁLCULO DINÁMICO DE RUTAS ABSOLUTAS
# =====================================================================
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(DIR_ACTUAL)

PATH_MODELO = os.path.join(RAIZ_PROYECTO, "models", "modelo_fibra_optica.pkl")
PATH_SCALER = os.path.join(RAIZ_PROYECTO, "models", "scaler_fibra_optica.pkl")
PATH_NODOS = os.path.join(RAIZ_PROYECTO, "data", "raw", "nodos_por_columnas.csv")
PATH_FEATURES = os.path.join(RAIZ_PROYECTO, "data", "processed", "features_localidades.csv")

# =====================================================================
# 2. CARGA DE CONTROLADORES Y BASES DE DATOS
# =====================================================================
modelo = joblib.load(PATH_MODELO)
scaler = joblib.load(PATH_SCALER)

nodos_df = pd.read_csv(PATH_NODOS, sep=";", encoding="latin-1")
features_df = pd.read_csv(PATH_FEATURES)

# =====================================================================
# 3. CONFIGURACIÓN DEL CORE DE FASTAPI
# =====================================================================
app = FastAPI(title="AI Fiber Radar - Core Engine V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Coordenada(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)

@app.exception_handler(RequestValidationError)
async def manejador_error_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "COORDENADA_INEXISTENTE", "mensaje": "La latitud o longitud ingresada no pertenece al plano terrestre."}
    )

def distancia_km(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111

# =====================================================================
# 4. ENDPOINT GET: ALIMENTA LAS OLAS 2D EN TU MAPA
# =====================================================================
@app.get("/api/nodos")
def obtener_nodos_infraestructura():
    lista_nodos = []
    for _, fila in nodos_df.iterrows():
        if pd.isna(fila["lat"]) or pd.isna(fila["lon"]) or fila["lat"] == "" or fila["lon"] == "":
            continue
        lista_nodos.append({
            "name": str(fila["NOMBRE NODO"]),
            "lat": float(fila["lat"]),
            "lon": float(fila["lon"])
        })
    return lista_nodos

# =====================================================================
# 5. ENDPOINT POST: INFERENCIA TOTALMENTE ACOPLADA AL FRONTEND
# =====================================================================
@app.post("/api/analizar")
def analizar_coordenada(punto: Coordenada):

    # Paso A: Búsqueda demográfica automatizada en features_localidades.csv
    dist_min_pob = float("inf")
    poblacion_detectada = 0.0

    for _, fila in features_df.iterrows():
        d_pob = distancia_km(punto.lat, punto.lon, float(fila["centroide_lat"]), float(fila["centroide_lon"]))
        if d_pob < dist_min_pob:
            dist_min_pob = d_pob
            poblacion_detectada = float(fila["population"])

    # Paso B: Búsqueda de infraestructura de red cercana
    dist_min_nodo = float("inf")
    nodo_cercano = None

    for _, nodo in nodos_df.iterrows():
        if pd.isna(nodo["lat"]) or pd.isna(nodo["lon"]) or nodo["lat"] == "" or nodo["lon"] == "":
            continue
        d_nodo = distancia_km(punto.lat, punto.lon, float(nodo["lat"]), float(nodo["lon"]))
        if d_nodo < dist_min_nodo:
            dist_min_nodo = d_nodo
            nodo_cercano = nodo["NOMBRE NODO"]

    # Paso C: Inferencia de Machine Learning
    datos_entrada = np.array([[punto.lat, punto.lon, poblacion_detectada]])
    datos_escalados = scaler.transform(datos_entrada)
    
    probabilidades = modelo.predict_proba(datos_escalados)[0]
    viabilidad_num = probabilidades[1] * 100

    if viabilidad_num >= 80:
        diagnostico = "VIABILIDAD MUY ALTA"
    elif viabilidad_num >= 60:
        diagnostico = "VIABILIDAD ALTA"
    elif viabilidad_num >= 40:
        diagnostico = "VIABILIDAD MEDIA"
    else:
        diagnostico = "VIABILIDAD BAJA"

    # Retorno limpio con nombres sincronizados uno a uno con la interfaz
    return {
        "latitud_solicitada": punto.lat,
        "longitud_solicitada": punto.lon,
        "poblacion_automatica": int(poblacion_detectada),
        "nodo_cercano": str(nodo_cercano) if nodo_cercano else "No detectado",
        "distancia_nodo_km": round(dist_min_nodo, 2) if dist_min_nodo != float("inf") else 0.0,
        "viabilidad": f"{viabilidad_num:.2f}%",
        "diagnostico": diagnostico
    }

@app.get("/")
def root():
    return {"mensaje": "AI Fiber Radar funcionando exitosamente"}