#  SIC-FAMILY-ARMONY-AI

> **Sistema Inteligente de Recomendación para Vacaciones Familiares**

Este proyecto unifica un **Backend analítico (FastAPI + XGBoost)** con un **Frontend interactivo (Streamlit)**.

La herramienta fue diseñada para resolver la complejidad de los viajes grupales: permite al usuario **ingresar el número exacto de participantes** y definir las **características específicas** que buscan (cultura, recreación, descanso, etc.). A partir de estos inputs, el sistema utiliza Inteligencia Artificial para recomendar los destinos que maximizan la satisfacción colectiva.

---

##  Descripción General

El sistema opera bajo una arquitectura cliente-servidor donde el usuario configura la experiencia y el modelo predice el éxito del destino.

### Características Principales:
* **Gestión Dinámica de Grupos**: Ingreso de *N* cantidad de participantes con roles específicos (Padres, Hijos, Abuelos).
* **Perfilado de Preferencias**: Definición de gustos en 6 categorías clave (Cultural, Recreación, Alojamiento, Gastronomía, Entretenimiento, Servicios).
* **Motor de Recomendación AI**: Uso de **XGBoost** para procesar las características ingresadas y predecir el destino óptimo.
* **Analítica Visual**: Gráficos de radar y tablas comparativas para entender la "armonía" del grupo.

---

##  Estructura del Proyecto

```text
SIC-FAMILY-ARMONY-AI/
├── api/                          #  Backend (Lógica y Modelo AI)
│   ├── app/                      # Código fuente de la API
│   └── .env                      # Configuración del servidor
├── data/                         #  Datos procesados y análisis
│   ├── AnalisisExploratorio.ipynb
│   ├── datos_sintetico.csv
│   └── nuevos_viajes.csv
├── datasets_base/                #  Fuentes de datos originales
│   ├── atractivos_tur.csv
│   └── google_review_ratings.csv
├── frontend/                     #  Frontend (Interfaz de Usuario)
│   ├── .streamlit/               # Configuración de estilos
│   ├── pagina/                   # Páginas: Familia, Recomendaciones, Análisis
│   ├── utils/                    # Funciones auxiliares
│   ├── app.py                    #  Punto de entrada de Streamlit
│   └── .env                      # Configuración del cliente
├── generar_data_sintetica_...py  # Script para generación de datos
├── union_y_preprocesamiento.py   # Script ETL de limpieza de datos
└── .gitignore
````

-----

##  Guía de Instalación y Ejecución

Para levantar el sistema completo, necesitarás dos terminales: una para el cerebro (API) y otra para la interfaz (Frontend).

### 1\. Clonar el Repositorio

```bash
git clone [https://github.com/fundestpuente/SIC-Family-Armony-Ai.git](https://github.com/fundestpuente/SIC-Family-Armony-Ai.git)
cd SIC-FAMILY-ARMONY-AI
```

### 2\. Configurar el Backend (Terminal A)

```bash
# Navegar a la carpeta del servidor
cd api

# Instalar dependencias de IA y API
pip install fastapi uvicorn[standard] pandas numpy scikit-learn xgboost python-dotenv python-multipart

# Configurar variables de entorno
# Crea un archivo .env y agrega:
echo "DATA_PATH=../data/datos_sintetico.csv" > .env
echo "PORT=8000" >> .env

# Levantar el servidor
uvicorn app.main:app --reload --port 8000
```

>  **Estado:** La API estará escuchando en `http://localhost:8000`

### 3\. Configurar el Frontend (Terminal B)

```bash
# Navegar a la carpeta de la interfaz
cd frontend

# Instalar librerías gráficas
pip install streamlit requests python-dotenv plotly pandas numpy streamlit-option-menu streamlit-folium folium

# Configurar conexión con el backend
# Crea un archivo .env y agrega:
echo "API_BASE_URL=http://localhost:8000" > .env

# Iniciar la aplicación
streamlit run app.py

# Personalizado (puerto específico)
streamlit run app.py --server.port 8501 --server.address localhost
```

> **Estado:** La Web App se abrirá en `http://localhost:8501`

-----

##  Flujo de Uso

1.  **Página "Familia" (Input):**

      * El usuario indica cuántas personas viajan.
      * Se registran los perfiles y se califican (1-5 estrellas) las características que buscan (ej. *Alta Gastronomía*, *Bajo Entretenimiento*).

2.  **Página "Recomendaciones" (Procesamiento):**

      * Se solicita al backend el **Top 3 o 5** destinos.
      * El modelo XGBoost cruza las preferencias del grupo con la base de datos de destinos.

3.  **Página "Análisis" (Output):**

      * Visualización de gráficos de radar para ver la compatibilidad entre los miembros del grupo y el destino elegido.

-----

## Mejoras Futuras

  - [ ] Integración con Google Maps API para visualización geográfica.
  - [ ] Exportación de itinerarios a PDF.
  - [ ] Pestaña de análisis.