from fastapi import APIRouter, HTTPException
from ..schemas import FamilyBase
from ..core.model_manager import ModelManager
import os
from dotenv import load_dotenv
import pandas as pd

# Cargar variables de entorno desde .env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

# Rutas a los archivos de datos (definidas en .env)
DATA_PATH = os.getenv("DATA_PATH")
NEW_DATA_PATH = os.getenv("NEW_DATA_PATH")

router = APIRouter()

# Inicializar y entrenar el modelo al arrancar la app
model_manager = ModelManager(DATA_PATH, NEW_DATA_PATH)
model_manager.train_model() # Entrenar con los datos historicos

@router.post("/recommend_destinations")
def recommend_destinations(family: FamilyBase, top_k: int = 3):
    miembros = family.miembros
    if not miembros:
        raise HTTPException(status_code=400, detail="No se proporcionaron miembros de la familia.")

    aggregated_preferences = {}
    counts = {}

    # Agregar preferencias de cada miembro
    for member in miembros:
        for key, value in member.preferencias.items():
            for col in model_manager.feature_columns:
                if key.lower() in col.lower():
                    aggregated_preferences[col] = aggregated_preferences.get(col, 0.0) + value
                    counts[col] = counts.get(col, 0) + 1

    # Promediar
    for col in aggregated_preferences:
        aggregated_preferences[col] /= counts[col]

    # Cargar destinos históricos
    df_destinos = pd.read_csv(DATA_PATH, sep="|")

    # Repetir agregadas para todos los destinos
    X_pred = df_destinos[model_manager.feature_columns].copy()
    for col in aggregated_preferences:
        X_pred[col] = aggregated_preferences[col]

    df_destinos["predicted_score"] = model_manager.model.predict(X_pred)

    top_destinos = df_destinos.sort_values("predicted_score", ascending=False).head(top_k)
    recommendations = top_destinos[["nombre", "provincia", "canton", "predicted_score"]].to_dict(orient="records")

    return {"recommendations": recommendations}

@router.post("/save_family_record")
def save_family_record(record: dict):
    """
    Guarda un nuevo registro en CSV para futuros reentrenamientos.
    Se espera que el record contenga todas las columnas necesarias.
    """
    if not record:
        raise HTTPException(status_code=400, detail="No se proporcionó información del registro")
    
    model_manager.save_new_record(record)
    return {"status": "ok", "message": "Registro guardado"}