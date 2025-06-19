import pandas as pd
import numpy as np

# Cargar archivos originales y de distancias lejanas
df_localidades = pd.read_csv('muestreo_localidades.csv', header=None, names=['lat', 'lng'], dtype=float)
df_radiobases = pd.read_csv('muestreo_radiobases.csv', header=None, names=['lat', 'lng'], dtype=float)
df_lejanas = pd.read_csv('distancias_lejanas.csv')

coords_radiobases = df_radiobases[['lat', 'lng']].to_numpy()

# Lista para los resultados
resumen = []

for _, fila in df_lejanas.iterrows():
    lat1, lng1 = fila['lat1'], fila['lng1']
    lat2, lng2 = fila['lat2'], fila['lng2']
    distancia_actual = fila['distancia_km']
    limite_superior = distancia_actual * 1.5

    comunidad = f"({lat1:.5f}, {lng1:.5f})"
    punto_actual = f"({lat2:.5f}, {lng2:.5f})"
    distancia_txt = f"{distancia_actual:.2f} km"

    # Revisar todas las radiobases como alternativas
    coord1 = np.array([lat1, lng1])
    distancias = np.linalg.norm(coords_radiobases - coord1, axis=1) * 111.32

    alternativas = []
    for i, d in enumerate(distancias):
        alt_lat, alt_lng = coords_radiobases[i]
        if distancia_actual < d <= limite_superior:
            alt_txt = f"({alt_lat:.5f}, {alt_lng:.5f}) → {d:.2f} km"
            alternativas.append(alt_txt)

    resumen.append({
        "Comunidad": comunidad,
        "Punto actual más cercano": punto_actual,
        "Distancia actual (km)": distancia_txt,
        "Alternativas (dentro de +50%)": "; ".join(alternativas) if alternativas else "—"
    })

# Guardar el resumen
df_resumen = pd.DataFrame(resumen)
df_resumen.to_csv('resumen_alternativas_legibles.csv', index=False)

try:
    df_resumen.to_excel('resumen_alternativas_legibles.xlsx', index=False)
except:
    print("⚠️ No se pudo guardar como Excel. Instala openpyxl con: pip install openpyxl")

print("✅ Archivo generado: resumen_alternativas_legibles.csv")
