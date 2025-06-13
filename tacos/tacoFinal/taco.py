import pandas as pd
import numpy as np

# Leer el archivo limpio y ya ordenado
df = pd.read_csv("tacos_CDMX_sorted.csv")

print("Columnas disponibles:")
print(df.columns.tolist())

# Mostrar el DataFrame completo
print(df)


# Contar entradas válidas (no vacías) en columnas clave
rating_count = df['rating'].notna().sum()
priceLevel_count = df['priceLevel'].notna().sum()
website_count = df['website'].notna().sum()
lat_count = df['lat'].notna().sum()

# Mostrar conteo
print("Con lat:", lat_count)
print("Con rating:", rating_count)
print("Con priceLevel:", priceLevel_count)
print("Con website:", website_count)

# Ordenar por número de calificaciones (userRatingCount)
df_sorted = df.sort_values(by='userRatingCount', ascending=False)

# Mostrar las primeras filas del DataFrame ordenado
print(df_sorted)
# Guardar el DataFrame ordenado en un nuevo archivo CSV
df_sorted.to_csv("tacos_CDMX_sorted.csv", index=False)