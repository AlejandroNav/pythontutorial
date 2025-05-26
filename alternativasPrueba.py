import pandas as pd
import numpy as np

PREFIX = "prueba - "

# ────────────────────────────────────────────────────────────────────
# 1. Cargar y depurar
df = pd.read_csv("Muestreo - Hoja1.csv", encoding="latin1")
df = df.dropna(subset=["LAT_DECIMAL", "LON_DECIMAL",
                       "LATITUD_RADIOBASE", "LONGITUD_RADIOBASE"])

# ────────────────────────────────────────────────────────────────────
# 2. Distancia comunidad-radiobase
coord_com = df[["LAT_DECIMAL", "LON_DECIMAL"]].to_numpy()
coord_rb  = df[["LATITUD_RADIOBASE", "LONGITUD_RADIOBASE"]].to_numpy()
df["distancia_km_calculada"] = np.linalg.norm(coord_com - coord_rb, axis=1) * 111.32

# Clasificar por rango; sólo buscaremos alternativas si > 30 km
df["grupo_distancia"] = pd.cut(df["distancia_km_calculada"],
                               bins=[-np.inf, 3, 30, np.inf],
                               labels=["<=3 km", "3-30 km", ">30 km"])

# ────────────────────────────────────────────────────────────────────
# 3. Preparar DataFrame-resumen (solo > 30 km)
registros = []
coords_rbs = df[["ID_RADIOBASE_CERCANA",
                 "LATITUD_RADIOBASE", "LONGITUD_RADIOBASE"]].drop_duplicates().to_numpy()

for _, row in df[df["grupo_distancia"] == ">30 km"].iterrows():
    # Coordenadas comunidad y radiobase asignada
    lat_c, lon_c = row["LAT_DECIMAL"], row["LON_DECIMAL"]
    lat_rb, lon_rb = row["LATITUD_RADIOBASE"], row["LONGITUD_RADIOBASE"]
    dist_actual = row["distancia_km_calculada"]
    id_actual   = row["ID_RADIOBASE_CERCANA"]

    # Buscar alternativas (+50 %)
    limite = dist_actual * 1.5
    dists = np.linalg.norm(coords_rbs[:, 1:3].astype(float) - np.array([lat_c, lon_c]), axis=1) * 111.32
    candidatos = [
        (id_rb, float(lat_rb2), float(lon_rb2), d)
        for (id_rb, lat_rb2, lon_rb2), d in zip(coords_rbs, dists)
        if id_rb != id_actual and dist_actual < d <= limite
    ]
    candidatos = sorted(candidatos, key=lambda x: x[3])[:3]

    registro = {
        "Comunidad":                 row["NOM_LOC"],
        "Coordenadas Comunidad":     f"({lat_c:.5f}, {lon_c:.5f})",
        "ID radio actual":           id_actual,
        "Punto actual más cercano":  f"({lat_rb:.5f}, {lon_rb:.5f})",
        "Distancia actual (km)":     f"{dist_actual:.2f} km",
    }

    # Añadir hasta tres alternativas
    for i, (id_rb, lat_alt, lon_alt, d_alt) in enumerate(candidatos, start=1):
        registro.update({
            f"ID Alternativa {i}":             id_rb,
            f"Coordenadas Alternativa {i}":    f"({lat_alt:.5f}, {lon_alt:.5f})",
            f"Distancia Alternativa {i} (km)": f"{d_alt:.2f} km",
            f"Ruta Alternativa {i} (Google Maps)":
                f"https://www.google.com/maps/dir/{lat_c},{lon_c}/{lat_alt},{lon_alt}",
        })

    # Rellenar con em-dash si faltan alternativas
    for j in range(len(candidatos) + 1, 4):
        registro.update({
            f"ID Alternativa {j}":             "—",
            f"Coordenadas Alternativa {j}":    "—",
            f"Distancia Alternativa {j} (km)": "—",
            f"Ruta Alternativa {j} (Google Maps)": "—",
        })

    registros.append(registro)

df_resumen = pd.DataFrame(registros)

# ────────────────────────────────────────────────────────────────────
# 4. Orden de columnas exacto
orden = ["Comunidad", "Coordenadas Comunidad",
         "ID radio actual", "Punto actual más cercano",
         "Distancia actual (km)"]
for n in range(1, 4):
    orden.extend([
        f"ID Alternativa {n}",
        f"Coordenadas Alternativa {n}",
        f"Distancia Alternativa {n} (km)",
        f"Ruta Alternativa {n} (Google Maps)"
    ])

df_resumen = df_resumen[orden]

# ────────────────────────────────────────────────────────────────────
# 5. Guardar
salida = PREFIX + "comunidades_mayor_30km_con_3_alternativas.csv"
df_resumen.to_csv(salida, index=False)
print(f"✅ Archivo generado: {salida}")
