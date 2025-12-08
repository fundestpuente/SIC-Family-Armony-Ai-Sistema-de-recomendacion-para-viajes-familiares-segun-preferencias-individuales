import pandas as pd
import numpy as np
import random

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from category_encoders import TargetEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

# =======================================================
# Cargar Dataset
# =======================================================
df = pd.read_csv("reseñas_con_atractivos_turisticos.csv", sep="|")

# =======================================================
# columnas
# =======================================================
num_cols = [c for c in df.columns if "Calif promedio" in c]
cat_cols = ["provincia", "canton", "parroquia"]

# =======================================================
# eliminar columnas NO deseadas
# =======================================================
df = df.drop(columns=[
    "ID unico de usuario",
    "user_id",
    "desc_",
    "desc2",
    "desc3"
], errors="ignore")

# =======================================================
# Crear SCORE
# =======================================================
df["score"] = df[num_cols].mean(axis=1)
target = "score"

# =======================================================
# Eliminar filas vacías
# =======================================================
df = df.dropna(subset=num_cols + cat_cols)

# =======================================================
# Generar Datos Sintéticos
# =======================================================

N = 3000
sintetico = pd.DataFrame()

# ---------- Simulación multivariada ----------
cov_matrix = np.cov(df[num_cols].values.T)
mean_vector = df[num_cols].mean().values

vals = np.random.multivariate_normal(
    mean=mean_vector,
    cov=cov_matrix * 0.4,
    size=N
)

for i, col in enumerate(num_cols):
    sintetico[col] = np.clip(vals[:, i], 0, 5)

# ---------- Categóricas realistas ----------
pc_map = df.groupby("provincia")["canton"].unique().to_dict()
cp_map = df.groupby("canton")["parroquia"].unique().to_dict()
provincias = df["provincia"].unique()

def generar_registro_categ():
    prov = np.random.choice(provincias)
    canton = np.random.choice(pc_map[prov])
    parroquia = np.random.choice(cp_map[canton])
    return prov, canton, parroquia

cats = [generar_registro_categ() for _ in range(N)]
cats = pd.DataFrame(cats, columns=cat_cols)
sintetico[cat_cols] = cats

# ---------- Score sintético ----------
sintetico["score"] = sintetico[num_cols].mean(axis=1)

# =======================================================
# Unir datos
# =======================================================
df_final = pd.concat([df, sintetico], ignore_index=True)

print(f"Datos sintéticos generados: {len(sintetico)} filas")
print(f"Dataset final para entrenamiento: {len(df_final)} filas")

df_final.to_csv("datos_sintetico.csv", sep="|", index=False)
print("Dataset combinado guardado")
