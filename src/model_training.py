import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from data_processing import cargar_y_preparar_datos

def ejecutar_entrenamiento():
    # Asegúrate de que el archivo final de tu compañera esté en esta ruta con este nombre
    path_datos = "data/processed/features_localidades.csv"
    
    try:
        # 1. Preparar y obtener los datos limpios
        X_train, X_test, y_train, y_test, scaler = cargar_y_preparar_datos(path_datos)
        
        # 2. Inicializar el clasificador con balanceo de pesos automático
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        
        # 3. Entrenamiento del núcleo técnico del sistema funcionando
        print("Entrenando el modelo de Machine Learning con la estructura del notebook...")
        model.fit(X_train, y_train)
        
        # 4. Evaluación sobre el conjunto de test independiente
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='binary')
        
        print("\n==============================================")
        print("     NÚCLEO TÉCNICO EVALUADO EXITOSAMENTE     ")
        print("==============================================")
        print(f"Accuracy General del Modelo: {acc:.4f}")
        print(f"F1-Score (Clase con Fibra):  {f1:.4f}")
        print("\nReporte de Clasificación Detallado por Clase:")
        print(classification_report(y_test, y_pred))
        print("==============================================")
        
        # 5. Guardar los archivos .pkl en la carpeta /models
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/modelo_fibra_optica.pkl")
        joblib.dump(scaler, "models/scaler_fibra_optica.pkl")
        print("-> ¡Éxito! Los archivos binarios se guardaron en la carpeta /models")
        
    except FileNotFoundError:
        print(f"\n[ERROR]: No se encontró el archivo en '{path_datos}'.")
        print("Verifica que hayas guardado el archivo final de tu compañera dentro de 'data/processed/' con el nombre 'features_localidades.csv'.")
    except KeyError as e:
        print(f"\n[ERROR de Columnas]: No se encontró la columna {e} en el archivo.")
        print("Verifica que el dataset contenga exactamente las columnas: 'centroide_lat', 'centroide_lon', 'population' y 'con_fibra'.")

if __name__ == "__main__":
    ejecutar_entrenamiento()