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

## 6. Despligue del modelo (Avance 3)
En este proceso se agrego se desplego el modelo y creacion del interfa.

### Arquitectura de despliegue del *modelo de fibra optica*
*1* Se inplemento una API (FastAPI app.py )para que se conecte con la interfasz del frontend.
*2* Se desarrollo el Frontend :
      -Html para organizar la interfaze
      -css se utilizo la darle estilo y diseño  
      -JavaScrip -para darle interactividar
                 -agregar el metodo de busqueda
                 -Mortarlos sisrecargar la pantalla de forma dinamica
                 -Comunicarse con el servidor
*3*Se dokerizo🐳 para desplegarlo todo el backend y modelo
*4*Despliege o deploy:
       1-Se desplego el Modelos y banckend en un servidor en la nube(Render)
       2-Se Desplego la interfaze en Vercel y Github page



###Visualizacion
Se Inplemento un formato de busqueda que permite a los usuarios un encontrar localidades  especificas en el mapa de forma rapida y sensilla 
agrego un punto de del usuairo donde puedea agregar la distancia mas sercana al nodo de fibra optica mas sercana 

link--https://braian004.github.io/FIBRA.OPTICA-ML-frontend/
## 6. Despliegue del Modelo (Avance 3)

En esta etapa se realizó el despliegue del modelo predictivo y la integración con la interfaz de usuario.

### Arquitectura de Despliegue del Modelo de Fibra Óptica

1. **Capa de API (Backend):** Se implementó una API REST con **FastAPI** (`app.py`) para conectar la lógica del modelo con la interfaz del usuario.
2. **Capa de Presentación (Frontend):** Se desarrolló una interfaz web desacoplada utilizando tecnologías nativas:
   - **HTML5:** Estructuración y organización de la interfaz gráfica.
   - **CSS3:** Diseño responsivo, estilos visuales y maquetación.
   - **JavaScript (ES6):** Gestión de interactividad, consumo asíncrono de la API mediante peticiones HTTP (sin recargar la página) y renderizado dinámico de mapas.
3. **Contenedorización:** Se utilizó **Docker** 🐳 para empaquetar de forma aislada el entorno de Python, las dependencias (`requirements.txt`) y el backend.
4. **Estrategia de Deploy:**
   - **Backend & Modelos:** Desplegados de forma continua en **Render**, ejecutando el servidor FastAPI dentro del contenedor Docker.
   - **Frontend:** Alojado de manera estática y con alta velocidad de carga en **Vercel** / **GitHub Pages**.

---

### Visualización y Funcionalidades Básicas

* **Búsqueda Avanzada:** Se implementó un motor de búsqueda geográfico que permite localizar áreas específicas en el mapa de forma rápida y sencilla.
* **Análisis de Cercanía:** El sistema detecta la ubicación seleccionada por el usuario y calcula la distancia en tiempo real hacia el nodo de fibra óptica más cercano, mostrando el porcentaje de viabilidad.

🔗 **Link del Proyecto:** [FIBRA.OPTICA-ML-frontend](https://braian004.github.io/FIBRA.OPTICA-ML-frontend/)

