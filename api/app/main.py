import os
from fastapi import FastAPI
from .routes import family


# Crear la aplicación FastAPI
app = FastAPI(
    title="Family Harmony AI: Recomendador de Vacaciones Familiares",
    description="API para recomendar destinos óptimos basados en preferencias familiares usando XGBoost.",
    version="0.1.0"
)

# Incluir rutas
app.include_router(family.router, prefix="/api/family", tags=["family"])

# Ruta raíz (para comprobar que la API está funcionando)
@app.get("/")
async def root():
    return {
        "mensaje": "¡Bienvenido al sistema de recomendación de vacaciones familiares!",
        "documentación": "/docs"
    }