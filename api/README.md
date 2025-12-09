# 🧳 Sistema de Recomendación de Destinos para Vacaciones Familiares

Backend en **FastAPI** que entrena un modelo **XGBoost** con datos históricos de preferencias familiares para recomendar destinos óptimos que maximicen la satisfacción grupal.

## 📁 Estructura del Proyecto
SIC-FAMILY-ARMONY-AI/
├── data/
│   └── datos_sinteticos.csv           # Datos históricos (entrenamiento)
└── api/                               # Backend (FastAPI)
    ├── app/
    ├── environment.yml                # Entorno Conda
    ├── .env                           # Variables de entorno
    └── .gitignore


## 🛠️ Configuración del Entorno

1. **Clonar el repositorio**:
   ```bash
   git clone <tu-repo-url>
   cd <nombre-del-repo>

2. **Configurar variables de entorno**:
Crea un archivo .env en SIC-FAMILY-ARMONY-AI/api/

Ejemplo:
    DATA_PATH=../data/viajes_familiares.csv -> datos de entrenamiento
    NEW_DATA_PATH=../data/nuevos_viajes.csv -> nuevos datos historicos
    PORT=8000                               -> puerto donde se ejecuta la API

3. **Ejecutar la API**:
uvicorn app.main:app --reload --port 8000