import pandas as pd
import os

def generar_dataset_final():
    print("==================================================")
    print("   INICIANDO GENERACIÓN AUTOMÁTICA DEL DATASET   ")
    print("==================================================")
    
    # 1. Definir y verificar rutas
    path_loc = "data/raw/localidades.csv"
    path_pob = "data/raw/poblacion.csv"
    path_nodos = "data/raw/nodos_fibra.csv"
    
    for p in [path_loc, path_pob, path_nodos]:
        if not os.path.exists(p):
            print(f"[ERROR OBLIGATORIO]: No encontré el archivo: '{p}'")
            print("Por favor, verifica que los nombres en la carpeta data/raw/ sean exactos.")
            return

    # 2. Cargar los archivos CSV originales con codificación adaptada para español (latin-1)
    print("- Cargando archivos CSV solucionando problemas de acentos...")
    try:
        df_loc = pd.read_csv(path_loc, encoding='latin-1')
        df_pob = pd.read_csv(path_pob, encoding='latin-1')
        df_nodos = pd.read_csv(path_nodos, sep=';', encoding='latin-1')
    except Exception as e:
        print(f"[ERROR AL LEER]: Intentando otra codificación por error: {e}")
        df_loc = pd.read_csv(path_loc, encoding='utf-8', errors='replace')
        df_pob = pd.read_csv(path_pob, encoding='utf-8', errors='replace')
        df_nodos = pd.read_csv(path_nodos, sep=';', encoding='utf-8', errors='replace')

    # 3. Procesar datos de Población (SimpleMaps)
    df_pob = df_pob[df_pob['country'] == 'Argentina'].copy()
    df_pob['match_name'] = df_pob['city'].str.lower().str.strip()

    # 4. Preparar el dataset principal de localidades
    df_loc['match_name'] = df_loc['nombre'].str.lower().str.strip()

    print("- Cruzando localidades con datos de población...")
    df_merged = pd.merge(df_loc, df_pob[['match_name', 'population']], on='match_name', how='left')
    
    # Rellenar poblaciones vacías con la mediana general para evitar NaNs
    mediana_poblacion = df_pob['population'].median()
    df_merged['population'] = df_merged['population'].fillna(mediana_poblacion)

    print("- Determinando conectividad con nodos de REFEFO...")
    nodos_names = df_nodos['NOMBRE NODO'].str.lower().str.strip().unique()
    df_merged['con_fibra'] = df_merged['match_name'].isin(nodos_names)

    # 5. Filtrar y estructurar las columnas finales exactas como tu compañera
    df_final = df_merged[['centroide_lat', 'centroide_lon', 'population', 'con_fibra']].copy()
    
    # Limpieza final de filas sin coordenadas válidas
    df_final = df_final.dropna(subset=['centroide_lat', 'centroide_lon'])

    # 6. Crear la carpeta processed y guardar el archivo final
    print("- Guardando el archivo final...")
    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/features_localidades.csv"
    df_final.to_csv(output_path, index=False)
    
    print("\n==================================================")
    print(" -> ¡ÉXITO TOTAL! Dataset unificado y creado sin errores.")
    print(f" Archivo guardado en: {output_path}")
    print(f" Total de filas generadas: {len(df_final)}")
    print("==================================================")
    print(df_final.head(5))

if __name__ == "__main__":
    generar_dataset_final()