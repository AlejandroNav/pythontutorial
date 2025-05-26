import pandas as pd
import numpy as np
import re

# Cargar el archivo con las alternativas
df = pd.read_csv("resumen_con_alternativas.csv")

# Columnas nuevas para cada alternativa
ids, coords, distancias, links = [[] for _ in range(4)], [[] for _ in range(4)], [[] for _ in range(4)], [[] for _ in range(4)]
coordenadas_comunidad = []

# Extraer lat/lng de comunidad
for _, row in df.iterrows():
    match_com = re.match(r'\(([-\d.]+), ([-\d.]+)\)', row['Punto actual más cercano'])
    if not match_com:
        coordenadas_comunidad.append("—")
        for i in range(3):
            ids[i].append("—")
            coords[i].append("—")
            distancias[i].append("—")
            links[i].append("—")
        continue

    lat_com, lon_com = map(float, match_com.groups())
    coord_com = np.array([lat_com, lon_com])
    coordenadas_comunidad.append(f"({lat_com}, {lon_com})")  # guardar coordenadas originales

    # Extraer alternativas (ID, coordenadas)
    alternativas_raw = row['Alternativas (dentro de +50%)']
    coincidencias = re.findall(r'([A-Z0-9]+) \(([-\d.]+), ([-\d.]+)\)', alternativas_raw)

    # Recalcular la distancia
    alternativas_recalculadas = []
    for id_alt, lat_alt, lon_alt in coincidencias:
        coord_alt = np.array([float(lat_alt), float(lon_alt)])
        distancia_real = np.linalg.norm(coord_com - coord_alt) * 111.32
        alternativas_recalculadas.append((id_alt, lat_alt, lon_alt, distancia_real))

    # Ordenar y tomar las 3 más cercanas
    alternativas_ordenadas = sorted(alternativas_recalculadas, key=lambda x: x[3])[:3]

    for i in range(3):
        if i < len(alternativas_ordenadas):
            id_alt, lat_alt, lon_alt, distancia = alternativas_ordenadas[i]
            ids[i].append(id_alt)
            coords[i].append(f"({lat_alt}, {lon_alt})")
            distancias[i].append(f"{distancia:.2f} km")
            link = f"https://www.google.com/maps/dir/{lat_com},{lon_com}/{lat_alt},{lon_alt}"
            links[i].append(link)
        else:
            ids[i].append("—")
            coords[i].append("—")
            distancias[i].append("—")
            links[i].append("—")

# Asignar columnas al DataFrame
df['Coordenadas Comunidad'] = coordenadas_comunidad
for i in range(3):
    n = i + 1
    df[f"ID Alternativa {n}"] = ids[i]
    df[f"Coordenadas Alternativa {n}"] = coords[i]
    df[f"Distancia Alternativa {n} (km)"] = distancias[i]
    df[f"Ruta Alternativa {n} (Google Maps)"] = links[i]

# Eliminar la columna original de texto
df.drop(columns=['Alternativas (dentro de +50%)'], inplace=True)

# Guardar resultado final
df.to_csv("resumen_con_3_alternativas_completo.csv", index=False)

print("✅ Archivo 'resumen_con_3_alternativas_completo.csv' generado con coordenadas de comunidad, distancias reales y enlaces.RRRRRRRRRRRRRRRRRRRRRRRR")
print(df[[
    'Comunidad',
    'Coordenadas Comunidad',
    'ID Alternativa 1', 'Distancia Alternativa 1 (km)', 'Ruta Alternativa 1 (Google Maps)'
]].head(3))
