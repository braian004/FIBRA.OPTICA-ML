# Predicción de conectividad a fibra óptica en localidades argentinas

Este proyecto corresponde al **Trabajo Integrador Final (TIF)** para la materia Modelado y Ciencia de Datos. El objetivo es desarrollar un sistema de Machine Learning capaz de predecir si una localidad de la República Argentina tiene acceso a la Red Federal de Fibra Óptica (REFEFO) en función de sus características geográficas y demográficas.

---

## 1. Definición de la Arquitectura del Sistema
El sistema implementa una **Arquitectura Centralizada**. 

**Justificación:** Debido a que el volumen total de datos unificados no supera unos pocos megabytes, la centralización permite un procesamiento local eficiente y de bajo costo. No se requiere la complejidad de un entorno distribuido. Todo el ciclo de vida del dato —desde la ingesta en bruto, la unificación, el entrenamiento del algoritmo y la exportación de artefactos— se ejecuta de forma unificada en un único entorno local controlado dentro de Visual Studio Code.

---

## 2. Estructura del Repositorio
El proyecto sigue una estructura modular y organizada bajo las buenas prácticas de la Ciencia de Datos:

* `data/raw/`: Almacena los tres datasets originales sin alterar (`localidades.csv`, `poblacion.csv`, `nodos_fibra.csv`).
* `data/processed/`: Contiene el archivo consolidado final `features_localidades.csv`.
* `docs/`: Documentación del proyecto (`avance1.md` y `avance2.md`).
* `models/`: Almacena los archivos binarios serializados (`.pkl`) listos para producción.
* `src/data_processing.py`: Script modular de carga, limpieza y partición estratificada.
* `src/model_training.py`: Script de entrenamiento, optimización y evaluación del modelo.
* `requirements.txt`: Archivo de configuración con las dependencias del entorno.

---

## 3. Justificación de Decisiones Técnicas
* **Algoritmo Seleccionado:** Se optó por **Random Forest (Bosques Aleatorios)** como clasificador local probabilístico. Se justifica su elección debido a que las coordenadas geográficas no poseen una relación lineal simple respecto a la infraestructura física de red. Al ser un ensamble de múltiples árboles de decisión independientes, es robusto frente al ruido intrínseco de los datos estimados de población y reduce eficazmente el sobreajuste (*overfitting*).
* **Tratamiento de Datos:** Durante el pipeline de datos, se identificó un problema de codificación de caracteres en las fuentes públicas gubernamentales. Se resolvió forzando el descifrado local mediante la codificación `latin-1` para asegurar la integridad de nombres de localidades con tildes y eñes.

---

## 4. Elección de Métricas de Evaluación
El conjunto de prueba refleja la asimetría del territorio nacional, arrojando un fuerte **desbalance de clases** en el sostenimiento de los datos (*Support*): **617 localidades desconectadas frente a 216 conectadas**. 

**Justificación de Métricas:** En este escenario, la métrica tradicional de *Accuracy* (Exactitud) resulta insuficiente y engañosa. Se seleccionó el **F1-Score** como métrica principal de optimización, ya que calcula la media armónica entre la *Precisión* y la *Sensibilidad (Recall)*, garantizando que el modelo aprenda a identificar las localidades conectadas sin descuidar el impacto de los desbalances.

---

## 5. Resultados del Núcleo Técnico (Avance 2)
Al ejecutar el script de entrenamiento independiente en la terminal de Visual Studio Code (`python src/model_training.py`), el núcleo técnico arrojó las siguientes métricas oficiales de evaluación:

* **Accuracy General del Sistema:** 0.7575 (75.75% de aciertos globales).
* **F1-Score - Clase 0 (Sin Fibra):** 0.85
* **F1-Score - Clase 1 (Con Fibra):** 0.44

### Reporte Detallado de Clasificación:
```text
              precision    recall  f1-score   support

           0       0.80      0.89      0.85       617
           1       0.55      0.37      0.44       216

    accuracy                           0.76       833
```

## 6. Despliegue del modelo (Avance 3)

En este proceso se agregó y desplegó el modelo predictivo, junto con la creación de la interfaz de usuario.

### Arquitectura de despliegue del *modelo de fibra óptica*

![Arquitectura del Sistema](docs/arquitectura.png)

* **1.** Se implementó una API (**FastAPI** en `app.py`) para gestionar las peticiones y conectar la lógica con la interfaz del Frontend.
* **2.** Se desarrolló el **Frontend** utilizando tecnologías web nativas:
  * **HTML:** Para estructurar y organizar los elementos de la interfaz.
  * **CSS:** Utilizado para definir el diseño visual, estilos y adaptabilidad.
  * **JavaScript:** Encargado de proporcionar interactividad al sistema:
    * Incorporación del método de búsqueda geográfica.
    * Renderizado dinámico de resultados en pantalla (sin necesidad de recargar la página).
    * Comunicación asíncrona directa con el servidor backend.
* **3.** Se **dockerizó** 🐳 el entorno completo para empaquetar de forma aislada el backend y las dependencias del modelo.
* **4.** Estrategia de **Despliegue (Deploy)**:
  1. El modelo de Machine Learning y el Backend fueron alojados en un servidor en la nube a través de **Render**.
  2. La interfaz de usuario (Frontend) fue desplegada para producción en **Vercel** y **GitHub Pages**.

---

### Visualización y Funcionalidades

* **Búsqueda Eficiente:** Se implementó un motor de búsqueda que permite a los usuarios localizar áreas y localidades específicas sobre el mapa de forma rápida y sencilla.
* **Cálculo de Proximidad:** El sistema permite añadir un punto de referencia para calcular la distancia en tiempo real hacia el nodo de fibra óptica más cercano y evaluar su viabilidad.

🔗 **Link del Proyecto en Producción:** [FIBRA.OPTICA-ML-frontend](https://braian004.github.io/FIBRA.OPTICA-ML-frontend/)



