import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def cargar_y_preparar_datos(path_csv):
    # Carga del dataset unificado por tu compañera
    df = pd.read_csv(path_csv)
    
    # 1. Definimos las variables predictoras y el target según sus capturas
    features = ['centroide_lat', 'centroide_lon', 'population']
    
    # Convertimos la columna booleana (True/False) de tu compañera a binaria (1/0)
    df['tiene_fibra_optica'] = df['con_fibra'].astype(int)
    target = 'tiene_fibra_optica'
    
    # 2. Limpieza de valores nulos en las columnas que usará el modelo
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]
    
    # 3. Partición balanceada (80% entrenamiento, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # 4. Escalado/Normalización de los datos numéricos y geográficos
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler