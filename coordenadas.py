import pandas as pd
import numpy as np

# Leer archivos
df1 = pd.read_csv('muestreo_localidades.csv', header=None, names=['lat', 'lng'], dtype=float)
df2 = pd.read_csv('muestreo_radiobases.csv', header=None, names=['lat', 'lng'], dtype=float)

coords1 = df1[['lat', 'lng']].to_numpy()
coords2 = df2[['lat', 'lng']].to_numpy()

# Crear matriz para guardar pares
pares = []
for coord1 in coords1:
    # Distancia euclidiana entre coord1 y todas en coords2
    distancias = np.linalg.norm(coords2 - coord1, axis=1)
    idx_min = np.argmin(distancias)
    coord2 = coords2[idx_min]
    pares.append([coord1[0], coord1[1], coord2[0], coord2[1], distancias[idx_min]])

# Guardar en CSV
df_pares = pd.DataFrame(pares, columns=['lat1', 'lng1', 'lat2', 'lng2', 'distancia_grados'])
df_pares.to_csv('pares_mas_cercanos.csv', index=False)

print(df_pares)

df_pares['distancia_km'] = df_pares['distancia_grados'] * 111.32
#imprimir las distnacias en km
print(df_pares[['lat1', 'lng1', 'lat2', 'lng2', 'distancia_km']])
# imprimir las distnacias mas lejanas
print(df_pares[['lat1', 'lng1', 'lat2', 'lng2', 'distancia_km']].sort_values(by='distancia_km', ascending=False).head(10))

# Estadísticas básicas
print(df_pares['distancia_km'].describe())

# Porcentiles específicos
percentiles = [10, 25, 50, 75, 90, 95, 99]
valores_percentiles = np.percentile(df_pares['distancia_km'], percentiles)
for p, v in zip(percentiles, valores_percentiles):
    print(f"{p} percentil: {v:.2f} km")

# Umbral de confianza basado en el percentil 75
umbral_confianza_km = 12.89

# Filtrar los datos
df_cercanas = df_pares[df_pares['distancia_km'] <= umbral_confianza_km]
df_lejanas = df_pares[df_pares['distancia_km'] > umbral_confianza_km]

# Guardar a archivos CSV
df_cercanas.to_csv('distancias_cercanas.csv', index=False)
df_lejanas.to_csv('distancias_lejanas.csv', index=False)

# Imprimir cuántas hay en cada grupo
print(f"Número de distancias cercanas (<= {umbral_confianza_km} km):", len(df_cercanas))
print(f"Número de distancias lejanas  (> {umbral_confianza_km} km):", len(df_lejanas))