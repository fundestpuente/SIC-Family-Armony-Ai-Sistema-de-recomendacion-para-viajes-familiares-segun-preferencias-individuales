'''
ESTE CODIGO FUSIONA LOS DOS DATASETS BASE Y DEJ ACOMO RESULTADO EL 'reseñas_con_atractivos_turisticos' CON
UN TOTAL DE 1133 REGISTROS
'''

import pandas as pd
import numpy as np

# ------------------------------------------------------
# Cargar datasets
# ------------------------------------------------------
df_atractivos = pd.read_csv('datasets_base/atractivos_tur.csv')
df_ratings = pd.read_csv('datasets_base/google_review_ratings.csv')

# ------------------------------------------------------
# Eliminar columnas vacías tipo "Unnamed"
# ------------------------------------------------------
df_ratings = df_ratings.loc[:, ~df_ratings.columns.str.contains('^Unnamed')]

# ------------------------------------------------------
# Lista correcta de columnas (25)
# ------------------------------------------------------
nuevos_nombres_es = [
    "ID unico de usuario",
    "Calif promedio iglesias",
    "Calif promedio resorts",
    "Calif promedio playas",
    "Calif promedio parques",
    "Calif promedio teatros",
    "Calif promedio museos",
    "Calif promedio centros_comerciales",
    "Calif promedio zoologicos",
    "Calif promedio restaurantes",
    "Calif promedio bares_pubs",
    "Calif promedio servicios_locales",
    "Calif promedio pizzerias_hamburgueserias",
    "Calif promedio hoteles_alojamientos",
    "Calif promedio juguerias",
    "Calif promedio galerias_arte",
    "Calif promedio discotecas",
    "Calif promedio piscinas",
    "Calif promedio gimnasios",
    "Calif promedio panaderias",
    "Calif promedio belleza_spas",
    "Calif promedio cafeterias",
    "Calif promedio miradores",
    "Calif promedio monumentos",
    "Calif promedio jardines"
]

# ------------------------------------------------------
# Renombrar columnas de ratings
# ------------------------------------------------------
if len(df_ratings.columns) == len(nuevos_nombres_es):
    df_ratings.columns = nuevos_nombres_es
else:
    raise ValueError(
        f"ERROR: El CSV tiene {len(df_ratings.columns)} columnas, pero la lista tiene 25 nombres."
    )

# ------------------------------------------------------
# Seleccionar columnas del dataset de atractivos
# ------------------------------------------------------
columnas_deseadas = [
    'provincia', 'canton', 'parroquia',
    'nombre', 'desc_', 'desc2', 'desc3',
    'lat', 'lon'
]

df_atractivos = df_atractivos[columnas_deseadas].copy()

# ------------------------------------------------------
# LIMPIEZA Y PREPROCESAMIENTO PROFUNDO
# ------------------------------------------------------

# Reemplazar espacios vacíos por NaN
df_ratings.replace(r'^\s*$', np.nan, regex=True, inplace=True)
df_atractivos.replace(r'^\s*$', np.nan, regex=True, inplace=True)

# Rellenar columnas numéricas con 0
num_cols = df_ratings.select_dtypes(include=[np.number]).columns
df_ratings[num_cols] = df_ratings[num_cols].fillna(0)

# Rellenar textos vacíos con “Sin información”
text_cols = df_atractivos.select_dtypes(include=['object']).columns
df_atractivos[text_cols] = df_atractivos[text_cols].fillna("Sin información")

# Arreglar encoding roto en descripciones
def fix_encoding(x):
    x = str(x)
    x = x.replace("Ã¡","á").replace("Ã©","é").replace("Ã­","í")
    x = x.replace("Ã³","ó").replace("Ãº","ú").replace("Ã±","ñ")
    return x

for col in ['desc_', 'desc2', 'desc3']:
    if col in df_atractivos.columns:
        df_atractivos[col] = df_atractivos[col].apply(fix_encoding)

# Limpiar saltos de línea y caracteres
def limpiar_texto(x):
    if pd.isna(x):
        return "Sin información"
    x = str(x)
    x = x.replace("\n", " ")
    x = x.replace("\r", " ")
    x = x.replace("|", " ")
    x = x.replace(";", ",")
    return x.strip()

for col in df_atractivos.columns:
    if df_atractivos[col].dtype == object:
        df_atractivos[col] = df_atractivos[col].apply(limpiar_texto)

# Validar coordenadas
df_atractivos['lat'] = pd.to_numeric(df_atractivos['lat'], errors='coerce').fillna(0)
df_atractivos['lon'] = pd.to_numeric(df_atractivos['lon'], errors='coerce').fillna(0)

# ------------------------------------------------------
# Empatar número de filas
# ------------------------------------------------------
n_filas = min(len(df_ratings), len(df_atractivos))
df_ratings = df_ratings.head(n_filas).reset_index(drop=True)
df_atractivos = df_atractivos.head(n_filas).reset_index(drop=True)

# ------------------------------------------------------
# Fusionar datasets horizontalmente
# ------------------------------------------------------
df_final = pd.concat([df_ratings, df_atractivos], axis=1)

# ------------------------------------------------------
# Guardar en CSV 
# ------------------------------------------------------
df_final.to_csv(
    'reseñas_con_atractivos_turisticos.csv',
    index=False,
    encoding='utf-8-sig',
    sep='|'
)

print(f"Archivo generado correctamente con {n_filas} filas.")
