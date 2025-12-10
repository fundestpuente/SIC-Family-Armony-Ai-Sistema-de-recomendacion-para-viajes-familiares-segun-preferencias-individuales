# 🏖️ Family Harmony AI - Frontend

Interfaz web interactiva desarrollada con **Streamlit** que permite a registrar la familia yy seleccionar preferencias de viaje para recibir recomendaciones de destinos óptimos basadas en un modelo de machine learning (XGBoost).

## 📋 Descripción General

El frontend de Family Harmony AI es una aplicación web moderna que conecta con un backend basado en FastAPI. Permite:

- **Gestionar miembros familiares** con roles (Padres, Hijos, Abuelos, etc.)
- **Configurar preferencias individuales** en 6 categorías (Cultural, Recreación, Alojamiento, Gastronomía, Entretenimiento, Servicios)
- **Buscar destinos recomendados** optimizados para toda la familia
- **Analizar preferencias** con gráficos interactivos (Radar, Comparación, Estadísticas)

## 📁 Estructura del Proyecto

```
frontend/
├── app.py                          # Punto de entrada principal de Streamlit
├── .env                            # Variables de entorno (no compartir)
├── .streamlit/
│   └── config.toml                # Configuración de tema y estilos Streamlit
├── pagina/                         # Módulos de páginas de la aplicación
│   ├── familia_page.py            # Gestión de miembros y preferencias
│   ├── recomendaciones_page.py    # Búsqueda y visualización de destinos
│   └── analisis_page.py           # Análisis de preferencias familiares
├── utils/                          # Funciones utilitarias
│   ├── config.py                  # Constantes y configuración global
│   ├── api_client.py              # Cliente HTTP para comunicarse con la API
│   ├── helpers.py                 # Funciones auxiliares (validación, limpieza)
│   └── visualizations.py          # Gráficos interactivos con Plotly
└── __pycache__/                   # Cache de Python (ignorar)
```

## 🛠️ Configuración del Entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/fundestpuente/SIC-Family-Armony-Ai-Sistema-de-recomendacion-para-viajes-familiares-segun-preferencias-individuales.git
cd frontend
```

### 3. Instalar dependencias

```bash
pip install streamlit requests python-dotenv plotly pandas numpy streamlit-option-menu streamlit-folium folium
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# URL del servidor Backend (FastAPI)
API_BASE_URL=http://localhost:8000
```

**Valores por defecto:**

- `API_BASE_URL`: `http://localhost:8000` (API local)

Para usar API en servidor remoto:

```env
API_BASE_URL=https://tu-api.com
```

### 5. Ejecutar la aplicación

```bash
# Desarrollo
streamlit run app.py

# Personalizado (puerto específico)
streamlit run app.py --server.port 8501 --server.address localhost
```

La aplicación se abrirá en: `http://localhost:8501`

## 🎯 Flujo de la Aplicación

### 1. **Página Familia** (`pagina/familia_page.py`)

- ➕ Agregar miembros con nombre y rol
- ⭐ Seleccionar preferencias (1-5 estrellas)
- 👥 Ver lista de miembros agregados
- 🔍 Transición a búsqueda de destinos

### 2. **Página Recomendaciones** (`pagina/recomendaciones_page.py`)

- 🎯 Configurar cantidad de destinos (3 o 5)
- ✨ Buscar recomendaciones via API
- 🏆 Mostrar top destinos con puntuación

### 3. **Página Análisis** (`pagina/analisis_page.py`)

- 📊 Resumen general (preferencias, ratings, actividades únicas)
- 📈 Gráfico de comparación familiar
- 👤 Perfiles individuales (Radar de preferencias)
- 📊 Estadísticas familares detalladas

### Endpoints Utilizados

```python
# GET - Verificar estado de la API
GET http://localhost:8000/

# POST - Obtener recomendaciones
POST http://localhost:8000/api/family/recommend_destinations
Parámetros:
  - top_k: int (cantidad de destinos, default=3)
  - body: JSON con estructura de familia
```

**Ejemplo de dato enviado:**

```json
{
  "miembros": [
    {
      "nombre": "Juan",
      "rol": "Padre",
      "preferencias": {
        "Calif promedio playas": 5,
        "Calif promedio museos": 3,
        "Calif promedio restaurantes": 4
      }
    }
  ]
}
```

## 📈 Mejoras Futuras

- [ ] Exportar recomendaciones a PDF
- [ ] Integración con Google Maps
- [ ] Historial de viajes y satisfacción
