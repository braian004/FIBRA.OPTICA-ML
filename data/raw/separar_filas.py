import pandas as pd
import os

# =====================================================================
# CÁLCULO DINÁMICO DE RUTAS (Evita el FileNotFoundError)
# =====================================================================
# Detecta la carpeta exacta donde está guardado este script (data/raw)
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))

PATH_ENTRADA = os.path.join(DIR_ACTUAL, "nodos_fibra.csv")
PATH_SALIDA = os.path.join(DIR_ACTUAL, "nodos_por_columnas.csv")

# =====================================================================
# 1. LEER EL ARCHIVO ORIGINAL
# =====================================================================
# Usamos encoding="latin-1" para proteger los caracteres especiales de Argentina
df_nodos = pd.read_csv(PATH_ENTRADA, sep=";", encoding="latin-1")

# =====================================================================
# 2. FUNCIÓN EXTRACTORA SEGURA
# =====================================================================
def segmentar_coordenada(coordenada_cruda, indice_objetivo):
    try:
        # Si el dato está vacío o es un guion, devolvemos texto vacío
        if pd.isna(coordenada_cruda) or coordenada_cruda == "-":
            return ""
        
        # Quitamos los corchetes de los extremos y separamos por la coma
        texto_aislado = str(coordenada_cruda).strip("[]")
        componentes = texto_aislado.split(",")
        
        # Devolvemos el número limpio
        return componentes[indice_objetivo].strip()
    except Exception:
        return ""

# =====================================================================
# 3. CREAR LAS DOS COLUMNAS NUEVAS (Separación limpia)
# =====================================================================
# Índice 0 es Longitud, Índice 1 es Latitud
df_nodos["lon"] = df_nodos["COORDENADAS"].apply(lambda x: segmentar_coordenada(x, 0))
df_nodos["lat"] = df_nodos["COORDENADAS"].apply(lambda x: segmentar_coordenada(x, 1))

# =====================================================================
# 4. LIMPIAR Y GUARDAR
# =====================================================================
# Borramos la columna vieja combinada porque ya tenemos las dos columnas nuevas
df_final = df_nodos.drop(columns=["COORDENADAS"])

# Guardamos el resultado en la misma carpeta data/raw/
df_final.to_csv(PATH_SALIDA, index=False, sep=";")

print("¡Excelente! Archivo 'nodos_por_columnas.csv' generado correctamente.")