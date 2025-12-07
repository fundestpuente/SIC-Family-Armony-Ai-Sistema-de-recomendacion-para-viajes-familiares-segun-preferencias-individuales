import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import joblib

# -------------------------------------------
# Cargar dataset fuente
# -------------------------------------------
df = pd.read_csv("reseñas_con_atractivos_turisticos.csv", sep="|")

# Detectar columnas de actividades
col_act = [c for c in df.columns if c.lower().startswith("calif promedio")]

# Crear catálogo de destinos agregados
group_cols = ['nombre', 'provincia', 'canton', 'parroquia', 'lat', 'lon', 'desc_']
agg_dict = {c: 'mean' for c in col_act}
agg_dict.update({
    'provincia': 'first',
    'canton': 'first',
    'parroquia': 'first',
    'lat': 'median',
    'lon': 'median',
    'desc_': 'first'
})

destinos = df.groupby('nombre').agg(agg_dict).reset_index()
destinos = destinos.rename(columns={'desc_': 'descripcion'})

# -------------------------------------------
# Función para generar datos sintéticos (3000)
# -------------------------------------------
def generar_datos_sint(dest_df, n_examples=3000, seed=42):
    rng = np.random.RandomState(seed)
    rows = []
    destinos_ids = dest_df["nombre"].values

    for i in range(n_examples):
        # Preferencias sintéticas (0-5)
        prefs = {
            f"pref_{c.replace('Calif promedio ', '')}":
                float(np.round(rng.beta(2, 2) * 5, 2))
            for c in col_act
        }

        duracion = int(rng.randint(1, 15))

        # Escoger destino al azar
        destino_name = rng.choice(destinos_ids)
        dest_row = dest_df[dest_df["nombre"] == destino_name].iloc[0]

        dest_acts = np.array([dest_row[c] for c in col_act], dtype=float)
        pref_vals = np.array(
            [prefs[f"pref_{c.replace('Calif promedio ', '')}"] for c in col_act],
            dtype=float
        )

        # Score sintético basado en similitud
        dist = np.linalg.norm(dest_acts - pref_vals)
        sim = 5 - (dist / np.sqrt(len(col_act)))
        score = sim + rng.normal(0, 0.2)

        rows.append({
            **prefs,
            "duracion_deseada": duracion,
            "destino": destino_name,
            "score": float(score)
        })

    return pd.DataFrame(rows)

# -------------------------------------------
# 3. Generar 3000 ejemplos sintéticos
# -------------------------------------------
ejemplos_entrena = generar_datos_sint(destinos, n_examples=3000)
print("Ejemplos generados:", len(ejemplos_entrena))