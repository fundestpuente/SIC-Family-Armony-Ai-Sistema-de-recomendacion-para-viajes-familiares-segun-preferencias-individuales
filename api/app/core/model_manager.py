import os
import pandas as pd
import numpy as np
from typing import Dict, Any
from xgboost import XGBRegressor

# Columnas de calificación de atractivos (mismo orden que el CSV)
RATING_COLUMNS = [
    "Calif promedio iglesias","Calif promedio resorts","Calif promedio playas","Calif promedio parques",
    "Calif promedio teatros","Calif promedio museos","Calif promedio centros_comerciales",
    "Calif promedio zoologicos","Calif promedio restaurantes","Calif promedio bares_pubs",
    "Calif promedio servicios_locales","Calif promedio pizzerias_hamburgueserias","Calif promedio hoteles_alojamientos",
    "Calif promedio juguerias","Calif promedio galerias_arte","Calif promedio discotecas","Calif promedio piscinas",
    "Calif promedio gimnasios","Calif promedio panaderias","Calif promedio belleza_spas","Calif promedio cafeterias",
    "Calif promedio miradores","Calif promedio monumentos","Calif promedio jardines"
]

class ModelManager:
    def __init__(self, data_path: str, new_data_path: str):
        self.data_path = os.path.abspath(data_path)
        self.new_data_path = os.path.abspath(new_data_path)
        self.model: XGBRegressor | None = None
        self.is_trained = False
        self.feature_columns = RATING_COLUMNS.copy()

    def _load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Archivo de datos no encontrado: {self.data_path}")
        df = pd.read_csv(self.data_path, sep="|")
        # Asegurar que existan todas las columnas de preferencias
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0.0
        return df

    def train_model(self):
        """
        Entrena el modelo con los datos históricos
        """
        df = self._load_data()
        if "score" not in df.columns:
            raise ValueError("Falta la columna 'score' en el dataset")
        
        X = df[self.feature_columns]
        y = df["score"].astype(float)

        self.model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1,
            objective="reg:squarederror",
            random_state=42
        )
        self.model.fit(X, y)
        self.is_trained = True
        print(f"Modelo entrenado con {len(df)} registros.")

    def predict_score(self, aggregated_preferences: Dict[str, float]) -> float:
        """
        Recibe un diccionario con preferencias agregadas y devuelve el score predicho
        """
        if not self.is_trained or self.model is None:
            raise RuntimeError("El modelo no ha sido entrenado. Llama a 'train_model()' primero.")

        X_input = np.array([aggregated_preferences.get(col, 0.0) for col in self.feature_columns]).reshape(1, -1)
        score_pred = self.model.predict(X_input)[0]
        return float(score_pred)

    def save_new_record(self, record: Dict[str, Any]):
        """
        Guarda un nuevo registro en el archivo CSV para futuros reentrenamientos
        """
        all_columns = self.feature_columns + ["provincia","canton","parroquia","nombre","lat","lon","score (promedio preferencias)"]
        df_record = pd.DataFrame([record], columns=[c for c in all_columns if c in record])
        
        if os.path.exists(self.new_data_path):
            df_record.to_csv(self.new_data_path, mode='a', header=False, index=False)
        else:
            df_record.to_csv(self.new_data_path, index=False)
        print(f"Nuevo registro guardado en {self.new_data_path}")
