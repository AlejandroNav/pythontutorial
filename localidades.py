import pandas as pd
import numpy as np

print("📥 Cargando el archivo CSV original...")
df = pd.read_csv("Muestreo - Hoja1.csv", encoding='latin1')

print(f"✅ Total de registros cargados: {len(df)}")
print(df.head(2))

# Filtrar filas con coordenadas válidas
df = df.dropna(subset=['LAT_DECIMAL', 'LON_DECIMAL', 'LATITUD_RADIOBASE', 'LONGITUD_RADIOBASE'])
print(f"✅ Registros con coordenadas válidas: {len(df)}")
print(df.head(2))

# Calcular distancia euclidiana en km
coord_comunidades = df[['LAT_DECIMAL', 'LON_DECIMAL']].to_numpy()
coord_asignadas = df[['LATITUD_RADIOBASE', 'LONGITUD_RADIOBASE']].to_numpy()
distancias = np.linalg.norm(coord_comunidades - coord_asignadas, axis=1) * 111.32
df['distancia_km_calculada'] = distancias

print("\n📊 Estadísticas de distancia a radiobase asignada:")
print(df['distancia_km_calculada'].describe())
print(df[['NOM_LOC', 'LAT_DECIMAL', 'LON_DECIMAL', 'distancia_km_calculada']].head(2))

# Clasificar por grupos de distancia
df['grupo_distancia'] = pd.cut(
    df['distancia_km_calculada'],
    bins=[-np.inf, 3, 30, np.inf],
    labels=['<=3 km', '3-30 km', '>30 km']
)

# Separar los tres grupos
df_menor_3 = df[df['grupo_distancia'] == '<=3 km']
df_entre_3_30 = df[df['grupo_distancia'] == '3-30 km']
df_mayor_30 = df[df['grupo_distancia'] == '>30 km']

print(f"\n📂 Comunidades <=3 km: {len(df_menor_3)}")
print(df_menor_3[['NOM_LOC', 'distancia_km_calculada']].head(2))

print(f"\n📂 Comunidades entre 3 y 30 km: {len(df_entre_3_30)}")
print(df_entre_3_30[['NOM_LOC', 'distancia_km_calculada']].head(2))

print(f"\n📂 Comunidades >30 km: {len(df_mayor_30)}")
print(df_mayor_30[['NOM_LOC', 'distancia_km_calculada']].head(2))

# Buscar alternativas para comunidades lejanas (>30 km)
coords_radiobases = df[['LATITUD_RADIOBASE', 'LONGITUD_RADIOBASE']].drop_duplicates().to_numpy()
resumen = []

print("\n🔎 Buscando alternativas para comunidades con distancia >30 km...")

for _, fila in df_mayor_30.iterrows():
    lat1, lng1 = fila['LAT_DECIMAL'], fila['LON_DECIMAL']
    lat2, lng2 = fila['LATITUD_RADIOBASE'], fila['LONGITUD_RADIOBASE']
    distancia_actual = fila['distancia_km_calculada']
    id_radiobase_actual = fila['ID_RADIOBASE_CERCANA']
    comunidad = fila['NOM_LOC']
    coord1 = np.array([lat1, lng1])
    limite_superior = distancia_actual * 1.5

    distancias_alt = np.linalg.norm(coords_radiobases - coord1, axis=1) * 111.32
    alternativas = []

    for i, d in enumerate(distancias_alt):
        alt_lat, alt_lng = coords_radiobases[i]
        if distancia_actual < d <= limite_superior:
            match = df[
                (df['LATITUD_RADIOBASE'] == alt_lat) &
                (df['LONGITUD_RADIOBASE'] == alt_lng)
            ]
            id_alt = match['ID_RADIOBASE_CERCANA'].iloc[0] if not match.empty else "N/D"
            alternativas.append(f"{id_alt} ({alt_lat:.5f}, {alt_lng:.5f}) → {d:.2f} km")

    resumen.append({
        "Comunidad": comunidad,
        "Punto actual más cercano": f"({lat2:.5f}, {lng2:.5f})",
        "ID radio actual": id_radiobase_actual,
        "Distancia actual (km)": f"{distancia_actual:.2f} km",
        "Alternativas (dentro de +50%)": "; ".join(alternativas) if alternativas else "—"
    })

print(f"\n✅ Total de comunidades analizadas: {len(resumen)}")

df_resumen = pd.DataFrame(resumen)
print("\n📋 Vista previa del resumen:")
print(df_resumen.head(2))

# Separar con/sin alternativas
df_con_alternativas = df_resumen[df_resumen['Alternativas (dentro de +50%)'] != "—"]
df_sin_alternativas = df_resumen[df_resumen['Alternativas (dentro de +50%)'] == "—"]

print(f"\n✅ Con alternativas: {len(df_con_alternativas)}")
print(df_con_alternativas.head(2))
print(f"\n❌ Sin alternativas: {len(df_sin_alternativas)}")
print(df_sin_alternativas.head(2))


# ruta de gogolke maps
# Crear columna con enlace de Google Maps para las comunidades <= 3 km
df_menor_3['ruta_google_maps'] = df_menor_3.apply(
    lambda fila: f"https://www.google.com/maps/dir/{fila['LAT_DECIMAL']},{fila['LON_DECIMAL']}/{fila['LATITUD_RADIOBASE']},{fila['LONGITUD_RADIOBASE']}",
    axis=1
)

print("\n🌐 Muestra de enlaces de ruta en Google Maps para comunidades <= 3 km:")
print(df_menor_3[['NOM_LOC', 'ruta_google_maps']].head(3))

# Guardar archivos
df.to_csv("muestreo_con_distancias.csv", index=False)
df_menor_3.to_csv("comunidades_menor_3km.csv", index=False)
df_entre_3_30.to_csv("comunidades_entre_3_30km.csv", index=False)
df_mayor_30.to_csv("comunidades_mayor_30km.csv", index=False)
df_resumen.to_csv("resumen_alternativas_legibles.csv", index=False)
df_con_alternativas.to_csv("resumen_con_alternativas.csv", index=False)
df_sin_alternativas.to_csv("resumen_sin_alternativas.csv", index=False)

print("\n📁 Archivos guardados:")
print(" - muestreo_con_distancias.csv")
print(" - comunidades_menor_3km.csv")
print(" - comunidades_entre_3_30km.csv")
print(" - comunidades_mayor_30km.csv")
print(" - resumen_alternativas_legibles.csv")
print(" - resumen_con_alternativas.csv")
print(" - resumen_sin_alternativas.csv")

print("\n✅ ¡Listo!")